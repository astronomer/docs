from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator

from pendulum import datetime, duration

# Instantiate DAG
with DAG(
    dag_id="s3_to_snowflake",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    default_args={"retries": 1, "retry_delay": duration(minutes=5)},
    catchup=False,
):
    # Instantiate tasks within the DAG context
    load_file = S3ToSnowflakeOperator(
        task_id="load_file",
        s3_keys=["key_name.csv"],
        stage="snowflake_stage",
        table="my_table",
        schema="my_schema",
        file_format="csv",
        snowflake_conn_id="snowflake_default",
    )

    snowflake_query = SnowflakeOperator(
        task_id="run_query", sql="SELECT COUNT(*) FROM my_table"
    )

    send_email = EmailOperator(
        task_id="send_email",
        to="noreply@astronomer.io",
        subject="Snowflake DAG",
        html_content="<p>The Snowflake DAG completed successfully.<p>",
    )

    # Define dependencies
    load_file >> snowflake_query >> send_email
