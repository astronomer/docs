from pendulum import datetime, duration
import requests
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def api_function(**kwargs):
    url = "http://catfact.ninja/fact"
    res = requests.get(url)
    return res.json()


with DAG(
    "pool_unimportant_dag",
    start_date=datetime(2023, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args={"retries": 1, "retry_delay": duration(minutes=5)},
) as dag:
    task_w = EmptyOperator(task_id="start")

    task_x = PythonOperator(
        task_id="task_x",
        python_callable=api_function,
        pool="api_pool",
        priority_weight=2,
    )

    task_y = PythonOperator(
        task_id="task_y", python_callable=api_function, pool="api_pool"
    )

    task_z = EmptyOperator(task_id="end")

    task_w >> [task_x, task_y] >> task_z
