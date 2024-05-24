---
sidebar_label: 'Create a Deployment'
title: 'Create a Deployment on Astronomer Software'
id: create-deployment
description: Configure an Airflow Deployment's resources on Astronomer Software.
---

Use this document to learn how to create a Deployment on Astronomer Software.

## Prerequisites

- [The Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
- A [Workspace](manage-workspaces.md)

## Create a Deployment in the Software UI

To create an Airflow Deployment on Astronomer:

1. Log in to your Astronomer platform at `app.BASEDOMAIN`, select a Workspace, and then click **New Deployment**.
2. Complete the following fields:

    - **Name**: Enter a descriptive name for the Deployment.
    - **Description**: (Optional) Enter a description for your Deployment. 
    - **Airflow Version**: Select the Airflow version/ Astro Runtime version that the Deployment should run with.
    - **Executor**: Astronomer recommends starting with Local.

3. Click **Create Deployment** and wait a few moments. After the Deployment is created, you can access the **Settings** page of your new Deployment:

   ![New Deployment Celery Dashboard](/img/software/v0.23-new_deployment-dashboard.png)

    On this tab you can modify resources for your Deployment. Specifically, you can:

    - Choose a strategy for how you configure resources to Airflow components. See [Customize resource usage](customize-resource-usage.md).
    - Select an Airflow executor
    - Allocate resources to your Airflow scheduler and webserver
    - Set scheduler count (_Airflow 2.0+ only_)
    - Add extra capacity (_Kubernetes only_)
    - Set worker count (_Celery only_)
    - Adjust your worker termination grace period (_Celery only_)

## Customize Deployment release names

An Airflow Deployment's release name on Astronomer is a unique, immutable identifier for that Deployment. The release name corresponds to its Kubernetes namespace and that renders in Grafana, Kibana, and other platform-level monitoring tools. 

By default, release names are randomly generated in the following format: `noun-noun-<4-digit-number>`. For example: `elementary-zenith-7243`. Alternatively, you can customize the release name for a Deployment if you want all namespaces in your cluster to follow a specific style.

To customize the release name for a Deployment as you're creating it, you first need to enable the feature on your Astronomer platform. To do so, set the following value in your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        manualReleaseNames: true # Allows you to set your release names
```

Then, push the updated `config.yaml` file to your installation as described in [Apply a config change](apply-platform-config.md).

After applying this change, the **Release Name** field in the Software UI becomes configurable:

![Custom Release Name Field](/img/software/custom-release-name.png)

## Programmatically create or update Deployments

You can programmatically create or update Deployments with all possible configurations using the Houston API `upsertDeployment` mutation. See [Create or update a Deployment with configurations](houston-api.md#create-or-update-a-deployment-with-configurations).
