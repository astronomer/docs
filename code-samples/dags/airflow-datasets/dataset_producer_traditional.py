from pendulum import datetime
from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.operators.python import PythonOperator

API = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")


def get_cocktail_func(api):
    import requests

    r = requests.get(api)
    return r.json()


def write_instructions_to_file_func(response):
    cocktail_name = response["drinks"][0]["strDrink"]
    cocktail_instructions = response["drinks"][0]["strInstructions"]
    msg = f"See how to prepare {cocktail_name}: {cocktail_instructions}"

    f = open("include/cocktail_instructions.txt", "a")
    f.write(msg)
    f.close()


def write_info_to_file_func(response):
    import time

    time.sleep(30)
    cocktail_name = response["drinks"][0]["strDrink"]
    cocktail_category = response["drinks"][0]["strCategory"]
    alcohol = response["drinks"][0]["strAlcoholic"]
    msg = (
        f"{cocktail_name} is a(n) {alcohol} cocktail from category {cocktail_category}."
    )
    f = open("include/cocktail_info.txt", "a")
    f.write(msg)
    f.close()


with DAG(
    dag_id="datasets_producer_dag",
    start_date=datetime(2022, 10, 1),
    schedule=None,
    catchup=False,
    render_template_as_native_obj=True
):
    get_cocktail = PythonOperator(
        task_id="get_cocktail",
        python_callable=get_cocktail_func,
        op_kwargs={"api": API},
    )

    write_instructions_to_file = PythonOperator(
        task_id="write_instructions_to_file",
        python_callable=write_instructions_to_file_func,
        op_kwargs={"response": "{{ ti.xcom_pull(task_ids='get_cocktail') }}"},
        outlets=[INSTRUCTIONS],
    )

    write_info_to_file = PythonOperator(
        task_id="write_info_to_file",
        python_callable=write_info_to_file_func,
        op_kwargs={"response": "{{ ti.xcom_pull(task_ids='get_cocktail') }}"},
        outlets=[INFO],
    )

    get_cocktail >> write_instructions_to_file >> write_info_to_file
