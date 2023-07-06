from pendulum import datetime
from airflow import DAG, settings
from airflow.models import Connection
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


session = settings.Session()
conns = (
    session.query(Connection.conn_id)
    .filter(Connection.conn_id.ilike("%MY_DATABASE_CONN%"))
    .all()
)

for conn in conns:
    dag_id = "connection_hello_world_{}".format(conn[0])

    default_args = {"owner": "airflow", "start_date": datetime(2018, 1, 1)}

    schedule = "@daily"
    dag_number = conn

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
