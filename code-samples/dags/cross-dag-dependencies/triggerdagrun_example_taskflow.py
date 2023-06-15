from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from pendulum import datetime, duration


@task
def start_task(task_type):
    return f"The {task_type} task has completed."


@task
def end_task(task_type):
    return f"The {task_type} task has completed."


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
    trigger_dependent_dag = TriggerDagRunOperator(
        task_id="trigger_dependent_dag",
        trigger_dag_id="dependent_dag",
        wait_for_completion=True,
        deferrable=True,  # Note that this parameter only exists in Airflow 2.6+
    )

    start_task("starting") >> trigger_dependent_dag >> end_task("ending")


trigger_dagrun_dag()
