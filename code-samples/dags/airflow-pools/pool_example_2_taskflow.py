from pendulum import datetime, duration
import requests
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@task
def api_function(**kwargs):
    url = "http://catfact.ninja/fact"
    res = requests.get(url)
    return res.json()


@dag(
    start_date=datetime(2023, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args={"retries": 1, "retry_delay": duration(minutes=5)},
)
def pool_unimportant_dag():
    task_w = EmptyOperator(task_id="start")

    task_x = api_function.override(
        task_id="task_x",
        pool="api_pool",
        priority_weight=2,
    )()

    task_y = api_function.override(task_id="task_y", pool="api_pool")()

    task_z = EmptyOperator(task_id="end")

    task_w >> [task_x, task_y] >> task_z


pool_unimportant_dag()
