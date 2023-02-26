from airflow import DAG
from pendulum import datetime

from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

with DAG(
    schedule=None,
    start_date=datetime(2022, 7, 1),
    dag_id="gx_example_dag",
    catchup=False,
) as dag:
    # task running the Expectation Suite defined in the JSON above
    ge_test = GreatExpectationsOperator(
        task_id="gx_test",
        data_context_root_dir="/usr/local/airflow/include/great_expectations",
        conn_id="my_db_conn",
        data_asset_name="my_table",
        do_xcom_push=False,
    )
