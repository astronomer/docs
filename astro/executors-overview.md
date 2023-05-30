---
sidebar_label: 'Overview'
title: 'Manage Airflow executors on Astro'
id: 'executors-overview'
---

The Airflow executor determines which worker resources run your scheduled tasks. 

On Astro, every Deployment requires an executor and you can update the executor at any time. After you choose an executor for an Astro Deployment, you can configure your DAGs and Deployment resources to maximize the executor's efficiency and performance. Use the information provided in this topic to learn how to configure the Celery and Kubernetes executors on Astro.

To learn more about executors in Airflow, see [Airflow executors](https://docs.astronomer.io/learn/airflow-executors-explained).

## Choose an executor

The difference between executors is based on how tasks are distributed across worker resources. The executor you choose affects the infrastructure cost of a Deployment and how efficiently your tasks execute. Astro currently supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

Read the following topics to learn about the benefits and limitations of each executor. For information about how to change the executor of an existing Deployment, see [Update the Deployment executor](configure-deployment-resources.md#update-the-deployment-executor).

### Celery executor

The Celery executor is the default for all new Deployments. It uses a group of workers, each of which can run multiple tasks at a time. Astronomer uses [worker autoscaling logic](celery-executor.md#celery-worker-autoscaling-logic) to determine how many workers run on your Deployment at a given time.

The Celery executor is a good option for most use cases. Specifically, the Celery executor is a good fit for your Deployment if:

- You're just getting started with Airflow.
- You want to use different worker types based on the type of task you're running. See [Configure worker queues](configure-worker-queues.md).
- You have a high number of short-running tasks and want to ensure low latency between tasks.
- You don't often experience conflicts between Python or OS-level packages and don't require dependency isolation.

If you regularly experience dependency conflicts or find that some tasks consume the resources of other tasks and cause them to fail, Astronomer recommends implementing worker queues or moving to the Kubernetes executor.

See [Manage the Celery executor](celery-executor.md) to learn more about how to configure the Celery executor.

### Kubernetes executor

The Kubernetes executor runs each task in an individual Kubernetes Pod instead of in shared Celery workers. For each task that needs to run, the executor calls the Kubernetes API to dynamically launch a Pod for the task. You can specify the configuration of the task's Pod, including CPU and memory, as part of your DAG definition using the [Kubernetes Python Client](https://github.com/kubernetes-client/python) and the `pod_override` arg. When the task completes, the Pod terminates. 

On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every Deployment and is managed by Astronomer. Kubernetes Pods belonging to Deployments in the same Workspace can run on the same worker node, which reduces the amount of resources that are required to start up new Pods.

The Kubernetes executor is a good fit for teams that want fine-grained control over the execution environment of each of their tasks. Specifically, the Kubernetes executor is a good fit for your Deployment if:

- You have long-running tasks that require more than 24 hours to execute. The Kubernetes executor ensures that tasks longer than 24 hours are not interrupted when you deploy code.
- Your tasks are compute-intensive or you are processing large volumes of data within the task. Kubernetes executor tasks run separately in a dedicated pod per task. 
- You have a strong understanding of the CPU and memory that your tasks require and would benefit from being able to allocate and optimize infrastructure resources at the task level.
- You have had issues running certain tasks reliably with the Celery executor.
  
The primary limitation with the Kubernetes executor is that each task takes up to 1 minute to start running once scheduled. If you're running short-running tasks and cannot tolerate high latency, Astronomer recommends the Celery executor. To learn more about using the Kubernetes executor, see [Manage the Kubernetes executor](kubernetes-executor.md).

:::tip

If only some of your tasks need an isolated execution environment, consider using the [KubernetesPodOperator](kubernetespodoperator.md) with the Celery executor.

:::