from __future__ import annotations
import os
from pprint import pprint
from pendulum import datetime
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2022, 10, 10),
    schedule=None,
    catchup=False,
    tags=["pythonvirtualenv"],
)
def py_virtual_env():
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return "Whatever you return gets printed in the logs"

    @task.external_python(
        task_id="external_python", python=os.environ["ASTRO_PYENV_snowpark"]
    )
    def callable_external_python():
        from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
        from snowflake.snowpark import Session

        hook = SnowflakeHook("snowflake_default")
        conn_params = hook._get_conn_params()
        session = Session.builder.configs(conn_params).create()
        query = """
            select avg(reps_upper), avg(reps_lower) 
            from dog_intelligence;
            """
        df = session.sql(query)
        print(df)
        print(df.collect())
        session.close()

    task_print = print_context()
    task_external_python = callable_external_python()

    task_print >> task_external_python


py_virtual_env()
