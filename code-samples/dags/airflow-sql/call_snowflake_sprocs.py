from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    "call_snowflake_sprocs",
    start_date=datetime(2020, 6, 1),
    max_active_runs=3,
    schedule="@daily",
    default_args=default_args,
    template_searchpath="/usr/local/airflow/include",
    catchup=False,
)
def call_snowflake_sprocs():
    opr_call_sproc1 = SQLExecuteQueryOperator(
        task_id="call_sproc1", conn_id="snowflake", sql="call-sproc1.sql"
    )

    opr_call_sproc2 = SQLExecuteQueryOperator(
        task_id="call_sproc2", conn_id="snowflake", sql="call-sproc2.sql"
    )

    opr_call_sproc1 >> opr_call_sproc2


call_snowflake_sprocs()
