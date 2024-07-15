---
sidebar_label: 'Overview'
title: 'Manage Airflow executors on Astro'
id: 'executors-overview'
---

The Apache Airflow® executor determines which worker resources run your scheduled tasks.

On Astro, every Deployment requires an executor and you can change the executor at any time. After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. Use the information provided in this topic to learn how to configure the Celery and Kubernetes executors on Astro.

To learn more about executors in Airflow, see [Airflow executors](https://www.astronomer.io/docs/learn/airflow-executors-explained).

## Choose an executor

The difference between executors is based on how tasks are distributed across worker resources. The executor you choose affects the infrastructure cost of a Deployment and how efficiently your tasks execute. Astro currently supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

Read the following topics to learn about the benefits and limitations of each executor. For information about how to change the executor of an existing Deployment, see [Update the Deployment executor](deployment-resources.md#update-the-deployment-executor).

### Celery executor

The Celery executor is the default for all new Deployments. It uses a group of workers, each of which can run multiple tasks at a time. Astronomer uses [worker autoscaling logic](celery-executor.md#celery-worker-autoscaling-logic) to determine how many workers run on your Deployment at a given time.

The Celery executor is a good option for most use cases. Specifically, the Celery executor is a good fit for your Deployment if:

- You're just getting started with Airflow.
- You don't have tasks that require more than 24 hours to execute. Celery workers give their tasks only 24 hours to finish so they can restart in the event of a code deploy.
- You want to use different worker types based on the type of task you're running. See [Configure worker queues](configure-worker-queues.mdx).
- You have many short-running tasks.
- Your tasks require the shortest startup latency (often milliseconds).
- You don't require task or dependency isolation.
- You want to direct tasks to run in worker queues with varying resources. This is useful if you want to run a subset of tasks with priority for SLA reasons, or if your tasks have varied resource requirements.

If you find that some tasks consume the resources of other tasks and cause them to fail, Astronomer recommends implementing worker queues or moving to the Kubernetes executor.

See [Manage the Celery executor](celery-executor.md) to learn more about how to configure the Celery executor.

### Kubernetes executor

The Kubernetes executor runs each task in an individual Kubernetes Pod that's defined either in your task or Deployment configuration. When a task completes, its Pod is terminated and the resources are returned to your cluster. On Astro, the infrastructure required to run the Kubernetes executor is built into every Deployment and is managed by Astronomer. 

You can specify the configuration of a task's Pod, including CPU and memory, as part of your DAG definition using the [Kubernetes Python Client](https://github.com/kubernetes-client/python) and the `pod_override` arg. Any task without a `pod_override` runs in a [default Pod](deployment-resources.md#configure-kubernetes-pod-resources) as configured on your Deployment. 

The Kubernetes executor is a good option for some use cases. Specifically, the Kubernetes executor is a good fit for your Deployment if:

- You have long-running tasks that might require more than 24 hours to execute.
- Your tasks are compute-intensive or you are processing large volumes of data within the task. Kubernetes executor tasks run separately in a dedicated Pod per task.
- Your tasks can tolerate some startup latency (often seconds)
- Your tasks require task or dependency isolation.
- You have had issues running certain tasks reliably with the Celery executor.

If you're running a high task volume or cannot tolerate startup latency, Astronomer recommends the Celery executor. To learn more about using the Kubernetes executor, see [Manage the Kubernetes executor](kubernetes-executor.md).

:::info Running costs for the Kubernetes executor

On Astro Hosted, the Kubernetes executor runs Pods on the smallest possible [Astro machine type](configure-worker-queues.mdx#hosted-worker-types) that can support the Pod. For example, if a Pod has a limit of 1 vCPU and 2.5 Gib memory, it will run on an A10 machine type. Astro attempts to group as many possible Pods on the same worker instance before provisioning a new worker machine. This is why charges for the Kubernetes executor appear as Astro machine type usage on your billing statements.

:::

:::tip

The Kubernetes executor is primarily used for resource optimization. If you want more control over the environment and dependencies that your tasks run with, consider using the [KubernetesPodOperator](kubernetespodoperator.md) with either the Celery executor or Kubernetes executor.

:::
