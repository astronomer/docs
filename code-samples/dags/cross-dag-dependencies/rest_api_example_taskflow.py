from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator
from pendulum import datetime, duration
import json

# Define body of POST request for the API call to trigger another DAG
date = "{{ execution_date }}"
request_body = {"execution_date": date}
json_body = json.dumps(request_body)


@task
def print_task_type(task_type):
    """
    Example function to call before and after downstream DAG.
    """
    print(f"The {task_type} task has completed.")
    print(request_body)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}


@dag(
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule="@daily",
    catchup=False,
)
def api_dag_taskflow():
    start_task = print_task_type("starting")

    api_trigger_dependent_dag = SimpleHttpOperator(
        task_id="api_trigger_dependent_dag",
        http_conn_id="airflow-api",
        endpoint="/api/v1/dags/dependent-dag/dagRuns",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json_body,
    )

    end_task = print_task_type("ending")

    start_task >> api_trigger_dependent_dag >> end_task


api_dag_taskflow()
