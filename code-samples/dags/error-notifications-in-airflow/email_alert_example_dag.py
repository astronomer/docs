from pendulum import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2018, 1, 30),
    "email_on_failure": False,
    "email": ["noreply@astronomer.io"],
    "retries": 1,
}

with DAG(
    "sample_dag", default_args=default_args, schedule="@daily", catchup=False
) as dag:
    wont_email = EmptyOperator(task_id="wont_email")

    will_email = EmptyOperator(task_id="will_email", email_on_failure=True)
