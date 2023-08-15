from pendulum import datetime
from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import random


@dag(
    start_date=datetime(2023, 6, 1),
    schedule="@daily",
    catchup=False,
)
def tdro_example_upstream():
    @task
    def choose_color():
        color = random.choice(["blue", "red", "green", "yellow"])
        return color

    tdro = TriggerDagRunOperator(
        task_id="tdro",
        trigger_dag_id="tdro_example_downstream",
        conf={"upstream_color": "{{ ti.xcom_pull(task_ids='choose_color')}}"},
    )

    choose_color() >> tdro


tdro_example_upstream()
