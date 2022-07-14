---
sidebar_label: 'Create a Deployment'
title: 'Create a Deployment'
id: create-deployment
description: Learn how to create an Astro Deployment.
---

An Astro Deployment is an Astro Runtime environment that is powered by the core components of Apache Airflow, including the Airflow webserver, scheduler, and one or more workers.

You can create a Deployment from a Workspace on Astro. After you create a Deployment, you can deploy DAGs to it from the Astro CLI or from a continuous delivery (CI/CD) process. All DAGs and tasks on Astro are executed within a Deployment.

Every Deployment is hosted on a single Astro cluster with its own dedicated resources, which you can customize to meet the unique requirements of your Organization. Every Astro cluster operates with a primary database that hosts the individual databases for each Deployment.  To restrict communication between Deployments, resources for each Deployment are isolated within a corresponding Kubernetes namespace in the data plane. See [Deployment network isolation](data-protection.md#deployment-network-isolation).

## Prerequisites

- A [Workspace](manage-workspaces.md)

## Create a Deployment

If you prefer, you can run the `astro deployment create` command in the Astro CLI to create a Deployment. See [CLI Command Reference](cli/astro-deployment-create.md).

1. Log in to the [Cloud UI](https://cloud.astronomer.io) and select a Workspace.
2. Click the **Deployment** button.
3. Complete the following fields:
    - **Name**: Enter a name for your Deployment.
    - **Astro Runtime**: By default, the latest version of Astro Runtime is selected. The Astro Runtime versions provided in the Cloud UI are limited to patches for the most recent major and minor releases. Deprecated versions of Astro Runtime aren't available.

        To upgrade the Astro Runtime version for your Deployment, you’ll need to update your Docker image in your Astro project directory. For more information about upgrading Astro Runtime, see [Upgrade Astro Runtime](upgrade-runtime.md).

    - **Description**: Optional. Enter a description for your Deployment.
    - **Cluster**: Select the Astro cluster in which you want to create this Deployment.
4. Optional. Edit the Deployment resource settings. See [Configure Deployment resources](configure-deployment-resources.md).
5. Click **Create Deployment**.

    The initial status of all new Deployments is `UNHEALTHY`. This indicates that the webserver and scheduler for the Deployment are being created in your Astro cluster. In a few minutes, the status changes to `HEALTHY`.

## Next steps

- [Configure Deployment resources](configure-deployment-resources.md)

- [Set environment variables on Astro](environment-variables.md)

- [Manage Deployment API keys](api-keys.md)
