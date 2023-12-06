"""
## Use the OpenSearch provider to ingest and search Hamilton lyrics

This DAG uses the OpenSearch provider to create an index in OpenSearch, 
ingest Hamilton lyrics into the index, and search for which character and which song
mention a keyword the most.
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.opensearch.operators.opensearch import (
    OpenSearchAddDocumentOperator,
    OpenSearchCreateIndexOperator,
    OpenSearchQueryOperator,
)
from airflow.providers.opensearch.hooks.opensearch import OpenSearchHook
from pendulum import datetime
import csv
import uuid
import pandas as pd

OPENSEARCH_INDEX_NAME = "hamilton_lyrics"
OPENSEARCH_CONN_ID = "opensearch_default"
LYRICS_CSV_PATH = "include/hamilton_lyrics.csv"
KEYWORD_TO_SEARCH = "write"


@dag(
    start_date=datetime(2023, 10, 18),
    schedule=None,
    catchup=False,
)
def search_hamilton():
    @task.branch
    def check_if_index_exists(index_name: str, conn_id: str) -> str:
        client = OpenSearchHook(open_search_conn_id=conn_id, log_query=True).client
        is_index_exist = client.indices.exists(index_name)
        if is_index_exist:
            return "index_exists"
        return "create_index"

    create_index = OpenSearchCreateIndexOperator(
        task_id="create_index",
        opensearch_conn_id=OPENSEARCH_CONN_ID,
        index_name=OPENSEARCH_INDEX_NAME,
        index_body={
            "settings": {"index": {"number_of_shards": 1}},
            "mappings": {
                "properties": {
                    "title": {"type": "keyword"},
                    "speaker": {
                        "type": "keyword",
                    },
                    "lines": {"type": "text"},
                }
            },
        },
    )

    index_exists = EmptyOperator(task_id="index_exists")

    @task
    def csv_to_dict_list(csv_file_path: str) -> list:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            list_of_hamilton_lines = list(reader)

        list_of_kwargs = []
        for line in list_of_hamilton_lines:
            unique_line_id = uuid.uuid5(
                name=" ".join([line["title"], line["speaker"], line["lines"]]),
                namespace=uuid.NAMESPACE_DNS,
            )
            kwargs = {"doc_id": str(unique_line_id), "document": line}

            list_of_kwargs.append(kwargs)

        return list_of_kwargs

    list_of_document_kwargs = csv_to_dict_list(csv_file_path=LYRICS_CSV_PATH)

    add_lines_as_documents = OpenSearchAddDocumentOperator.partial(
        task_id="add_lines_as_documents",
        opensearch_conn_id=OPENSEARCH_CONN_ID,
        trigger_rule="none_failed",
        index_name=OPENSEARCH_INDEX_NAME,
    ).expand_kwargs(list_of_document_kwargs)

    search_for_keyword = OpenSearchQueryOperator(
        task_id=f"search_for_{KEYWORD_TO_SEARCH}",
        opensearch_conn_id=OPENSEARCH_CONN_ID,
        index_name=OPENSEARCH_INDEX_NAME,
        query={
            "size": 0,
            "query": {
                "match": {"lines": {"query": KEYWORD_TO_SEARCH, "fuzziness": "AUTO"}}
            },
            "aggs": {
                "most_mentions_person": {"terms": {"field": "speaker"}},
                "most_mentions_song": {"terms": {"field": "title"}},
            },
        },
    )

    @task
    def print_query_result(query_result: dict, keyword: str) -> None:
        results_most_mentions_person = query_result["aggregations"][
            "most_mentions_person"
        ]["buckets"]
        results_most_mentions_song = query_result["aggregations"]["most_mentions_song"][
            "buckets"
        ]

        df_person = pd.DataFrame(results_most_mentions_person)
        df_person.columns = ["Character", f"Number of lines that include '{keyword}'"]
        df_song = pd.DataFrame(results_most_mentions_song)
        df_song.columns = ["Song", f"Number of lines that include '{keyword}'"]

        print(
            f"\n Top 3 Hamilton characters that mention '{keyword}' the most:\n ",
            df_person.head(3).to_string(index=False),
        )
        print(
            f"\n Top 3 Hamilton songs that mention '{keyword}' the most:\n ",
            df_song.head(3).to_string(index=False),
        )

    chain(
        check_if_index_exists(
            index_name=OPENSEARCH_INDEX_NAME, conn_id=OPENSEARCH_CONN_ID
        ),
        [create_index, index_exists],
        add_lines_as_documents,
    )
    chain(
        list_of_document_kwargs,
        add_lines_as_documents,
        search_for_keyword,
        print_query_result(
            query_result=search_for_keyword.output,
            keyword=KEYWORD_TO_SEARCH,
        ),
    )


search_hamilton()
