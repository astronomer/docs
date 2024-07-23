---
sidebar_label: 'Deploy a dbt project'
title: 'Deploy dbt projects to Astro'
id: deploy-dbt-project
description: Learn how to deploy dbt projects to Astro.
---
import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

:::privatepreview
:::

Use dbt Deploys to deploy your dbt projects directly to Astro without changing your DAGs or making an image deploy. This is ideal for deploying dbt code that lives outside of your Astro project 

When you use a dbt project deploy, Astro bundles all files in your dbt project and pushes them to Astro, where they are mounted on your Airflow containers so that your DAGs can access them.

## Prerequisites

- An Astro Deployment
- An Astro Project that includes your dbt project

## Step 1: Deploy your full Astro image

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

