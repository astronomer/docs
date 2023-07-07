from pendulum import datetime
from airflow import Dataset
from airflow.decorators import dag, task

INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")


@dag(
    dag_id="datasets_consumer_dag",
    start_date=datetime(2022, 10, 1),
    schedule=[INSTRUCTIONS, INFO],  # Scheduled on both Datasets
    catchup=False,
)
def datasets_consumer_dag():
    @task
    def read_about_cocktail():
        cocktail = []
        for filename in ("info", "instructions"):
            with open(f"include/cocktail_{filename}.txt", "r") as f:
                contents = f.readlines()
                cocktail.append(contents)

        return [item for sublist in cocktail for item in sublist]

    read_about_cocktail()


datasets_consumer_dag()
