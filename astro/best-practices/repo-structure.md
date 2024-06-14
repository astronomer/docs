---
title: 'Organizing code for CI/CD'
sidebar_label: 'Organizing code for CI/CD'
id: repo-structure
---

Astro supports a range of options when it comes to setting up Continuous Integration and Continuous Delivery (CI/CD) pipelines for the code you deploy to Astro. 

Astronomer recommends weighing the pros and cons of each option, along with the needs of your team and structure of your organization, when organizing your Astro project code and developing your CI/CD pipelines.

This guide covers the options along with their pros and cons, so you can choose the best option for your team.

## Feature overview

Astro supports a number of CI/CD strategies. You can:
1. Maintain a single Git repository for all files in a *single* Astro project (one-to-one).
2. Separate your DAGs from other files and maintain multiple Git repositories for a *single* Astro project (many-to-one).
3. Host multiple Astro projects in a single repository for deployment to *multiple* Astro projects (one-to-many).
4. Separate your DAGs from other files and maintain multiple Git repositories for *multiple* Astro projects (many-to-many).
5. Store your DAGs in a cloud provider solution, such as AWS S3, and the rest of your Astro project files in a dedicated Git repository (many-to-one or many-to-many).

## Best practice guidance

Implementing CI/CD is a general software development best practice enabling automated building, testing, merging, and delivery of code. If you haven't yet implemented CI/CD pipelines for your Deployments, consider these benefits:
- faster feedback loops
- improved code quality
- streamlined development workflows
- consistent deployments across environments
- less time spent getting code to production
- enhanced collaboration.

All the CI/CD strategies that Astro supports require utilization of a version control tool such as [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/). Implementation of version control is a longstanding software development best practice that enables:
- simultaneous collaboration
- easy review of code changes
- safe and secure experimentation on new features and fixes
- improved traceability and auditing.

With a version control system in place, you can set up CI/CD by following the guidance in [Develop a CI/CD workflow for deploying code to Astro](https://docs.astronomer.io/astro/set-up-ci-cd). The way you organize the code in your shared repository and deploy it to Astro should reflect the size and needs of your team.

### Option 1: one repo to one Deployment

Creating a single Git repository for each Astro project is the strategy Astronomer recommends for smaller teams (under 30 members) in organizations where a single team is responsible for both developing DAGs and maintaining Deployments on Astro.

Pros of this approach:
- Your code history and project configuration are centralized, making it easy for developers to contribute changes to DAGs and Deployments while avoiding synchronization problems across files.
- You don't have to maintain multiple environments for managing dependencies and testing DAGs.

Cons of this approach:
- You can't easily restrict access to sensitive project settings.
- You can't take this approach and simultaneously collect DAGs used in multiple Deployments in a single repository.
- You can't also keep Deployment configuration code separate from DAG code, which is required when you want to [manage Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code) and when you want to restrict access to Deployment settings.

### Option 2: multiple repos to one Deployment

A common use case for multiple repos is separating configuration code and DAG code. Astronomer recommends this approach when:
- You have strict security requirements for who can update particular project files, such as Astro Deployment settings.
- You want to minimize complexity for project contributors, automate Deployment creation, or manage Deployments more efficiently.
- You can set up and maintain a somewhat complex CI/CD pipeline.

Pros of this approach:
- You have more options when it comes to maintaining Deployemnts and deploying code, including setting up automated deploys.
- Managing Astro settings is potentially much easier, as keeping configuration code in a separate repository enables the use of a single repository for configuring multiple Deployments.
- The possibility of accidental changes to Astro Deployment settings is minimized.

Cons of this approach:
- You must keep any local copies of an Astro project synchronized with multiple repositories in order to test Deployment code locally and ensure that updates from your configuration repo do not erase your DAGs or vice versa.
- Team members might have inconsistencies in their local environments if they lack access to the configuration repo. For this reason, Astronomer recommends setting up a dev Deployment where DAG authors can see and modify project configurations for testing purposes when taking this approach.

:::info

This strategy requires [DAG-only deploys](https://www.astronomer.io/docs/astro/deploy-dags#enable-or-disable-dag-only-deploys-on-a-deployment) on the target Deployment and CI/CD pipeline setup for both Git repositories.

:::

:::warn

This strategy is required when [configuring Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code).

:::

### Option 3: one repo with multiple projects to multiple Deployments with CI/CD

Astronomer recommends this approach when:
- You do not have strict security requirements for who can access particular projects or settings.
- You can set up and maintain a more complex CI/CD pipeline.

Pros of this approach:
- DAGs and configuration are centralized rather than distributed across multiple repos.
- It is less likely that team members might have inconsistencies in their local environments.

Cons of this approach:
- Restricting access to Astro settings or particular projects is more difficult to implement than at the repo level.
- Dependencies and environments might be more difficult to manage, to the extent that they differ from project to project.

### Option 4: multiple repos to multiple Deployments with CI/CD

Pros of this approach:
- Managing Astro settings is potentially much easier, as keeping configuration code in a separate repository allows for the sharing of Astro settings among multiple Deployments.

