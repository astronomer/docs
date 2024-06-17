---
title: 'Organizing code for CI/CD'
sidebar_label: 'Organizing code for CI/CD'
id: repo-structure
---

Astro supports a range of options when it comes to organizing your project code and setting up Continuous Integration and Continuous Delivery (CI/CD) pipelines for automated deploys to Astro. 

Astronomer recommends considering the pros and cons of each option, along with the needs of your team and structure of your organization, when organizing your Astro project code and developing your CI/CD pipelines.

This guide covers the options along with their pros and cons, so you can choose the best option for your team.

## Feature overview

Astro supports a number of CI/CD strategies. You can:
1. Maintain a *single* Git repository for all files in a *single* Astro project (one-to-one).
2. Separate your DAGs from other files and maintain *multiple* Git repositories for a *single* Astro project (many-to-one).
3. Host multiple Astro projects in a *single* repository for deployment to *multiple* Astro projects (one-to-many).

## Best practice guidance

Implementing CI/CD is a general software development best practice that enables automated building, testing, merging, and delivery of code. If you haven't yet implemented CI/CD pipelines for your Deployments, benefits of doing so include:
- Faster feedback loops.
- Improved code quality.
- Streamlined development workflows.
- Consistent deployments across environments.
- Less time spent getting code to production.
- Enhanced collaboration.

All the CI/CD strategies that Astro supports require utilization of a version control tool such as [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/). Implementation of version control is a longstanding software development best practice that enables:
- Simultaneous collaboration.
- Easy review of code changes.
- Safe and secure experimentation on new features and fixes.
- Improved traceability and auditing.

With a version control system in place, you can set up CI/CD by following the guidance in [Develop a CI/CD workflow for deploying code to Astro](https://astronomer.io/docs/astro/set-up-ci-cd). The option you choose for organizing the code in your shared repository and deploying to Astro should reflect the size and needs of your team. [Deployment API tokens](https://www.astronomer.io/docs/astro/deployment-api-tokens) are required for implementing CI/CD for automated deploys to Astro. 

Once you have set up CI/CD, Astronomer recommends [enabling CI/CD enforcement](https://www.astronomer.io/docs/astro/set-up-ci-cd#enforce-cicd) so that code pushes can be completed only when using a Deployment or Workspace token.

### Option 1: one repository to one Deployment

Creating a single Git repository for each Astro project is the strategy Astronomer recommends for smaller teams (under 30 members) in organizations where a single team is responsible for both developing DAGs and maintaining Deployments on Astro.

This strategy requires:
- One Astro project.
- One Workspace for your project.
- One repository.
- One Astro Deployment.

Pros of this approach:
- Your code history and project configuration are centralized, making it easy for developers to contribute changes to DAGs and Deployments while avoiding synchronization problems across files.
- You don't have to maintain multiple environments for managing dependencies and testing DAGs.

Cons of this approach:
- You can't easily restrict access to sensitive project settings.
- You can't take this approach and simultaneously collect DAGs used in multiple Deployments in a single repository.
- You can't also keep Deployment configuration code separate from DAG code, which is required when you want to [manage Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code) and when you want to restrict access to Deployment settings.

:::info 

Repository options for setting up one-to-one deploys with CI/CD include AWS S3. Supported CI/CD tools include Jenkins, GitHub Actions, and AWS CodeBuild. For details about setting up CI/CD workflows using these and other systems, see [Automate actions on Astro](https://www.astronomer.io/docs/astro/automation-overview).

:::

### Option 2: multiple repositories to one Deployment

A common use case for multiple repositories is keeping configuration code separate from DAG code. Astronomer recommends this approach when:
- You have strict security requirements for who can update particular project files, such as Astro Deployment settings.
- You want to minimize complexity for project contributors, automate Deployment creation, or manage Deployments more efficiently.
- You can set up and maintain a somewhat complex CI/CD pipeline.

This strategy requires:
- One Astro project.
- One Workspace for your project.
- Multiple repositories.
- One Astro Deployment.

Pros of this approach:
- You have more options when it comes to maintaining Deployments and deploying code.
- Managing Astro settings is potentially much easier, as keeping configuration code in a separate repository enables the use of a single repository for configuring multiple Deployments.
- The possibility of accidental changes to Astro Deployment settings is minimized.

Cons of this approach:
- You must keep any local copies of an Astro project synchronized with multiple repositories in order to test Deployment code locally and ensure that updates from your configuration repository do not erase your DAGs.
- Team members might have inconsistencies in their local environments if they lack access to the configuration repository. For this reason, Astronomer recommends [setting up a dev Deployment](manage-dev-deployments) where DAG authors can see and modify project configurations for testing purposes.

:::info

This strategy requires [DAG-only deploys](https://www.astronomer.io/docs/astro/deploy-dags#enable-or-disable-dag-only-deploys-on-a-deployment) on the target Deployment and CI/CD pipeline setup for both Git repositories.

:::

:::warning

This strategy is required when [configuring Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code).

:::

### Option 3: one repository with multiple permanent branches to multiple Deployments with CI/CD

When your DAGs are critical to your business, the ability to test your DAGs is critical, as well. Setting up automated deploys from multiple permanent branches of a single repository allows you to implement a robust testing regime for the code you intend to deploy to production. Astronomer recommends this approach when:
- You have business-critical DAGs.
- You can set up and maintain a somewhat complex CI/CD pipeline.

This strategy requires:
- One Astro project.
- One Astro Workspace for your project.
- At least two permanent branches in your repository, each representing an environment. Astro recommends naming the branches `main` and `dev`.
- At least two Astro Deployments.

Pros of this approach:
- You can test code changes to your DAGs in an isolated environment on Astro before deploying the changes to production.
- It is scaleable: you can map additional branches to additional Deployments, allowing for more testing or ephemeral Deployments for feature development. See [Manage dev Deployments on Astro](manage-dev-deployments). Also, if you work at a larger organization, you can create a Workspace and Astro project for each team or business use case.
- It supports separate environment configurations. If you use Snowflake, for example, your development Deployment on Astro can use a virtual data warehouse for development (`DWH Dev`), and your production Deployment can use a different virtual data warehouse for production (`DWH Prod`).

Cons of this approach:
- Restricting access to Astro settings or to particular Astro projects is more complicated at the level of sud to implement and maintain in sudirectories.
- Dependencies and environments might be more difficult to manage, to the extent that they differ from project to project.

:::tip

For more guidance on setting up CI/CD for deploys to multiple Deployments from a single repository, see [Multiple environments](https://www.astronomer.io/docs/astro/set-up-ci-cd#multiple-environments).

:::
