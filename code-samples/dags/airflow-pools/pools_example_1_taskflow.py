from pendulum import datetime, duration

import requests
from airflow.decorators import dag, task


@task
def api_function(**kwargs):
    url = "http://catfact.ninja/fact"
    res = requests.get(url)
    return res.json()


@dag(
    start_date=datetime(2021, 8, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args={
        "pool": "api_pool",
        "retries": 1,
        "retry_delay": duration(minutes=5),
        "priority_weight": 3,
    },
)
def pool_priority_dag():
    api_function.override(task_id="task_a")()

    api_function.override(task_id="task_b")()

    api_function.override(task_id="task_c")()


pool_priority_dag()
