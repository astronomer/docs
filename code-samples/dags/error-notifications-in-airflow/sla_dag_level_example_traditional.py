import time
from pendulum import datetime, duration

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


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
    "sla": duration(seconds=30),
}

with DAG(
    "sla-dag",
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule=duration(minutes=2),
    default_args=default_args,
    catchup=False,
) as dag:
    t0 = EmptyOperator(task_id="start")
    t1 = EmptyOperator(task_id="end")
    sla_task = PythonOperator(task_id="sla_task", python_callable=my_custom_function)

    t0 >> sla_task >> t1
