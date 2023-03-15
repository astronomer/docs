import time
from pendulum import datetime, duration

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@task(task_id="sla_task", sla=duration(seconds=5))
def my_custom_function():
    print("task is sleeping")
    time.sleep(40)


# Default settings applied to all tasks
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": "noreply@astronomer.io",
    "email_on_retry": False,
}


@dag(
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    schedule=duration(minutes=2),
    default_args=default_args,
    catchup=False,
)
def sla_dag_task_level():
    t0 = EmptyOperator(task_id="start", sla=duration(seconds=50))
    t1 = EmptyOperator(task_id="end", sla=duration(seconds=500))
    sla_task = my_custom_function()

    t0 >> sla_task >> t1


sla_dag_task_level()
