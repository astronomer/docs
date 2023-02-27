---
title: "Use the Kubernetes Executor on Astro"
id: kubernetes-executor
---

:::caution

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews).

:::

The [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) dynamically launches and terminates Pods to run Airflow tasks. The executor starts a new Kubernetes Pod to execute each individual task run, and then shuts down the Pod when the task run completes. This executor is recommended when you need to control resource optimization, isolate your workloads, maintain long periods without running tasks, or run tasks for extended periods during deployments.

By default, each task on Astro runs in a dedicated Kubernetes Pod with up to 1 CPU and 256Mi of memory. These Pods run on a cloud worker node, which can run multiple worker Pods at once. If a worker node can’t run any more Pods, Astro automatically provisions a new worker node to begin running any queued tasks in new Pods.

## Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

## Use the Kubernetes executor in a Deployment

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. Select **Kubernetes** in the **Executor** list. If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.
5. Click **Update**.

## Run tasks in a custom Kubernetes worker Pod

While you can technically customize all values for a worker Pod, Astronomer recommends against configuring complex Kubernetes infrastructure in your Pods such as sidecars. These configurations have not been tested by Astronomer.

You can configure multiple different custom worker Pods to override the default Astro worker Pod on a per-task basis. You might complete this setup to change how many resources the Pod uses, or to create an `empty_dir` for tasks to store temporary files.

1. Add the following import to your DAG file:
    
    ```
    from kubernetes.client import models as k8s
    ```
    
2. Add a `pod_override` configuration to the DAG file containing the task. See the `[kubernetes-client](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md)` GitHub for a list of all possible settings you can include in the configuration.
3. Specify the `pod_override` in the task’s parameters.

See [Manage task CPU and memory](about:blank#manage-task-cpu-and-memory) for an example `pod_override` configuration.

## Manage task CPU and memory

One of the most common uses cases for customizing a Kubernetes worker Pod is to request a specific amount of resources for your task. The following example shows how you can use a `pod_override` configuration in your DAG code to request custom resources for a task:

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

## Change the Pod worker node type

A Deployment using the Kubernetes executor runs worker Pods on a single `default` worker queue. You can change the type of worker node that this queue uses from the Cloud UI.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Worker Queues** tab and then click **Edit** to edit the `default` worker queue.
3. In the **Worker Type** list, select the type of worker node to run your worker Pods on.
4. Click **Update Queue**.

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors](https://docs.astronomer.io/learn/airflow-executors-explained)
