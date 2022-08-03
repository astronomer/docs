---
sidebar_label: 'Run the KubernetesPodOperator on Astro'
title: "Run the KubernetesPodOperator on Astro"
id: kubernetespodoperator
---

The [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) is one of the most powerful Apache Airflow operators. Similar to the Kubernetes executor, this operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod once the task is complete. This results in an isolated, containerized execution environment for each task that is separate from tasks otherwise being executed by Celery workers.

## Benefits of the KubernetesPodOperator

The KubernetesPodOperator enables you to:

- Execute a custom Docker image per task with Python packages and dependencies that would otherwise conflict with the rest of your Deployment's dependencies. This includes Docker images in a private registry or repository.
- Run tasks Kubernetes cluster outside of the Astro data plane. This allows you to run individual tasks on infrastructure that might not be supported on Astro yet, such as GPU nodes or on other third-party services.
- Specify CPU and Memory as task-level limits or minimums to optimize for cost and performance.
- Write task logic in a language other than Python. This gives you flexibility and can enable new use cases across teams.
- Scale task growth horizontally in a way that is cost-effective, dynamic, and minimally dependent on worker resources.
- Set Kubernetes-native configurations in a YAML file, including volumes, secrets, and affinities.

On Astro, the Kubernetes infrastructure required to run the KubernetesPodOperator is built into every cluster in the data plane and is managed by Astronomer.

## Known limitations

- Cross-account service accounts are not supported on pods launched in the Astro cluster.
- PersistentVolumes (PVs) are not supported on pods launched in the Astro cluster.

## Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

## Set Up the KubernetesPodOperator

To use the KubernetesPodOperator in a DAG, add the following import statements and instantiation to your DAG file:

```python
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


namespace = conf.get("kubernetes", "NAMESPACE")

KubernetesPodOperator(
    namespace=namespace,
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

For each instantiation of the KubernetesPodOperator, you must specify the following values:

- `namespace = conf.get("kubernetes", "NAMESPACE")`: Every Deployment runs on its own Kubernetes namespace within a cluster. Information about this namespace can be programmatically imported as long as you set this variable.
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. The value you specify is assumed to be an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, read [Pull images from a Private Registry](kubernetespodoperator.md#run-images-from-a-private-registry).
- `in_cluster=True`: When this value is set, your task will run within the cluster from which it's instantiated on Astro. This ensures that the Kubernetes Pod running your task has the correct permissions within the cluster.
- `is_delete_operator_pod=True`: This setting ensures that once a KubernetesPodOperator task is complete, the Kubernetes Pod that ran that task is terminated. This ensures that there are no unused pods in your cluster taking up resources.

This is the minimum configuration required to run tasks with the KubernetesPodOperator on Astro. To further customize the way your tasks are run, see the topics below.

## Configure Task-Level Pod Resources

Astro automatically allocates resources to Pods created by the KubernetesPodOperator. Resources used by the KubernetesPodOperator are not technically limited, meaning that the operator could theoretically use any CPU and memory that's available in your cluster to complete a task. Because of this, we recommend specifying [compute resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) per task.

To do so, define a `kubernetes.client.models.V1ResourceRequirements` object and provide that to the `resources` argument of the KubernetesPodOperator:

```python {20}
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu": "800m", "memory": "3Gi"},
    requests={"cpu": "800m", "memory": "3Gi"}
)

namespace = conf.get("kubernetes", "NAMESPACE")

KubernetesPodOperator(
    namespace=namespace,
    image="<your-docker-image>",
    cmds=["<commands-for-image>"],
    arguments=["<arguments-for-image>"],
    labels={"<pod-label>": "<label-name>"},
    name="<pod-name>",
    is_delete_operator_pod=True,
    in_cluster=True,
    resources=compute_resources,
    task_id="<task-name>",
    get_logs=True,
)
```

Applying the code above ensures that when this DAG runs, it will launch a Kubernetes Pod with exactly 800m of CPU and 3Gi of memory as long as that infrastructure is available in your cluster. Once the task finishes, the Pod will terminate gracefully.

## Run images from a Private Registry

By default, the KubernetesPodOperator expects to pull a Docker image that's hosted publicly on Docker Hub. If you want to execute a Docker image that's hosted in a private registry, complete the setup below.

:::caution

Running Docker images that are hosted on [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/) (ECR) is not supported on Astro. Authentication tokens generated by ECR expire after 12 hours and cannot be recreated, which means that KubernetesPodOperator tasks would not reliably have the necessary credentials to pull and run any Docker image hosted on ECR.

If you're using ECR and are interested in exploring other solutions, contact [Astronomer support](https://support.astronomer.io).

:::

### Prerequisites

To complete this setup, you need:

- An [Astro project](create-project.md).
- An [Astro Deployment](configure-deployment-resources.md).
- Access to a private Docker registry.
- [kubectl](https://kubernetes.io/docs/reference/kubectl/), the command line tool for Kubernetes.

### Step 1: Create a Kubernetes Secret

To run Docker images from a private registry on Astro, you first need to create a Kubernetes secret that contains credentials to your registry. Astronomer will then inject that secret into your Deployment's namespace, which will give your tasks access to Docker images within your registry. To do this, complete the following setup:

1. Log in to your Docker registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
2. In the Cloud UI, select a Workspace and then select the Deployment you want to use the KubernetesPodOperator with.
3. Copy the value in the **NAMESPACE** field.
4. Reach out to [Astronomer support](https://support.astronomer.io) and provide the namespace of the Deployment.

Astronomer Support will give you instructions on how to securely send the output of your `/.docker/config.json` file. Do not send this file by email, as it contains sensitive credentials to your registry.

### Step 2: Specify the Kubernetes Secret in your DAG

Once Astronomer has added the Kubernetes secret to your Deployment, you will be notified and provided with the name of the secret.

From here, you can run images from your private registry by importing `models` from `kubernetes.client` and configuring `image_pull_secrets` in your KubernetesPodOperator instantiation:

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
## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [KubernetesPodOperator Airflow Guide](https://www.astronomer.io/guides/kubepod-operator/)
