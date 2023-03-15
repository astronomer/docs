from airflow.decorators import dag
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from pendulum import datetime, duration

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=1),
}


@dag(
    start_date=datetime(2020, 6, 1),
    max_active_runs=3,
    schedule="@daily",
    default_args=default_args,
    template_searchpath="/usr/local/airflow/include",
    catchup=False,
)
def parameterized_query():
    opr_param_query = SnowflakeOperator(
        task_id="param_query", snowflake_conn_id="snowflake", sql="param-query.sql"
    )

    opr_param_query


parameterized_query()
