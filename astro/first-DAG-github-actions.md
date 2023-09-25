---
sidebar_label: 'Run your first DAG with GitHub Actions'
title: 'Run your first DAG with GitHub Actions'
id: 'first-DAG-ga'
---

<head>
  <meta name="description" content="Learn how to run your first Apache Airflow DAG on Astro using the Cloud UI." />
  <meta name="og:description" content="Learn how to run your first Apache Airflow DAG on Astro using the Cloud UI." />
</head>

import {siteVariables} from '@site/src/versions';

Astro is the industry's leading managed service for Apache Airflow. You can quickly learn how Astro works by running an Apache Airflow DAG with GitHub Actions. This quickstart explains the steps required to deploy an example DAG to Astro and trigger a DAG run with Github Actions.

Specifically, you will:

- Start an Astro trial
- Authenticate and log in to Astro. 
- Create a Deployment. 
- Configure GitHub Actions.
- Deploy DAGs to Astro in the Cloud UI.
- Trigger a run of an example DAG in the Airflow UI. 

This tutorial takes about 15 minutes. You can also create and run your first DAG [from the Astro CLI](create-first-dag.md) in about 15 minutes. However, if you're new to Airflow and want a more in-depth tutorial, see [Write your First DAG](https://docs.astronomer.io/learn/get-started-with-airflow).

## Prerequisites

- An Astro account. To start an Astro trial, see [Start a trial](trial.md).
- A [GitHub](https://docs.github.com/en/get-started/signing-up-for-github) account.

:::info

If you're on your organization's network and can't access Astro, make a request to allowlist the following domains on your network:

- `https://cloud.astronomer.io/`
- `https://api.astronomer.io/`
- `https://images.astronomer.cloud/`
- `https://auth.astronomer.io/`
- `https://updates.astronomer.io/`
- `https://install.astronomer.io/`
- `https://astro-<your-org>.datakin.com/`
- `https://<your-org>.astronomer.run/`

:::

## Step 1: Create a Deployment

An Astro _Deployment_ is an instance of Apache Airflow that is powered by all core Airflow components, including a webserver, scheduler, and one or more workers. You deploy DAGs to a Deployment, and you can have one or more Deployments within a Workspace.

1. Log in to the [Cloud UI](https://cloud.astronomer.io)

2. On the **Deployments** page, click **+ Deployment**.

3. In the **Name** field, enter a name for your Deployment. You can leave the other fields at their default values. This creates a basic Deployment on a standard Astronomer-hosted cluster. You can delete the Deployment after you finish testing your example DAG runs. 

4. Click **Create Deployment**.

    A confirmation message appears indicating that the Deployment status is **Creating** until all underlying components in the Deployment are healthy. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health). Or, to learn more about how to customize your Deployment settings, see [Deployment settings](deployment-settings.md).

You can now complete the remaining steps to deploy a DAG using GitHub actions by either using this document or by following the instructions in the Cloud UI. On your Deployment page, click **Deploy your first DAG ... with GitHub Actions** to view the remaining instructions on the Deployment details page in the Cloud UI.

## Step 2: Retrieve credentials

When you use GitHub Actions to deploy DAGs to Astro, you need to provide GitHub with your **Deployment ID** and an **API Token** so that the workflow has a Deployment destination to send the DAG to and an API Token for authentication.

1. Copy your **Deployment ID** from the Deployment information on the **Deployment** page. 

2. Go to **Workspace settings > Access management** and then click **Workspace API Token**.

3. Enter the API Token name and choose the credentials permissions level. Then generate your token.

4. Leave this browser window open, so you can quickly access your API token in a later step.

## Step 3: Fork the example DAGs Repository

The example DAGs repository contains an _Astro Project_ which contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. 

In this tutorial, you'll be deploying these example DAGs to your Deployment on Astro with GitHub Actions.

1. Open a new tab or browser window and make a fork of the example DAGs Repository on [GitHub](https://github.com/astronomer/astro-example-dags/fork).

  :::info
  
  This repository contains an example Astro project that's similar to the project that `astro dev init` creates when you run your first DAG [with the CLI](create-first-dag.md).

  :::

## Step 4: Manually trigger the GitHub Actions

1. In GitHub, choose **Actions** from the repository menu.

2. Click **I understand my workflows, go ahead and enable them.**

  The [workflow](https://github.com/astronomer/astro-example-dags/blob/c2c63ced1923488d797ce0eba6b37f5658e92570/.github/workflows/deploy-to-astro.yaml) is a script that uses API tokens to deploy DAGs from a GitHub repository to your Deployment, without requiring any local development.

3. Choose **Astronomer CI - Deploy Code** workflow. 

4. Click **Run workflow**

4. Paste your **Deployment ID** from Step 1.

  You can also retrieve your Deployment ID from the Deployment page in the [Cloud UI](https://cloud.astronomer.io).

5. In the [Cloud UI](https://cloud.astronomer.io), Go to **Workspace settings > Access management** and then click **Workspace API Token**.

6. Copy the API Token and paste in the **API Token** field on your GitHub Actions workflow page.

7. Then click, **Run workflow**. 

This automatically deploys the DAGs in your forked repository to your Deployment worker queue. 

## Next Steps

- Install [the CLI](/astro/cli/install-cli.md)
- Develop your [Astro project](/astro/cli/run-airflow-locally)
- Read more about [Developing CI/CD workflows](set-up-ci-cd.md).
