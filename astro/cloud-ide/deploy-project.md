---
sidebar_label: Deploy a project
title: Deploy a project from the Cloud IDE to Astro
id: deploy-project
description: Learn how to use the Astro Cloud IDE's built-in GitHub support to manage your data pipelines and deploy them to Astro.
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in [Public Preview](feature-previews.md). If you have any feedback, submit it on the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

After you create a project in the Cloud IDE, you can deploy it to Astro and run tasks on a schedule using one of the following options:

- Download your pipelines' Python files from the Cloud IDE, copy them to an existing Astro project, and deploy your project to Astro.
- Use the Astro Cloud IDE's built-in GitHub integration to commit your project to a GitHub repository and deploy it to Astro using a GitHub action.

## Export your pipelines to a local Astro project

Astro Cloud IDE projects use the same structure as Astro projects created with the Astro CLI. You can download your pipeline code from the Astro Cloud IDE, copy it to an existing Astro project, and deploy that project to Astro using the [Astro CLI](cli/overview.md).

1. Create an Astro project. See [Create a project](create-project.md).
2. In the Cloud UI, select a Workspace and then click **Cloud IDE**.
3. Select the project you'd like to deploy.
4. Select a pipeline that you want to export.
5. Click **Code**, then click **Download**.

    ![Code screen and download button](/img/cloud-ide/download-code.png)

6. Add the downloaded Python file to the `dags` folder of your Astro project. 
7. Manually configure the connections, dependencies, and variables from your Astro Cloud IDE project in your local Astro project. Automatic exporting for these resources coming soon. 
8. Optional. Deploy your Astro project. See [Deploy code](deploy-code.md).

## Commit your project to GitHub

The Cloud IDE includes a robust GitHub integration for managing different versions and features of your Cloud IDE projects. Configuring GitHub is also the first step to deploying Cloud IDE project to Astro. Astronomer recommends one GitHub repository for every Cloud IDE project.

### Prerequisites 

- A Cloud IDE project. See the [Quickstart](/astro/cloud-ide/quickstart.md).
- A GitHub account with a personal access token. See [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

### Setup

1. In the Cloud UI, select a Workspace and then click **Cloud IDE**.
2. Select the project you'd like to deploy.
3. In the **GitHub Repo** pane, click **Configure**.
4. Configure the following values: 

    - **Personal Access Token**: Enter your personal access token. If you don't have an access token, follow the instructions to generate one.
    - **Repository**: Enter the name of your GitHub repository. The format is `<owner>/<repository>`.
    - **Default Branch**: Select the branch you want to commit your project to.
    - **Clone GitHub repo during cell execution**: Click the toggle to allow the Cloud IDE to access your GitHub repository files when executing an individual cell. Turn on this feature if you have cells that depend on helper files, such as helper functions in `include`.
    - **Disable auto sync in favor of manual sync**: When you click this toggle, a button appears in the pane that you can use to manually sync your GitHub repository to your Cloud IDE environment.

6. Click **Configure**.

After you configure a GitHub repository, you can use the **Commit** button in the Cloud IDE to commit your changes to your repository. 

1. Click **Commit**.
2. Select a branch type in the **Branch Type** list and then enter a name for the branch in the **Branch Name** field.
3. In the **Commit Message** field, enter a commit message. This is the commit message for changes committed  from the Astro Cloud IDE to GitHub.
4. Click **Commit**.

## Deploy a project from GitHub to Astro

On the first GitHub commit of your project, the Astro Cloud IDE automatically pushes a Github action to your repository that includes steps for deploying to Astro. You can then configure your GitHub repository to push your Astro Cloud IDE project to a Deployment when you commit to specific branches. 

You can commit changes from the Astro Cloud IDE to your GitHub repository without configuring Deployments in GitHub. However, you can't disable the GitHub action that the Astro Cloud IDE pushes to your repository. If you don't complete the following steps, the GitHub action fails, you can't deploy your changes to Astro, but the rest of your commit processes are successful.

:::caution

When the GitHub action first runs, it automatically enables DAG-only deploys on your Deployment. DAG-only deploys are a Public Preview feature that change how DAGs and configuration changes are pushed to the Deployment. See [Deploy DAGs only](deploy-code.md#deploy-dags-only).

:::

The following steps describe how to set up GitHub to run the default GitHub action, which assumes one `main` and one `dev` branch. You can modify these steps and the GitHub action to deploy to any number of differently named Deployments. 

### Prerequisites

- A Cloud IDE Project. See the [Quickstart](/astro/cloud-ide/quickstart.md).
- A GitHub account connected to your Cloud IDE project. See [Commit your project to GitHub](#commit-your-project-to-github).
- A Deployment on Astro. See [Create a Deployment](/astro/create-deployment.md).

### Step 1: Link your Deployments to GitHub

The default GitHub action provided by the Astro Cloud IDE will:

- Deploy your Cloud IDE project to your development Deployment when you commit to a `dev` branch.
- Deploy your Cloud IDE project to your production Deployment when you commit to a `main` branch.

These actions are not dependent on each other, meaning that you can modify the following steps to deploy only a single production or development Deployment. 

1. Identify a Deployment for production and a Deployment for development. Note the Deployment ID for each Deployment. To retrieve a Deployment ID, open your Deployment in the Cloud UI and copy the value in the **ID** section of the Deployment page.
2. Create a Deployment API key for your Deployments. See [Create an API key](api-keys.md#create-an-api-key). Note the API key and secret for each Deployment.
3. Configure the following GitHub secrets in your GitHub repository:
   
   - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-api-key-id>`
   - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-api-key-secret>`
   - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`
   - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-api-key-id>`
   - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-api-key-secret>`
   - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`

After configuring your Github actions, commits from the Cloud IDE to your `main` or `dev` branches are automatically deployed to Astro.

Astronomer recommends creating a feature branch for every new pipeline and creating a pull request (PR) with new changes that merge into the `dev` branch. Merging the PR triggers a push to your development Deployment, where you can confirm that your data pipeline is functional. When you confirm your changes, submit a pull request from your `dev` branch into `main`. This deploys your tested changes to your production Deployment.

### Step 2: Commit to Astro

After you configure a GitHub repository, the **Configure** button in the Cloud IDE updates to **Commit**. You can now commit your changes to your repository. You can also view the status of your repository and any changes that were committed from the Cloud IDE.

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
