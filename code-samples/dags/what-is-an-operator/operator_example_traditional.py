import hashlib
import json

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.transfers.local_to_s3 import (
    LocalFilesystemToS3Operator,
)
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.sql import SQLCheckOperator
from airflow.utils.task_group import TaskGroup


# The file(s) to upload shouldn't be hardcoded in a production setting,
# this is just for demo purposes.
CSV_FILE_NAME = "forestfires.csv"
CSV_FILE_PATH = f"include/sample_data/forestfire_data/{CSV_FILE_NAME}"


with DAG(
    "simple_redshift_3",
    start_date=datetime(2021, 7, 7),
    description="""A sample Airflow DAG to load data from csv files to S3
                 and then Redshift, with data integrity and quality checks.""",
    schedule=None,
    template_searchpath="/usr/local/airflow/include/sql/redshift_examples/",
    catchup=False,
):
    """
    Before running the DAG, set the following in an Airflow
    or Environment Variable:
    - key: aws_configs
    - value: { "s3_bucket": [bucket_name], "s3_key_prefix": [key_prefix],
             "redshift_table": [table_name]}
    Fully replacing [bucket_name], [key_prefix], and [table_name].
    """

    upload_file = LocalFilesystemToS3Operator(
        task_id="upload_to_s3",
        filename=CSV_FILE_PATH,
        dest_key="{{ var.json.aws_configs.s3_key_prefix }}/" + CSV_FILE_PATH,
        dest_bucket="{{ var.json.aws_configs.s3_bucket }}",
        aws_conn_id="aws_default",
        replace=True,
    )

    def validate_etag_function():
        """
        #### Validation function
        Check the destination ETag against the local MD5 hash to ensure
        the file was uploaded without errors.
        """
        s3 = S3Hook()
        aws_configs = Variable.get("aws_configs", deserialize_json=True)
        obj = s3.get_key(
            key=f"{aws_configs.get('s3_key_prefix')}/{CSV_FILE_PATH}",
            bucket_name=aws_configs.get("s3_bucket"),
        )
        obj_etag = obj.e_tag.strip('"')
        # Change `CSV_FILE_PATH` to `CSV_CORRUPT_FILE_PATH` for the "sad path".
        file_hash = hashlib.md5(open(CSV_FILE_PATH).read().encode("utf-8")).hexdigest()
        if obj_etag != file_hash:
            raise AirflowException(
                """Upload Error: Object ETag in S3 did not match
                hash of local file."""
            )

    validate_file = PythonOperator(
        task_id="validate_etag", python_callable=validate_etag_function
    )

    # --- Create Redshift Table --- #
    create_redshift_table = PostgresOperator(
        task_id="create_table",
        sql="create_redshift_forestfire_table.sql",
        postgres_conn_id="redshift_default",
    )

    # --- Second load task --- #
    load_to_redshift = S3ToRedshiftOperator(
        task_id="load_to_redshift",
        s3_bucket="{{ var.json.aws_configs.s3_bucket }}",
        s3_key="{{ var.json.aws_configs.s3_key_prefix }}" + f"/{CSV_FILE_PATH}",
        schema="PUBLIC",
        table="{{ var.json.aws_configs.redshift_table }}",
        copy_options=["csv"],
    )

    # --- Redshift row validation task --- #
    validate_redshift = SQLCheckOperator(
        task_id="validate_redshift",
        conn_id="redshift_default",
        sql="validate_redshift_forestfire_load.sql",
        params={"filename": CSV_FILE_NAME},
    )

    # --- Row-level data quality check --- #
    with open("include/validation/forestfire_validation.json") as ffv:
        with TaskGroup(group_id="row_quality_checks") as quality_check_group:
            ffv_json = json.load(ffv)
            for id, values in ffv_json.items():
                values["id"] = id
                SQLCheckOperator(
                    task_id=f"forestfire_row_quality_check_{id}",
                    conn_id="redshift_default",
                    sql="row_quality_redshift_forestfire_check.sql",
                    params=values,
                )

    # --- Drop Redshift table --- #
    drop_redshift_table = PostgresOperator(
        task_id="drop_table",
        sql="drop_redshift_forestfire_table.sql",
        postgres_conn_id="redshift_default",
    )

    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    # --- Define task dependencies --- #
    chain(
        begin,
        upload_file,
        validate_file,
        create_redshift_table,
        load_to_redshift,
        validate_redshift,
        quality_check_group,
        drop_redshift_table,
        end,
    )
