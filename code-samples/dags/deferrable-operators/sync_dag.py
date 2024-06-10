from airflow.decorators import dag
from airflow.sensors.date_time import DateTimeSensor
from pendulum import datetime


@dag(
    start_date=datetime(2024, 5, 23, 20, 0),
    end_date=datetime(2024, 5, 23, 20, 19),
    schedule="* * * * *",
    catchup=True,
)
def sync_dag_2():
    DateTimeSensor(
        task_id="sync_task",
        target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
    )


sync_dag_2()
