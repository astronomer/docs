from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator

S3_CONN_ID = "astro-s3-workshop"
BUCKET = "astro-workshop-bucket"
name = "cat_data"  # swap your name here


def upload_to_s3(cat_fact_number):
    # Instantiate
    s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)

    # Base URL
    url = "http://catfact.ninja/fact"

    # Grab data
    res = requests.get(url)

    # Take string, upload to S3 using predefined method
    s3_hook.load_string(
        res.text,
        "cat_fact_{0}.csv".format(cat_fact_number),
        bucket_name=BUCKET,
        replace=True,
    )


number_of_cat_facts = 3

with DAG(
    "cat_data_s3_to_snowflake",
    start_date=datetime(2020, 6, 1),
    max_active_runs=3,
    schedule="@daily",
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5)},
    catchup=False,
):
    t0 = EmptyOperator(task_id="start")

    for i in range(number_of_cat_facts):
        generate_files = PythonOperator(
            task_id="generate_file_{0}".format(i),
            python_callable=upload_to_s3,
            op_kwargs={"cat_fact_number": i},
        )

        snowflake = S3ToSnowflakeOperator(
            task_id="upload_{0}_snowflake".format(i),
            s3_keys=["cat_fact_{0}.csv".format(i)],
            stage="cat_stage",
            table="CAT_DATA",
            schema="SANDBOX_KENTEND",
            file_format="cat_csv",
            snowflake_conn_id="snowflake",
        )

        t0 >> generate_files >> snowflake
