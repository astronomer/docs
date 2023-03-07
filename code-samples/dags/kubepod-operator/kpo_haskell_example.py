from airflow import DAG
from pendulum import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.configuration import conf

# get the current Kubernetes namespace Airflow is running in
namespace = conf.get("kubernetes", "NAMESPACE")

# set the name that will be printed
name = "your_name"

# instantiate the DAG
with DAG(
    start_date=datetime(2022, 6, 1),
    catchup=False,
    schedule="@daily",
    dag_id="KPO_different_language_example_dag",
) as dag:
    say_hello_name_in_haskell = KubernetesPodOperator(
        # unique id of the task within the DAG
        task_id="say_hello_name_in_haskell",
        # the Docker image to launch
        image="<image location>",
        # launch the Pod on the same cluster as Airflow is running on
        in_cluster=True,
        # launch the Pod in the same namespace as Airflow is running in
        namespace=namespace,
        # Pod configuration
        # name the Pod
        name="my_pod",
        # give the Pod name a random suffix, ensure uniqueness in the namespace
        random_name_suffix=True,
        # attach labels to the Pod, can be used for grouping
        labels={"app": "backend", "env": "dev"},
        # reattach to worker instead of creating a new Pod on worker failure
        reattach_on_restart=True,
        # delete Pod after the task is finished
        is_delete_operator_pod=True,
        # get log stdout of the container as task logs
        get_logs=True,
        # log events in case of Pod failure
        log_events_on_failure=True,
        # pass your name as an environment var
        env_vars={"NAME_TO_GREET": f"{name}"},
    )
