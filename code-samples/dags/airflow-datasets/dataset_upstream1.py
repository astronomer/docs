from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator
import pendulum

# Define datasets
dag1_dataset = Dataset("s3://dataset1/output_1.txt")
dag2_dataset = Dataset("s3://dataset2/output_2.txt")


with DAG(
    dag_id="dataset_upstream1",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
) as dag1:
    BashOperator(
        task_id="upstream_task_1",
        bash_command="sleep 5",
        outlets=[dag1_dataset],  # Define which dataset is updated by this task
    )

    BashOperator(
        task_id="upstream_task_2",
        bash_command="sleep 5",
        outlets=[dag2_dataset],  # Define which dataset is updated by this task
    )
