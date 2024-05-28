from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pendulum import datetime, duration

# Default settings applied to all tasks
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=1),
}

state = "Ohio"


# Instantiate DAG
@dag(
    start_date=datetime(2023, 1, 1),
    max_active_runs=3,
    schedule="@daily",
    default_args=default_args,
    catchup=False,
    # include path to look for external files
    template_searchpath="/usr/local/airflow/include",
)
def good_practices_dag_1():
    query = PostgresOperator(
        task_id="covid_query_{0}".format(state),
        postgres_conn_id="postgres_default",
        # reference query kept in separate file
        sql="covid_state_query.sql",
        params={"state": f"'{state}'"},
    )

    query


good_practices_dag_1()
