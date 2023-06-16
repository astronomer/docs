from pendulum import datetime
from airflow.decorators import dag, task
from airflow.models.param import Param


@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
    params={
        "param1": "Hello!",
        "param2": Param(
            23,
            type="integer",
        ),
    },
)
def simple_param_dag():
    @task
    def print_all_params(**context):
        print(context["params"]["param1"] * 3)
        print(context["params"]["param2"])

    print_all_params()


simple_param_dag()
