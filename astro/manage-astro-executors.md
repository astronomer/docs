---
sidebar_label: 'Manage Deployment executors'
title: 'Manage Deployment executors'
id: 'manage-astro-executors'
---

<head>
  <meta name="description" content="Learn how to select and manage Astro executors." />
  <meta name="og:description" content="Learn how to select and manage Astro executors." />
</head>

After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. Use the information provided in this topic to learn how to configure the Celery and Kubernetes executors on Astro. To choose an executor for your Deployment, see [Choose an executor](configure-deployment-resources.md#choose-an-executor).

## Manage the Celery executor

The Celery executor assigns tasks to workers with preset amounts of CPU and memory. 

On Astro, each Celery worker utilizes an entire worker node instance on your cloud and can run multiple tasks at once. Workers are organized into pools called worker queues that automatically scale worker count based on how many tasks you're running. Each Deployment running the Celery executor has a default worker queue that requires no additional configuration to start running tasks. 

This topic discusses basic Celery executor configurations for scaling workers in a worker queue. For advanced resource configuration steps, including how to configure multiple worker queues, see [Configure worker queues](configure-worker-queues.md).

### Prerequisites

- An Astro [Deployment](create-deployment.md).

### Celery worker autoscaling logic

The following values are used to determine the number of workers that run for each Deployment worker queue at a given time:

- The total number of tasks in a `queued` or `running` state
- The **Default Max Tasks Per Worker** setting for the worker queue

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

The number of workers determines Deployment [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment and across worker queues. To ensure that you can always run as many tasks as your workers allow, parallelism is calculated with the following expression:

`[Parallelism]= ([Total number of running workers for all worker queues] * [The sum of all **Maximum tasks per worker*** values for all worker queues])`.

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, see [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Configure Celery worker scaling

Celery worker scaling is configured at the worker queue level. Changing worker scaling behavior ensures that your Deployment always has enough resources to run tasks, but never so much that you pay for unnecessary infrastructure.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit a worker queue.

3. Configure the following settings:

    - **Max Tasks Per Worker**: The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. It is 16 by default.
    - **Worker Count (Min-Max)**: The minimum and maximum number of workers that can run at a time. The number of running workers changes regularly based on **Maximum Tasks per Worker** and the current number of tasks in a queued or running state. By default, the minimum number of workers is 1 and the maximum is 10.
    
4. Click **Update Queue**.

## Manage the Kubernetes executor

The [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) dynamically launches and terminates Pods to run Airflow tasks. The executor starts a new Kubernetes Pod to execute each individual task run, and then shuts down the Pod when the task run completes. This executor is recommended when you need to control resource optimization, isolate your workloads, maintain long periods without running tasks, or run tasks for extended periods during deployments.

By default, each task on Astro runs in a dedicated Kubernetes Pod with 1 CPU and 512Mi of memory. These Pods run on a cloud worker node, which can run multiple worker Pods at once. If a worker node can't run any more Pods, Astro automatically provisions a new worker node to begin running any queued tasks in new Pods.

### Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

### Run tasks in a custom Kubernetes worker Pod

:::warning

While you can technically customize all values for a worker Pod, Astronomer recommends against configuring complex Kubernetes infrastructure in your Pods such as sidecars. These configurations have not been tested by Astronomer.

:::

You can configure multiple different custom worker Pods to override the default Astro worker Pod on a per-task basis. You might complete this setup to change how many resources the Pod uses, or to create an `empty_dir` for tasks to store temporary files.

1. Add the following import to your DAG file:

    ```sh
    from kubernetes.client import models as k8s
    ```

2. Add a `pod_override` configuration to the DAG file containing the task. See the [`kubernetes-client`](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md) GitHub for a list of all possible settings you can include in the configuration.
3. Specify the `pod_override` in the task's parameters.

See [Manage task CPU and memory](#manage-task-cpu-and-memory) for an example `pod_override` configuration. 

### Manage task CPU and memory

One of the most common use cases for customizing a Kubernetes worker Pod is to request a specific amount of resources for your task. When requesting resources, make sure that your requests don't exceed the available resources in your current [Pod worker node type](#change-the-pod-worker-node-type).

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

### Create temporary storage for tasks

The Airflow metadata database has limited temporary storage for Airflow tasks. Creating or storing files in the metadata database system is not recommended, as it is unlikely that there will be sufficient storage for your tasks and the data will be available to other worker Pods. To create or store temporary files for task execution, Astronomer recommends creating a temporary folder for each task worker Pod.

The following example shows how you can add a temporary folder to a Pod using a `pod_override` configuration:

```python
from kubernetes.client import models as k8s
import pendulum
import time

from airflow import DAG
from airflow.decorators import task
from airflow.example_dags.libs.helper import print_stuff


volumes = [k8s.V1Volume(name="cache-volume", empty_dir=k8s.V1EmptyDirVolumeSource())]

volume_mounts = [k8s.V1VolumeMount(mount_path="/cache", name="cache-volume")]

executor_config = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[k8s.V1Container(name="base", volume_mounts=volume_mounts)],
            volumes=volumes,
        )
    )
}

with DAG(
    dag_id="empty_dir_example_dag",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:

    @task(executor_config=executor_config)
    def empty_dir_example():
        """
        Tests whether the volume has been mounted.
        """
        with open('/cache/volume_mount_test.txt', 'w') as foo:
            foo.write('Hello')

        return_code = os.system("cat /cache/volume_mount_test.txt")
        assert return_code == 0

    empty_dir_example()
```

### Change the Pod worker node type

A Deployment using the Kubernetes executor runs worker Pods on a single `default` worker queue. You can change the type of worker node that this queue uses from the Cloud UI.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit the `default` worker queue.

3. In the  **Worker Type** list, select the type of worker node to run your worker Pods on.

4. Click **Update Queue**.

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors](https://docs.astronomer.io/learn/airflow-executors-explained)
