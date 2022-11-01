---
sidebar_label: Deploy to Astro
title: Deploy a project from the Astro Cloud IDE to Astro
id: deploy-project
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_ and it is available to all Astro customers. It is still in development and features and functionality are subject to change. Creating projects in the Cloud IDE does not affect running tasks on existing Deployments. If you have feedback on the Cloud IDE you'd like to share, you can submit it on the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

After you've created a pipeline in the Cloud IDE, you can deploy it to Astro as part of your Cloud IDE project and run tasks using an existing schedule. To deploy a pipeline from the Cloud IDE, you first push the pipeline to a GitHub repository and then you deploy it to Astro using the CI/CD script included with the Cloud IDE.

## Prerequisites

- A Project. For instructions on how to create a Project, see the [Quickstart](/astro/cloud-ide/quickstart.md).
- At least one Deployment on Astro. For instructions on how to create a Deployment, see the [Create a Deployment](/astro/create-deployment.md) guide.
- A GitHub account with a personal access token. See [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Step 1: Link your Cloud IDE project to GitHub

To deploy your pipeline and Cloud IDE project to Astro, you first need to link your Cloud IDE project to a GitHub repository. Astronomer recommends one GitHub repository for every Cloud IDE project.

1. In the Cloud UI, select a Workspace and then click **Cloud IDE** in the left menu.
2. Select the Project you'd like to deploy.
3. Click **Configure**.
4. Enter your GitHub Personal Access Token and click **Update**.
5. Enter your GitHub repository information.
6. Click **Update**.

After you configure a GitHub repository, you can start committing changes from the Astro Cloud IDE to the repository.

1. Click **Commit**.
2. Click **New Branch**, then choose from either an existing branch or create a new branch.
3. In the **COMMIT MESSAGE** field, enter a commit message. This will be the commit message for committing your changes from the Astro Cloud IDE to GitHub.
4. Click **Commit**.

## Step 2: Link your Deployments to GitHub

On your first commit, the Astro Cloud IDE will automatically push a Github Actions workflow to your repository that includes steps for deploying to Astro. Currently, the GitHub action will:

- Deploy your Cloud IDE project to your development Deployment when you commit to a `dev` branch.
- Deploy your Cloud IDE project to your production Deployment when you commit to a `main` branch.

Astronomer recommends creating a feature branch for every new pipeline and creating a pull request (PR) with new changes that merge into the `dev` branch. Merging the PR triggers a push to your development Deployment, where you can confirm that your data pipeline is functional. When you confirm your changes, submit a pull request from your `dev` branch into `main`. This deploys your tested changes to your production Deployment.

You can commit changes from the Astro Cloud IDE to your GitHub repository without configuring Deployments in GitHub. However, there is currently no way to disable the GitHub Action that the Astro Cloud IDE pushes to your repository. If you don't complete the following steps, the GitHub Action fails and you can't deploy your changes to Astro, but the rest of your commit processes are successful.

1. Identify a Deployment for production and a Deployment for development. Note the Deployment ID for each Deployment. The Deployment ID can be found in the URL when you select a Deployment in the Cloud UI. For example, if your Deployment URL is `https://cloud.astronomer.io/cku7t3fvx59046554xr4g0siv7r/deployments/cl9redx5196158bqytlww0mqz2/analytics`, the Deployment ID is `cl9redx5196158bqytlww0mqz2`.
2. Create a Deployment API key for your production and development Deployments. See [Create an API key](api-keys.md#create-an-api-key). Note the API key and secret for each Deployment.
3. Create the following GitHub secrets in your GitHub repository:
   - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-api-key-id>`
   - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-api-key-secret>`
   - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`
   - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-api-key-id>`
   - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-api-key-secret>`
   - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`

After configuring your Github actions, commits from the Cloud IDE to your `main` or `dev` branches are automatically deployed to Astro.

## Step 3: Commit to Astro

After you've configured a GitHub repository, the **Configure** button in the Cloud IDE updates to **Commit**. You can now commit your changes to your repository. You can also view the status of your repository and any changes that were committed from the Cloud IDE.

1. Open your project in the Astro Cloud IDE.
2. Click **Commit**.
3. In **BRANCH**, select a branch to commit to.
4. In **COMMIT MESSAGE**, enter a commit message. This will be the commit message for committing your changes from the Astro Cloud IDE to GitHub.
5. Click **Commit**

   ![Commit Changes](/img/cloud-ide/commit.png)

   Your changes are automatically pushed to GitHub, then pushed to your configured Deployments.

6. Open your Deployments in the Cloud UI and click **Open Airflow** to confirm that your changes were successfully deployed.

:::tip

You can select or deselect files to commit by clicking on the checkbox next to the file name. Commits are made at the project level, so by default, all files in your project will be committed. You cannot currently commit a single pipeline without committing the rest of your project.

:::
