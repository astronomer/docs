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

Use dbt on Astro, so you can now deploy your dbt projects directly to Astro, without changes tied to updates with your DAGs or full image code deploys. When you use a dbt project deploy, Astro bundles all files in your dbt project and pushes them to Astro, where they are mounted on your Airflow containers so that your DAGs can access them.

## Prerequisites

- An Astro Deployment
- An Astro Project that includes your dbt project

## Step 1: Deploy your full Astro image

``bash

astro deploy

```

## Step 2: Deploy your dbt project

Choose a Deployment that you want to deploy your dbt project to.

```bash

astro dbt deploy

```

:::tip

If you have a dbt project in a different location than your Astro Project, such as a different folder in your local environment or at a different path, you can specify the mount path.

```bash

astro dbt deploy --mount-path /usr/local/airflow/dbt/example-dbt-project

```
:::

## Step 3: Delete your dbt project

```bash

astro dbt delete

```

