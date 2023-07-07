from airflow.decorators import dag
from pendulum import datetime
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

DB_CONN = "snowflake_default"
SCHEMA = "schema_name"
TABLE = "example_table"


@dag(
    start_date=datetime(2023, 7, 1),
    schedule="@daily",
    catchup=False,
)
def gx_example_dag():
    GreatExpectationsOperator(
        task_id="gx_test",
        data_context_root_dir="/usr/local/airflow/include/great_expectations",
        conn_id=DB_CONN,
        schema=SCHEMA,
        data_asset_name=TABLE,
        expectation_suite_name="my_expectation_suite",
        do_xcom_push=False,
    )


gx_example_dag()
