from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from pendulum import datetime, duration


@task
def print_task_type(task_type):
    """
    Example function to call before and after dependent DAG.
    """
    print(f"The {task_type} task has completed.")


# Default settings applied to all tasks
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}


@dag(
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    schedule="@daily",
    default_args=default_args,
    catchup=False,
)
def trigger_dagrun_dag():
    start_task = print_task_type("starting")

    trigger_dependent_dag = TriggerDagRunOperator(
        task_id="trigger_dependent_dag",
        trigger_dag_id="dependent-dag",
        wait_for_completion=True,
    )

    end_task = print_task_type("ending")

    start_task >> trigger_dependent_dag >> end_task


trigger_dagrun_dag()
