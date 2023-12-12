---
sidebar_label: 'Create a Deployment'
title: 'Create a Deployment'
id: create-deployment
---

<head>
  <meta name="description" content="Learn how to create an Astro Deployment. After you’ve created a Deployment, you can deploy DAGs to it from the Astro command-line interface (CLI), or from a continuous integration and continuous delivery (CI/CD) pipeline." />
  <meta name="og:description" content="Learn how to create an Astro Deployment. After you’ve created a Deployment, you can deploy DAGs to it from the Astro command-line interface (CLI), or from a continuous integration and continuous delivery (CI/CD) pipeline." />
</head>

An Astro Deployment is an Airflow environment that is powered by [Astro Runtime](runtime-image-architecture.md). It runs all core Airflow components, including the Airflow webserver, scheduler, and workers, plus additional tooling for reliability and observability.

There are three ways to create a Deployment: 

- Manually, using the Cloud UI. This is the most basic way to create a Deployment and is the focus of this document.
- Programmatically, using [`astro deployment create`](cli/astro-deployment-create.md).
- Programmatically, using a Deployment template file. See [Manage Deployments as code](manage-deployments-as-code.md#create-a-deployment-from-a-template-file).

To create a Deployment, you must choose a cluster type to host the Deployment:

- A **standard cluster** is the default cluster type and the quickest way to get an Airflow environment up and running on Astro. A standard cluster is a multi-tenant cluster managed by Astronomer where each Deployment exists in its own dedicated Kubernetes namespace. To run a Deployment in a standard cluster, you select a cloud provider and region when you create the Deployment. Then, Astro automatically creates your Deployment in an existing standard cluster based on your configuration.

- A **dedicated cluster** is a single-tenant Kubernetes cluster that's used exclusively by your team. Choose this option if:

    - You need private networking support between Astro and your cloud or on-premise data services.
    - You want to use a specific cloud provider or region that is not supported on standard clusters.
    - You need to run Airflow environments in separate clusters for business or security reasons.
    
    Note that due to expanded resource usage, dedicated clusters cost more than standard clusters. If no dedicated clusters are available to select, see [Create a Dedicated cluster](create-dedicated-cluster.md) to create a new one.

After you create a Deployment, you can deploy DAGs to it using the Astro CLI on your local machine or a continuous integration/continuous delivery (CI/CD) tool. All DAGs and tasks on Astro are executed within a Deployment.

Every Deployment is hosted on an Astro cluster with its own dedicated resources that you can [customize](deployment-settings.md) to fine-tune your resource usage. To restrict communication between Deployments, resources for each Deployment are isolated within a corresponding Kubernetes namespace. See [Deployment network isolation](data-protection.md#deployment-network-isolation).

## Prerequisites

- A [Workspace](manage-workspaces.md)

## Create a Deployment

1. In the Cloud UI, go to **Deployments**.

2. Click **+ Deployment**.

    ![Deployment creation button](/img/docs/create-button.png)

3. Enter a **Name** for the Deployment.

4. (Optional) Configure other details for your Deployment, including cluster, executor, and worker resources. If you have no specific resource requirements for running Airflow, the default configurations should work in most cases. For all available Deployment options, see [Deployment settings](deployment-settings.md).

5. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment is in progress. The Deployment status is **Creating** until all underlying components in your Astro cluster are healthy, including the Airflow webserver and scheduler. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
     
You can continue to access your other Deployments by selecting the **Deployments** link.
    
For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health).

## Next steps

- [Deployment settings](deployment-settings.md)
- [Set environment variables on Astro](environment-variables.md)
- [Authenticate an automation tool to Astro](automation-authentication.md)
