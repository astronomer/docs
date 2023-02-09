---
sidebar_label: 'Run the Kubernetes executor on Astro'
title: "Run the Kubernetes executor on Astro"
id: kubernetesexecutor
---

<head>
  <meta name="description" content="Learn how to run the Kubernetes executor on Astro. This executor dynamically launches a Pod in Kubernetes for each task and terminates each Pod when the task is complete." />
  <meta name="og:description" content="Learn how to run the Kubernetes executor on Astro. This executor dynamically launches a Pod in Kubernetes for each task and terminates each Pod when the task is complete." />
</head>

Like the [KubernetesPodOperator](kubernetespodoperator.md), the [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) dynamically launches and terminates Pods to run Airflow tasks. In addition, the KubernetesPodOperator and the Kubernetes executor can use the Kubernetes API to create Pods for running tasks. However, the Kubernetes executor is implemented at the configuration level of the Airflow instance, which means a new Kubernetes Pod is created for every task instance. The Kubernetes executor is recommended when you need to control resource optimization.

## Benefits

You can use the Kubernetes executor to:

- Execute a custom Docker image per task with Python packages and dependencies that would otherwise conflict with the rest of your Deployment's dependencies. This includes Docker images in a private registry or repository.
- Run tasks in a Kubernetes cluster outside of the Astro data plane. This can be helpful when you need to run individual tasks on infrastructure that isn't currently supported by Astro, such as GPU nodes or other third-party services.
- Specify CPU and memory as task-level limits or minimums to optimize performance and reduce costs.
- Write task logic in a language other than Python. This gives you flexibility and can enable new use cases across teams.
- Scale task growth horizontally in a way that is cost-effective, dynamic, and minimally dependent on worker resources.
- Set Kubernetes-native configurations in a YAML file, including volumes, secrets, and affinities.

On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every cluster in the data plane and is managed by Astronomer.

## Known limitations

- Tasks take longer to start and this causes task latency
- Cross-account service accounts are not supported on Pods launched in an Astro cluster. To allow access to external data sources, you can provide credentials and secrets to tasks.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- You cannot run a Kubernetes executor task in a worker queue or node pool that is different than the worker queue of its parent worker. For example, a Kubernetes executor task that is triggered by an `m5.4xlarge` worker on AWS will also be run on an `m5.4xlarge` node. To run a task on a different node instance type, you must launch it in a Kubernetes cluster outside of the Astro data plane. If you need assistance launching Kubernetes executor tasks in external Kubernetes clusters, contact [Astronomer support](https://support.astronomer.io).
- The `pod_template_file` argument is not supported on Pods launched in an Astro cluster. If you use the `pod_template_file` argument, customized values are overridden when they are required by Astronomer and your tasks will fail. Astronomer recommends using `python-kubernetes-sdk`. See [Astro Python SDK ReadTheDocs](https://astro-sdk-python.readthedocs.io/en/stable/).

## Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

## Set up the Kubernetes executor

To use the Kubernetes executor in a DAG, add the following import statements and instantiation to your DAG file:

```python
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import Kubernetes executor


namespace = conf.get("kubernetes", "NAMESPACE")

Kubernetes executor(
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
For each instantiation of the Kubernetes executor, you must specify the following values:

- `namespace = conf.get("kubernetes", "NAMESPACE")`: Every Deployment runs on its own Kubernetes namespace within a cluster. Information about this namespace can be programmatically imported as long as you set this variable.
- `image`: This is the Docker image that the operator will use to run its defined task, commands, and arguments. The value you specify is assumed to be an image tag that's publicly available on [Docker Hub](https://hub.docker.com/). To pull an image from a private registry, see [Pull images from a Private Registry](Kubernetes executor.md#run-images-from-a-private-registry).

This is the minimum configuration required to run tasks with the Kubernetes executor on Astro. To further customize the way your tasks are run, see the topics below.

## Configure task-level Pod resources

Astro automatically allocates resources to Pods created by the Kubernetes executor. Resources used by the Kubernetes executor are not technically limited, meaning that the operator could theoretically use any CPU and memory that's available in your cluster to complete a task. Because of this, Astronomer recommends specifying [compute resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for each task.

To do so, define a `kubernetes.client.models.V1ResourceRequirements` object and provide that to the `resources` argument of the Kubernetes executor. For example:

```python {20}
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import Kubernetes executor
from kubernetes.client import models as k8s

compute_resources = k8s.V1ResourceRequirements(
    limits={"cpu": "800m", "memory": "3Gi"},
    requests={"cpu": "800m", "memory": "3Gi"}
)

namespace = conf.get("kubernetes", "NAMESPACE")

Kubernetes executor(
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

To run a task run the Kubernetes executor that utilizes ephemeral storage:

1. Create a [worker queue](configure-worker-queues.md) with `m5d` workers. See [Modify a cluster](modify-cluster.md) for instructions on adding `m5d` workers to your cluster.
2. Mount and [emptyDir volume](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example) to the Kubernetes executor. For example:

    ```python {5-14,26-27}
    from airflow.configuration import conf
    from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import Kubernetes executor
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

    example_volume_test = Kubernetes executor(
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

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
