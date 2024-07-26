from airflow.decorators import dag, task
from pendulum import datetime
import os


def create_dag(dag_id, schedule, dag_number, default_args):
    @dag(dag_id=dag_id, schedule=schedule, default_args=default_args, catchup=False)
    def hello_world_dag():
        @task()
        def hello_world(*args):
            print("Hello World")
            print("This is DAG: {}".format(str(dag_number)))

        hello_world()

    generated_dag = hello_world_dag()

    return generated_dag


number_of_dags = os.getenv("DYNAMIC_DAG_NUMBER", default=3)
number_of_dags = int(number_of_dags)

for n in range(1, number_of_dags):
    dag_id = "variable_hello_world_{}".format(str(n))

    default_args = {"owner": "airflow", "start_date": datetime(2023, 7, 1)}

    schedule = "@daily"
    dag_number = n

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
