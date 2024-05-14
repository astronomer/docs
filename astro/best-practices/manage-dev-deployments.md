---
title: 'Manage development Deployments on Astro'
sidebar_label: 'Manage dev Deployments'
id: manage-dev-deployments
---

For most teams working on Astro, Astronomer recommends using multiple Airflow Deployments for running and testing development and production versions of your pipelines, and promoting code between them using CI/CD. This allows you to develop your pipelines faster, more securely, and more reliably.

There are many strategies for organizing your code, CI/CD pipelines, and Deployments to support a sustainable development lifecycle on Astro, and no single setup will work for every team. However, there are a few frequently used methods for managing your development Deployments and promoting code from development to production when working on Astro:

1. Maintain a permanent development Deployment with a hibernation schedule that contains the code from a permanent `dev` branch of your project repository.
2. Create ephemeral Deployments that map to feature branches in your repository, that are deleted when the feature branch is merged into production. 

In this guide, we cover how to choose which method is best for your team and how to implement both using Astro features.

## Feature overview

This guide highlights when to use the following Astro features to manage your Deployments:

- Branch-based, or multi-branch Deployments using [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- [Hibernating development Deployments](https://domanagecs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).

## Best practice guidance

### Single environments

Smaller teams that can tolerate testing and applying bug fixes in production will likely find that a [Single environment](https://docs.astronomer.io/astro/set-up-ci-cd#single-environment) will meet their needs. To use a single environment, deploy from a single, permanent branch to a single Astro Deployment using CI/CD. If the GitHub integration is used, changes to the branch are deployed automatically on Astro and available in the Airflow UI. An advantage of this approach is that it is the most cost-effective way to manage Deployments on Astro. A disadvantage, especially for teams with business-critical DAGs, is that you lack the ability to test changes on Astro prior to deploying to production.

### Multiple environments

Larger teams and teams with business-critical DAGs will likely prefer to maintain [Multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments) and deploy separate development and production versions of their pipelines to Astro. The GitHub integration supports automated deployment from multiple permanent branches of the same GitHub repository in a single Astro Workspace. An advantage of this approach is that you can test multiple versions of your DAGs on Astro before deploying to production. A disadvantage is that each additional Deployment adds to the cost of infrastructure for your pipelines.

:::tip

[Hibernating development Deployments](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment) reduces the cost of maintaining multiple permanent Deployments.

:::

### A hybrid approach

Some teams might prefer some combination of the above. For example, some teams might prefer to use ephemeral Deployments for production code rather than maintain a permanent production Deployment. Other teams might choose to maintain permanent sandbox Deployments in addition to development and production Deployments.



## Hibernating development Deployment example

This example shows how to implement a permanent development Deployment with a hibernation schedule and a CI/CD pipeline to promote code from development to production.

### Prerequisites

To implement this example, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- A CI/CD tool.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a git repository.

However, you can extend this example to encompass any number of Astro Deployments.

### Implementation

To implement this example:

1. Create a new development Deployment. Make sure **Development Mode** is enabled when you create the Deployment. See [Create a Deployment](https://docs.astronomer.io/astro/create-deployment).
2. Create a hibernation schedule for your development Deployment. Choose a schedule that will not interfere with your typical development times. Note that you cannot deploy to a Deployment that is hibernating. See [Hibernate a development Deployment](https://docs.astronomer.io/astro/deployment-resources#hibernate-a-development-deployment).
3. Implement a branch-based CI/CD pipeline. Your pipeline should deploy the `dev` branch of your project repository to the development Deployment you created on a push to that branch, and deploy the `main` branch of your repository to your production Deployment on a merge to that branch. See [Develop a CI/CD workflow for multiple environments](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).

## Ephemeral feature Deployment example

This example shows how to implement ephemeral Deployments for feature development that are created and destroyed by CI/CD.

### Prerequisites

To implement this example, you need:

- One [Astro Deployment](https://docs.astronomer.io/astro/create-deployment) for production.
- A CI/CD tool.
- One [Astro project](https://docs.astronomer.io/astro/cli/develop-project) in a git repository.

However, you can extend this example to encompass any number of Astro Deployments.

### Implementation

To implement this example:

1. 


## See also

- [Manage Astro connections in branch-based deploy workflows](connections-branch-deploys.md)
