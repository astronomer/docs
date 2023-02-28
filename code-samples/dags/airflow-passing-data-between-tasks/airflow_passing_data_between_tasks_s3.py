from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

s3_conn_id = "s3-conn"
bucket = "astro-workshop-bucket"


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


def process_data(cat_fact_number):
    """Reads data from S3, processes, and saves to new S3 file"""
    # Connect to S3
    s3_hook = S3Hook(aws_conn_id=s3_conn_id)

    # Read data
    data = StringIO(
        s3_hook.read_key(
            key="cat_fact_{0}.csv".format(cat_fact_number), bucket_name=bucket
        )
    )
    df = pd.read_csv(data, sep=",")

    # Process data
    processed_data = df[["fact"]]

    # Save processed data to CSV on S3
    s3_hook.load_string(
        processed_data.to_string(),
        "cat_fact_{0}_processed.csv".format(cat_fact_number),
        bucket_name=bucket,
        replace=True,
    )


with DAG(
    "intermediary_data_storage_dag",
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule="@daily",
    default_args={"retries": 1, "retry_delay": timedelta(minutes=1)},
    catchup=False,
) as dag:
    generate_file = PythonOperator(
        task_id="generate_file_{0}".format(state),
        python_callable=upload_to_s3,
        op_kwargs={"cat_fact_number": 1},
    )

    process_data = PythonOperator(
        task_id="process_data_{0}".format(state),
        python_callable=process_data,
        op_kwargs={"cat_fact_number": 1},
    )

    generate_file >> process_data
