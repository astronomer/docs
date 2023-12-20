"""
## Vectorize book descriptions with OpenAI and store them in Postgres with pgvector

This DAG shows how to use the OpenAI API 1.0+ to vectorize book descriptions and 
store them in Postgres with the pgvector extension.
It will also help you pick your next book to read based on a mood you describe.

You will need to set the following environment variables:
- `AIRFLOW_CONN_POSTGRES_DEFAULT`: an Airflow connection to your Postgres database
    that has pgvector installed
- `OPENAI_API_KEY`: your OpenAI API key
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.models.param import Param
from airflow.providers.pgvector.operators.pgvector import PgVectorIngestOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.exceptions import AirflowSkipException
from pendulum import datetime
from openai import OpenAI
import uuid
import re
import os

POSTGRES_CONN_ID = "postgres_default"
TEXT_FILE_PATH = "include/book_data.txt"
TABLE_NAME = "Book"
OPENAI_MODEL = "text-embedding-ada-002"
MODEL_VECTOR_LENGTH = 1536


def create_embeddings(text: str, model: str):
    """Create embeddings for a text with the OpenAI API."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(input=text, model=model)
    embeddings = response.data[0].embedding

    return embeddings


@dag(
    start_date=datetime(2023, 9, 1),
    schedule=None,
    catchup=False,
    tags=["pgvector"],
    params={
        "book_mood": Param(
            "A philosophical book about consciousness.",
            type="string",
            description="Describe the kind of book you want to read.",
        ),
    },
)
def query_book_vectors():
    enable_vector_extension_if_not_exists = PostgresOperator(
        task_id="enable_vector_extension_if_not_exists",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="CREATE EXTENSION IF NOT EXISTS vector;",
    )

    create_table_if_not_exists = PostgresOperator(
        task_id="create_table_if_not_exists",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (          
            book_id UUID PRIMARY KEY,
            title TEXT,
            year INTEGER,
            author TEXT,
            description TEXT,
            vector VECTOR(%(vector_length)s)
        );
        """,
        parameters={"vector_length": MODEL_VECTOR_LENGTH},
    )

    get_already_imported_book_ids = PostgresOperator(
        task_id="get_already_imported_book_ids",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""
        SELECT book_id
        FROM {TABLE_NAME};
        """,
    )

    @task
    def import_book_data(text_file_path: str, table_name: str) -> list:
        "Read the text file and create a list of dicts from the book information."
        with open(text_file_path, "r") as f:
            lines = f.readlines()

            num_skipped_lines = 0
            list_of_params = []
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

                author = parts[2].strip()
                description = parts[3].strip()

                list_of_params.append(
                    {
                        "book_id": str(
                            uuid.uuid5(
                                name=" ".join([title, str(year), author, description]),
                                namespace=uuid.NAMESPACE_DNS,
                            )
                        ),
                        "title": title,
                        "year": year,
                        "author": author,
                        "description": description,
                    }
                )

            print(
                f"Created a list with {len(list_of_params)} elements "
                " while skipping {num_skipped_lines} lines."
            )
            return list_of_params

    @task
    def create_embeddings_book_data(
        book_data: dict, model: str, already_imported_books: list
    ) -> dict:
        "Create embeddings for a book description and add them to the book data."
        already_imported_books_ids = [x[0] for x in already_imported_books]
        if book_data["book_id"] in already_imported_books_ids:
            raise AirflowSkipException("Book already imported.")
        embeddings = create_embeddings(text=book_data["description"], model=model)
        book_data["vector"] = embeddings
        return book_data

    @task
    def create_embeddings_query(model: str, **context) -> list:
        "Create embeddings for the user provided book mood."
        query = context["params"]["book_mood"]
        embeddings = create_embeddings(text=query, model=model)
        return embeddings

    book_data = import_book_data(text_file_path=TEXT_FILE_PATH, table_name=TABLE_NAME)
    book_embeddings = create_embeddings_book_data.partial(
        model=OPENAI_MODEL,
        already_imported_books=get_already_imported_book_ids.output,
    ).expand(book_data=book_data)
    query_vector = create_embeddings_query(model=OPENAI_MODEL)

    import_embeddings_to_pgvector = PgVectorIngestOperator.partial(
        task_id="import_embeddings_to_pgvector",
        trigger_rule="none_failed",
        conn_id=POSTGRES_CONN_ID,
        sql=(
            f"INSERT INTO {TABLE_NAME} "
            "(book_id, title, year, author, description, vector) "
            "VALUES (%(book_id)s, %(title)s, %(year)s, "
            "%(author)s, %(description)s, %(vector)s) "
            "ON CONFLICT (book_id) DO NOTHING;"
        ),
    ).expand(parameters=book_embeddings)

    get_a_book_suggestion = PostgresOperator(
        task_id="get_a_book_suggestion",
        postgres_conn_id=POSTGRES_CONN_ID,
        trigger_rule="none_failed",
        sql=f"""
            SELECT title, year, author, description
            FROM {TABLE_NAME}
            ORDER BY vector <-> CAST(%(query_vector)s AS VECTOR)
            LIMIT 1;
        """,
        parameters={"query_vector": query_vector},
    )

    @task
    def print_suggestion(query_result, **context):
        "Print the book suggestion."
        query = context["params"]["book_mood"]
        book_title = query_result[0][0]
        book_year = query_result[0][1]
        book_author = query_result[0][2]
        book_description = query_result[0][3]
        print(f"Book suggestion for '{query}':")
        print(
            f"You should read {book_title} by {book_author}, published in {book_year}!"
        )
        print(f"Goodreads describes the book as: {book_description}")

    chain(
        enable_vector_extension_if_not_exists,
        create_table_if_not_exists,
        get_already_imported_book_ids,
        import_embeddings_to_pgvector,
        get_a_book_suggestion,
        print_suggestion(query_result=get_a_book_suggestion.output),
    )

    chain(query_vector, get_a_book_suggestion)
    chain(get_already_imported_book_ids, book_embeddings)


query_book_vectors()
