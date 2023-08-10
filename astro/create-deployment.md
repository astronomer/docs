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

The most basic way to create a Deployment is through the Cloud UI. After you create a Deployment, you can deploy DAGs to it using the Astro CLI on your local machine or a continuous integration/continuous delivery (CI/CD) tool. All DAGs and tasks on Astro are executed within a Deployment.

Every Deployment is hosted on an Astro cluster with its own dedicated resources, which you can customize to fine-tune your resource usage. To restrict communication between Deployments, resources for each Deployment are isolated within a corresponding Kubernetes namespace. See [Deployment network isolation](data-protection.md#deployment-network-isolation).

This document explains how to create Deployments through the Cloud UI. To create Deployments programmatically using the Astro CLI, see:

- [Astro CLI reference guide](cli/astro-deployment-create.md)
- [Manage Deployments as code](manage-deployments-as-code.md)

## Prerequisites

- A [Workspace](manage-workspaces.md)

## Create a Deployment

1. In the Cloud UI, go to **Deployments**.

2. Click **+ Deployment**.

    ![Deployment creation button](/img/docs/create-button.png)

3. Enter a **Name** for the Deployment.

4. (Optional) Configure other details for your Deployment, including cluster, executor, and worker resources. If you have no specific resource requirements for running Airflow, the default configurations should work in most cases. For all available Deployment options, see [Configure Deployment resources](configure-deployment-resources.md).

5. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment is in progress. Select the **Deployments** link to go to the **Deployments** page. The Deployment status is **Creating** until all underlying components in your Astro cluster are healthy, including the Airflow webserver and scheduler. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health).

## Next steps

- [Configure Deployment resources](configure-deployment-resources.md)
- [Set environment variables on Astro](environment-variables.md)
- [Manage Deployment API keys](api-keys.md)
