from pendulum import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator


@dag(
    start_date=datetime(2023, 3, 23),
    description="An Airflow DAG to invoke simple dbt commands",
    schedule="@daily",
)
def simple_dbt_dag():
    dbt_run = BashOperator(task_id="dbt_run", bash_command="dbt run")

    dbt_test = BashOperator(task_id="dbt_test", bash_command="dbt test")

    dbt_run >> dbt_test


simple_dbt_dag()
