from airflow.decorators import dag
from airflow.operators.python import ShortCircuitOperator
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from pendulum import datetime

DBT_CLOUD_CONN_ID = "dbt_conn"
JOB_ID = "<your dbt Cloud job id>"


def _check_job_not_running(job_id):
    """
    Retrieves the last run for a given dbt Cloud job and checks
    to see if the job is not currently running.
    """
    hook = DbtCloudHook(DBT_CLOUD_CONN_ID)
    runs = hook.list_job_runs(job_definition_id=job_id, order_by="-id")
    latest_run = runs[0].json()["data"][0]

    return DbtCloudJobRunStatus.is_terminal(latest_run["status"])


@dag(
    start_date=datetime(2022, 2, 10),
    schedule="@daily",
    catchup=False,
)
def check_before_running_dbt_cloud_job():
    check_job = ShortCircuitOperator(
        task_id="check_job_is_not_running",
        python_callable=_check_job_not_running,
        op_kwargs={"job_id": JOB_ID},
    )

    trigger_job = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job",
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        job_id=JOB_ID,
        check_interval=600,
        timeout=3600,
    )

    check_job >> trigger_job


check_before_running_dbt_cloud_job()
