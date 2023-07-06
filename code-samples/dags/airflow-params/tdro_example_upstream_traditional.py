from pendulum import datetime
from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator
import random


def choose_color_func():
    color = random.choice(["blue", "red", "green", "yellow"])
    return color


@dag(
    start_date=datetime(2023, 6, 1),
    schedule="@daily",
    catchup=False,
)
def tdro_example_upstream_traditional():
    choose_color = PythonOperator(
        task_id="choose_color",
        python_callable=choose_color_func,
    )

    tdro = TriggerDagRunOperator(
        task_id="tdro",
        trigger_dag_id="tdro_example_downstream",
        conf={"upstream_color": "{{ ti.xcom_pull(task_ids='choose_color')}}"},
    )

    choose_color() >> tdro


tdro_example_upstream_traditional()
