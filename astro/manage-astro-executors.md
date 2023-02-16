---
sidebar_label: 'Manage Deployment executors'
title: 'Manage Deployment executors'
id: 'manage-astro-executors'
---

<head>
  <meta name="description" content="Learn how to select and manage Astro executors." />
  <meta name="og:description" content="Learn how to select and manage Astro executors." />
</head>

After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. This document provides you with an overview of how to configure the Celery and Kubernetes executors on Astro. To choose an executor for your Deployment, see [Choose an executor](configure-deployment-resources.md#choose-an-executor) and [Airflow executors](https://docs.astronomer.io/learn/airflow-executors-explained).

## Manage the Celery executor

The Celery executor assigns tasks to workers with preset amounts of CPU and memory based on the cloud instance type they run on. On Astro, workers are organized into pools called worker queues that automatically scale worker count based on how many tasks you're running. Each Deployment running the Celery executor has a default worker queue that requires no additional configuration to start running tasks. 

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

Celery worker scaling is configured at the worker queue level. Changing how Celery workers scale ensures that your Deployment always has enough resources to run tasks, but never too much that you pay for unnecessary infrastructure.

- **Max Tasks Per Worker**: The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. It is 16 by default.
- **Worker Count (Min-Max)**: The minimum and maximum number of workers that can run at a time. The number of running workers changes regularly based on **Maximum Tasks per Worker** and the current number of tasks in a queued or running state. By default, the minimum number of workers is 1 and the maximum is 10.

## Kubernetes executor

The [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) dynamically launches and terminates Pods to run Airflow tasks. The Kubernetes executor leverages the Kubernetes API to create Pods for running tasks. The Kubernetes executor is implemented at the configuration level of the Airflow instance, which means a new Kubernetes Pod is created for every task instance. The Kubernetes executor is recommended when you need to control resource optimization, isolate your workloads, maintain long periods without running tasks, or run tasks for extended periods during deployments.

You select and modify Kubernetes executor settings in the Cloud UI. Astro automatically allocates resources to Pods created by the Kubernetes executor, but you can adjust them to meet your requirements. See [Configure a Deployment](configure-deployment-resources.md).

### Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

### Manage task CPU and memory

Astro automatically allocates resources to Pods created by the Kubernetes executor. By default, Pods are configured to use 1 cpu and 512Mi.  A `pod_template_file` can't be used on Astro to override the default settings. The following example shows how you can use `pod_override` within a Kubernetes V1pod to override these settings to meet your specific requirements:

```python {20}
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


## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors](https://docs.astronomer.io/learn/airflow-executors-explained)
