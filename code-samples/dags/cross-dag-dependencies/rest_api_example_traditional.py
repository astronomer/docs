from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from pendulum import datetime, duration
import json

# Define body of POST request for the API call to trigger another DAG
date = "{{ execution_date }}"
request_body = {"execution_date": date}
json_body = json.dumps(request_body)


def print_task_type(**kwargs):
    """
    Example function to call before and after downstream DAG.
    """
    print(f"The {kwargs['task_type']} task has completed.")
    print(request_body)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}

with DAG(
    "api-dag",
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule="@daily",
    catchup=False,
) as dag:
    start_task = PythonOperator(
        task_id="starting_task",
        python_callable=print_task_type,
        op_kwargs={"task_type": "starting"},
    )

    api_trigger_dependent_dag = SimpleHttpOperator(
        task_id="api_trigger_dependent_dag",
        http_conn_id="airflow-api",
        endpoint="/api/v1/dags/dependent-dag/dagRuns",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json_body,
    )

    end_task = PythonOperator(
        task_id="end_task",
        python_callable=print_task_type,
        op_kwargs={"task_type": "ending"},
    )

    start_task >> api_trigger_dependent_dag >> end_task
