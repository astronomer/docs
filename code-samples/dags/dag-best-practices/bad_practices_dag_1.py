"""WARNING: This DAG is used as an example for _bad_ Airflow practices. Do not
use this DAG."""

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime

# Bad practice: top-level code in a DAG file
hook = PostgresHook("database_conn")
results = hook.get_records("SELECT * FROM grocery_list;")

sql_queries = []

for result in results:
    grocery = result[0]
    amount = result[1]
    sql_query = f"INSERT INTO purchase_order VALUES ('{grocery}', {amount});"

    sql_queries.append(sql_query)


@dag(
    start_date=datetime(2023, 1, 1), max_active_runs=3, schedule="@daily", catchup=False
)
def bad_practices_dag_1():
    insert_into_purchase_order_postgres = PostgresOperator.partial(
        task_id="insert_into_purchase_order_postgres",
        postgres_conn_id="postgres_default",
    ).expand(sql=sql_queries)


bad_practices_dag_1()
