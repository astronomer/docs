"""
### DuckDB Tutorial DAG 1

This DAG shows how to use the DuckDB package directly in a @task decorated task.
"""

from airflow.decorators import dag
from pendulum import datetime
import duckdb
import pandas as pd
from airflow.operators.python import PythonOperator


def create_pandas_df_func():
    "Create a pandas DataFrame with toy data and return it."
    ducks_in_my_garden_df = pd.DataFrame(
        {"colors": ["blue", "red", "yellow"], "numbers": [2, 3, 4]}
    )

    return ducks_in_my_garden_df


def create_duckdb_table_from_pandas_df_func(ducks_in_my_garden_df):
    "Create a table in DuckDB based on a pandas DataFrame and query it"

    # change the path to connect to a different database
    conn = duckdb.connect("include/my_garden_ducks.db")
    conn.sql(
        f"""CREATE TABLE IF NOT EXISTS ducks_garden AS 
        SELECT * FROM ducks_in_my_garden_df;"""
    )

    sets_of_ducks = conn.sql("SELECT numbers FROM ducks_garden;").fetchall()
    for ducks in sets_of_ducks:
        print("quack " * ducks[0])


@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
    render_template_as_native_obj=True,
)
def duckdb_tutorial_dag_1():
    create_pandas_df = PythonOperator(
        task_id="create_pandas_df",
        python_callable=create_pandas_df_func,
    )

    create_duckdb_table_from_pandas_df = PythonOperator(
        task_id="create_duckdb_table_from_pandas_df",
        python_callable=create_duckdb_table_from_pandas_df_func,
        op_kwargs={
            "ducks_in_my_garden_df": "{{ ti.xcom_pull(task_ids='create_pandas_df') }}"
        },
    )

    create_pandas_df >> create_duckdb_table_from_pandas_df


duckdb_tutorial_dag_1()
