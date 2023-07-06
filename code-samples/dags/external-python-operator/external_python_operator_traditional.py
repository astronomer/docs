from __future__ import annotations

import os
from pprint import pprint
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator, ExternalPythonOperator


def print_context_func(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"


def callable_external_python_func():
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


with DAG(
    "py_virtual_env",
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 10, 10, tz="UTC"),
    catchup=False,
    tags=["pythonvirtualenv"],
) as dag:
    print_the_context = PythonOperator(
        task_id="print_the_context",
        python_callable=print_context_func,
    )

    external_python = ExternalPythonOperator(
        task_id="external_python",
        python=os.environ["ASTRO_PYENV_snowpark"],
        python_callable=callable_external_python_func,
    )

    print_the_context >> external_python
