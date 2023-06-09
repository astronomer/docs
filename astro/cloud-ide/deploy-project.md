---
sidebar_label: Deploy a project
title: Deploy a project from the Cloud IDE to Astro
id: deploy-project
description: Learn how to use the Astro Cloud IDE's built-in GitHub support to manage your data pipelines and deploy them to Astro.
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in [Public Preview](feature-previews.md).

:::

After you create a project in the Cloud IDE, you can deploy it to Astro and run tasks on a schedule using one of the following options:

- Download your pipelines' Python files from the Cloud IDE, copy them to an existing Astro project, and deploy your project to Astro.
- Use the Astro Cloud IDE's built-in GitHub integration to commit your project to a GitHub repository and deploy it to Astro using a GitHub action.

## Export your pipelines to a local Astro project

Astro Cloud IDE projects use the same structure as Astro projects created with the Astro CLI. You can download your pipeline code from the Astro Cloud IDE, copy it to an existing Astro project, and deploy that project to Astro using the [Astro CLI](cli/overview.md).

1. Create an Astro project. See [Create a project](develop-project.md#create-an-astro-project).
2. In the Cloud UI, select a Workspace and then click **Cloud IDE**.
3. Select the project you'd like to deploy.
4. Select a pipeline that you want to export.
5. Click **Code**, then click **Download**.

    ![Code screen and download button](/img/cloud-ide/download-code.png)

6. Add the downloaded Python file to the `dags` folder of your Astro project. 
7. Manually configure the connections, dependencies, and variables from your Astro Cloud IDE project in your local Astro project. Automatic exporting for these resources coming soon. 
8. Optional. Deploy your Astro project. See [Deploy code](deploy-code.md).

## Commit your project to a Git repository

The Cloud IDE includes Git vendor integrations for managing different versions and features of your Cloud IDE projects. Configuring a Git repository is also the first step to deploying your Cloud IDE project to Astro. Astronomer recommends setting up a separate Git repository for every Cloud IDE project.

### Prerequisites 

- A Cloud IDE project. See the [Quickstart](/cloud-ide/quickstart.md#step-1-log-in-and-create-a-project).
- A Git repository hosted with a supported Git vendor. 
- A user account on your Git vendor with a personal access token (PAT). 

Your user account and PAT must have specific permissions depending on your Git vendor. See the following table to determine which permissions you need to configure for each supported Git vendor. 

| Git vendor                                                                                                                | PAT permissions                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) | <ul><li> [PAT scopes](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes): `repo` and `workflow`. `workflow` is optional for GitHub repositories that already have a [Cloud IDE GitHub action](#deploy-a-project-from-a-git-repository-to-astro). </li></ul>                   |
| [GitLab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)                                             | <ul><li> [User role](https://docs.gitlab.com/ee/user/permissions.html#project-members-permissions): `Developer` </li><li> [PAT scope](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-token-scopes): `api` </li></ul> |

### Connect your repository

1. In the Cloud UI, select a Workspace and then click **Cloud IDE**.
2. Select the project you'd like to deploy.
3. In the **Git Repo** pane, click **Configure**.
4. Configure the following values: 

    - **Git Vendor**: Select the Git vendor that hosts your repository. 
    - **Personal Access Token**: Enter your personal access token.
    - **Repository**: Enter the name of your Git repository. The format is `<owner>/<repository>`.
    - **Default Branch**: Select the branch you want to commit your project to.
    - **Clone GitHub/GitLab repo during cell execution**: Click the toggle to allow the Cloud IDE to access your Git repository files when executing an individual cell. Turn on this feature if you have cells that depend on helper files, such as helper functions in `include`.
    - **Disable auto sync in favor of manual sync**: When you click this toggle, a button appears in the pane that you can use to manually sync your Git repository to your Cloud IDE environment.

5. Click **Configure**.

### Commit to your repository

After you configure a Git repository, you can use the **Commit** button in the Cloud IDE to commit your changes to your repository. 

1. Click **Commit**.
2. Select a branch type in the **Branch Type** list and then enter a name for the branch in the **Branch Name** field.
3. In the **Commit Message** field, enter a commit message. This is the commit message for changes committed from the Astro Cloud IDE to your Git vendor.
4. Click **Commit**.

When you first make a commit to your repository, the Cloud IDE commits an additional workflow file that includes steps for pushing your code to Astro. You can then configure your GitHub repository to push your code to a Deployment whenever you commit to specific branches from the Astro Cloud IDE.

You can commit changes from the Astro Cloud IDE to your Git repository without configuring destination Deployments. However, if you don't configure any destination Deployments, the workflow fails and your changes aren't deployed to Astro. See [Deploy a project from a Git repository to Astro](#deploy-a-project-from-a-git-repository-to-astro) to learn how to deploy to Astro from the Astro Cloud IDE.

## Deploy a project from a Git repository to Astro

Follow these steps to deploy to Astro whenever you merge commits to a `main` or a `dev` branch on the Git repository hosting your Astro Cloud IDE project. You can modify these steps and the workflow to deploy to any number of Deployments from any number of branches.

:::caution

When the deploy workflow first runs from your repository, it automatically enables DAG-only deploys on your Deployment. DAG-only deploying is a feature that allows you to deploy your DAGs directory independently of the rest of your Astro project. See [Deploy DAGs only](deploy-code.md#deploy-dags-only).

:::

### Prerequisites

- A Cloud IDE Project. See the [Quickstart](/astro/cloud-ide/quickstart.md).
- A Git repository connected to your Cloud IDE project. See [Commit your project to a Git repository](#commit-your-project-to-a-git-repository).
- A Deployment on Astro. See [Create a Deployment](/astro/create-deployment.md).

### Step 1: Link your Deployments to your Git repository

The default workflow provided by the Astro Cloud IDE will:

- Deploy your Cloud IDE project to your development Deployment when you commit to a `dev` branch.
- Deploy your Cloud IDE project to your production Deployment when you commit to a `main` branch.

These actions are not dependent on each other, meaning that you can modify the following steps to deploy only a single production or development Deployment. 

1. Identify a Deployment for production and a Deployment for development. Note the Deployment ID for each Deployment. To retrieve a Deployment ID, open your Deployment in the Cloud UI and copy the value in the **ID** section of the Deployment page.
2. Create a Workspace or Organization API token for each of your Deployments. See [Create a Workspace API token](workspace-api-tokens.md) and [Create an Organization API token](organization-api-tokens.md). Note the API token for each Deployment.
3. Set the following environment variables in your Git repository as secrets:
   
    - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
    - `DEV_ASTRO_API_TOKEN`: The value for your development Workspace or Organization API token.

    See [GitHub](https://docs.github.com/en/actions/learn-github-actions/variables) and [GitLab](https://docs.gitlab.com/ee/ci/variables/) documentation on setting environment variables.  

After configuring your repository, commits from any source to your `main` or `dev` branches are automatically deployed to Astro.

Astronomer recommends creating a feature branch for every new pipeline and creating a pull request (PR) with new changes that merge into the `dev` branch. Merging the PR triggers a push to your development Deployment, where you can confirm that your data pipeline is functional. When you confirm your changes, submit a pull request from your `dev` branch into `main`. This deploys your tested changes to your production Deployment.

### Step 2: Commit to Astro

1. Open your project in the Astro Cloud IDE.
2. Click **Commit**.
3. In **BRANCH**, select a branch to commit to.
4. In **COMMIT MESSAGE**, enter a commit message. This will be the commit message for committing your changes from the Astro Cloud IDE to your Git repository.
5. Click **Commit**.

   ![Commit Changes](/img/cloud-ide/commit.png)

   Your changes are automatically pushed to your Git repository, then deployed from your repository to your configured Deployments.

6. Based on which branch you committed to, open the Deployment in the Cloud UI and click **Open Airflow** to confirm that your changes were successfully deployed.

:::tip

You can select or deselect files to commit by clicking on the checkbox next to the file name. Commits are made at the project level, so by default, all files in your project will be committed. You cannot currently commit a single pipeline without committing the rest of your project.

:::
