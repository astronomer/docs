---
sidebar_label: 'Celery executor'
title: 'Configure the Celery executor'
id: 'celery-executor'
---

On Astro, you can configure Celery executor in the following ways:

- The type and size of your workers.
- The minimum and maximum number of workers that your Deployment can run at a time.
- The number of tasks that each worker can run at a time.

You can set these configurations per [worker queue](configure-worker-queues.md). With the celery executor, you can configure multiple worker queues for different types of tasks and assign tasks to those queues in your DAG code.

The following document explains basic Celery executor configurations for a single worker queue. For instructions on how to configure multiple worker queues, see [Create a worker queue](configure-worker-queues.md#create-or-edit-a-worker-queue).

:::tip

If you plan to use only the KubernetesPodOperator in your Deployment, set your Celery executor resources to the lowest possible amounts, because the executor is only required for launching your Pods. See [KubernetesPodOperator](kubernetespodoperator.md) for more information. 

:::

## Celery worker autoscaling logic

The number of Celery workers running per worker queue on your Deployment at a given time is based on two values:

- The total number of tasks in a `queued` or `running` state
- The worker queue's setting for **Maximum Tasks per Worker**

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

Deployment [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism) is the maximum number of tasks that can run concurrently across worker queues. To ensure that you can always run as many tasks as your worker queues allow, parallelism is calculated with the following expression:

`[Parallelism]= ([The sum of all 'Max Worker Count' values for all worker queues] * [The sum of all 'Maximum tasks per worker' values for all worker queues])`.

[Kubernetest Event Driven Autoscaling](https://keda.sh/) (KEDA) computes these calculations every ten seconds. When KEDA determines that it can scale down a worker, it waits for five minutes after the last running task on the worker finishes before terminating the worker Pod.

When you push code to a Deployment, workers running tasks from before the code push do not scale down until those tasks is complete. To learn more about how changes to a Deployment can affect worker resource allocation, see [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Configure Celery worker scaling

For each worker queue on your Deployment, you have to specify certain settings that affect worker autoscaling behavior. If you're new to Airflow, Astronomer recommends using the defaults in Astro for each of these settings.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Edit** to edit a worker queue.

3. Configure the following settings:

    - **Worker type**: Choose the amount of resources that each worker will have.
    - **Concurrency**: The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. It is 16 by default. Note that on Astro Hybrid, this setting is called **Max Tasks per Worker**
    - **Worker Count (Min-Max)**: The minimum and maximum number of workers that can run at a time. The number of running workers changes based on **Concurrency** and the current number of tasks in a queued or running state. By default, the minimum number of workers is 1 and the maximum is 10.
    
4. Click **Update Queue**.

## See also

- [Configure worker queues](configure-worker-queues.md).
- [Airflow Executors explained](https://docs.astronomer.io/learn/airflow-executors-explained)
