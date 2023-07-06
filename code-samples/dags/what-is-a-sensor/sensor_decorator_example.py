"""
### Create a custom sensor using the @task.sensor decorator

This DAG showcases how to create a custom sensor using the @task.sensor decorator
to check the availability of an API.
"""

from airflow.decorators import dag, task
from pendulum import datetime
import requests

# importing the PokeReturnValue
from airflow.sensors.base import PokeReturnValue


@dag(start_date=datetime(2022, 12, 1), schedule="@daily", catchup=False)
def sensor_decorator():
    # supply inputs to the BaseSensorOperator parameters in the decorator
    @task.sensor(poke_interval=30, timeout=3600, mode="poke")
    def check_shibe_availability() -> PokeReturnValue:
        r = requests.get("http://shibe.online/api/shibes?count=1&urls=true")
        print(r.status_code)

        # set the condition to True if the API response was 200
        if r.status_code == 200:
            condition_met = True
            operator_return_value = r.json()
        else:
            condition_met = False
            operator_return_value = None
            print(f"Shibe URL returned the status code {r.status_code}")

        # the function has to return a PokeReturnValue
        # if is_done = True the sensor will exit successfully, if
        # is_done=False, the sensor will either poke or be rescheduled
        return PokeReturnValue(is_done=condition_met, xcom_value=operator_return_value)

    # print the URL to the picture
    @task
    def print_shibe_picture_url(url):
        print(url)

    print_shibe_picture_url(check_shibe_availability())


sensor_decorator()
