import time
from datetime import datetime, timedelta

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
}

with DAG(
    "sla-dag",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    schedule=timedelta(minutes=2),
    default_args=default_args,
    catchup=False,
) as dag:

    t0 = EmptyOperator(task_id="start", sla=timedelta(seconds=50))
    t1 = EmptyOperator(task_id="end", sla=timedelta(seconds=500))
    sla_task = PythonOperator(
        task_id="sla_task",
        python_callable=my_custom_function,
        sla=timedelta(seconds=5),
    )

    t0 >> sla_task >> t1
