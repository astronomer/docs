from airflow import settings
from airflow.decorators import dag, task
from airflow.models import Connection
from pendulum import datetime


def create_dag(dag_id, schedule, dag_number, default_args):
    @dag(dag_id=dag_id, schedule=schedule, default_args=default_args, catchup=False)
    def hello_world_dag():
        @task()
        def hello_world():
            print("Hello World")
            print("This is DAG: {}".format(str(dag_number)))

        hello_world()

    generated_dag = hello_world_dag()

    return generated_dag


session = settings.Session()

# adjust the filter criteria to filter which of your connections to use
# to generated your DAGs
conns = (
    session.query(Connection.conn_id)
    .filter(Connection.conn_id.ilike("%MY_DATABASE_CONN%"))
    .all()
)

for conn in conns:
    dag_id = "connection_hello_world_{}".format(conn[0])

    default_args = {"owner": "airflow", "start_date": datetime(2013, 7, 1)}

    schedule = "@daily"
    dag_number = conn

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
