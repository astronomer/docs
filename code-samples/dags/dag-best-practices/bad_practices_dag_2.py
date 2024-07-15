"""WARNING: This DAG is used as an example for _bad_ Airflow practices. Do not
use this DAG."""

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
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

today = "2023-01-02"
yesterday = "2023-01-01"


# Instantiate DAG
@dag(
    start_date=datetime(2021, 1, 1),
    max_active_runs=3,
    schedule="@daily",
    default_args=default_args,
    catchup=False,
)
def bad_practices_dag_2():
    t0 = EmptyOperator(task_id="start")

    # Bad practice: long SQL query directly in the DAG file
    query_1 = PostgresOperator(
        task_id="covid_query_wa",
        postgres_conn_id="postgres_default",
        sql="""WITH yesterday_covid_data AS (
                SELECT *
                FROM covid_state_data
                WHERE date = {{ params.today }}
                AND state = 'WA'
            ),
            today_covid_data AS (
                SELECT *
                FROM covid_state_data
                WHERE date = {{ params.yesterday }}
                AND state = 'WA'
            ),
            two_day_rolling_avg AS (
                SELECT AVG(a.state, b.state) AS two_day_avg
                FROM yesterday_covid_data AS a
                JOIN yesterday_covid_data AS b
                ON a.state = b.state
            )
            SELECT a.state, b.state, c.two_day_avg
            FROM yesterday_covid_data AS a
            JOIN today_covid_data AS b
            ON a.state=b.state
            JOIN two_day_rolling_avg AS c
            ON a.state=b.two_day_avg;""",
        params={"today": today, "yesterday": yesterday},
    )

    t0 >> query_1


bad_practices_dag_2()
