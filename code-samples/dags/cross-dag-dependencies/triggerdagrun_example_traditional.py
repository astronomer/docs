from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from pendulum import datetime, duration


def print_task_type(**kwargs):
    print(f"The {kwargs['task_type']} task has completed.")


# Default settings applied to all tasks
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}

with DAG(
    dag_id="trigger_dagrun_dag",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    schedule="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    start_task = PythonOperator(
        task_id="start_task",
        python_callable=print_task_type,
        op_kwargs={"task_type": "starting"},
    )

    trigger_dependent_dag = TriggerDagRunOperator(
        task_id="trigger_dependent_dag",
        trigger_dag_id="dependent_dag",
        wait_for_completion=True,
        deferrable=True  # Note that this parameter only exists in Airflow 2.6+
    )

    end_task = PythonOperator(
        task_id="end_task",
        python_callable=print_task_type,
        op_kwargs={"task_type": "ending"},
    )

    start_task >> trigger_dependent_dag >> end_task
