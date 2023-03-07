from pendulum import datetime, duration

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


def api_function(**kwargs):
    url = "http://catfact.ninja/fact"
    res = requests.get(url)
    return res.json()


with DAG(
    "pool_priority_dag",
    start_date=datetime(2021, 8, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args={
        "pool": "api_pool",
        "retries": 1,
        "retry_delay": duration(minutes=5),
        "priority_weight": 3,
    },
) as dag:
    task_a = PythonOperator(task_id="task_a", python_callable=api_function)

    task_b = PythonOperator(task_id="task_b", python_callable=api_function)

    task_c = PythonOperator(task_id="task_c", python_callable=api_function)
