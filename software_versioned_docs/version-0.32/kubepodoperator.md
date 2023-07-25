---
title: 'Run the KubernetesPodOperator on Astronomer Software'
sidebar_label: 'Run the KubernetesPodOperator on Astronomer Software'
id: kubepodoperator
description: Run the KubernetesPodOperator on Astronomer Software.
---

The [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) is one of the most powerful Apache Airflow operators. Similar to the Kubernetes executor, this operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod once the task is complete. This results in an isolated, containerized execution environment for each task that is separate from tasks otherwise being executed by Celery workers.

## Benefits of the KubernetesPodOperator

The KubernetesPodOperator enables you to:

- Execute a custom Docker image per task with Python packages and dependencies that would otherwise conflict with the rest of your Deployment's dependencies. This includes Docker images in a private registry or repository.
- Specify CPU and Memory as task-level limits or minimums to optimize for cost and performance.
- Write task logic in a language other than Python. This gives you flexibility and can enable new use cases across teams.
- Scale task growth horizontally in a way that is cost-effective, dynamic, and minimally dependent on worker resources.
- Set Kubernetes-native configurations in a YAML file, including volumes, secrets, and affinities.

## Prerequisites

- A running Airflow Deployment on Astronomer Software

> **Note:** If you haven't already, Astronomer recommends testing the KubernetesPodOperator in your local environment. See [Running KubernetesPodOperator locally](https://docs.astronomer.io/learn/kubepod-operator).

## Set Up the KubernetesPodOperator

### Import the operator

1. Run the following command to install the  `apache-airflow-providers-cncf-kubernetes` package:

    ``bash
    pip install apache-airflow-providers-cncf-kubernetes
    ``
2. Run the following command to import the KubernetesPodOperator:

    ``python
    from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
    ``
### Specify parameters

Instantiate the operator based on your image and setup:

```python
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


namespace = conf.get("kubernetes", "NAMESPACE")

KubernetesPodOperator(
    namespace=namespace,
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    arguments=["echo", "10", "echo pwd"],
    labels={"<pod-label>": "<label-name>"},
    name="airflow-test-pod",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="task-two",
    get_logs=True,
)
```

For each instantiation of the KubernetesPodOperator, you must specify the following values:

- `namespace = conf.get("kubernetes", "NAMESPACE")`: Every Deployment runs on its own Kubernetes namespace. Information about this namespace can be programmatically imported as long as you set this variable.
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. The value you specify is assumed to be an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, read [Pull images from a Private Registry](#pulling-images-from-a-private-registry).
- `in_cluster=True`: When this value is set, your task will run within the cluster from which it's instantiated. This ensures that the Kubernetes Pod running your task has the correct permissions within the cluster.
- `is_delete_operator_pod=True`: This setting ensures that once a KubernetesPodOperator task is complete, the Kubernetes Pod that ran that task is terminated. This ensures that there are no unused pods in your cluster taking up resources.

#### Add resources to your Deployment on Astronomer

The KubernetesPodOperator is entirely powered by the resources allocated to the `Extra Capacity` slider of your deployment's `Configure` page in the [Software UI](manage-workspaces.md) in lieu of needing a Celery worker (or scheduler resources for those running the Local Executor). Raising the slider will increase your namespace's [resource quota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) such that Airflow has permissions to successfully launch pods within your deployment's namespace.

> **Note:** Your Airflow scheduler and webserver will remain necessary fixed resources that ensure the rest of your tasks can execute and that your deployment stays up and running.

In terms of resource allocation, Astronomer recommends starting with **10AU** in `Extra Capacity` and scaling up from there as needed. If it's set to 0, you'll get a permissions error:

```
ERROR - Exception when attempting to create namespace Pod.
Reason: Forbidden
"Failure","message":"pods is forbidden: User \"system:serviceaccount:astronomer-cloud-solar-orbit-4143:solar-orbit-4143-airflow-worker\" cannot create pods in the namespace \"datarouter\"","reason":"Forbidden","details":{"kind":"pods"},"code":403}
```

On Astronomer Software, the largest node a single pod can occupy is dependent on the size of your underlying node pool.

> **Note:** If you need to increase your [limit range](https://kubernetes.io/docs/concepts/policy/limit-range/) on Astronomer Software, contact your system admin. \\

#### Define resources per task

A notable advantage of leveraging Airflow's KubernetesPodOperator is that you can control compute resources in the task definition.

> **Note:** If you're using the Kubernetes Executor, note that this value is separate from the `executor_config` parameter. In this case, the `executor_config` would only define the Airflow worker that is launching your Kubernetes task.

### Example Task Definition:

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get('kubernetes', 'NAMESPACE')

# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = '/usr/local/airflow/include/.kube/config'
    in_cluster = False
else:
    in_cluster = True
    config_file = None

dag = DAG("example_kubernetes_pod", schedule="@once", default_args=default_args)

# This is where you define your resource allocation.
compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu": "800m", "memory": "3Gi"},
    requests={"cpu": "800m", "memory": "3Gi"}
)

with dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="hello-world",
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-for-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        container_resources=compute_resources,
        is_delete_operator_pod=True,
        get_logs=True,
    )
```

In the example above, the resources are defined by building the following `V1ResourceRequirements` object:

```python
from kubernetes.client import models as k8s

compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu": "800m", "memory": "3Gi"},
    requests={"cpu": "800m", "memory": "3Gi"}
)
```

This object allows you to specify Memory and CPU requests and limits for any given task and its corresponding Kubernetes Pod. For more information, read [Kubernetes Documentation on Requests and Limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits).

Once you've created the object, apply it to the `resources` parameter of the task. When this DAG runs, it will launch a Pod that runs the `hello-world` image, which is pulled from Docker Hub, in your Airflow Deployment's namespace with the resource requests defined above. Once the task finishes, the Pod will be gracefully terminate.

:::info

On Astronomer, the equivalent of 1AU is: `requests={"cpu": "100m", "memory": "384Mi"}, limits={"cpu": "100m", "memory": "384Mi"}`.

:::

## Pulling images from a private registry

By default, the KubernetesPodOperator will look for images hosted publicly on [Docker Hub](https://hub.docker.com/). If you want to pull images from a private registry, you may do so.

To pull images from a private registry on Astronomer Software:

1. Retrieve a `config.json` file that contains your Docker credentials by following the [Docker documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials). The generated file should look something like this:

   ```json
   {
       "auths": {
           "https://index.docker.io/v1/": {
               "auth": "c3R...zE2"
           }
       }
   }
   ```

2. Follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials) to create a secret based on your credentials.

3. In your DAG code, import `models` from `kubernetes.client` and specify `image_pull_secrets` with your Kubernetes secret. After configuring this value, you can pull an image as you would from a public registry like in the following example.

    ```python {1,5}
    from kubernetes.client import models as k8s

    KubernetesPodOperator(
        namespace=namespace,
        image_pull_secrets=[k8s.V1LocalObjectReference("<your-secret-name>")],
        image="<your-docker-image>",
        cmds=["<commands-for-image>"],
        arguments=["<arguments-for-image>"],
        labels={"<pod-label>": "<label-name>"},
        name="<pod-name>",
        is_delete_operator_pod=True,
        in_cluster=True,
        task_id="<task-name>",
        get_logs=True,
    )
    ```

## Local testing

Astronomer recommends testing your DAGs locally before pushing them to a Deployment on Astronomer. For more information, read [How to run the KubernetesPodOperator locally](https://docs.astronomer.io/learn/kubepod-operator). That guide provides information on how to use [MicroK8s](https://microk8s.io/) or [Docker for Kubernetes](https://matthewpalmer.net/kubernetes-app-developer/articles/how-to-run-local-kubernetes-docker-for-mac.html) to run tasks with the KubernetesPodOperator in a local environment.

> **Note:** To pull images from a private registry locally, you'll have to create a secret in your local namespace and similarly call it in your operator following the guidelines above.
