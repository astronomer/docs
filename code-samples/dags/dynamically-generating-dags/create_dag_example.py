from pendulum import datetime
from airflow import DAG
from airflow.decorators import task


def create_dag(dag_id, schedule, dag_number, default_args):
    dag = DAG(dag_id, schedule=schedule, default_args=default_args)

    with dag:

        @task
        def hello_world(*args):
            print("Hello World")
            print("This is DAG: {}".format(str(dag_number)))

        hello_world()

    return dag


# build a dag for each number in range(10)
for n in range(1, 4):
    dag_id = "loop_hello_world_{}".format(str(n))

    default_args = {"owner": "airflow", "start_date": datetime(2021, 1, 1)}

    schedule = "@daily"
    dag_number = n

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
