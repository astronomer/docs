from airflow.decorators import dag
from pendulum import datetime, duration
from operators.my_operator import MyOperator
from sensors.my_sensor import MySensor

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}


@dag(max_active_runs=3, schedule="@once", default_args=default_args)
def example_dag():
    sens = MySensor(task_id="taskA")

    op = MyOperator(task_id="taskB", my_field="some text")

    sens >> op


example_dag()
