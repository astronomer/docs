"""
### Create a custom sensor using the PythonSensor

This DAG showcases how to create a custom sensor using the PythonSensor 
to check the availability of an API.
"""

from airflow.decorators import dag, task
from pendulum import datetime
import requests
from airflow.sensors.python import PythonSensor


def check_shibe_availability_func(**context):
    r = requests.get("http://shibe.online/api/shibes?count=1&urls=true")
    print(r.status_code)

    # set the condition to True if the API response was 200
    if r.status_code == 200:
        operator_return_value = r.json()
        # pushing the link to the Shibe picture to XCom
        context["ti"].xcom_push(key="return_value", value=operator_return_value)
        return True
    else:
        operator_return_value = None
        print(f"Shibe URL returned the status code {r.status_code}")
        return False


@dag(
    start_date=datetime(2022, 12, 1),
    schedule=None,
    catchup=False,
    tags=["sensor"],
)
def pythonsensor_example():
    # turn any Python function into a sensor
    check_shibe_availability = PythonSensor(
        task_id="check_shibe_availability",
        poke_interval=10,
        timeout=3600,
        mode="reschedule",
        python_callable=check_shibe_availability_func,
    )

    # click the link in the logs for a cute picture :)
    @task
    def print_shibe_picture_url(url):
        print(url)

    print_shibe_picture_url(check_shibe_availability.output)


pythonsensor_example()
