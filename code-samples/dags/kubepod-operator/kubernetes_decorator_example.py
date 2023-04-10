from pendulum import datetime
from airflow.configuration import conf
from airflow.decorators import dag, task
import random

# get the current Kubernetes namespace Airflow is running in
namespace = conf.get("kubernetes", "NAMESPACE")


@dag(
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily",
)
def kubernetes_decorator_example_dag():
    @task
    def extract_data():
        # simulating querying from a database
        data_point = random.randint(0, 100)
        return data_point

    @task.kubernetes(
        # specify the Docker image to launch, it needs to be able to run a Python script
        image="python",
        # launch the Pod on the same cluster as Airflow is running on
        in_cluster=True,
        # launch the Pod in the same namespace as Airflow is running in
        namespace=namespace,
        # Pod configuration
        # naming the Pod
        name="my_pod",
        # log stdout of the container as task logs
        get_logs=True,
        # log events in case of Pod failure
        log_events_on_failure=True,
        # enable pushing to XCom
        do_xcom_push=True,
    )
    def transform(data_point):
        multiplied_data_point = 23 * int(data_point)
        return multiplied_data_point

    @task
    def load_data(**context):
        # pull the XCom value that has been pushed by the KubernetesPodOperator
        transformed_data_point = context["ti"].xcom_pull(
            task_ids="transform", key="return_value"
        )
        print(transformed_data_point)

    load_data(transform(extract_data()))


kubernetes_decorator_example_dag()
