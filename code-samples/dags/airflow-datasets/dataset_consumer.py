import pendulum
from datetime import datetime

from airflow import DAG, Dataset
from airflow.decorators import task

INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")

with DAG(
    dag_id="datasets_consumer_dag",
    start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
    schedule=[INSTRUCTIONS, INFO],  # Scheduled on the Datasets
    tags=["datasets", "cross-DAG dependencies"],
    catchup=False,
):

    @task
    def read_about_cocktail():
        cocktail = []
        for filename in ("info", "instructions"):
            with open(f"include/cocktail_{filename}.txt", "r") as f:
                contents = f.readlines()
                cocktail.append(contents)

        return [item for sublist in cocktail for item in sublist]

    read_about_cocktail()
