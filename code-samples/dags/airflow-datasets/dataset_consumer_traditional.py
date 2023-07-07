from pendulum import datetime
from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator

INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")


def read_about_cocktail_func():
    cocktail = []
    for filename in ("info", "instructions"):
        with open(f"include/cocktail_{filename}.txt", "r") as f:
            contents = f.readlines()
            cocktail.append(contents)

    return [item for sublist in cocktail for item in sublist]


with DAG(
    dag_id="datasets_consumer_dag",
    start_date=datetime(2022, 10, 1),
    schedule=[INSTRUCTIONS, INFO],  # Scheduled on both Datasets
    catchup=False,
):
    PythonOperator(
        task_id="read_about_cocktail",
        python_callable=read_about_cocktail_func,
    )
