from airflow.decorators import dag, task
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from pendulum import datetime

DBT_CLOUD_CONN_ID = "dbt_conn"
JOB_ID = "<your dbt Cloud job id>"


@dag(
    start_date=datetime(2022, 2, 10),
    schedule="@daily",
    catchup=False,
)
def check_before_running_dbt_cloud_job():
    @task.short_circuit
    def check_job(job_id):
        """
        Retrieves the last run for a given dbt Cloud job and checks
        to see if the job is not currently running.
        """
        hook = DbtCloudHook(DBT_CLOUD_CONN_ID)
        runs = hook.list_job_runs(job_definition_id=job_id, order_by="-id")
        if not runs[0].json().get("data"):
            return True
        else:
            latest_run = runs[0].json()["data"][0]
            return DbtCloudJobRunStatus.is_terminal(latest_run["status"])

    trigger_job = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job",
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        job_id=JOB_ID,
        check_interval=600,
        timeout=3600,
    )

    check_job(job_id=JOB_ID) >> trigger_job


check_before_running_dbt_cloud_job()
