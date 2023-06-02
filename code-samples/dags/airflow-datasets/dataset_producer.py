import pendulum
from datetime import datetime

from airflow import DAG, Dataset
from airflow.decorators import task

API = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
INSTRUCTIONS = Dataset("file://localhost/airflow/include/cocktail_instructions.txt")
INFO = Dataset("file://localhost/airflow/include/cocktail_info.txt")

with DAG(
    dag_id="datasets_producer_dag",
    start_date=pendulum.datetime(2022, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
):

    @task
    def get_cocktail(api):
        import requests

        r = requests.get(api)
        return r.json()

    @task(outlets=[INSTRUCTIONS])
    def write_instructions_to_file(response):
        cocktail_name = response["drinks"][0]["strDrink"]
        cocktail_instructions = response["drinks"][0]["strInstructions"]
        msg = f"See how to prepare {cocktail_name}: {cocktail_instructions}"

        f = open("include/cocktail_instructions.txt", "a")
        f.write(msg)
        f.close()

    @task(outlets=[INFO])
    def write_info_to_file(response):
        import time

        time.sleep(30)
        cocktail_name = response["drinks"][0]["strDrink"]
        cocktail_category = response["drinks"][0]["strCategory"]
        alcohol = response["drinks"][0]["strAlcoholic"]
        msg = f"{cocktail_name} is a(n) {alcohol} cocktail from category {cocktail_category}."
        f = open("include/cocktail_info.txt", "a")
        f.write(msg)
        f.close()

    cocktail = get_cocktail(api=API)

    write_instructions_to_file(cocktail)
    write_info_to_file(cocktail)
