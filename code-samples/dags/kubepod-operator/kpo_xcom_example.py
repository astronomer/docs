from airflow import DAG
from pendulum import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.configuration import conf
from airflow.decorators import task

import random

# get the current Kubernetes namespace Airflow is running in
namespace = conf.get("kubernetes", "NAMESPACE")

# instantiate the DAG
with DAG(
    start_date=datetime(2022, 6, 1),
    catchup=False,
    schedule="@daily",
    dag_id="KPO_XComs_example_dag",
) as dag:

    @task
    def extract_data():
        # simulating querying from a database
        data_point = random.randint(0, 100)
        return data_point

    transform = KubernetesPodOperator(
        # set task id
        task_id="transform",
        # specify the Docker image to launch
        image="<image location>",
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
        # pull a variable from XComs using Jinja templating and provide it
        # to the Pod as an environment variable
        env_vars={
            "DATA_POINT": """{{ ti.xcom_pull(task_ids='extract_data',
                                                 key='return_value') }}"""
        },
        # push the contents from xcom.json to Xcoms. Remember to only set this
        # argument to True if you have created the `airflow/xcom/return.json`
        # file within the Docker container run by the KubernetesPodOperator.
        do_xcom_push=True,
    )

    @task
    def load_data(**context):
        # pull the XCom value that has been pushed by the KubernetesPodOperator
        transformed_data_point = context["ti"].xcom_pull(
            task_ids="transform", key="return_value"
        )
        print(transformed_data_point)

    # set dependencies (tasks defined using Decorators need to be called)
    extract_data() >> transform >> load_data()
