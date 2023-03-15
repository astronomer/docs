from airflow import Dataset
from airflow.decorators import task, dag
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import pendulum

s3_bucket = "sagemaker-us-east-2-559345414282"
test_s3_key = "demo-sagemaker-xgboost-adult-income-prediction/test/test.csv"
dataset_uri = "s3://" + test_s3_key


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def datasets_ml_example_publish():
    @task(outlets=Dataset(dataset_uri))
    def upload_data_to_s3(s3_bucket, test_s3_key):
        """
        Uploads validation data to S3 from /include/data
        """
        s3_hook = S3Hook(aws_conn_id="aws-sagemaker")

        #  Upload the file using the .load_file() method
        s3_hook.load_file(
            filename="include/data/test.csv",
            key=test_s3_key,
            bucket_name=s3_bucket,
            replace=True,
        )

    upload_data = upload_data_to_s3(s3_bucket, test_s3_key)


datasets_ml_example_publish = datasets_ml_example_publish()
