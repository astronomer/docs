---
title: 'Run the Kubernetes executor on Astronomer Software'
sidebar_label: 'Kubernetes executor'
id: kubernetes-executor
description: Run and configure the Kubernetes executor on Astronomer.
---

The [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html) creates individual Pods that dynamically delegate work and resources to individual tasks. For each task that needs to run, the executor talks to the Kubernetes API and dynamically launches Pods which terminate when the task is completed.

You can customize your Kubernetes Pods to scale depending on how many Airflow tasks you're running at a given time. It also means you can configure the following for each individual Airflow task:

- Memory allocation
- Service accounts
- Airflow image

To configure these resources for a given tasks's Pod, you specify a `pod_override` in your DAG code. To specify a Pod template for many or all of your tasks, you can write a helper function to construct a `pod_override` in your DAGs or configure a global For more information on configuring Pod template values, reference the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates).

## Prerequisites

You must have an Airflow Deployment on Astronomer running with the Kubernetes executor. For more information on configuring an executor, see [Configure a Deployment](configure-deployment.md). To learn more about different executor types, see [Airflow executors explained](https://docs.astronomer.io/learn/airflow-executors-explained).

## Configure Kubernetes Pods for a specific task using a `pod_override` configuration

For each task with the Kubernetes executor, you can customize its individual worker Pod and override the defaults used in Astronomer Software by configuring a `pod_override` file.

1. Add the following import to your DAG file:

    ```sh
    from kubernetes.client import models as k8s
    ```

2. Add a `pod_override` configuration to the DAG file containing the task. See the [`kubernetes-client`](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md) GitHub for a list of all possible settings you can include in the configuration.
3. Specify the `pod_override` in the task's parameters.

### Example: Set CPU or memory limits and requests

One of the most common use cases for customizing a Kubernetes worker Pod is to request a specific amount of resources for a task.

The following example shows how you can use a `pod_override` configuration in your DAG code to request custom resources for a task:

```python
import pendulum
import time

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.example_dags.libs.helper import print_stuff
from kubernetes.client import models as k8s


k8s_exec_config_resource_requirements = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="base",
                    resources=k8s.V1ResourceRequirements(
                        requests={"cpu": 0.5, "memory": "1024Mi"},
                        limits={"cpu": 0.5, "memory": "1024Mi"}
                    )
                )
            ]
        )
    )
}

with DAG(
    dag_id="example_kubernetes_executor_pod_override_sources",
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False
):


    @task(executor_config=k8s_exec_config_resource_requirements)
    def resource_requirements_override_example():
        print_stuff()
        time.sleep(60)

    resource_requirements_override_example()
```

When this DAG runs, it launches a Kubernetes Pod with exactly 0.5m of CPU and 1024Mi of memory as long as that infrastructure is available in your cluster. Once the task finishes, the Pod terminates gracefully.

## Mount secret environment variables to worker Pods

<!-- Same content in other products -->

[Deployment environment variables](environment-variables.md) marked as secrets are stored in a Kubernetes secret called `<release-name>-env` on your Deployment namespace. To use a secret value in a task running on the KubernetesExecutor, mount the secret to the Pod running the task.

1. Run the following command to find the namespace (release name) of your Airflow Deployment:

    ```sh
    kubectl get ns
    ```

2. Add the following import to your DAG file:
   
    ```python
    from airflow.kubernetes.secret import Secret
    ```

3. Define a Kubernetes `Secret` in your DAG instantiation in the following format:

    ```python
    secret_env = Secret(deploy_type="env", deploy_target="<SECRET_KEY>", secret="<release-name>-env", key="<SECRET_KEY>")
    namespace = conf.get("kubernetes", "<release-name>")
    ```

4. Specify the `Secret` in the `secret_key_ref` section of your `pod_override` configuration.

5. In the task where you want to use the secret value, add the following task-level argument:

    ```python
    op_kwargs={
            "env_name": secret_env.deploy_target
    },
    ```

6. In the executable for the task, call the secret value using `os.environ[env_name]`.

In the following example, a secret named `MY_SECRET` is pulled from `infrared-photon-7780-env` and printed to logs.
 
```python
import pendulum
from kubernetes.client import models as k8s

from airflow.configuration import conf
from airflow.kubernetes.secret import Secret
from airflow.models import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.python import PythonOperator


def print_env(env_name):
    import os
    print(os.environ[env_name])

with DAG(
        dag_id='test-secret',
        start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
        end_date=pendulum.datetime(2022, 1, 5, tz="UTC"),
        schedule_interval="@once",
) as dag:
    secret_env = Secret(deploy_type="env", deploy_target="MY_SECRET", secret="infrared-photon-7780-env", key="MY_SECRET")
    namespace = conf.get("kubernetes", "infrared-photon-7780")

    p = PythonOperator(
        python_callable=print_env,
        op_kwargs={
            "env_name": secret_env.deploy_target
        },
        task_id='test-py-env',
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env=[
                                k8s.V1EnvVar(
                                    name=secret_env.deploy_target,
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(name=secret_env.secret,
                                                                               key=secret_env.key)
                                    ),
                                )
                            ],
                        )
                    ]
                )
            ),
        }
    )
```