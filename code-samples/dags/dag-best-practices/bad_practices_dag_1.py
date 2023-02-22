"""WARNING: This DAG is used as an example for _bad_ Airflow practices. Do not
use this DAG."""

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime

# Bad practice: top-level code in a DAG file
hook = PostgresHook("database_conn")
result = hook.get_records("SELECT * FROM grocery_list;")


@dag(
    start_date=datetime(2023, 1, 1), max_active_runs=3, schedule="@daily", catchup=False
)
def bad_practices_dag_1():
    for grocery_item in result:
        query = PostgresOperator(
            task_id="query_{0}".format(grocery_item),
            postgres_conn_id="postgres_default",
            sql="INSERT INTO purchase_order VALUES (value1, value2, value3);",
        )

        query


bad_practices_dag_1()
