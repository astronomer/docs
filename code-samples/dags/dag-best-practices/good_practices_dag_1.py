from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime


@dag(
    start_date=datetime(2023, 1, 1), max_active_runs=3, schedule="@daily", catchup=False
)
def good_practices_dag_1():
    @task
    def get_list_of_results():
        # good practice: wrap database connections into a task
        hook = PostgresHook("database_conn")
        results = hook.get_records("SELECT * FROM grocery_list;")
        return results

    @task
    def create_sql_query(result):
        grocery = result[0]
        amount = result[1]
        sql = f"INSERT INTO purchase_order VALUES ('{grocery}', {amount});"
        return sql

    sql_queries = create_sql_query.expand(result=get_list_of_results())

    insert_into_purchase_order_postgres = PostgresOperator.partial(
        task_id="insert_into_purchase_order_postgres",
        postgres_conn_id="postgres_default",
    ).expand(sql=sql_queries)


good_practices_dag_1()
