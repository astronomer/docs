---
sidebar_label: 'Configure Deployment Resources'
title: 'Configure Deployment Resources'
id: configure-deployment-resources
description: Learn how to create and configure Astro Deployment resources.
---

## Overview

After you create an Astro Deployment, you can modify its resource settings to make sure that your tasks have the CPU and memory required to complete successfully.

## Worker Resources

A worker is responsible for executing tasks, which are first scheduled and queued by the Scheduler. On Astro, task execution is powered by the [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html) with [KEDA](https://www.astronomer.io/blog/the-keda-autoscaler), which enables workers to autoscale between 1 and 10 depending on real-time workload. Each worker is a Kubernetes Pod that is hosted within a Kubernetes Node in your Astro Cluster.

To modify the resources allocated to the workers in your Deployment, specify a quantity of AUs in the **Worker Resources** field of the Cloud UI. This value determines the size of each worker in your Deployment. While the total number of workers running at any given time may change, all workers will be created with the amount of CPU and memory you specify here. If you set **Worker Resources** to 10 AU, for example, your Deployment might scale up to 3 workers using 10 AU each for a total consumption of 30 AU.

To ensure reliability, the minimum worker size supported is 10 AU. Beyond that, the maximum worker size you can set depends on the node instance type that is configured for the Cluster in which your Deployment is hosted. If you attempt to provision a worker size that is not supported by your Cluster's instance type, you will see an error in the Cloud UI. For example, if the node instance type for a given Cluster is set to `m5.xlarge`, the maximum worker size supported for any Deployment within that Cluster is 27 AU (2.7 CPUs, 10.1 GiB memory). This limit accounts for overhead that is required for system components.

For a list of supported node instance types and their corresponding worker size limits, see [AWS Resource Reference](resource-reference-aws.md#deployment-worker-size-limits). To request a different instance type for your Cluster, reach out to [Astronomer Support](https://support.astronomer.io).

### Worker Autoscaling Logic

While the **Worker Resources** setting affects the amount of computing power allocated to each worker, the number of workers running on your Deployment is based solely on the number of tasks in a queued or running state.

The maximum number of tasks that a single worker can execute at once is 16. This value is known in Airflow as **Worker Concurrency**. Worker Concurrency is currently a [system-wide setting on Astro](platform-variables.md) that cannot be changed. As soon as there are more than 16 tasks queued or running at any given time, one or more new workers is spun up to execute the additional tasks. The number of workers running on a Deployment at any given time can be calculated with the following expression, where Worker Concurrency is 16:

`[Number of Workers]= ([Queued tasks]+[Running tasks])/(Worker Concurrency)`

The number of workers subsequently determines the Deployment's [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment. To ensure that you can always run as many tasks as your workers allow, parallelism is calculated with the following expression:

`[Parallelism]= [Number of Workers] * [Worker Concurrency]`

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, read [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Scheduler Resources

The [Airflow Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met. By adjusting the **Scheduler Count** slider in the Cloud UI, you can configure up to 4 Schedulers, each of which will be provisioned with the AU specified in **Scheduler Resources**.

For example, if you set Scheduler Resources to 10 AU and Scheduler Count to 2, your Airflow Deployment will run with 2 Airflow Schedulers using 10 AU each.

If you experience delays in task execution, which you can track via the Gantt Chart view of the Airflow UI, we recommend increasing the AU allocated towards the Scheduler. The default resource allocation is 10 AU.

## Edit Deployment Resource Settings

If you haven't created a Deployment, see [Create a Deployment](create-deployment.md).

1. Log in to the [Cloud UI](https://cloud.astronomer.io) and select a Workspace.
2. Select a Deployment.
3. Click **Edit Configuration**.
4. Edit the Deployment resource settings. For more information about these settings, review the content in this topic.
5. Click **Update Deployment**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Next Steps

- [Set Environment Variables on Astro](environment-variables.md).

- [Manage Deployment API Keys](api-keys.md).
