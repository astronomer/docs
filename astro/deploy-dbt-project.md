---
sidebar_label: 'Deploy a dbt project'
title: 'Deploy dbt projects to Astro'
id: deploy-dbt-project
description: Learn how to deploy and run dbt projects with Apache Airflow on Astro.
---
import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

:::privatepreview
:::

To orchestrate dbt jobs with Apache Airflow, you need to deploy your dbt project to Astro alongside your DAGs and the rest of your Airflow code. dbt Deploys allow you to easily deploy your dbt project to Astro without needing complex processes to incorporate your two sets of code. When you use a dbt project deploy, Astro bundles all files in your dbt project and pushes them to Astro, where they are mounted on your Airflow containers so that your DAGs can access them.

Depending on your organization's software development lifecycle, your dbt project might live in the same Git repository as your Airflow code or in a different repository. Astronomer supports both methods but recommends having a dedicated Git repository for your dbt code that is separate from your Airflow code. 

To learn more about running dbt core or dbt Cloud with Apache Airflow, see [Orchestrate dbt Core jobs with Airflow](/learn/airflow-dbt.md).

## Prerequisites

- An Astro Deployment
- An Astro project
- A dbt project

## Step 1: Deploy your full Astro image

In order to first deploy a dbt project to Astro, Astronomer recommends that you have an Astro project already running on your Deployment with DAGs that need to read from dbt. That way, your dbt project will be read and used when you deploy it.

If you are using a new Deployment, first deploy your Astro project with the Astro CLI by running:
```bash

astro deploy

```

## Step 2: Deploy your dbt project

Choose a Deployment that you want to deploy your dbt project to.

```bash

astro dbt deploy

```

:::tip

If your dbt code is accessed at a different path or folder than the default path, specify the mount path.

```bash

astro dbt deploy --mount-path /usr/local/airflow/dbt/example-dbt-project

```
:::

## Step 3: Delete your dbt project

```bash

astro dbt delete

```

