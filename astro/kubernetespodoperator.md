---
sidebar_label: 'KubernetesPodOperator'
title: "Run the KubernetesPodOperator on Astro"
id: kubernetespodoperator
---

## Overview

This guide provides steps for configuring and running the KubernetesPodOperator on DAGs deployed to Astro.

The [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) is one of Apache Airflow's most powerful operators. Similar to the Kubernetes Executor, this operator talks to the Kubernetes API to dynamically launch a Pod in Kubernetes for each task that needs to run and terminates each Pod once the task is completed. This results in an isolated, containerized execution environment for each task that is separate from tasks otherwise being executed by Celery workers. The KubernetesPodOperator enables you to:

- Execute a custom Docker image per task with Python packages and dependencies that would otherwise conflict with the rest of your Deployment's dependencies. This includes Docker images in a private registry or repository.
- Specify CPU and Memory as task-level limits or minimums to optimize for cost and performance.
- Write task logic in a language other than Python. This gives you flexibility and can enable new use cases across teams.
- Scale task growth horizontally in a way that is cost-effective, dynamic, and minimally dependent on Worker resources.
- Set Kubernetes-native configurations in a YAML file, including volumes, secrets, and affinities.

On Astro, the Kubernetes infrastructure required to run the KubernetesPodOperator is built into every Cluster in the Data Plane and is managed by Astronomer.

## Prerequisites

To use the KubernetesPodOperator, you need:

- An [Astro project](create-project.md).
- An Astro [Deployment](configure-deployment.md).

## Set Up the KubernetesPodOperator

To use the KubernetesPodOperator in a DAG, add the following import statements and instantiation to your DAG file:

```python
from airflow.contrib.operators.kubernetes_pod_operator import kubernetes_pod_operator

# Pulls environment information from Astro
from airflow import configuration as conf
...

namespace = conf.get('kubernetes', 'NAMESPACE')
k = kubernetes_pod_operator.KubernetesPodOperator(
    namespace=namespace,
    image="<your-docker-image>",
    cmds=["<commands-for-image>"],
    arguments=["<arguments-for-image>"],
    labels={"<pod-label>": "<label-name>"},
    name="<pod-name>",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="<task-name>",
    get_logs=True)
```

For each instantiation of the KubernetesPodOperator, you must specify the following values:

- `namespace = conf.get('kubernetes', 'NAMESPACE')`: Every Deployment runs on its own Kubernetes namespace within a Cluster. Information about this namespace can be programmatically imported as long as you set this variable.
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. The value you specify is assumed to be an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, read [Pull Images from a Private Registry](kubernetespodoperator.md#run-images-from-a-private-registry).
- `in_cluster=True`: When this value is set, your task will run within the Cluster from which it's instantiated on Astro. This ensures that the Kubernetes Pod running your task has the correct permissions within the Cluster.
- `is_delete_operator_pod=True`: This setting ensures that once a KubernetesPodOperator task is complete, the Kubernetes Pod that ran that task is terminated. This ensures that there are no unused pods in your Cluster taking up resources.

This is the minimum configuration required to run tasks with the KubernetesPodOperator on Astro. To further customize the way your tasks are run, see the topics below.

## Configure Task-Level Pod Resources

Astro automatically allocates resources to Pods created by the KubernetesPodOperator. Resources used by the KubernetesPodOperator are not technically limited, meaning that the operator could theoretically use any CPU and memory that's available in your Cluster to complete a task. Because of this, we recommend specifying [compute resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) per task.

To do so, define a dictionary of compute resources in your DAG. For example, applying the following dictionary to a task would ensure that a Pod runs that task with exactly 800m of CPU and 3Gi of memory at all times:

```python
compute_resources = \
  {'request_cpu': '800m',
  'request_memory': '3Gi',
  'limit_cpu': '800m',
  'limit_memory': '3Gi'}
```

To use a dictionary, specify the `resources` variable in your instantiation of the KubernetesPodOperator:

```python {11}
namespace = conf.get('kubernetes', 'NAMESPACE')
with dag:
    k = KubernetesPodOperator(
        namespace=namespace,
        image="<your-docker-image>",
        labels={"<pod-label>": "<label-name>"},
        name="<pod-name>",
        task_id="<task-name>",
        in_cluster=True,
        cluster_context='docker-for-desktop',
        resources=compute_resources,
        is_delete_operator_pod=True,
        get_logs=True)
```

## Run Images from a Private Registry

By default, the KubernetesPodOperator expects to pull a Docker image that's hosted publicly on Docker Hub. If you want to execute a Docker image that's hosted in a private registry, complete the setup below.

### Prerequisites

To complete this setup, you need:

- An [Astro project](create-project.md).
- An [Astro Deployment](configure-deployment.md).
- Access to a private Docker registry.
- [kubectl](https://kubernetes.io/docs/reference/kubectl/), the command line tool for Kubernetes.

### Step 1: Create a Kubernetes Secret

To run Docker images from a private registry on Astro, you first need to create a Kubernetes secret that contains credentials to your registry. Astronomer will then inject that secret into your Deployment's namespace, which will give your tasks access to Docker images within your registry. To do this, complete the following setup:

1. Log in to your Docker registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
2. Reach out to [Astronomer Support](https://support.astronomer.io) and include the namespace of the Deployment you want to use the KubernetesPodOperator with. A Deployment's namespace can be found in the Deployment view of the Astronomer UI.

From here, Astronomer Support will give you instructions on how to securely send the output of your `/.docker/config.json` file. Do not send this file via email, as it contains sensitive credentials to your registry.

### Step 2: Specify the Kubernetes Secret in your DAG

Once Astronomer has added the Kubernetes secret to your Deployment, you will be notified and provided with the name of the secret.

From here, you can run images from your private registry by importing `models` from `kubernetes.client` and configuring `image_pull_secrets` in your KubernetesPodOperator instantiation:

```python {1,5}
from kubernetes.client import models as k8s

k = kubernetes_pod_operator.KubernetesPodOperator(
    namespace=namespace,
    image_pull_secrets=[k8s.V1LocalObjectReference('<your-secret-name>')],
    image="<your-docker-image>",
    cmds=["<commands-for-image>"],
    arguments=["<arguments-for-image>"],
    labels={"<pod-label>": "<label-name>"},
    name="<pod-name>",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="<task-name>",
    get_logs=True)
```
