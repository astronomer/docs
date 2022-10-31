---
sidebar_label: Deploy to Astro
title: Deploy a project from the Astro Cloud IDE to Astro
id: deploy-project
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_. This means that it is available to all Astro customers, but is still undergoing heavy development and features are subject to change. Using the Cloud IDE has no impact to your Deployments or pipelines running in production. If you have any feedback, please submit it to the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

Once you've created a pipeline and configured the schedule, you're ready to deploy your project and run it on your specified schedule. To deploy a pipeline from the Cloud IDE, you must first push the pipeline to a GitHub repository and then deploy it using CI/CD.

## Prerequisites

- Two Deployments on Astro, one for production deploys and one for development deploys. See [Create a Deployment](/astro/create-deployment.md).
- A GitHub account with a personal access token. See [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Step 1: Link your Cloud IDE project to GitHub

To deploy your pipeline to Airflow, you'll need to link your Cloud IDE project to a GitHub repository.

1. Open your project in the Astro Cloud IDE. 
2. Click **Configure**.
3. Enter your GitHub repository information.
4. Click **Update**. 

After you configure a GitHub repository, you can start committing changes from the Astro Cloud IDE to the repository.

1. Click **Configure**.
2. Click **New Branch**, then choose from either an existing branch or create a new branch.
3. In the **COMMIT MESSAGE** field, enter a commit message. This will be the commit message for committing your changes from the Astro Cloud IDE to GitHub.
4. Click **Commit**

## Step 2: Link your GitHub repository to Astro

The Astro Cloud IDE will automatically push a Github Actions workflow to your repository that includes steps for deploying to Astro. Currently, the GitHub action will:

- Push code to an configured production Deployment whenever you commit to a `main` branch.
- Push code to an configured development Deployment whenever you commit to a `dev` branch.

Astronomer recommends creating a feature branch, PRing those changes into the `dev` branch, confirming the changes are functional in a dev environment, then PRing the dev branch into the main branch.

To make this GitHub action work: 

1. Identify a Deployment for production deploys and a Deployment for development deploys. Note the Deployment ID for both Deployments.
2. Create a Deployment API key in each Deployment. See [Manage Deployment API keys](api-keys.md). Note the API key and secret for both API keys.
3. Create the following GitHub secrets in your GitHub repository: 
    - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
    - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
    - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`
    - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
    - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
    - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`

After configuring your Github actions, your commits from the Astro Cloud IDE to your `main` or `dev` branches will be automatically deployed to Astro.

If you skip these steps, the GitHub action will fail. However, you can still commit changes from the Astro Cloud IDE to GitHub without configuring Deployments. 


## Step 3: Push to Astro

Once you've configured a repository, the **Configure** button changes to **Commit**. This tab allows you to commit your changes to your repository. You can also view the status of your repository and any changes that were committed from the Astro Cloud IDE. To commit your changes:

1. Open your project in the Astro Cloud IDE. 
2. Click **Commit**.
3. In **BRANCH**, select a branch to commit to.
4. In **COMMIT MESSAGE**, enter a commit message. This will be the commit message for committing your changes from the Astro Cloud IDE to GitHub.
5. Click **Commit**

![Commit Changes](/img/cloud-ide/commit.png)

Your changes are automatically pushed to GitHub, then pushed to your configured Deployments. To confirm that the changes were applied, open your Deployments in the Cloud UI and click **Open Airflow**. 
   
:::tip

You can select/deselect files to commit by clicking on the checkbox next to the file name. Commits are made at the project level, so by default, all files in your project will be committed.

:::

