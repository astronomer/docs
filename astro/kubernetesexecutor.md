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

- Fault tolerance.  A task that fails doesn't cause other tasks to fail.
- Run tasks in a Kubernetes cluster outside of the Astro data plane. This can be helpful when you need to run individual tasks on infrastructure that isn't currently supported by Astro, such as GPU nodes or other third-party services.
- Specify CPU and memory limits or minimums to optimize performance and reduce costs.
- Task isolation. A task uses only the resources allocated to it and it can't consume resources allocated to other tasks. 
- Running tasks are not interrupted when a deploy is pushed.

On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every cluster in the data plane and is managed by Astronomer.

## Known limitations

- Tasks take longer to start and this causes task latency.
- Cross-account service accounts are not supported on Pods launched in an Astro cluster. To allow access to external data sources, you can provide credentials and secrets to tasks.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- The `pod_template_file` argument is not supported on Pods launched in an Astro cluster. If you use the `pod_template_file` argument, customized values are overridden when they are required by Astronomer and your tasks will fail. Astronomer recommends using `python-kubernetes-sdk`. See [Astro Python SDK ReadTheDocs](https://astro-sdk-python.readthedocs.io/en/stable/).

## Prerequisites

- An [Astro project](create-project.md).
- An Astro [Deployment](create-deployment.md).

## Set up and configure the Kubernetes executor

The Kubernetes executor runs as a process in the Airflow Scheduler. You select and modify Kubernetes executor settings in the Cloud UI. Astro automatically allocates resources to Pods created by the Kubernetes executor, but you can adjust them to meet your requirements. See [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

## Related documentation

- [How to use cluster ConfigMaps, Secrets, and Volumes with Pods](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-to-use-cluster-configmaps-secrets-and-volumes-with-pod)
- [Kubernetes executor Airflow Guide](https://airflow.apache.org/docs/apache-airflow/2.1.2/executor/kubernetes.html)
- [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md)
- [Airflow Executors](https://docs.astronomer.io/learn/airflow-executors-explained)
