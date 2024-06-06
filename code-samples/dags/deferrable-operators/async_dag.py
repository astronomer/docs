from airflow.decorators import dag
from pendulum import datetime
from airflow.sensors.date_time import DateTimeSensorAsync


@dag(
    start_date=datetime(2024, 5, 23, 20, 0),
    end_date=datetime(2024, 5, 23, 20, 19),
    schedule="* * * * *",
    catchup=True,
)
def async_dag_2():
    DateTimeSensorAsync(
        task_id="async_task",
        target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
    )


async_dag_2()
