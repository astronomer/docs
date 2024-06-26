import os
import requests

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.models.param import Param
from airflow.providers.qdrant.hooks.qdrant import QdrantHook
from airflow.providers.qdrant.operators.qdrant import QdrantIngestOperator
from pendulum import datetime
from qdrant_client import models


QDRANT_CONNECTION_ID = "qdrant_default"
DATA_FILE_PATH = "include/books.txt"
COLLECTION_NAME = "airflow_tutorial_collection"

EMBEDDING_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
SIMILARITY_METRIC = models.Distance.COSINE


def embed(text: str) -> list:
    HUGGINFACE_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMBEDDING_MODEL_ID}"
    response = requests.post(
        HUGGINFACE_URL,
        headers={"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"},
        json={"inputs": [text], "options": {"wait_for_model": True}},
    )
    return response.json()[0]


@dag(
    dag_id="books_recommend",
    start_date=datetime(2023, 10, 18),
    schedule=None,
    catchup=False,
    params={"preference": Param("Something suspenseful and thrilling.", type="string")},
)
def recommend_book():
    @task
    def import_books(text_file_path: str) -> list:
        data = []
        with open(text_file_path, "r") as f:
            for line in f:
                _, title, genre, description = line.split("|")
                data.append(
                    {
                        "title": title.strip(),
                        "genre": genre.strip(),
                        "description": description.strip(),
                    }
                )

        return data

    @task
    def init_collection():
        hook = QdrantHook(conn_id=QDRANT_CONNECTION_ID)

        hook.conn.recreate_collection(
            COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIMENSION, distance=SIMILARITY_METRIC
            ),
        )

    @task
    def embed_description(data: dict) -> list:
        return embed(data["description"])

    books = import_books(text_file_path=DATA_FILE_PATH)
    embeddings = embed_description.expand(data=books)

    qdrant_vector_ingest = QdrantIngestOperator(
        conn_id=QDRANT_CONNECTION_ID,
        task_id="qdrant_vector_ingest",
        collection_name=COLLECTION_NAME,
        payload=books,
        vectors=embeddings,
    )

    @task
    def embed_preference(**context) -> list:
        user_mood = context["params"]["preference"]
        response = embed(text=user_mood)

        return response

    @task
    def search_qdrant(
        preference_embedding: list,
    ) -> None:
        hook = QdrantHook(conn_id=QDRANT_CONNECTION_ID)

        result = hook.conn.search(
            collection_name=COLLECTION_NAME,
            query_vector=preference_embedding,
            limit=1,
            with_payload=True,
        )

        print("Book recommendation: " + result[0].payload["title"])
        print("Description: " + result[0].payload["description"])

    chain(
        init_collection(),
        qdrant_vector_ingest,
        search_qdrant(embed_preference()),
    )


recommend_book()
