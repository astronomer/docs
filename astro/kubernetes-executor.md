---
sidebar_label: 'Configure the Kubernetes executor'
title: 'Configure the Kubernetes executor'
id: 'kubernetes-executor'
---

On Astro, you can configure Kubernetes executor in the following ways:

- Change the resource usage for the default Pods on which your tasks run in the Cloud UI.
- Customize individual Pods for tasks, including CPU and memory requests, using a `pod_override` configuration in your DAG code. 

:::info

This document describes how to configure individual task Pods for different use cases. To configure defaults for all Kubernetes executor task pods, see [Configure Kubernetes Pod resources](deployment-settings.md#configure-kubernetes-pod-resources).

:::

## Customize a task's Kubernetes Pod

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

### Example: Set CPU or memory limits and requests

You can request a specific amount of resources for a Kubernetes worker Pod so that a task always has enough resources to run successfully. When requesting resources, make sure that your requests don't exceed the resource limits in your [default Pod](deployment-settings.md#configure-kubernetes-pod-resources).

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

When this DAG runs, it launches a Kubernetes Pod with exactly 0.5m of CPU and 1024Mi of memory, as long as that infrastructure is available in your Deployment. After the task finishes, the Pod terminates gracefully.

## (Astro Hybrid only) Change the Kubernetes executor's worker node type

:::info

This section applies only to [Astro Hybrid](hybrid-overview.md) users. To see whether you're an Astro Hybrid user, open go to the Cloud UI, click on your Workspace name and go to **Organization Settings** > **General**. Your Astro product type is listed under **Product Type**.

:::

A Deployment on Astro Hybrid that uses the Kubernetes executor runs worker Pods on a single `default` worker queue. You can change the type of worker that this queue uses from the Cloud UI.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit the `default` worker queue.

3. In the **Worker Type** list, select the type of worker to run your Pods on.

4. Click **Update Queue**.


## See also

- [Configure Kubernetes Pod resources](deployment-settings.md#configure-kubernetes-pod-resources)
- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors explained](https://docs.astronomer.io/learn/airflow-executors-explained)
