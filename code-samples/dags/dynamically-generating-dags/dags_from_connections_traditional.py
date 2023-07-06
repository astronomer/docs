from pendulum import datetime
from airflow import DAG, settings
from airflow.models import Connection
from airflow.operators.python import PythonOperator


def create_dag(dag_id, schedule, dag_number, default_args):
    def hello_world_py(*args):
        print("Hello World")
        print("This is DAG: {}".format(str(dag_number)))

    dag = DAG(dag_id, schedule=schedule, default_args=default_args)

    with dag:
        t1 = PythonOperator(task_id="hello_world", python_callable=hello_world_py)

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
