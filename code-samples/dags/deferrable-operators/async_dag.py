from pendulum import datetime
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensorAsync

with DAG(
    "async_dag_2",
    start_date=datetime(2021, 12, 22, 20, 0),
    end_date=datetime(2021, 12, 22, 20, 19),
    schedule="* * * * *",
    catchup=True,
) as dag:
    async_sensor = DateTimeSensorAsync(
        task_id="async_task",
        target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
    )
