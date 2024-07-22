---
sidebar_label: 'When Signing Up for Astro'
title: 'Run your first DAG on Astro'
id: 'first-dag-github-actions'
description: "Learn how to run your first Apache Airflow® DAG on Astro when you sign up for Astro."
---

Astro is the industry's leading managed service for [Apache Airflow®](https://airflow.apache.org/). To quickly learn how Astro works, follow the steps in this quickstart to create an Airflow environment and run your first DAG.

When you first sign up for Astro, you can choose to

## Step 1: Tailor your Astro experience

Based on how you plan to use Astro, you can find more resources for particular topics relevant to your needs.

- **Business** or **Personal** use
- Familiarity with Apache Airflow
- Use cases, including:
    - AI/ML
    - Business Operations
    - Reporting and Analytics
    - Extract, transform, and loading operations (ETL)
    - Other

## Step 2: Create your Oganization and Workspace

Enter a name for your Organization and Workspace. These can be changed later in the Astro UI.

## Step 3: Select a template

You can choose a template Astro project that shows a demonstration of particular scenarios.

- **Generative AI**: Airflow is a common orchestration engines for AI/Machine Learning jobs, especially for retrieval-augmented generation (RAG).This [generative AI project](https://github.com/astronomer/templates/blob/main/generative-ai/README.md) shows an simple example of building vector embeddings for text and then performing a semantic search on the embeddings.
- **ETL**: Use a template to make an example [ETL pipeline](https://github.com/astronomer/templates/blob/main/etl/README.md). This template shows an example pattern for defining an ETL workload using DuckDB as the data warehouse of choice.
- **Learning Airflow**: This example project is generated when you run 'astro dev init' using the Astro CLI. It shows a basic Astro project with Airflow components and DAGs.
- **None**: This option allows you to manually deploy a project after making a Deployment. See [Deploy code with GitHub](deploy-github-integration.md) to use a GitHub connection with an existing project in a repo. Or, you can choose to manually build and Deploy an example DAG by following the steps in [Run your first DAG with the Astro CLI](first-dag-cli.md) or [Run your first DAG with GitHub Actions](first-dag-github-actions.md).

## Step 4: Set up your Astro Deployment

You can now confirm your selected template and finish configuring your Deployment resources and whether you want to use a GitHub connection for code deploys.

- **Selected template**: When you finalize your Deployment, you can confirm or change the template option you selected in Step 3.
- **Git connection**: Enter your **GitHub Owner** and **Repository Owner** information to deploy code directly to an Astro Deployment when you merge changes to a specific branch. If you choose to skip connecting to GitHub, later, you can return and manually build and Deploy an example DAG by following the steps in [Run your first DAG with the Astro CLI](first-dag-cli.md) or [Run your first DAG with GitHub Actions](first-dag-github-actions.md).
- **Review Deployment**: Enter a **Name** for your Deployment and choose the **Provider** that you want to use and **Region** where you'd like to host your resources.

After you finish configuring your Deployment, click **Create your Project Repository and Deploy to Astro**.

## Step 5: Explore Astro

When you create your project and deploy it to Astro, it automatically creates a new Deployment on Astro, and also makes a private GitHub repository in your account with the template that you selected.

Click **Deployments** and then choose your active Deployment to view details about it.

If you click **Deploy History**, you can see when your code successfully deploys from your GitHub repository. After your deploy is successful, you can click **Open Airflow** to view and run your DAGs.



