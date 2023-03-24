---
sidebar_label: 'Create a Deployment'
title: 'Create a Deployment'
id: create-deployment
---

<head>
  <meta name="description" content="Learn how to create an Astro Deployment. After you’ve created a Deployment, you can deploy DAGs to it from the Astro command-line interface (CLI), or from a continuous integration and continuous delivery (CI/CD) pipeline." />
  <meta name="og:description" content="Learn how to create an Astro Deployment. After you’ve created a Deployment, you can deploy DAGs to it from the Astro command-line interface (CLI), or from a continuous integration and continuous delivery (CI/CD) pipeline." />
</head>


An Astro Deployment is an Astro Runtime environment that is powered by the core components of Apache Airflow, including the Airflow webserver, scheduler, and one or more workers.

You can create a Deployment from a Workspace on Astro. After you create a Deployment, you can deploy DAGs to it from the Astro CLI or from a continuous delivery (CI/CD) process. All DAGs and tasks on Astro are executed within a Deployment.

Every Deployment is hosted on a single Astro cluster with its own dedicated resources, which you can customize to meet the unique requirements of your Organization. Every Astro cluster operates with a primary database that hosts the individual databases for each Deployment.  To restrict communication between Deployments, resources for each Deployment are isolated within a corresponding Kubernetes namespace in the data plane. See [Deployment network isolation](data-protection.md#deployment-network-isolation).

## Prerequisites

- A [Workspace](manage-workspaces.md)

## Create a Deployment

:::cli
If you prefer, you can also run the `astro deployment create` command in the Astro CLI to create a Deployment. See [CLI Command Reference](cli/astro-deployment-create.md).
:::

1. In the Cloud UI, select a Workspace.

2. On the **Deployments** page, click **Deployment**.

3. Complete the following fields:

    - **Name**: Enter a name for your Deployment.
    - **Astro Runtime**: By default, the latest version of Astro Runtime is selected. The Astro Runtime versions provided in the Cloud UI are limited to patches for the most recent major and minor releases. Deprecated versions of Astro Runtime aren't available.

        To upgrade the Astro Runtime version for your Deployment, you’ll need to update your Docker image in your Astro project directory. For more information about upgrading Astro Runtime, see [Upgrade Astro Runtime](upgrade-runtime.md).

    - **Description**: Optional. Enter a description for your Deployment.
    - **Cluster**: Select the Astro cluster in which you want to create this Deployment.
    - **Executor**: Select an executor to run your scheduled tasks. The Celery executor runs multiple tasks in a single worker and is a good choice for most teams. The Kubernetes executor runs each task in an isolated Kubernetes Pod and is a good option for teams that want fine-grained control over the execution environment for each of their tasks. For more information about the benefits and limitations of each executor, see [Choose an executor](configure-deployment-resources.md#choose-an-executor).
    - **Worker Type**: Select the worker type for your default worker queue. See [Worker queues](configure-deployment-resources.md#worker-queues).

4. Optional. Edit additional Deployment resource settings. See [Configure Deployment resources](configure-deployment-resources.md). If you don't change any Deployment resource settings, your Deployment is created with the following resources:

    - The celery executor
    - A worker queue named `default` that runs a maximum of 10 workers. Each of these workers can run a maximum of 16 tasks can run at a time.
    - A single scheduler with 0.5 CPUs and 1.88 GiB of memory.

5. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment is in progress. Select the **Deployments** link to go to the **Deployments** page. The Deployment status is **Creating** until all underlying components in your Astro cluster are healthy, including the Airflow webserver and scheduler. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health).

## Next steps

- [Configure Deployment resources](configure-deployment-resources.md)
- [Set environment variables on Astro](environment-variables.md)
- [Manage Deployment API keys](api-keys.md)
