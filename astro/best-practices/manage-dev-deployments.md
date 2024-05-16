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

This guide does not provide detailed guidance on how to set up code repositories such as GitHub or how to configure and manage CI/CD workflows. Consult the documentation for your organization's tooling for specific and up-to-date guidance.

:::

## Feature overview

This guide highlights when to use the following Astro features to manage your Deployments:

- Branch-based, including multi-branch, Deployments using [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- [Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).
- Astro's [GitHub integration](https://docs.astronomer.io/astro/deploy-github-integration).

## Best practice guidance

### Permanent dev deployment

Follow the guidance in [Deploy code with GitHub](https://docs.astronomer.io/astro/deploy-github-integration) to map a permanent development branch on GitHub to a permanent Astro Deployment. Generally speaking, maintaining [Multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments) for separate development and production versions of pipelines on Astro is a best practice, and Astro's GitHub integration makes it easy to do this with one of the most widely-used version control platforms. The integration supports automated deployment from multiple permanent branches of the same GitHub repository in a single Workspace, so your main and dev branches on GitHub can share a Workspace on Astro. 

Advantages of this approach:
- You can test multiple versions of your DAGs _on Astro_ before deploying to production (by merging your dev and prod branches on GitHub, for example). 

Disadvantages of this approach:
- Each additional Deployment adds to the cost of infrastructure for your pipelines.

:::tip

[Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment) reduces the cost of maintaining multiple permanent Deployments.

::: 

### Ephemeral feature-based dev Deployments

Some teams might prefer to configure CI/CD workflows to spin up individual Deployments for feature testing in place of (or in addition to) a permanent dev Deployment. 

Advantages of this approach:
- Much more flexibility in configuring Deployments for feature testing.
- Automated deployment of projects means less time spent managing environments on Astro. 

Disadvantages of this approach:
- Automation of ephemeral Deployments potentially makes the cost of your infrastructure hard to control. 
- Configuration of CI/CD workflows to automate the deployment process is a more involved process than setting up the GitHub integration.

### A hybrid approach

Some teams might prefer some combination of the above. For example, some teams might prefer to use ephemeral Deployments for production code rather than maintain a permanent production Deployment. Other teams might choose to maintain permanent sandbox Deployments in addition to development and production Deployments.

## Hibernating development Deployment example

This example shows how to implement a permanent development Deployment with a hibernation schedule mapped to a permanent branch on GitHub.

### Prerequisites

To implement this example, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a GitHub repository.

:::note

You can extend this example to encompass any number of Astro Deployments.

:::

### Implementation

To implement this example:

1. Create a new development Deployment. Make sure **Development Mode** is enabled when you create the Deployment. See [Create a Deployment](https://docs.astronomer.io/astro/create-deployment).
2. Create a hibernation schedule for your development Deployment. Choose a schedule that will not interfere with your typical development times. Note that you cannot deploy to a Deployment that is hibernating. See [Hibernate a development Deployment](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).
3. Implement a branch-based . Your pipeline should deploy the `dev` branch of your project repository to the development Deployment you created on a push to that branch, and deploy the `main` branch of your repository to your production Deployment on a merge to that branch. See [Develop a CI/CD workflow for multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).

## Ephemeral feature Deployment example

This example shows how to implement ephemeral Deployments for feature development that are created and destroyed by CI/CD.

### Prerequisites

To implement this example, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- A GitHub repository
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a git repository.

However, you can extend this example to encompass any number of Astro Deployments.

### Implementation

To implement this example:

1. 


## See also

- [Manage Astro connections in branch-based deploy workflows](connections-branch-deploys.md)
