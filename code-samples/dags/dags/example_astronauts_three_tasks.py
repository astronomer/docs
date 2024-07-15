"""
## Astronaut ETL example DAG

This DAG queries the list of astronauts currently in space from the
Open Notify API and prints each astronaut's name and flying craft.

There are three tasks, one to get the data from the API and save the results,
one to print the results and a final task to react. The first two tasks are
written in Python using Airflow's TaskFlow API, which allows you to easily turn
Python functions into Airflow tasks, and automatically infer dependencies and pass data.

The second task uses dynamic task mapping to create a copy of the task for
each Astronaut in the list retrieved from the API. This list will change
depending on how many Astronauts are in space, and the DAG will adjust
accordingly each time it runs.

The third task is defined using the BashOperator, which is a traditional
operator, allowing you to run a bash command.
"""

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.models.baseoperator import chain
from pendulum import datetime
import requests


# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
)
def example_astronauts_three_tasks():
    # Define tasks
    @task
    def get_astronauts(**context) -> list[dict]:
        """
        This task uses the requests library to retrieve a list of Astronauts
        currently in space. The results are pushed to XCom with a specific key
        so they can be used in a downstream pipeline. The task returns a list
        of Astronauts to be used in the next task.
        """
        r = requests.get("http://api.open-notify.org/astros.json")
        number_of_people_in_space = r.json()["number"]
        list_of_people_in_space = r.json()["people"]

        context["ti"].xcom_push(
            key="number_of_people_in_space", value=number_of_people_in_space
        )
        return list_of_people_in_space

    @task
    def print_astronaut_craft(greeting: str, person_in_space: dict) -> None:
        """
        This task creates a print statement with the name of an
        Astronaut in space and the craft they are flying on from
        the API request results of the previous task, along with a
        greeting which is hard-coded in this example.
        """
        craft = person_in_space["craft"]
        name = person_in_space["name"]

        print(f"{name} is currently in space flying on the {craft}! {greeting}")

    # define a task using a traditional operator
    # this task will run a bash command
    print_reaction = BashOperator(
        task_id="print_reaction",
        bash_command="echo This is awesome!",
    )

    # Use dynamic task mapping to run the print_astronaut_craft task for each
    # Astronaut in space
    print_astronaut_craft_obj = print_astronaut_craft.partial(
        greeting="Hello! :)"
    ).expand(
        person_in_space=get_astronauts()  # Define dependencies using TaskFlow API syntax
    )

    # set the dependency between the second and third task explicitly
    chain(print_astronaut_craft_obj, print_reaction)


# Instantiate the DAG
example_astronauts_three_tasks()
