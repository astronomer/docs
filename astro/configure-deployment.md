---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment'
id: configure-deployment
description: Learn how to create and configure an Astro Deployment.
---

## Overview

A Deployment on Astro is an instance of Astro Runtime that is powered by Apache Airflow's core components - a metadata database, a Webserver, one or more Schedulers, and one or more Workers. Every Deployment is hosted on a single Astro Cluster, has an isolated set of resources, and operates with a dedicated Postgres metadata database.

This guide walks you through the process of creating and configuring an Airflow Deployment.

## Configure a Workspace

When you first sign up for Astro, you can expect to be invited to a Workspace created for your team. Within a Workspace, you can create Deployments and push DAGs to any Deployment from the Astro CLI or from a CI/CD process. You're free to invite other users to that Workspace and create as many Deployments as you'd like.

## Create a Deployment

To create an Airflow Deployment on Astro:

1. Log in to the [Cloud UI](https://cloud.astronomer.io) and go to the **Deployments** tab on the left navigation bar.
2. On the top right-hand side of the Deployments page, click **New Deployment**.
3. Set the following:
    - **Name**
    - **Description**
    - **Astro Runtime**: By default, the latest version of Astro Runtime is selected
    - **Deployment Location**: The Astro Cluster in which you want to create this Deployment

3. Click **Create Deployment** and give it a few moments to spin up. Within a few seconds, you should see the following:

    ![Cloud UI Deployment Configuration](/img/docs/deployment-configuration.png)

    All Deployments show an initial health status of `UNHEALTHY` after their creation. This indicates that the Deployment's Webserver and Scheduler are still spinning up in your cloud. Wait a few minutes for this status to become `HEALTHY` before proceeding to the next step.

4. To access the Airflow UI, select **Open Airflow** on the top right.

:::tip

If you prefer to work with the Astro CLI, you can also create a Deployment by running the `astrocloud deployment create` command. For more information, see [CLI Command Reference](cli-reference/astrocloud-deployment-create.md).

:::

## Configure Deployment Resources

Once you create a Deployment, you can choose to modify its resources and configurations to best fit the needs of your tasks. Specifically, you can modify these two components:

- Worker(s)
- Scheduler

For reference, Astro supports the `AU` as the primary resource unit. In this context,

- 1 AU = 0.1 CPU, .375 GB Memory
- 10 AU = 1 CPU, 3.75 GB Memory

Read below for guidelines on how to configure each component.

### Worker Resources

A worker is responsible for executing tasks, which are first scheduled and queued by the Scheduler. On Astro, task execution is powered by the [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html) with [KEDA](https://www.astronomer.io/blog/the-keda-autoscaler), which enables workers to autoscale between 1 and 10 depending on real-time workload. Each worker is a Kubernetes Pod that is hosted within a Kubernetes Node in your Astro Cluster.

To modify the resources allocated to the workers in your Deployment, specify a quantity of AUs in the **Worker Resources** field of the Cloud UI. This value determines the size of each worker in your Deployment. While the total number of workers running at any given time may change, all workers will be created with the amount of CPU and memory you specify here. If you set **Worker Resources** to 10 AU, for example, your Deployment might scale up to 3 workers using 10 AU each for a total consumption of 30 AU.

To ensure reliability, the minimum worker size supported is 10 AU. Beyond that, the maximum worker size you can set depends on the node instance type that is configured for the Cluster in which your Deployment is hosted. If you attempt to provision a worker size that is not supported by your Cluster's instance type, you will see an error in the Cloud UI. For example, if the node instance type for a given Cluster is set to `m5.xlarge`, the maximum worker size supported for any Deployment within that Cluster is 27 AU (2.7 CPUs, 10.1 GiB memory). This limit accounts for overhead that is required for system components.

For a list of supported node instance types and their corresponding worker size limits, see [AWS Resource Reference](aws-resource-reference.md#deployment-worker-size-limits). To request a different instance type for your Cluster, reach out to [Astronomer Support](https://support.astronomer.io).

:::info Worker Autoscaling Logic

While the **Worker Resources** setting affects the amount of computing power allocated to each worker, the number of workers running on your Deployment is based solely on the number of tasks in a queued or running state.

The maximum number of tasks that a single worker can execute at once is 16. This value is known in Airflow as **Worker Concurrency**. Worker Concurrency is currently a [system-wide setting on Astro](platform-variables.md) that cannot be changed. As soon as there are more than 16 tasks queued or running at any given time, one or more new workers is spun up to execute the additional tasks. The number of workers running on a Deployment at any given time can be calculated by the following expression, where Worker Concurrency is 16:

`[Number of Workers]= ([Queued tasks]+[Running tasks])/(Worker Concurrency)`

This calculation is computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, read [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).
:::

### Scheduler

The [Airflow Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met. By adjusting the **Scheduler Count** slider in the Cloud UI, you can configure up to 4 Schedulers, each of which will be provisioned with the AU specified in **Scheduler Resources**.

For example, if you set Scheduler Resources to 10 AU and Scheduler Count to 2, your Airflow Deployment will run with 2 Airflow Schedulers using 10 AU each.

If you experience delays in task execution, which you can track via the Gantt Chart view of the Airflow UI, we recommend increasing the AU allocated towards the Scheduler. The default resource allocation is 10 AU.

## Set Environment Variables

Environment Variables can be used to set [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) and custom values, both of which can be applied to your Deployment. For example, you can configure Airflow Parallelism or a secrets backend to manage Airflow Connections.

To set Environment Variables, add them to the corresponding section of the Cloud UI or in your project's `Dockerfile`. If you're developing locally, they can also be added to a local `.env` file.

For more information on configuring Environment Variables, read [Environment Variables on Astro](environment-variables.md).
