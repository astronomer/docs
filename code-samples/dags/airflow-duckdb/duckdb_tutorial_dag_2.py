"""
### DuckDB tutorial DAG 2

This DAG shows how to use the DuckDBHook in an Airflow task.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from duckdb_provider.hooks.duckdb_hook import DuckDBHook

DUCKDB_CONN_ID = "my_local_duckdb_conn"
DUCKDB_TABLE_NAME = "ducks_garden"


@dag(start_date=datetime(2023, 6, 1), schedule=None, catchup=False)
def duckdb_tutorial_dag_2():
    @task
    def query_duckdb(my_table, conn_id):
        my_duck_hook = DuckDBHook.get_hook(conn_id)
        conn = my_duck_hook.get_conn()

        r = conn.execute(f"SELECT * FROM {my_table};").fetchall()
        print(r)

        return r

    query_duckdb(my_table=DUCKDB_TABLE_NAME, conn_id=DUCKDB_CONN_ID)


duckdb_tutorial_dag_2()
