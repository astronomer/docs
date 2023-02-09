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

The Kubernetes executor runs as a process in the Airflow Scheduler. You can select and modify the Kubernetes executor in the Cloud UI. See [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
