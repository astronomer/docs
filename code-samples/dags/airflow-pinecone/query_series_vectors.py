"""
## Use the Pinecone Airflow Provider to generate and query vectors for series descriptions

This DAG runs a simple MLOps pipeline that uses the Pinecone Airflow Provider to import 
series descriptions, generate vectors for them, and query the vectors for series based on
a user-provided mood.
"""

from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.models.baseoperator import chain
from airflow.providers.pinecone.operators.pinecone import PineconeIngestOperator
from airflow.providers.pinecone.hooks.pinecone import PineconeHook
from pendulum import datetime
from openai import OpenAI
import uuid
import re
import os

PINECONE_INDEX_NAME = "series-to-watch"
DATA_FILE_PATH = "include/series_data.txt"
PINECONE_CONN_ID = "pinecone_default"
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_MODEL_DIMENSIONS = 1536


def generate_uuid5(identifier: list) -> str:
    "Create a UUID5 from a list of strings and return the uuid as a string."
    name = "/".join([str(i) for i in identifier])
    namespace = uuid.NAMESPACE_DNS
    uuid_obj = uuid.uuid5(namespace=namespace, name=name)
    return str(uuid_obj)


def create_embeddings(text: str, model: str) -> list:
    """Create embeddings for a text with the OpenAI API."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(input=text, model=model)
    embeddings = response.data[0].embedding

    return embeddings


@dag(
    start_date=datetime(2023, 10, 18),
    schedule=None,
    catchup=False,
    tags=["Pinecone"],
    params={"series_mood": Param("A series about astronauts.", type="string")},
)
def query_series_vectors():
    @task
    def import_data_func(text_file_path: str) -> list:
        "Import data from a text file and return it as a list of dicts."
        with open(text_file_path, "r") as f:
            lines = f.readlines()
            num_skipped_lines = 0
            descriptions = []
            data = []
            for line in lines:
                parts = line.split(":::")
                title_year = parts[1].strip()
                match = re.match(r"(.+) \((\d{4})\)", title_year)
                try:
                    title, year = match.groups()
                    year = int(year)
                except:
                    num_skipped_lines += 1
                    continue

                genre = parts[2].strip()
                description = parts[3].strip()
                descriptions.append(description)
                data.append(
                    {
                        "id": generate_uuid5(
                            identifier=[title, year, genre, description]
                        ),  # an `id` property is required for Pinecone
                        "metadata": {
                            "title": title,
                            "year": year,
                            "genre": genre,
                            "description": description,  # this is the text we'll embed
                        },
                    }
                )

        return data

    series_data = import_data_func(text_file_path=DATA_FILE_PATH)

    @task
    def vectorize_series_data(series_data: dict, model: str) -> dict:
        "Create embeddings for the series descriptions."
        response = create_embeddings(
            text=series_data["metadata"]["description"], model=model
        )

        series_data["values"] = response

        return series_data

    vectorized_data = vectorize_series_data.partial(model=EMBEDDING_MODEL).expand(
        series_data=series_data
    )

    @task
    def vectorize_user_mood(model: str, **context) -> list:
        "Create embeddings for the user mood."
        user_mood = context["params"]["series_mood"]
        response = create_embeddings(text=user_mood, model=model)

        return response

    @task
    def create_index_if_not_exists(
        index_name: str, vector_size: int, pinecone_conn_id: str
    ) -> None:
        "Create a Pinecone index of the provided name if it doesn't already exist."
        hook = PineconeHook(conn_id=pinecone_conn_id)
        existing_indexes = hook.list_indexes()
        if index_name not in existing_indexes:
            newindex = hook.create_index(index_name=index_name, dimension=vector_size)
            return newindex
        else:
            print(f"Index {index_name} already exists")

    create_index_if_not_exists_obj = create_index_if_not_exists(
        vector_size=EMBEDDING_MODEL_DIMENSIONS,
        index_name=PINECONE_INDEX_NAME,
        pinecone_conn_id=PINECONE_CONN_ID,
    )

    pinecone_vector_ingest = PineconeIngestOperator(
        task_id="pinecone_vector_ingest",
        conn_id=PINECONE_CONN_ID,
        index_name=PINECONE_INDEX_NAME,
        input_vectors=vectorized_data,
    )

    @task
    def query_pinecone(
        index_name: str,
        pinecone_conn_id: str,
        vectorized_user_mood: list,
    ) -> None:
        "Query the Pinecone index with the user mood and print the top result."
        hook = PineconeHook(conn_id=pinecone_conn_id)

        query_response = hook.query_vector(
            index_name=index_name,
            top_k=1,
            include_values=True,
            include_metadata=True,
            vector=vectorized_user_mood,
        )

        print("You should watch: " + query_response["matches"][0]["metadata"]["title"])
        print("Description: " + query_response["matches"][0]["metadata"]["description"])

    query_pinecone_obj = query_pinecone(
        index_name=PINECONE_INDEX_NAME,
        pinecone_conn_id=PINECONE_CONN_ID,
        vectorized_user_mood=vectorize_user_mood(model=EMBEDDING_MODEL),
    )

    chain(
        create_index_if_not_exists_obj,
        pinecone_vector_ingest,
        query_pinecone_obj,
    )


query_series_vectors()
