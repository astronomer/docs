"""
## Use the Airflow Weaviate Provider to generate and query vectors for movie descriptions

This DAG runs a simple MLOps pipeline that uses the Weaviate Provider to import 
movie descriptions, generate vectors for them, and query the vectors for movies based on
concept descriptions.
"""

from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain
from airflow.providers.weaviate.hooks.weaviate import WeaviateHook
from airflow.providers.weaviate.operators.weaviate import WeaviateIngestOperator
from weaviate.util import generate_uuid5
from pendulum import datetime
import re


WEAVIATE_USER_CONN_ID = "weaviate_default"
TEXT_FILE_PATH = "include/movie_data.txt"
# the base class name is used to create a unique class name for the vectorizer
# note that it is best practice to capitalize the first letter of the class name
CLASS_NAME_BASE = "Movie"

# set the vectorizer to text2vec-openai if you want to use the openai model
# note that using the OpenAI vectorizer requires a valid API key in the
# AIRFLOW_CONN_WEAVIATE_DEFAULT connection.
# If you want to use a different vectorizer
# (https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules)
# make sure to also add it to the weaviate configuration's `ENABLE_MODULES` list
# for example in the docker-compose.override.yml file
VECTORIZER = "text2vec-transformers"

# the class name is a combination of the base class name and the vectorizer
CLASS_NAME = CLASS_NAME_BASE + "_" + VECTORIZER.replace("-", "_")


@dag(
    start_date=datetime(2023, 9, 1),
    schedule=None,
    catchup=False,
    tags=["weaviate"],
    params={
        "movie_concepts": Param(
            ["innovation", "friends"],
            type="array",
            description=(
                "What kind of movie do you want to watch today?"
                + " Add one concept per line."
            ),
        ),
    },
)
def query_movie_vectors():
    @task.branch
    def check_for_class(conn_id: str, class_name: str) -> bool:
        "Check if the provided class already exists and decide on the next step."
        hook = WeaviateHook(conn_id)
        client = hook.get_client()

        if not client.schema.get()["classes"]:
            print("No classes found in this weaviate instance.")
            return "create_class"

        existing_classes_names_with_vectorizer = [
            x["class"] for x in client.schema.get()["classes"]
        ]

        if class_name in existing_classes_names_with_vectorizer:
            print(f"Schema for class {class_name} exists.")
            return "class_exists"
        else:
            print(f"Class {class_name} does not exist yet.")
            return "create_class"

    @task
    def create_class(conn_id: str, class_name: str, vectorizer: str):
        "Create a class with the provided name and vectorizer."
        weaviate_hook = WeaviateHook(conn_id)

        class_obj = {
            "class": class_name,
            "vectorizer": vectorizer,
        }
        weaviate_hook.create_class(class_obj)

    class_exists = EmptyOperator(task_id="class_exists")

    def import_data_func(text_file_path: str, class_name: str):
        "Read the text file and create a list of dicts for ingestion to Weaviate."
        with open(text_file_path, "r") as f:
            lines = f.readlines()

            num_skipped_lines = 0
            data = []
            for line in lines:
                parts = line.split(":::")
                title_year = parts[1].strip()
                match = re.match(r"(.+) \((\d{4})\)", title_year)
                try:
                    title, year = match.groups()
                    year = int(year)
                # skip malformed lines
                except:
                    num_skipped_lines += 1
                    continue

                genre = parts[2].strip()
                description = parts[3].strip()

                data.append(
                    {
                        "movie_id": generate_uuid5(
                            identifier=[title, year, genre, description],
                            namespace=class_name,
                        ),
                        "title": title,
                        "year": year,
                        "genre": genre,
                        "description": description,
                    }
                )
                # note that to import pre-computed vectors you would add them to the dict
                # with the key `Vector`

            print(
                f"Created a list with {len(data)} elements while skipping {num_skipped_lines} lines."
            )
            return data

    import_data = WeaviateIngestOperator(
        task_id="import_data",
        conn_id=WEAVIATE_USER_CONN_ID,
        class_name=CLASS_NAME,
        input_json=import_data_func(
            text_file_path=TEXT_FILE_PATH, class_name=CLASS_NAME
        ),
        trigger_rule="none_failed",
    )

    @task
    def query_embeddings(weaviate_conn_id: str, class_name: str, **context):
        "Query the Weaviate instance for movies based on the provided concepts."
        hook = WeaviateHook(weaviate_conn_id)
        movie_concepts = context["params"]["movie_concepts"]

        movie = hook.query_without_vector(
            " ".join(movie_concepts),
            class_name,
            [
                "title",
                "year",
                "genre",
                "description",
            ],
            limit=1,
        )

        if movie["data"]["Get"][class_name] == []:
            print("No movies found for this query. Try again.")
            return

        movie_title = movie["data"]["Get"][class_name][0]["title"]
        movie_year = movie["data"]["Get"][class_name][0]["year"]
        movie_description = movie["data"]["Get"][class_name][0]["description"]

        print(
            "Your movie query was for the following concepts: "
            + " ".join(movie_concepts)
        )
        print(
            "You should watch the following movie(s): "
            + str(movie_title)
            + " ("
            + str(movie_year)
            + ")"
        )
        print("Description: " + str(movie_description))

        return movie

    chain(
        check_for_class(conn_id=WEAVIATE_USER_CONN_ID, class_name=CLASS_NAME),
        [
            create_class(
                conn_id=WEAVIATE_USER_CONN_ID,
                class_name=CLASS_NAME,
                vectorizer=VECTORIZER,
            ),
            class_exists,
        ],
        import_data,
        query_embeddings(weaviate_conn_id=WEAVIATE_USER_CONN_ID, class_name=CLASS_NAME),
    )


query_movie_vectors()
