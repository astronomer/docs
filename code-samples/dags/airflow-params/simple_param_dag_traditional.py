from pendulum import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.param import Param


def print_all_params_func(**context):
    print(context["params"]["param1"] * 3)
    print(context["params"]["param2"])


with DAG(
    dag_id="simple_param_dag",
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
):
    PythonOperator(
        task_id="print_all_params",
        python_callable=print_all_params_func,
    )
