from airflow.decorators import dag, task
from pendulum import datetime
import random


@dag(start_date=datetime(2022, 12, 20), schedule="@daily", catchup=False)
def simple_xcom_dag():
    @task
    def pick_a_random_number():
        return random.randint(1, 10)  # push to XCom

    @task
    def print_a_number(num):  # retrieve from XCom
        print(num)

    print_a_number(pick_a_random_number())


simple_xcom_dag()
