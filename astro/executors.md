---
sidebar_label: 'Configure an executor'
title: 'Configure your Deployment executor'
id: 'executors'
---

The Airflow executor determines which worker resources run your scheduled tasks. 

On Astro, every Deployment requires an executor and you can update the executor at any time. After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. Use the information provided in this topic to learn how to configure the Celery and Kubernetes executors on Astro.

To learn more about executors in Airflow, see [Airflow executors](https://docs.astronomer.io/learn/airflow-executors-explained).

## Choose an executor

The difference between executors is based on how exactly tasks are distributed across worker resources. The executor you choose primarily affects the infrastructure cost of a Deployment and how efficiently your tasks execute. Astro currently supports two executors, both of which are available in the Apache Airflow open source project:

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

The Kubernetes executor runs each task in an individual Kubernetes Pod instead of in shared Celery workers. For each task that needs to run, the executor calls the Kubernetes API to dynamically launch a Pod for the task. You can specify the configuration of the task and Pod, including CPU and memory, in a `pod_override` file. When the task completes, the Pod terminates. On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every Deployment and is managed by Astronomer.

The Kubernetes executor is a good fit for teams that want fine-grained control over the execution environment of each of their tasks. Specifically, the Kubernetes executor is a good fit for your Deployment if:

- You have long-running tasks that require more than 24 hours to execute. The Kubernetes executor ensures that tasks longer than 24 hours are not interrupted when you deploys code.
- You experience a high number of dependency conflicts between tasks and could benefit from task isolation. For example, one task in your Deployment requires a different version of pandas than another task.
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

This topic discusses basic Celery executor configurations for a single worker queue. For instructions on how to configure multiple worker queues, see [Configure worker queues](configure-worker-queues.md). To add more worker types to your Deployment, see [Manage worker types](modify-cluster.md#manage-worker-types).

### Celery worker autoscaling logic

The following values are used to determine the number of workers that run in a single worker queue for a Deployment at a given time:

- The total number of tasks in a `queued` or `running` state
- The **Max Tasks Per Worker** setting for the worker queue

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

The number of workers determines Deployment [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment and across worker queues. To ensure that you can always run as many tasks as your workers allow, parallelism on Astro is automatically calculated with the following expression:

`[Parallelism]= ([Total number of running workers for all worker queues] * [The sum of all **Maximum tasks per worker*** values for all worker queues])`.

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, see [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

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
- Change worker node size and type on which your Pods run.

By default, each Kubernetes executor task on Astro runs in a dedicated Kubernetes Pod with 1 CPU and 512Mi of memory. These Pods run on a worker node in your Astro data plane. A single worker node can run multiple worker Pods at once. If a worker node can't run any more Pods, Astro automatically provisions a new worker node to begin running any queued tasks in new worker Pods.

### Customize a task and Kubernetes Pod

:::warning

While you can customize all values for a worker Pod, Astronomer does not recommend configuring complex Kubernetes infrastructure in your Pods, such as sidecars. These configurations have not been tested by Astronomer.

:::

For each task with the Kubernetes executor, you can customize its individual worker Pod and override the defaults used in Astro by configuring a `pod_override` file.

1. Add the following import to your DAG file:

    ```sh
    from kubernetes.client import models as k8s
    ```

2. Add a `pod_override` configuration to the DAG file containing the task. See the [`kubernetes-client`](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md) GitHub for a list of all possible settings you can include in the configuration.
3. Specify the `pod_override` in the task's parameters.

See [Manage task CPU and memory](#example-set-CPU-or-memory-limits-and-requests) for an example `pod_override` configuration. 

### Example: Set CPU or memory limits and requests

One of the most common use cases for customizing a Kubernetes worker Pod is to request a specific amount of resources for a task. When requesting resources, make sure that your requests don't exceed the available resources in your current [Pod worker node type](#change-the-pod-worker-node-type).

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

### Change the worker node type

A Deployment using the Kubernetes executor runs worker Pods on a single `default` worker queue. You can change the type of worker node that this queue uses from the Cloud UI.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit the `default` worker queue.

3. In the **Worker Type** list, select the type of worker node to run your Pods on.

4. Click **Update Queue**.

## See also

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors explained](https://docs.astronomer.io/learn/airflow-executors-explained)
