"""
### Simple DAG that runs one task with params

This DAG uses one string type param and uses it in a python decorated task.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.models.param import Param
import random


@dag(
    start_date=datetime(2023, 4, 1),
    schedule=None,
    catchup=False,
    render_template_as_native_obj=True,
    params={"pet_name": Param("Undefined!", type="string")},
)
def walking_my_pet():
    @task
    def walking_your_pet(**context):
        pet_name = context["params"]["pet_name"]
        minutes = random.randint(2, 10)
        print(f"{pet_name} has been on a {minutes} minute walk!")

    walking_your_pet()


walking_my_pet()
