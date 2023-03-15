from pendulum import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


def custom_failure_function(context):
    "Define custom failure notification behavior"
    dag_run = context.get("dag_run")
    task_instances = dag_run.get_task_instances()
    print("These task instances failed:", task_instances)


def custom_success_function(context):
    "Define custom success notification behavior"
    dag_run = context.get("dag_run")
    task_instances = dag_run.get_task_instances()
    print("These task instances succeeded:", task_instances)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 1, 30),
    "on_failure_callback": custom_failure_function,
    "retries": 1,
}

with DAG(
    "sample_dag",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    failure_task = EmptyOperator(task_id="failure_task")

    success_task = EmptyOperator(
        task_id="success_task",
        on_success_callback=custom_success_function,
    )
