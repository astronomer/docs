import random
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from airflow.utils.trigger_rule import TriggerRule


@dag(start_date=datetime(2021, 1, 1), max_active_runs=1, schedule=None, catchup=False)
def branching_dag():
    # EmptyOperators to start and end the DAG
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)

    # Branching task
    @task.branch
    def branching(**kwargs):
        branches = ["branch_0", "branch_1", "branch_2"]
        return random.choice(branches)

    branching_task = branching()

    start >> branching_task

    # set dependencies
    for i in range(0, 3):
        d = EmptyOperator(task_id="branch_{0}".format(i))
        branching_task >> d >> end


branching_dag()
