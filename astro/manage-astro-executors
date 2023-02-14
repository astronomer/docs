---
sidebar_label: 'Manage executors on Astro'
title: 'Manage executors on Astro'
id: 'manage-astro-executors'
---

<head>
  <meta name="description" content="Learn how to select and manage Astro executors." />
  <meta name="og:description" content="Learn how to select and manage Astro executors." />
</head>

Executors are responsible for executing tasks within your DAGs. You can select Celery or Kubernetes executors in Astro. Selecting an appropriate executor can often be challenging and the intent of this topic is to provide you with the information you need to make an informed choice. If you're new to Astro and executors, see [Airflow Executors](/learn/airflow-executors-explained).

A single executor is assigned to each Deployment and you can change the executor assignment at any time. To assign an executor or modify its resource settings, see [Configure a Deployment](configure-deployment-resources.md).

## Celery executor

The Celery executor works with a pool of workers and communicates with them to delegate tasks. Workers are statically configured and running all the time regardless of workload. 

### Benefits

- High availability.
- Allows additional workers to be added to cope with higher demand (horizontal scaling).
- Provides a grace period for worker termination.

### Known limitations

- Expense.
- Complicated set up.
- More maintenance.

### Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

### Adjust worker settings

You select and modify Celery executor settings in the Cloud UI. Astro automatically allocates resources to workers created by the Celery executor, but you can adjust them to meet your requirements. See [Configure a Deployment](configure-deployment-resources.md). The settings you can adjust include:

- Default Max Tasks Per Worker - The maximum number of tasks that a single worker can process simultaneously.This is equivalent to worker concurrency in Airflow.
- Default Worker Count - The minimum and maximum number of workers that can run in parallel in the worker queue. 
- Scheduler Resources - The total CPU and memory allocated to each scheduler in your Deployment.
- Scheduler count - The number of Airflow schedulers available in your Deployment.

Worker settings are defined with worker queues. See [Configure worker queues](configure-worker-queues.md).

### Worker autoscaling logic

The following values are used to determine the number of workers that run for each Deployment worker queue at a given time:

- The total number of tasks in a `queued` or `running` state
- The **Default Max Tasks Per Worker** setting for the worker queue

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

The number of workers determines Deployment [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment and across worker queues. To ensure that you can always run as many tasks as your workers allow, parallelism is calculated with the following expression:

`[Parallelism]= ([Total number of running workers for all worker queues] * [The sum of all **Maximum tasks per worker*** values for all worker queues])`.

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, see [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Kubernetes executor

The [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) dynamically launches and terminates Pods to run Airflow tasks. The Kubernetes executor can use the Kubernetes API to create Pods for running tasks. The Kubernetes executor is implemented at the configuration level of the Airflow instance, which means a new Kubernetes Pod is created for every task instance. The Kubernetes executor is recommended when you need to control resource optimization, isolate your workloads, maintain long periods without running tasks, or run tasks for extended periods during deployments.

The Kubernetes executor runs as a process in the Airflow Scheduler. You select and modify Kubernetes executor settings in the Cloud UI. Astro automatically allocates resources to Pods created by the Kubernetes executor, but you can adjust them to meet your requirements. See [Configure a Deployment](configure-deployment-resources.md).

### Benefits

- Fault tolerance.  A task that fails doesn't cause other tasks to fail.
- Run tasks in a Kubernetes cluster outside of the Astro data plane. This can be helpful when you need to run individual tasks on infrastructure that isn't currently supported by Astro, such as GPU nodes or other third-party services.
- Specify CPU and memory limits or minimums to optimize performance and reduce costs.
- Task isolation. A task uses only the resources allocated to it and it can't consume resources allocated to other tasks. 
- Running tasks are not interrupted when a deploy is pushed.

On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every cluster in the data plane and is managed by Astronomer.

### Known limitations

- Tasks take longer to start and this causes task latency.
- Cross-account service accounts are not supported on Pods launched in an Astro cluster. To allow access to external data sources, you can provide credentials and secrets to tasks.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- The `pod_template_file` argument is not supported on Pods launched in an Astro cluster. If you use the `pod_template_file` argument, customized values are overridden when they are required by Astronomer and your tasks will fail. Astronomer recommends using `python-kubernetes-sdk`. See [Astro Python SDK ReadTheDocs](https://astro-sdk-python.readthedocs.io/en/stable/).

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

When this DAG runs, it launches a Kubernetes Pod with exactly 800m of CPU and 3Gi of memory as long as that infrastructure is available in your cluster. Once the task finishes, the Pod terminates gracefully.

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors](https://docs.astronomer.io/learn/airflow-executors-explained)
