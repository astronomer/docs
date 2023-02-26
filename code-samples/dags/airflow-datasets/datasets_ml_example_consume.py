from airflow import DAG, Dataset
from airflow.providers.amazon.aws.operators.sagemaker_transform import (
    SageMakerTransformOperator,
)
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

from pendulum import datetime, duration

# Define variables used in config and Python function
date = "{{ ds_nodash }}"  # Date for transform job name
s3_bucket = "sagemaker-us-east-2-559345414282"  # S3 Bucket used with SageMaker instance
test_s3_key = (
    "demo-sagemaker-xgboost-adult-income-prediction/test/test.csv"  # Test data S3 key
)
output_s3_key = (
    "demo-sagemaker-xgboost-adult-income-prediction/output/"  # Model output data S3 key
)
sagemaker_model_name = (
    "sagemaker-xgboost-2021-08-03-23-25-30-873"  # SageMaker model name
)
dataset_uri = "s3://" + test_s3_key

# Define transform config for the SageMakerTransformOperator
transform_config = {
    "TransformJobName": "test-sagemaker-job-{0}".format(date),
    "TransformInput": {
        "DataSource": {
            "S3DataSource": {
                "S3DataType": "S3Prefix",
                "S3Uri": "s3://{0}/{1}".format(s3_bucket, test_s3_key),
            }
        },
        "SplitType": "Line",
        "ContentType": "text/csv",
    },
    "TransformOutput": {
        "S3OutputPath": "s3://{0}/{1}".format(s3_bucket, output_s3_key)
    },
    "TransformResources": {"InstanceCount": 1, "InstanceType": "ml.m5.large"},
    "ModelName": sagemaker_model_name,
}


with DAG(
    "datasets_ml_example_consume",
    start_date=datetime(2021, 7, 31),
    max_active_runs=1,
    schedule=[
        Dataset(dataset_uri)
    ],  # Schedule based on the dataset published in another DAG
    default_args={
        "retries": 1,
        "retry_delay": duration(minutes=1),
        "aws_conn_id": "aws-sagemaker",
    },
    catchup=False,
) as dag:
    predict = SageMakerTransformOperator(task_id="predict", config=transform_config)

    results_to_redshift = S3ToRedshiftOperator(
        task_id="save_results",
        s3_bucket=s3_bucket,
        s3_key=output_s3_key,
        schema="PUBLIC",
        table="results",
        copy_options=["csv"],
    )

    predict >> results_to_redshift
