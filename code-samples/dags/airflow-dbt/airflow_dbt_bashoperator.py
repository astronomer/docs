from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dbt_dag",
    start_date=datetime(2021, 12, 23),
    description="An Airflow DAG to invoke simple dbt commands",
    schedule=timedelta(days=1),
) as dag:
    dbt_run = BashOperator(task_id="dbt_run", bash_command="dbt run")

    dbt_test = BashOperator(task_id="dbt_test", bash_command="dbt test")

    dbt_run >> dbt_test
