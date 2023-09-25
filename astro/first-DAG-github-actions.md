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

## Step 2: Fork the example DAGs Repository

The example DAGs repository contains an _Astro Project_ which contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. 

In this tutorial, you'll be deploying these example DAGs to your Deployment on Astro with GitHub Actions.

1. Open a new tab or browser window and make a fork of the example DAGs Repository on [GitHub](https://github.com/astronomer/astro-example-dags/fork).

  :::info
  
  This repository contains an example Astro project that's similar to the project that `astro dev init` creates when you run your first DAG [with the CLI](create-first-dag.md).

  :::

## Step 3: Set up the GitHub Actions Workflow

To enable GitHub to Deploy DAGs to your Astro workspace, you need to connect your Astro account with the workflow on GitHub. This means you need to have two browser windows open at the same time - one with the Cloud UI and one to your GitHub account.

1. Open the [Cloud UI](https://cloud.astronomer.io) to your Deployments page. Choose the Deployment where you want to deploy DAGs to. 

2. Open a new tab to the GitHub repository where you forked the example DAGs Repository.

3. In GitHub, choose **Actions** from the repository menu.

4. Click **I understand my workflows, go ahead and enable them.**

  The [workflow](https://github.com/astronomer/astro-example-dags/blob/c2c63ced1923488d797ce0eba6b37f5658e92570/.github/workflows/deploy-to-astro.yaml) is a script that uses API tokens to deploy DAGs from a GitHub repository to your Deployment, without requiring any local development.

5. Choose **Astronomer CI - Deploy Code** workflow. 

6. Click **Run workflow**. This opens a modal to enter your Astro Deployment information.

7. In the Cloud UI, copy your **Deployment ID** from the Deployment information. 

8. In GitHub, paste your **Deployment ID**.

9. On your **Deployment** page in the Cloud UI, click **API Tokens**.

10. Click **API Token** to create a new API Token, and then enter a **Name** and choose the **Expiration**.

11. Click **Create API Token** to make your new token.

  :::danger

  For security reasons, this is the only opportunity you have to copy your API token. After you exit the modal window, you cannot copy it again. Be sure to save your token in a safe place or paste it immediately.

  :::

12. Copy the API Token and paste in the **API Token** field on your GitHub Actions workflow page.

13. Then click, **Run workflow**. 

This automatically deploys the example DAGs to your Deployment.

## Step 4: Run your DAG in Airflow

1. On your **Deployments** page the Cloud UI, choose the Deployment where you deployed your DAGs. Then, click **Open in Airflow**.

2. **Unpause** the **S3** DAG and click **Run**. 

Congratulations! You deployed a DAG to your Astro Workspace using GitHub Actions!

## Next Steps

- Install [the CLI](/astro/cli/install-cli.md)
- Develop your [Astro project](/astro/cli/run-airflow-locally)
- Read more about [Developing CI/CD workflows](set-up-ci-cd.md).
