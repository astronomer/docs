"""
## Use the Airflow Weaviate Provider to generate and query vectors for movie descriptions

This DAG runs a simple MLOps pipeline that uses the Weaviate Provider to import 
movie descriptions, generate vectors for them, and query the vectors for movies based on
concept descriptions.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from pathlib import Path
from weaviate_provider.operators.weaviate import (
    WeaviateCheckSchemaOperator,
    WeaviateCreateSchemaOperator,
)
from weaviate_provider.hooks.weaviate import WeaviateHook
from airflow.models.param import Param
from include.movie_data.text_to_parquet_script import create_parquet_file_from_txt
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain
import json


WEAVIATE_USER_CONN_ID = "weaviate_user"
WEAVIATE_ADMIN_CONN_ID = "weaviate_admin"
PARQUET_FILE_PATH = "include/movie_data/movie_data.parquet"
TEXT_FILE_PATH = "include/movie_data/movie_data.txt"
SCHEMA_FILE_PATH = "include/movie_data/movie_schema.json"


@dag(
    start_date=datetime(2023, 9, 1),
    schedule=None,
    catchup=False,
    tags=["weaviate"],
    params={
        "movie_concepts": Param(
            ["innovation", "ensemble"],
            type="array",
            description=(
                "What kind of movie do you want to watch today?"
                + "Add one concept per line."
            ),
        ),
        "certainty_threshold_percent": Param(
            50,
            type="integer",
            description=(
                "How close should the movie at least be to your concepts? "
                + "100% means identical vectors, 0% means no similarity."
            ),
        ),
    },
)
def query_movie_vectors():
    # check if the movie schema exists in the weaviate instance
    # the operator returns True if the schema exists, False otherwise
    check_schema = WeaviateCheckSchemaOperator(
        task_id="check_schema",
        weaviate_conn_id=WEAVIATE_USER_CONN_ID,
        class_object_data=Path(SCHEMA_FILE_PATH).read_text(),
    )

    # decide if the movie schema should be created
    @task.branch
    def branch_create_schema(schema_exists: bool) -> str:
        """
        The WeaviateCheckSchemaOperator returns a boolean.  If the schema
        doesn't exist we can use a branch operator to conditionally create
        it.
        """
        if schema_exists:
            return "schema_exists"
        else:
            return "create_schema"

    create_schema = WeaviateCreateSchemaOperator(
        task_id="create_schema",
        weaviate_conn_id=WEAVIATE_ADMIN_CONN_ID,
        class_object_data=f"file://{SCHEMA_FILE_PATH}",
    )

    schema_exists = EmptyOperator(task_id="schema_exists")

    @task
    def create_parquet_file(text_file_path, parquet_file_path):
        create_parquet_file_from_txt(text_file_path, parquet_file_path)

    @task.weaviate_import(
        weaviate_conn_id=WEAVIATE_ADMIN_CONN_ID, trigger_rule="none_failed"
    )
    def import_data(class_name):
        """Import the movie data into Weaviate using automatic weaviate embeddings."""
        import pandas as pd

        df = pd.read_parquet(PARQUET_FILE_PATH)

        return {
            "data": df,
            "class_name": class_name,
            "uuid_column": "movie_id",
        }

    import_data_obj = import_data(class_name="Movie")

    @task
    def query_embeddings(weaviate_conn_id, **context):
        """Query the Weaviate instance for the movie that is closest to the given concepts."""
        hook = WeaviateHook(weaviate_conn_id)
        movie_concepts = context["params"]["movie_concepts"]
        certainty_threshold = context["params"]["certainty_threshold_percent"] / 100

        # instead of GraphQL you can also use the Weaviate Python client
        # https://weaviate.io/developers/weaviate/client-libraries/python
        query = (
            """
            {
                Get {
                    Movie(nearText: {
                        concepts: """
            + json.dumps(movie_concepts)
            + """,
                        certainty: """
            + json.dumps(certainty_threshold)
            + """
                    }) {
                        title
                        year
                        description
                        _additional {
                            certainty
                            distance
                        }
                    }
                }
            }
            """
        )

        response = hook.run(query=query)
        if len(response["data"]["Get"]["Movie"]):
            top_result = response["data"]["Get"]["Movie"][0]
            print(f"The top result for the concept(s) {movie_concepts} is:")
            print(f"The movie {top_result['title']}, released in {top_result['year']}.")
            print(f"IMDB describes the movie as: {top_result['description']}")
            print(
                f"The certainty of the result is {round(top_result['_additional']['certainty'],3)}."
            )
        else:
            print(
                f"No movie found for the given concept(s) {movie_concepts}"
                + f"with a certainty threshold of {certainty_threshold}. Try again!"
            )

    chain(
        branch_create_schema(check_schema.output),
        [create_schema, schema_exists],
        import_data_obj,
        query_embeddings(WEAVIATE_USER_CONN_ID),
    )

    chain(create_parquet_file(TEXT_FILE_PATH, PARQUET_FILE_PATH), import_data_obj)


query_movie_vectors()
