import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime
from airflow.utils.trigger_rule import TriggerRule


def return_branch(**kwargs):
    branches = ["branch_0", "branch_1", "branch_2"]
    return random.choice(branches)


with DAG(
    dag_id="branching_dag",
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule=None,
    catchup=False,
):
    # EmptyOperators to start and end the DAG
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)

    # Branching task
    branching = BranchPythonOperator(
        task_id="branching", python_callable=return_branch, provide_context=True
    )

    start >> branching

    # set dependencies
    for i in range(0, 3):
        d = EmptyOperator(task_id="branch_{0}".format(i))
        branching >> d >> end
