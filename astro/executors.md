---
sidebar_label: 'Configure an executor'
title: 'Configure your Deployment executor'
id: 'executors'
---

The Airflow executor determines which worker resources run your scheduled tasks. 

On Astro, every Deployment requires an executor and you can update the executor at any time. After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. Use the information provided in this topic to learn how to configure the Celery and Kubernetes executors on Astro.

To learn more about executors in Airflow, see [Airflow executors](https://docs.astronomer.io/learn/airflow-executors-explained).

## Choose an executor

The difference between executors is based on how tasks are distributed across worker resources. The executor you choose affects the infrastructure cost of a Deployment and how efficiently your tasks execute. Astro currently supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

Read the following topics to learn about the benefits and limitations of each executor. For information about how to change the executor of an existing Deployment, see [Update the Deployment executor](configure-deployment-resources.md#update-the-deployment-executor).

### Celery executor

The Celery executor is the default for all new Deployments. It uses a group of workers, each of which can run multiple tasks at a time. Astronomer uses [worker autoscaling logic](#celery-worker-autoscaling-logic) to determine how many workers run on your Deployment at a given time.

The Celery executor is a good option for most use cases. Specifically, the Celery executor is a good fit for your Deployment if:

- You're just getting started with Airflow.
- You want to use multiple worker queues. This allows you to use multiple worker node types for different types of tasks and optimize for task performance. See [Configure worker queues](configure-worker-queues.md).
- You have a high number of short-running tasks and want to ensure low latency between tasks.
- You don't often experience conflicts between Python or OS-level packages and don't require dependency isolation.

If you regularly experience dependency conflicts or find that some tasks consume the resources of other tasks and cause them to fail, Astronomer recommends implementing worker queues or moving to the Kubernetes executor.

See [Manage the Celery executor](#manage-the-celery-executor) to learn more about how to configure the Celery executor.

### Kubernetes executor

The Kubernetes executor runs each task in an individual Kubernetes Pod instead of in shared Celery workers. For each task that needs to run, the executor calls the Kubernetes API to dynamically launch a Pod for the task. You can specify the configuration of the task's Pod, including CPU and memory, as part of your DAG definition using the [Kubernetes Python Client](https://github.com/kubernetes-client/python) and the `pod_override` arg. When the task completes, the Pod terminates. On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every Deployment and is managed by Astronomer.

The Kubernetes executor is a good fit for teams that want fine-grained control over the execution environment of each of their tasks. Specifically, the Kubernetes executor is a good fit for your Deployment if:

- You have long-running tasks that require more than 24 hours to execute. The Kubernetes executor ensures that tasks longer than 24 hours are not interrupted when you deploy code.
- Your tasks are compute-intensive or you are processing large volumes of data within the task. Kubernetes executor tasks run separately in a dedicated pod per task. 
- You have a strong understanding of the CPU and memory that your tasks require and would benefit from being able to allocate and optimize infrastructure resources at the task level.
- You have had issues running certain tasks reliably with the Celery executor.
  
The primary limitation with the Kubernetes executor is that each task takes up to 1 minute to start running once scheduled. If you're running short-running tasks and cannot tolerate high latency, Astronomer recommends the Celery executor. To learn more about using the Kubernetes executor, see [Manage the Kubernetes executor](#manage-the-kubernetes-executor).

:::tip

If only some of your tasks need an isolated execution environment, consider using the [KubernetesPodOperator](kubernetespodoperator.md) with the Celery executor.

:::

## Configure the Celery executor

On Astro, you can configure Celery executor in the following ways:

- The type and size of your workers.
- The minimum and maximum number of workers that your Deployment can run at a time.
- The number of tasks that each worker can run at a time.

You can set these configurations per worker queue, which is a set of configurations that apply to a group of workers in your Deployment. With the celery executor, you can configure multiple worker queues for different types of tasks and assign tasks to those queues in your DAG code.

This topic discusses basic Celery executor configurations for a single worker queue. For instructions on how to configure multiple worker queues, see [Configure worker queues](configure-worker-queues.md).

### Celery worker autoscaling logic

The number of Celery workers running per worker queue on your Deployment at a given time is based on two values:

- The total number of tasks in a `queued` or `running` state
- The worker queue's setting for **Maximum Tasks per Worker**

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

Deployment [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism) is the maximum number of tasks that can run concurrently across worker queues. To ensure that you can always run as many tasks as your worker queues allow, parallelism is calculated with the following expression:

`[Parallelism]= ([The sum of all 'Max Worker Count' values for all worker queues] * [The sum of all 'Maximum tasks per worker' values for all worker queues])`.

KEDA computes these calculations every ten seconds. When KEDA determines that it can scale down a worker, it waits for five minutes after the last running task on the worker finishes before terminating the worker Pod.

To learn more about how changes to a Deployment can affect worker resource allocation, see [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Configure Celery worker scaling

For each worker queue on your Deployment, you have to specify certain settings that affect worker autoscaling behavior. If you're new to Airflow, Astronomer recommends using the defaults in Astro for each of these settings.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit a worker queue.

3. Configure the following settings:

    - **Max Tasks Per Worker**: The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. It is 16 by default.
    - **Worker Count (Min-Max)**: The minimum and maximum number of workers that can run at a time. The number of running workers changes regularly based on **Maximum Tasks per Worker** and the current number of tasks in a queued or running state. By default, the minimum number of workers is 1 and the maximum is 10.
    
4. Click **Update Queue**.

## Configure the Kubernetes executor

On Astro, you can configure Kubernetes executor in the following ways:

- Customize individual tasks, including CPU and memory requests, using a `pod_override` configuration. 
- Change the worker node type on which your Pods run.

### Kubernetes worker autoscaling logic

By default, each task on Astro runs in a dedicated Kubernetes Pod with 1 CPU and 256Mi of memory. These Pods run on a worker node in your Astro Deployment. If a worker node can't run any more Pods, Astro automatically provisions a new worker node to begin running any queued tasks in new Pods.

### Customize a task's Kubernetes Pod

:::warning

While you can customize all values for a worker Pod, Astronomer does not recommend configuring complex Kubernetes infrastructure in your Pods, such as sidecars. These configurations have not been tested by Astronomer.

:::

For each task running with the Kubernetes executor, you can customize its individual worker Pod and override the defaults used in Astro by configuring a `pod_override` file.

1. Add the following import to your DAG file:

    ```sh
    from kubernetes.client import models as k8s
    ```

2. Add a `pod_override` configuration to the DAG file containing the task. See the [`kubernetes-client`](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md) GitHub for a list of all possible settings you can include in the configuration.
3. Specify the `pod_override` in the task's parameters.

See [Manage task CPU and memory](#example-set-CPU-or-memory-limits-and-requests) for an example `pod_override` configuration. 

#### Example: Set CPU or memory limits and requests

One of the most common use cases for customizing a Kubernetes worker Pod is to request a specific amount of resources for a task. When requesting resources, make sure that your requests don't exceed the available resources in your current [Pod worker node type](#change-the-pod-worker-node-type).

The following example shows how you can use a `pod_override` configuration in your DAG code to request custom resources for a task:

```python
import pendulum
import time

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
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
    BashOperator(
      task_id="bash_resource_requirements_override_example",
      bash_command="echo hi",
      executor_config=k8s_exec_config_resource_requirements
    )

    @task(executor_config=k8s_exec_config_resource_requirements)
    def resource_requirements_override_example():
        print_stuff()
        time.sleep(60)

    resource_requirements_override_example()
```

When this DAG runs, it launches a Kubernetes Pod with exactly 0.5m of CPU and 1024Mi of memory as long as that infrastructure is available in your Deployment. Once the task finishes, the Pod terminates gracefully.

### Mount secret environment variables to worker Pods

<!-- Same content in other products -->

Astro [environment variables](environment-variables.md) marked as secrets are stored in a Kubernetes secret called `env-secrets`. To use a secret value in a task running on the Kubernetes executor, you pull the value from `env-secrets` and mount it to the Pod running your task as a new Kubernetes Secret.

1. Add the following import to your DAG file:
   
    ```python
    from airflow.kubernetes.secret import Secret
    ```

2. Define a Kubernetes `Secret` in your DAG instantiation using the following format:

    ```python
    secret_env = Secret(deploy_type="env", deploy_target="<VARIABLE_KEY>", secret="env-secrets", key="<VARIABLE_KEY>")
    namespace = conf.get("kubernetes", "NAMESPACE")
    ```

3. Specify the `Secret` in the `secret_key_ref` section of your `pod_override` configuration.

4. In the task where you want to use the secret value, add the following task-level argument:

    ```python
    op_kwargs={
            "env_name": secret_env.deploy_target
    },
    ```

5. In the executable for the task, call the secret value using `os.environ[env_name]`.

In the following example, a secret named `MY_SECRET` is pulled from `env-secrets` and printed to logs.
 
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
    secret_env = Secret(deploy_type="env", deploy_target="MY_SECRET", secret="env-secrets", key="MY_SECRET")
    namespace = conf.get("kubernetes", "NAMESPACE")

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

### Change the worker node type

A Deployment using the Kubernetes executor runs worker Pods on a single `default` worker queue. You can change the type of worker that this queue uses from the Cloud UI.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit the `default` worker queue.

3. In the **Worker Type** list, select the type of worker to run your Pods on.

4. Click **Update Queue**.

## See also

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors explained](https://docs.astronomer.io/learn/airflow-executors-explained)
