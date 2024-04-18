---
title: 'Deploy code with the Astro GitHub integration'
id: deploy-github-integration
description: Learn how to automatically deploy Apache Airflow code to Astro from GitHub with a built-in integration.
unlisted: true
---

:::privatepreview
:::

Astronomer's built-in GitHub integration is the fastest way to implement CI/CD for Apache Airflow and deploy code to Astro. Astro’s automatic deploy system eliminates the need to implement GitHub Actions and gives you greater visibility into the code you’re running on Astro.

To deploy code through an integrated GitHub repository, you first connect a GitHub repository with your Astro project to an Astro Workspace. Then, you map a Git branch in that repository to an Astro Deployment. When a pull request is merged into your mapped branch, your code is automatically deployed to Astro.

Compared to deploying code manually using the Astro CLI or through a custom CI/CD process, using Astro’s GitHub integration:

- Allows you to enforce software development best practices without maintaining custom CI/CD scripts.
- Makes it easy for developers to iterate on DAG code quickly.
- Enables you to see Git metadata directly in the Astro UI, including Git commit descriptions.
- Gives you greater visibility into the status and detailed logs of an individual deploy.

## Best practices

To make the most out of the Astro GitHub integration, Astronomer recommends the following:

- Consider mapping long-lasting `main` and `dev` branches in GitHub to Deployments. For example, you would map a `main` branch to a production Deployment and your `dev` branch to your development Deployment. This approach is described in [Develop a CI/CD strategy](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- Run CI checks on your DAGs and project code as part of your pull request review process. There is currently no testing included in the default GitHub deploy process, so ensure that your DAG changes pass unit tests before they’re merged and deployed.
- Write descriptive commit messages or pull request descriptions for any project changes. These messages appear in the Astro UI under **Deploy History** to give your team more context about each deploy.

## Limitations

The Astro GitHub integration is not supported if any of the following are true:

- You build a custom Astro Runtime image as part of your deploy process. However, using the `-base` distribution of Astro Runtime is supported.
- You need to deploy images from an external or private Docker registry.
- You use the `--image-only` flag in the Astro CLI, or you need to exclude DAGs from specific deploys. This is usually the case if you have a multiple-repository deploy strategy as described in [Develop a CI/CD strategy](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-repositories).
- Your repository is hosted in an on-premises GitHub Enterprise server. To deploy code from an on-premises repository, see [Private network CI/CD templates](https://docs.astronomer.io/astro/ci-cd-templates/github-actions-private-network).
- There are currently no checks to prevent you from downgrading your version of Astro Runtime. Astronomer recommends only downgrading Deployments using [rollbacks](https://docs.astronomer.io/astro/deploy-history#roll-back-to-a-past-deploy).

There is currently no limit or additional charge for deploying code to Astro with the GitHub integration, but Astronomer might reach out to discuss your usage if you trigger an unusually large number of deploys.

## Prerequisites

- Workspace Admin permissions on an Astro Workspace.
- A GitHub repository that contains an [Astro project](https://docs.astronomer.io/astro/cli/develop-project#create-an-astro-project). The Astro project can exist at any level in your repository.
- A GitHub account with read and write permissions to the repositories containing your Astro project. If you don't have these permissions, send a request to your GitHub repository administrator when prompted by Astro.
- At least one Astro Deployment.
- At least one GitHub branch that you want to deploy to Astro.

## Connect a GitHub repository to a Workspace

Before you begin, ensure that you’re logged in to GitHub with permissions to read code from the repository where you want to deploy code.

1. In your Workspace, click **Workspace Settings** > **Git Deploys.**
2. Click **Install GitHub Application.** A window appears instructing you to authorize the **Astro App** on your personal GitHub account. Follow the prompts to authorize the application.
3. Return to the Astro UI. From the **Git Deploys** screen, click **Connect Repository**.
4. Select the Organization that contains the repository you want to integrate with Astro, then click **Continue**. A new window prompts you to allow **Astro App** to access either all repositories or specific repositories within your GitHub Organization. Astronomer recommends **Only selected repositories**.
5. Choose which repositories you want to enable the app for, then click **Request.**

    ![The GitHub authorization screen for connecting a repository to GitHub. GitHub requests for the Astro App to connect to at least one of your repositories](/img/docs/request-astro-app.png)

5. Configure the following fields:

    - **Repository:** Select the repository you want to integrate with Astro.
    - **Astro Project Path:** Specify the path to your Astro project, up to and including the Astro project folder. For example, `/myorg/myprojects/my-astro-project`

6. Click **Connect Repository**.
7. Map specific branches in your repository to Deployments in your Workspace. When you map a branch to a Deployment, any commits to that branch trigger a code deploy to Astro. For example, you can map a development branch and your production branch to separate Deployments so that bugs in development don’t affect your production data pipelines.

Any commits to your mapped branches will now trigger a code deploy to the corresponding Deployment.

## Deploy from GitHub to Astro

To deploy code from your GitHub repository to Astro, you can either:

- Make a direct commit to one of your mapped branches.
- Merge a pull request against one of our mapped branches.

Both of these actions triggers the Astro App to deploy your Astro project to the mapped Astro Deployment. When DAG-only deploys are enabled, your GitHub repository triggers:

- A DAG-only deploy if only your DAGs are changed. 
- A full project image deploy if you change a configuration in your project.

If DAG-only deploys are disabled, all code changes will trigger a full project image deploy. To learn more about DAG-only deploys, see [Deploy DAGs to Astro](deploy-dags.md).


You can check the status of your deploy in the Astro UI.

## Review code deploys from the Astro UI

When you trigger a code deploy by committing a change to one of your mapped branches, details about the code deploy appear in the Astro UI. For past and currently running deploys, you can review:

- Which user triggered the deploy.
- At what time the deploy was triggered.
- Which pull request or commit triggered the deploy. This includes the Git commit description and a link to your Pull Request if applicable.

![The deploy history screen in the Astro UI with a GitHub deploy listed. The entry includes the commit that triggered the deploy and shows it was triggered by "GitHub App"](/img/docs/github-deploy-history.png)

To review code deploys:

1. In the Astro UI, open your Deployment.
2. Click **Deploy History.**
3. Deploys triggered by the Astro App include a commit ID in their **Description** and are **Deployed By** the **GitHub App.** Click on a deploy triggered by the Astro App to see the logs for the deploy.

![The status of a specific deploy in the Astro UI. The deploy is currently running and generating logs.](/img/docs/deploy-status.png)

## How it works

The Astro GitHub integration works through an app that you install in your GitHub repository. The app is also authorized to act on behalf of your personal account so that it can see the GitHub repositories and branches you have access to.

### Deploys

When you make a commit or merge a pull request to a mapped branch in your repository, the GitHub app sends a push event to the Astro API. After the Astro API confirms that the push event should result in a deploy, your project code is sent to Deployment-specific workers on Astro that deploy the code to your Deployment.

If an additional deploy is triggered while a deploy is currently processing, Astro will terminate the first deploy and begin processing the second deploy. The first deploy will appear with a **Failed** state in your deploy history.

### Rollbacks

When you roll back a deploy created by the GitHub integration, Astro does not roll back the code in your GitHub repository. Therefore, rollbacks should only be used as a last resort due to the potential for your repository code to become out of sync with your deploy code.

If you do roll back a deploy, manually revert the code in your GitHub repository as soon as possible so that it matches the code running in your rolled back deploy. For more information, see [What happens during a rollback](https://docs.astronomer.io/astro/deploy-history#what-happens-during-a-deploy-rollback).