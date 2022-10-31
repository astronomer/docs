---
sidebar_label: Deploying your pipeline
title: Deploying your pipeline
id: deploying
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_. This means that it is available to all Astro customers, but is still undergoing heavy development and features are subject to change. Using the Cloud IDE has no impact to your deployments or pipelines running in production. If you have any feedback, please submit it [here](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

Once you've created your pipeline and configured the schedule, you're ready to deploy it! Deploying a pipeline means that it will be scheduled to run at the specified interval. Currently, to deploy a pipeline from the Cloud IDE, you must first check the pipeline into a Git repository and then deploy it using CI/CD.

### Prerequisites

- An Airflow deployment. If you don't have one, you can create one by following the [Create Deployment Guide](/astro/create-deployment.md).
- A GitHub account

### Linking your Cloud IDE Project to GitHub

To deploy your pipeline to Airflow, you'll need to link your Cloud IDE project to a GitHub repository. To do so, click on the commit icon in the top right corner of the screen. Before configuring a GitHub repository, you'll see a configure tab to enter your GitHub credentials and select a repository.

![Configure GitHub](/img/cloud-ide/no-github-pat.png)

Here, you'll need to enter your [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). This token is used to authenticate with GitHub and give the Cloud IDE access to your repositories. Follow the instructions in the link above to create a token. Once you've created a token, copy it and paste it into the **Personal Access Token** field. Then, click **Update** next to the field. Your token will be saved and cleared from the field for security reasons.

After you've entered and saved your Personal Access Token, you can configure a repository. We recommend starting with a new repository. A repository is required to have a branch - the Cloud IDE does not create one for you. You can create a new repository [from GitHub](https://github.com/new). To initialize the repository with a branch, select the _Add a README file_ option. Once you've created a repository, enter the organization and repository name in the Cloud IDE and click **Update**.

### Linking your GitHub repository to your Airflow deployment

Build comes with a standard Github action workflow to push your updates to upstream Airflow deployments. Current behavior includes:

- Commits to `main` branch pushes code to an upstream configured production deployment
- Commits to `dev` branch pushes code to an upstream configured development deployment
- Commits to other branches do nothing

Our recommended workflow includes creating a feature branch, PRing those changes into the `dev` branch, confirming the changes are functional in a dev environment, then PRing the dev branch into the main branch.

All you need to do is configure deployment API keys for your Airflow deployment and enter them in GitHub Actions Secrets. To generate API keys, follow the instructions in our [Deployment API keys](/astro/api-keys.md) section. You can link your deployment by entering the following secrets in the GitHub repository settings:

- Production Airflow:
  - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
  - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
  - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`
- Development Airflow:
  - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
  - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
  - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`

Note that not configuring a development or production Airflow deployment will result in failed actions but will still allow commits, so this is all optional.

After configuring your Github actions, your new changes from Build will be properly deployed to upstream Airflow instances!

### Committing your changes

Once you've configured a repository, you'll see a commit tab. This tab allows you to commit your changes to your repository. You can also view the status of your repository and any changes that have been made. To commit your changes, enter a commit message and click **Commit**. Your changes will be committed to your repository.

:::tip

You can select/deselect files to commit by clicking on the checkbox next to the file name. Commits are made at the project level, so by default, all files in your project will be committed.

:::

![Commit Changes](/img/cloud-ide/commit.png)

You can select the branch you'd like to commit to. By default, the branch will be set to `main`. If you'd like to commit to a different branch, select the branch from options at the top. You can also create a new branch by clicking **New Branch**. This will create a new branch with the name you enter and commit your changes to that branch.

### Verifying your deployment

Once you've committed your changes, you can check the progress of your deployment by checking the GitHub Actions tab on your repository. Once your GitHub Actions have completed, you can check the status of your deployment by navigating to the deployment page in the Astro UI. Once your deployment is complete, you'll see your latest changes in the Astro and Airflow UIs!
