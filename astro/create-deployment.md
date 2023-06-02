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

Every Deployment is hosted on a single Astro cluster with its own dedicated resources, which you can customize to meet the unique requirements of your Organization. Every Astro cluster operates with a primary database that hosts the individual databases for each Deployment.  To restrict communication between Deployments, resources for each Deployment are isolated within a corresponding Kubernetes namespace. See [Deployment network isolation](data-protection.md#deployment-network-isolation).

## Prerequisites

- A [Workspace](manage-workspaces.md)

## Create a Deployment

:::cli

If you prefer, you can also run `astro deployment create` to create a Deployment. See [CLI Command Reference](cli/astro-deployment-create.md).

:::

1. In the Cloud UI, select a Workspace.

2. On the **Deployments** page, click **+ Deployment**.

3. Complete the following fields:

    - **Name**: Enter a name for your Deployment.
    - **Description**: Optional. Enter a description for your Deployment.
    - **Cluster**: Choose whether you want to run your Deployment in a **Standard cluster** or **Dedicated cluster**. If you don't have specific networking or cloud requirements, Astronomer recommends using the default **Standard cluster** configurations.

        To configure and use dedicated clusters, see [Create a dedicated cluster](create-dedicated-cluster.md). If you don't have the option of choosing between standard or dedicated, you are an Astro Hybrid user and must choose a cluster that has been configured for your Organization. See [Manage Hybrid clusters](manage-hybrid-clusters.md).

    - **Executor**: Select an executor to run your scheduled tasks. The Celery executor runs multiple tasks in a single worker and is a good choice for most teams. The Kubernetes executor runs each task in an isolated Kubernetes Pod and is a good option for teams that want fine-grained control over the execution environment for each of their tasks. For more information about the benefits and limitations of each executor, see [Choose an executor](configure-deployment-resources.md#choose-an-executor).
    - **Astro Runtime**: Choose which Astro Runtime version you want your Deployment to run. By default, the latest version of Astro Runtime is selected. The Astro Runtime versions available in the Cloud UI are limited to patches for the most recent major and minor releases. Deprecated versions of Astro Runtime aren't available.

        To upgrade the Astro Runtime version for your Deployment, you’ll need to update your Docker image in your Astro project directory. See [Upgrade Astro Runtime](upgrade-runtime.md).
    
    - **Scheduler**: Select the amount of resources you want your Deployment scheduler to use. The scheduler is responsible for queueing and scheduling your Airflow tasks. See [Configure Deployment resources](configure-deployment-resources.md#scheduler-resources) for more information.
    - **Worker queue**: Configure the `default` worker queue for your Deployment. A worker queue is a group of identically-configured workers responsible for running your tasks. The default options for the `default` worker queue are suitable for most workloads. See [Worker queues](configure-deployment-resources.md#worker-queues).
    - **Kubernetes Executor and KPO Pods**: (Optional) If you're using the Kubernetes executor or KubernetesPodOperator, configure the default Pods that tasks run in. See [Configure the Kubernetes executor](executors.md#configure-the-kubernetes-executor) and [Configure the KubernetesPodOperator](kubernetespodoperator.md#configure-the-kubernetespodoperator-in-the-cloud-ui).

    These are the essential fields for configuring a Deployment. You can optionally configure additional details for your Deployment based on resource usage, user permissions, and resiliency. For all available Deployment options, see [Configure Deployment resources](configure-deployment-resources.md).

4. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment is in progress. Select the **Deployments** link to go to the **Deployments** page. The Deployment status is **Creating** until all underlying components in your Astro cluster are healthy, including the Airflow webserver and scheduler. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health).

## Next steps

- [Configure Deployment resources](configure-deployment-resources.md)
- [Set environment variables on Astro](environment-variables.md)
- [Manage Deployment API keys](api-keys.md)
