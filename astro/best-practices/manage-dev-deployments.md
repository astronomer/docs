---
title: 'Manage development Deployments on Astro'
sidebar_label: 'Manage dev Deployments'
id: manage-dev-deployments
---

For most teams working on Astro, Astronomer recommends using multiple Airflow Deployments for running and testing development and production versions of your pipelines, and promoting code between them using CI/CD. This allows you to develop your pipelines faster, more securely, and more reliably.

There are many strategies for organizing your code, CI/CD pipelines, and Deployments to support a sustainable development lifecycle on Astro, and no single setup will work for every team. However, there are a few frequently used methods for managing your development Deployments and promoting code from development to production when working on Astro:

1. Maintain a permanent development Deployment with a hibernation schedule that contains the code from a permanent `dev` branch of your project repository on GitHub or another version control platform.
2. Configure CI/CD workflows to create preview Deployments that map to feature branches in your repository that are deleted when the feature branch is merged into production. 

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

Maintaining [multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments) for separate development and production versions of pipelines on Astro is a best practice. While there are many ways to do this, the two options covered in this guide, permanent dev Deployment with hibernation schedule or ephemeral preview Deployments mapped to feature branches, will work for most teams.

In general, preview Deployments offer a better development experience. Since each feature branch maps to its own Astro Deployment, you don't have to worry about conflicts from other developers working on a development branch at the same time. If you have larger teams working on Astro or deploy changes frequently, this is a good option. However, managing development Deployments in this way requires more setup to ensure the Deployments have access to external systems, secrets, etc. and a more complex CI/CD implementation.  Your team should have experience with CI/CD to make this pattern successful. Finally, this option can come with less predictable costs, especially at higher scale with many feature Deployments that are spun up and down frequently.

Permanent dev Deployments are easier to set up and manage. You only need to set up the environment once, and for GitHub users Astro's GitHub integration offers far simpler CI/CD implementation. In many cases, this pattern is also more cost-effective, as you can maintain one dev Deployment and use Astro's hibernation feature to reduce costs for the Deployment when you aren't using it. This option is often best for smaller teams, teams that deploy infrequently, and teams who are very cost conscious. 

:::tip

[Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment) reduce the cost of maintaining multiple permanent Deployments.

:::

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

## Ephemeral preview Deployment example

This example shows how to implement ephemeral Deployments for feature development that are created and destroyed by CI/CD.

### Prerequisites

For implementation, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- A CI/CD tool such as GitHub Actions, Jenkins, or CircleCI.
- A version control tool such as GitHub or GitLab.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a Git repository.
- [Deployment API tokens](https://docs.astronomer.io/astro/deployment-api-tokens) to automate your code deploys.

:::note

You can extend this example to encompass any number of Astro Deployments.

:::

### Implementation

1. Obtain an API token in the Astro UI. See [Create an API token](https://docs.astronomer.io/astro/automation-authentication#step-1-create-an-api-token).
2. Install the Astro CLI in your CI/CD tool. See [Authenticate an automation tool to Astro](https://docs.astronomer.io/astro/automation-authentication#step-2-install-the-astro-cli-in-your-automation-tool).
3. Create a CI/CD pipeline using a [GitHub Actions template](https://docs.astronomer.io/astro/ci-cd-templates/github-actions-deployment-preview) or, if using a different CI/CD tool, [shell scripts](https://docs.astronomer.io/astro/ci-cd-templates/template-overview#preview-deployment-templates) that contain logic for managing preview Deployments based on branches. These workflows require at least an Astro Deployment name or ID and a branch name. See [Create a CI/CD pipeline](https://docs.astronomer.io/astro/set-up-ci-cd#create-a-cicd-pipeline) and [Template options](https://docs.astronomer.io/astro/ci-cd-templates/template-overview#preview-deployment-templates).

:::tip

Business-tier uses can add an additional layer of security by enforcing CI/CD for deploys rather than allowing manual deploys with the Astro CLI. See [Enforce CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#enforce-cicd).

:::


## See also

- [Manage Astro connections in branch-based deploy workflows](connections-branch-deploys.md)
