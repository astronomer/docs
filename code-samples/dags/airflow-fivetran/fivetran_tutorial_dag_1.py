from airflow.decorators import dag, task
from pendulum import datetime
from fivetran_provider_async.operators import FivetranOperatorAsync

FIVETRAN_CONNECTOR_ID = "<your Fivetran connector ID>"
GITHUB_REPOSITORY = "<your GitHub handle>/airflow-fivetran-tutorial"
TAG_NAME = "sync-metadata"


@dag(start_date=datetime(2023, 1, 1), schedule="@daily", catchup=False)
def my_fivetran_dag():
    @task
    def upstream():
        return "Hello"

    run_fivetran_sync = FivetranOperatorAsync(
        task_id="run_fivetran_sync",
        fivetran_conn_id="fivetran_conn",
        connector_id=FIVETRAN_CONNECTOR_ID,
    )

    @task
    def downstream():
        return "Goodbye"

    upstream() >> run_fivetran_sync >> downstream()


my_fivetran_dag()
