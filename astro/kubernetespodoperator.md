---
sidebar_label: 'Run the KubernetesPodOperator on Astro'
title: "Run the KubernetesPodOperator on Astro"
id: kubernetespodoperator
---

<head>
  <meta name="description" content="Learn how to run the KubernetesPodOperator on Astro. This operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod when the task is complete." />
  <meta name="og:description" content="Learn how to run the KubernetesPodOperator on Astro. This operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod when the task is complete." />
</head>

The [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) is one of the most powerful Apache Airflow operators. Similar to the Kubernetes executor, this operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod once the task is complete. This results in an isolated, containerized execution environment for each task that is separate from tasks otherwise being executed by Celery workers.

## Benefits

You can use the KubernetesPodOperator to:

- Execute a custom Docker image per task with Python packages and dependencies that would otherwise conflict with the rest of your Deployment's dependencies. This includes Docker images in a private registry or repository.
- Run tasks in a Kubernetes cluster outside of the Astro data plane. This can be helpful when you need to run individual tasks on infrastructure that isn't currently supported by Astro, such as GPU nodes or other third-party services.
- Specify CPU and memory as task-level limits or minimums to optimize performance and reduce costs.
- Write task logic in a language other than Python. This gives you flexibility and can enable new use cases across teams.
- Scale task growth horizontally in a way that is cost-effective, dynamic, and minimally dependent on worker resources.
- Set Kubernetes-native configurations in a YAML file, including volumes, secrets, and affinities.

On Astro, the Kubernetes infrastructure required to run the KubernetesPodOperator is built into every cluster in the data plane and is managed by Astronomer.

## Known limitations

- Cross-account service accounts are not supported on Pods launched in an Astro cluster. To allow access to external data sources, you can provide credentials and secrets to tasks.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- You cannot run a KubernetesPodOperator task in a worker queue or node pool that is different than the worker queue of its parent worker. For example, a KubernetesPodOperator task that is triggered by an `m5.4xlarge` worker on AWS will also be run on an `m5.4xlarge` node. To run a task on a different node instance type, you must launch it in a Kubernetes cluster outside of the Astro data plane. If you need assistance launching KubernetesPodOperator tasks in external Kubernetes clusters, contact [Astronomer support](https://support.astronomer.io).

## Prerequisites

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project).
- An Astro [Deployment](create-deployment.md).

## Set up the KubernetesPodOperator

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
    task_id="<task-name>",
    get_logs=True,
)
```

For each instantiation of the KubernetesPodOperator, you must specify the following values:

- `namespace = conf.get("kubernetes", "NAMESPACE")`: Every Deployment runs on its own Kubernetes namespace within a cluster. Information about this namespace can be programmatically imported as long as you set this variable.
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. The value you specify is assumed to be an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, see [Pull images from a Private Registry](kubernetespodoperator.md#run-images-from-a-private-registry).

This is the minimum configuration required to run tasks with the KubernetesPodOperator on Astro. To further customize the way your tasks are run, see the topics below.

## Configure task-level Pod resources

Astro automatically allocates resources to Pods created by the KubernetesPodOperator. Resources used by the KubernetesPodOperator are not technically limited, meaning that the operator could theoretically use any CPU and memory that's available in your cluster to complete a task. Because of this, Astronomer recommends specifying [compute resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for each task.

To do so, define a `kubernetes.client.models.V1ResourceRequirements` object and provide that to the `resources` argument of the KubernetesPodOperator. For example:

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
    resources=compute_resources,
    task_id="<task-name>",
    get_logs=True,
)
```

Applying the code above ensures that when this DAG runs, it will launch a Kubernetes Pod with exactly 800m of CPU and 3Gi of memory as long as that infrastructure is available in your cluster. Once the task finishes, the Pod will terminate gracefully.

### Mount a temporary directory (_AWS only_)

Astronomer provisions `m5d` and `m6id` workers with NVMe SSD volumes that can be used by tasks for ephemeral storage. See [Amazon EC2 M6i Instances](https://aws.amazon.com/ec2/instance-types/m6i/) and [Amazon EC2 M5 Instances](https://aws.amazon.com/ec2/instance-types/m5/) for the amount of available storage in each node type.

To run a task run the KubernetesPodOperator that utilizes ephemeral storage:

1. Create a [worker queue](configure-worker-queues.md) with `m5d` workers. See [Modify a cluster](modify-cluster.md) for instructions on adding `m5d` workers to your cluster.
2. Mount and [emptyDir volume](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example) to the KubernetesPodOperator. For example:

    ```python {5-14,26-27}
    from airflow.configuration import conf
    from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
    from kubernetes.client import models as k8s

    volume = k8s.V1Volume(
        name="cache-volume",
        emptyDir={},
    )

    volume_mounts = [
        k8s.V1VolumeMount(
            mount_path="/cache", name="cache-volume"
        )
    ]

    example_volume_test = KubernetesPodOperator(
        namespace=namespace,
        image="<your-docker-image>",
        cmds=["<commands-for-image>"],
        arguments=["<arguments-for-image>"],
        labels={"<pod-label>": "<label-name>"},
        name="<pod-name>",
        resources=compute_resources,
        task_id="<task-name>",
        get_logs=True,
        volume_mounts=volume_mounts,
        volumes=[volume],
    )
    ```
 
## Run images from a private registry

By default, the KubernetesPodOperator expects to pull a Docker image that's hosted publicly on Docker Hub. If you want to execute a Docker image that's hosted in a private registry, you'll need to create a Kubernetes Secret and then specify the Kubernetes Secret in your DAG. If your Docker image is hosted in an Amazon Elastic Container Registry (ECR) repository, see [Docker images hosted in private Amazon ECR repositories](#docker-images-hosted-in-private-amazon-ecr-repositories)

### Prerequisites

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project).
- An [Astro Deployment](configure-deployment-resources.md).
- Access to a private Docker registry.
- [kubectl](https://kubernetes.io/docs/reference/kubectl/), the command line tool for Kubernetes.

### Step 1: Create a Kubernetes Secret

To run Docker images from a private registry on Astro, a Kubernetes Secret that contains credentials to your registry must be created. Injecting this secret into your Deployment's namespace will give your tasks access to Docker images within your private registry.

1. Log in to your Docker registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
2. In the Cloud UI, select a Workspace and then select the Deployment you want to use the KubernetesPodOperator with.
3. Copy the value in the **NAMESPACE** field.
4. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the namespace of the Deployment.

Astronomer Support will give you instructions on how to securely send the output of your `/.docker/config.json` file. Do not send this file by email, as it contains sensitive credentials to your registry. Astronomer will use this file to create a Kubernetes secret and inject it into your Deployment's namespace.

### Step 2: Specify the Kubernetes Secret in your DAG

Once Astronomer has added the Kubernetes secret to your Deployment, you will be notified and provided with the name of the secret.

After you receive the name of your Kubernetes secret from Astronomer, you can run images from your private registry by importing `models` from `kubernetes.client` and configuring `image_pull_secrets` in your KubernetesPodOperator instantiation:

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
    task_id="<task-name>",
    get_logs=True,
)
```
### Docker images hosted in private Amazon ECR repositories

If your Docker image is hosted in an Amazon ECR repository, add a permissions policy to the repository to allow the KubernetesPodOperator to pull the Docker image. You don't need to create a Kubernetes secret, or specify the Kubernetes secret in your DAG. Docker images hosted on Amazon ECR repositories can only be pulled from AWS clusters.

1. Log in to the Amazon ECR Dashboard and then select **Menu** > **Repositories**.
2. Click the **Private** tab and then click the name of the repository that hosts the Docker image. 
3. Click **Permissions** in the left menu.
4. Click **Edit policy JSON**.
5. Copy and paste the following policy into the **Edit JSON** pane:

    ```json
    {
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "AllowImagePullAstro",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<AstroAccountID>:root"
                },
                "Action": [
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage"
                ]
            }
        ]
    }
    ```
6. Replace `<AstroAccountID>` with your Astro AWS account ID. 
7. Click **Save** to create a new permissions policy named **AllowImagePullAstro**.
8. [Set up the KubernetesPodOperator](#set-up-the-kubernetespodoperator).
9. Replace `<your-docker-image>` in the instantiation of the KubernetesPodOperator with the Amazon ECR repository URI that hosts the Docker image. To locate the URI:

    - In the Amazon ECR Dashboard, click **Repositories** in the left menu.
    - Click the **Private** tab and then copy the URI of the repository that hosts the Docker image.

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [KubernetesPodOperator Airflow Guide](https://docs.astronomer.io/learn/kubepod-operator/)

