---
sidebar_label: 'KubernetesPodOperator'
title: "Run the KubernetesPodOperator on Astro"
id: kubernetespodoperator
description: "Learn how to run the KubernetesPodOperator on Astro. This operator dynamically launches a Pod in Kubernetes for each task and terminates each Pod when the task is complete."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

The [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) is one of the most customizable Apache Airflow operators. A task using the KubernetesPodOperator runs in a dedicated, isolated Kubernetes Pod that terminates after the task completes. To learn more about the benefits and usage of the KubernetesPodOperator, see the [KubernetesPodOperator Learn guide](https://docs.astronomer.io/learn/kubepod-operator).

On Astro, the infrastructure required to run the KubernetesPodOperator is built into every Deployment and is managed by Astronomer. Astro supports setting a default Pod configuration so that any task Pods without specific resource requests and limits cannot exceed your expected resource usage for the Deployment.

Some task-level configurations will differ on Astro compared to other Airflow environments. Use this document to learn how to configure individual task Pods for different use cases on Astro. To configure the default Pod resources for all KubernetesPodOperator Pods, see [Configure Kubernetes Pod resources](deployment-resources.md#configure-kubernetes-pod-resources).

## Known limitations

- Cross-account service accounts are not supported on Pods launched in an Astro cluster. To allow access to external data sources, you can provide credentials and secrets to tasks.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- (Hybrid only) You cannot run a KubernetesPodOperator task in a worker queue or node pool that is different than the worker queue of its parent worker. For example, a KubernetesPodOperator task that is triggered by an `m5.4xlarge` worker on AWS will also be run on an `m5.4xlarge` node. To run a task on a different node instance type, you must launch it in an external Kubernetes cluster. If you need assistance launching KubernetesPodOperator tasks in external Kubernetes clusters, contact [Astronomer support](https://support.astronomer.io).
- You can't use an image built for an ARM architecture in the KubernetesPodOperator. To build images using the x86 architecture on a Mac with an Apple chip, include the `--platform` flag in the `FROM` command of the `Dockerfile` that constructs your custom image. For example:

    ```bash
    FROM --platform=linux/amd64 postgres:latest
    ```

    If you use an ARM image, your KPO task will fail with the error: `base] exec /usr/bin/psql: exec format error`.

## Prerequisites

- An [Astro project](cli/develop-project.md#create-an-astro-project).
- An Astro [Deployment](create-deployment.md).

## Set up the KubernetesPodOperator on Astro

The following snippet is the minimum configuration you'll need to create a KubernetesPodOperator task on Astro:

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
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. Astro assumes that this value is an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, see [Pull images from a Private Registry](kubernetespodoperator.md#run-images-from-a-private-registry).

## Configure task-level Pod resources

Astro automatically allocates resources to Pods created by the KubernetesPodOperator. Unless otherwise specified in your task-level configuration, the amount of resources your task Pod can use is defined by your [default Pod resource configuration](deployment-resources.md#configure-kubernetes-pod-resources). To further optimize your resource usage, Astronomer recommends specifying [compute resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for each task.

To do so, define a `kubernetes.client.models.V1ResourceRequirements` object and provide that to the `container_resources` argument of the KubernetesPodOperator. For example:

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
    container_resources=compute_resources,
    task_id="<task-name>",
    get_logs=True,
)
```

Applying the previous code example ensures that when this DAG runs, it launches a Kubernetes Pod with exactly 800m of CPU and 3Gi of memory as long as that infrastructure is available in your Deployment. After the task finishes, the Pod will terminate gracefully.

:::warning

For Astro Hosted environments, if you set resource requests to be less than the maximum limit, Astro automatically requests the maximum limit that you set. This means that you might consume more resources than you expected if you set the limit much higher than the resource request you need. Check your [Billing and usage](manage-billing.md) to view your resource use and associated charges.

:::

### Mount a temporary directory

:::info Alternative Astro Hybrid setup

On Astro Hybrid, this configuration works only on AWS clusters where you have enabled `m5d` and `m6id` worker types. These worker types have NVMe SSD volumes that can be used by tasks for ephemeral storage. See [Amazon EC2 M6i Instances](https://aws.amazon.com/ec2/instance-types/m6i/) and [Amazon EC2 M5 Instances](https://aws.amazon.com/ec2/instance-types/m5/) for the amount of available storage in each node type.

The task which mounts a temporary directory must run on a worker queue that uses either `m5d` and `m6id` worker types. See [Modify a cluster](manage-hybrid-clusters.md) for instructions on enabling `m5d` and `m6id` workers on your cluster. See [Configure a worker queue](configure-worker-queues.md) to configure a worker queue to use one of these worker types.

:::

To run a task run the KubernetesPodOperator that utilizes your Deployment's ephemeral storage, mount an [emptyDir volume](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example) to the KubernetesPodOperator. For example:

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
    task_id="<task-name>",
    get_logs=True,
    volume_mounts=volume_mounts,
    volumes=[volume],
)
```

## Run images from a private registry

By default, the KubernetesPodOperator expects to pull a Docker image that's hosted publicly on Docker Hub. If your images are hosted on the container registry native to your cloud provider, you can grant access to the images directly. Otherwise, if you are using any other private registry, you need to create a Kubernetes Secret containing credentials to the registry, then specify the Kubernetes Secret in your DAG.

<Tabs
    defaultValue="PrivateRegistry"
    groupId="run-images-from-a-private-registry"
    values={[
        {label: 'Private Registry', value: 'PrivateRegistry'},
        {label: 'Amazon Elastic Container Registry (ECR)', value: 'AWSECR'},
        {label: 'Google Artifact Registry', value: 'GoogleArtifactRegistry'},
    ]}>
<TabItem value="PrivateRegistry">

#### Prerequisites

- An [Astro project](cli/get-started-cli.md).
- An [Astro Deployment](deployment-settings.md).
- Access to a private Docker registry.

#### Step 1: Create a Kubernetes Secret

To run Docker images from a private registry on Astro, a Kubernetes Secret that contains credentials to your registry must be created. Injecting this secret into your Deployment's namespace will give your tasks access to Docker images within your private registry.

1. Log in to your Docker registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file. If the generated `/docker/config.json` does not contain any credentials, copy your registry URL, username, and password.
2. In the Cloud UI, select a Workspace and then select the Deployment you want to use the KubernetesPodOperator with.
3. Copy the value in the **NAMESPACE** field.
4. Contact [Astronomer support](https://cloud.astronomer.io/open-support-request) and provide the namespace of the Deployment.

Astronomer Support will give you instructions on how to securely send your credentials. Do not send this file by email, as it contains sensitive credentials to your registry. Astronomer will use these credentials to create a Kubernetes secret in your Deployment's namespace.

#### Step 2: Specify the Kubernetes Secret in your DAG

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

</TabItem>

<TabItem value="AWSECR">

:::info

Policy-based setup is available only on Astro Hosted dedicated clusters and Astro Hybrid. To run images from a private registry on Astro Hosted standard clusters, follow the steps in [Private Registry](kubernetespodoperator.md?tab=PrivateRegistry#step-1-create-a-kubernetes-secret).

:::

If your Docker image is hosted in an Amazon ECR repository, add a permissions policy to the repository to allow the KubernetesPodOperator to pull the Docker image. You don't need to create a Kubernetes secret, or specify the Kubernetes secret in your DAG. Docker images hosted in Amazon ECR repositories can only be pulled from AWS clusters.

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

    Replace `<AstroAccountID>` with your Astro AWS account ID.

6. Click **Save** to create a new permissions policy named **AllowImagePullAstro**.
7. [Set up the KubernetesPodOperator](#set-up-the-kubernetespodoperator).
8. Replace `<your-docker-image>` in the instantiation of the KubernetesPodOperator with the Amazon ECR repository URI that hosts the Docker image. To locate the URI:

    - In the Amazon ECR Dashboard, click **Repositories** in the left menu.
    - Open the **Private** tab and then copy the URI of the repository that hosts the Docker image.

</TabItem>
<TabItem value="GoogleArtifactRegistry">

:::info

Passwordless setup is available only on Astro Hosted dedicated clusters and Astro Hybrid. For Astro Hosted standard clusters, please follow the steps in [Private Registry](https://docs.astronomer.io/astro/kubernetespodoperator?tab=PrivateRegistry#step-1-create-a-kubernetes-secret) to create a Kubernetes secret containing your registry credentials.

:::

If your Docker image is hosted in Google Artifact Registry repository, add a permissions policy to the repository to allow the KubernetesPodOperator to pull the Docker image. You don't need to create a Kubernetes secret or specify the Kubernetes secret in your DAG. Docker images hosted in Google Artifact Registry repositories can be pulled only to Deployments hosted on GCP clusters.

#### Setup

1. Contact [Astronomer support](https://support.astronomer.io) to request the Compute Engine default service account ID for your cluster.
2. Log in to Google Artifact Registry.
3. Click the checkbox next to the repository that you want to use.
4. In the **Properties** pane that appears, click **ADD PRINCIPAL** in the **PERMISSIONS** tab.
5. In the **Add Principals** text box, paste the Compute Engine default service account ID that was provided to you by Astronomer Support.
6. In the **Assign Roles** selector, search for `Artifact Registry Reader` and select the role that appears.
7. Click **Save** to grant read access for the registry  to Astro.
8. [Set up the KubernetesPodOperator](#set-up-the-kubernetespodoperator). When you configure an instantiation of the KubernetesPodOperator, replace `<your-docker-image>` with the Google Artifact Registry image URI. To retrieve the URI:

    - In the Google Artifact Registry, click the registry containing the image.
    - Click the image you want to use.
    - Click the copy icon next to the image in the top corner. The string you copy should be in the format `<GCP Region>-docker.pkg.dev/<Project Name>/<Registry Name>/<Image Name>`.

</TabItem>
</Tabs>

## Use secret environment variables with the KubernetesPodOperator

Astro [environment variables](environment-variables.md) marked as secrets are stored in a Kubernetes secret called `env-secrets`. To use a secret value in a task running on the Kubernetes executor, you pull the value from `env-secrets` and mount it to the Pod running your task as a new Kubernetes Secret.

1. Add the following import to your DAG file:

    ```python
    from airflow.kubernetes.secret import Secret
    ```

2. Define a Kubernetes `Secret` in your DAG instantiation using the following format:

    ```python
    secret_env = Secret(deploy_type="env", deploy_target="<VARIABLE_KEY>", secret="env-secrets", key="<VARIABLE_KEY>")
    namespace = conf.get("kubernetes", "NAMESPACE")
    ```

3. Reference the key for the environment variable, formatted as `$VARIABLE_KEY` in the task using the KubernetesPodOperator.

In the following example, a secret named `MY_SECRET` is pulled from `env-secrets` and printed to logs.

```python
import pendulum
from airflow.kubernetes.secret import Secret

from airflow.models import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.configuration import conf

with DAG(
        dag_id='test-kube-pod-secret',
        start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
        end_date=pendulum.datetime(2022, 1, 5, tz="UTC"),
        schedule_interval="@once",
) as dag:

    secret_env = Secret(deploy_type="env", deploy_target="MY_SECRET", secret="env-secrets", key="MY_SECRET")

    namespace = conf.get("kubernetes", "NAMESPACE")

    k = KubernetesPodOperator(
        namespace=namespace,
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo $MY_SECRET && sleep 150"],
        name="test-name",
        task_id="test-task",
        get_logs=True,
        secrets=[secret_env],
    )
```

## Launch a Pod in an external cluster

To launch a Pod in an external cluster from an Astro Deployment, you have to:

- Create a [network connection](https://docs.astronomer.io/astro/networking-overview) between the Astro Deployment and your external cluster.
- Add a `kubeconfig` file for the external cluster to your Astro project `include` folder, then deploy your changes to Astro.
- Set `in_cluster=false` and `config_file = <your-kubeconfig-file>` in your task configuration.

See the [Astronomer Learn guide](https://docs.astronomer.io/learn/kubepod-operator#example-use-kubernetespodoperator-to-run-a-pod-in-a-separate-cluster) for complete setup steps.

To test a task in a local environment using the Astro CLI, you must additionally mount credentials to the external cluster so that your local Airflow environment has permissions to launch a Pod in the external cluster. See [Authenticate to cloud services with user credentials](cli/authenticate-to-clouds.md) for setup steps.

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [KubernetesPodOperator Airflow Guide](https://docs.astronomer.io/learn/kubepod-operator/)

