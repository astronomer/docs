---
title: 'Manage development Deployments on Astro'
sidebar_label: 'Manage dev Deployments'
id: manage-dev-deployments
---

For most teams working on Astro, Astronomer recommends using multiple Airflow Deployments for running and testing development and production versions of your pipelines, and promoting code between them using CI/CD. This allows you to develop your pipelines faster, more securely, and more reliably.

There are many strategies for organizing your code, CI/CD pipelines, and Deployments to support a sustainable development lifecycle on Astro, and no single setup will work for every team. However, there are a few frequently used methods for managing your development Deployments and promoting code from development to production when working on Astro:

1. Maintain a permanent development Deployment with a hibernation schedule that contains the code from a permanent `dev` branch of your project repository on GitHub or another version control platform.
2. Configure CI/CD workflows to create ephemeral Deployments that map to feature branches in your repository that are deleted when the feature branch is merged into production. 

In this guide, we cover how to choose which method is best for your team and how to implement both using Astro features.

:::note

This guide does not provide detailed guidance on how to set up code repositories such as GitHub or how to configure CI/CD tools. Consult the documentation for your organization's tooling for specific and up-to-date guidance.

:::

## Feature overview

This guide highlights when to use the following Astro features to manage your Deployments:

- Astro's [GitHub integration](https://docs.astronomer.io/astro/deploy-github-integration).
- [Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).
- Branch-based, including multi-branch, Deployments using [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).


## Best practice guidance

### Permanent dev deployment

We recommend multiple environments to allow running and testing of multiple versions of your project. You can follow the guidance in [Deploy code with GitHub](https://docs.astronomer.io/astro/deploy-github-integration) to map a permanent development branch on GitHub to a permanent Astro Deployment. Generally speaking, maintaining [Multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments) for separate development and production versions of pipelines on Astro is a best practice, and Astro's GitHub integration makes it easy to do this with one of the most widely-used version control platforms. The integration supports automated deployment from multiple permanent branches of the same GitHub repository in a single Workspace, so your main and dev branches on GitHub can share an environment on Astro. 

Advantages of this approach:
- You can test multiple versions of your DAGs _on Astro_ before deploying to production.
- You can ensure that all changes to your Astro project are reviewed and approved by your team before they get pushed to Astro.
- Compared to creating a Deployment for each team member, a single dev Deployment can reduce the cost of infrastructure for your team.
- You don't have to run `astro deploy` every time you make a change to your Astro project.
- Mapping GitHub repository branches to Astro Deployments is _very_ easy to do and requires neither coding nor configuration on GitHub. 

A disadvantage of this approach:
- Sharing a single Deployment increases the complexity of managing code contributions and makes it possible for team members to accidentally overwrite one another's changes.

:::tip

[Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment) reduces the cost of maintaining multiple permanent Deployments.

::: 

### Ephemeral feature-based dev Deployments

Some teams might prefer to configure [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments) workflows to spin up individual Deployments for feature testing in place of (or in addition to) a permanent dev Deployment. 

Advantages of this approach:
- As with the GitHub integration, you can ensure that all changes to your Astro project are reviewed and approved by your team before they get pushed to Astro.
- As with GitHub, with branch-based deployment you have flexibility in configuring individual Deployments for testing.
- Automated deployment of projects means less time spent managing environments.
- You don't have to run `astro deploy` every time you make a change to your Astro project.
- You can automate promotion of code across development and production environments on Astro when pull requests to certain branches are merged.
- You can enforce automated testing, which improves code quality and allows your team to respond quickly in case of an error or failure.

Disadvantages of this approach:
- Automation of ephemeral Deployments potentially makes the cost of your infrastructure hard to predict and control. 
- Configuration of CI/CD workflows for automated deployment on Astro is a more involved process than setting up the GitHub integration.

### A hybrid approach

Some teams might prefer some combination of the above. For example, some teams might prefer to use ephemeral Deployments for production code rather than maintain a permanent production Deployment. Other teams might choose to maintain permanent sandbox Deployments in addition to development and production Deployments.

## Hibernating development Deployment example

This example shows you how to implement a permanent development Deployment with a hibernation schedule mapped to a permanent branch on GitHub. If your team does not use GitHub, you can also implement a branch-based hibernating development Deployment using [CI/CD workflows](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).

### Prerequisites

You will need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a GitHub repository.

:::note

You can extend this example to encompass any number of Astro Deployments.

:::

### Implementation

1. Create a new development Deployment. Make sure **Development Mode** is enabled when you create the Deployment. See [Create a Deployment](https://docs.astronomer.io/astro/create-deployment).
2. Create a hibernation schedule for your development Deployment. Choose a schedule that will not interfere with your typical development times. Note that you cannot deploy to a Deployment that is hibernating. See [Hibernate a development Deployment](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).
3. Configure branch-based deployment using the GitHub integration, mapping one branch of a GitHub repository to the development Deployment you created. See [Deploy code with the Astro GitHub integration](https://docs.astronomer.io/astro/deploy-github-integration).

## Ephemeral feature Deployment example

This example shows how to implement ephemeral Deployments for feature development that are created and destroyed by CI/CD.

### Prerequisites

To implement this example, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- A CI/CD tool such as GitHub Actions, Jenkins, or CircleCI.
- A version control tool such as GitHub or GitLab.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a Git repository.
- [Deployment API tokens](https://docs.astronomer.io/astro/deployment-api-tokens) to automate your code deploys.

:::note

You can extend this example to encompass any number of Astro Deployments.

:::

### Implementation

1. Obtain an API token in the Astro UI and install the Astro CLI in your CI/CD tool. See [Authenticate an automation tool to Astro](https://docs.astronomer.io/astro/automation-authentication).
2. Choose a deployment strategy. We recommend multiple environments. See [Develop a CI/CD workflow for multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
3. Create a CI/CD pipeline using a template. See [Create a CI/CD pipeline](https://docs.astronomer.io/astro/set-up-ci-cd#create-a-cicd-pipeline).
4. Enforce CI/CD to ensure a standardized and observable deployment process rather than allow manual deploys with the Astro CLI. See [Enforce CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#enforce-cicd).
5. Add testing to your pipeline. We recommend using [pytests](https://docs.astronomer.io/astro/set-up-ci-cd#test-and-validate-dags-in-your-cicd-pipeline).


## See also

- [Manage Astro connections in branch-based deploy workflows](connections-branch-deploys.md)
