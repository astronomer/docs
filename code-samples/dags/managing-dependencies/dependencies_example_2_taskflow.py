from airflow.decorators import dag, task
from datetime import datetime

import requests
import json

url = "http://catfact.ninja/fact"

default_args = {"start_date": datetime(2021, 1, 1)}


@dag(schedule="@daily", default_args=default_args, catchup=False)
def xcom_taskflow_dag():
    @task
    def get_a_cat_fact():
        """
        Gets a cat fact from the CatFacts API
        """
        res = requests.get(url)
        return {"cat_fact": json.loads(res.text)["fact"]}

    @task
    def print_the_cat_fact(cat_fact: str):
        """
        Prints the cat fact
        """
        print("Cat fact for today:", cat_fact)
        # run some further cat analysis here

    # Invoke functions to create tasks and define dependencies
    print_the_cat_fact(get_a_cat_fact())


xcom_taskflow_dag()
