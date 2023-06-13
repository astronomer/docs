"""
### DuckDB Tutorial DAG 1

This DAG shows how to use the DuckDB package directly in a @task decorated task.
"""

from airflow.decorators import dag, task
from pendulum import datetime
import duckdb
import pandas as pd


@dag(start_date=datetime(2023, 6, 1), schedule=None, catchup=False)
def duckdb_tutorial_dag_1():
    @task
    def create_pandas_df():
        "Create a pandas DataFrame with toy data and return it."
        ducks_in_my_garden_df = pd.DataFrame(
            {"colors": ["blue", "red", "yellow"], "numbers": [2, 3, 4]}
        )

        return ducks_in_my_garden_df

    @task
    def create_duckdb_table_from_pandas_df(ducks_in_my_garden_df):
        "Create a table in MotherDuck based on a pandas DataFrame and query it"

        # change the path to connect to a different database
        conn = duckdb.connect("include/my_garden_ducks.db")
        conn.sql(
            f"""CREATE TABLE IF NOT EXISTS ducks_garden AS 
            SELECT * FROM ducks_in_my_garden_df;"""
        )

        sets_of_ducks = conn.sql("SELECT numbers FROM ducks_garden;").fetchall()
        for ducks in sets_of_ducks:
            print("quack " * ducks[0])

    create_duckdb_table_from_pandas_df(ducks_in_my_garden_df=create_pandas_df())


duckdb_tutorial_dag_1()
