---
sidebar_label: 'Configure Deployment resources'
title: 'Configure Deployment resources'
id: configure-deployment-resources
description: Learn how to create and configure Astro Deployment resources.
---

## Overview

After you create an Astro Deployment, you can modify its resource settings to make sure that your tasks have the CPU and memory required to complete successfully.

## Worker resources

A worker is responsible for executing tasks, which are first scheduled and queued by the scheduler. On Astro, task execution is powered by the [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html) with [KEDA](https://www.astronomer.io/blog/the-keda-autoscaler), which enables workers to autoscale between 1 and 10 depending on real-time workload. Each worker is a Kubernetes Pod that is hosted within a Kubernetes Node in your Astro cluster.

To modify the resources allocated to the workers in your Deployment, specify a quantity of AUs in the **Worker Resources** field of the Cloud UI. This value determines the size of each worker in your Deployment. While the total number of workers running at any given time may change, all workers will be created with the amount of CPU and memory you specify here. If you set **Worker Resources** to 10 AU, for example, your Deployment might scale up to 3 workers using 10 AU each for a total consumption of 30 AU.

To ensure reliability, the minimum worker size supported is 10 AU. Beyond that, the maximum worker size you can set depends on the node instance type that is configured for the cluster in which your Deployment is hosted. If you attempt to provision a worker size that is not supported by your cluster's instance type, you will see an error in the Cloud UI. For example, if the node instance type for a given cluster is set to `m5.xlarge`, the maximum worker size supported for any Deployment within that cluster is 26 AU (2.6 CPUs, 9.7 GiB memory). This limit accounts for overhead that is required for system components.

For a list of supported node instance types and their corresponding worker size limits, see [AWS resource reference](resource-reference-aws.md#deployment-worker-size-limits). To request a different instance type for your cluster, reach out to [Astronomer support](https://support.astronomer.io).

### Worker autoscaling logic

While the **Worker Resources** setting affects the amount of computing power allocated to each worker, the number of workers running on your Deployment is based solely on the number of tasks in a queued or running state.

The maximum number of tasks that a single worker can execute at once is 16. This value is known in Airflow as **worker concurrency**. Worker concurrency is currently a [system-wide setting on Astro](platform-variables.md) that cannot be changed. As soon as there are more than 16 tasks queued or running at any given time, one or more new workers is spun up to execute the additional tasks. The number of workers running on a Deployment at any given time can be calculated by the following expression, where worker Concurrency is 16:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Worker concurrency)`

The number of workers subsequently determines the Deployment's [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment. To ensure that you can always run as many tasks as your workers allow, parallelism is calculated with the following expression:

`[Parallelism]= [Number of workers] * [Worker concurrency]`

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, read [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met. By adjusting the **Scheduler Count** slider in the Cloud UI, you can configure up to 4 schedulers, each of which will be provisioned with the AU specified in **Scheduler Resources**.

For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each.

If you experience delays in task execution, which you can track via the Gantt Chart view of the Airflow UI, we recommend increasing the AU allocated towards the scheduler. The default resource allocation is 10 AU.

## Edit Deployment resource settings

If you haven't created a Deployment, see [Create a Deployment](create-deployment.md).

1. Log in to the [Cloud UI](https://cloud.astronomer.io) and select a Workspace.
2. Select a Deployment.
3. Click **Edit Configuration**.
4. Edit the Deployment resource settings. For more information about these settings, review the content in this topic.
5. Click **Update Deployment**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Next steps

- [Set environment variables on Astro](environment-variables.md).

- [Manage Deployment API keys](api-keys.md).
