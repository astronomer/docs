---
title: 'Organizing code for CI/CD'
sidebar_label: 'Organizing code for CI/CD'
id: repo-structure
---

Astro supports a range of options when it comes to configuring Continuous Integration and Continuous Delivery (CI/CD) pipelines for the code you deploy to Astro. 

Astronomer recommends weighing the pros and cons of each option, along with the needs of your team and structure of your organization, when organizing your Astro project code and developing your CI/CD pipelines.

This guide covers the options along with their pros and cons so you can choose the best option for your team.

## Feature overview

Astro supports a number of CI/CD strategies:
- Maintain a single Git repository for all files in your Astro project (one-to-one).
- Separate your DAGs from other files and maintain multiple Git repositories for a *single* Astro project (many-to-one).
- Separate your DAGs from other files and maintain multiple Git repositories for *multiple* Astro projects (many-to-many).
- Store your DAGs in a cloud provider solution, such as AWS S3, and the rest of your Astro project files in a dedicated Git repository.

## Best practice guidance

If you haven't yet implemented CI/CD pipelines for your Deployments, consider these benefits:
- faster feedback loops
- improved code quality
- streamlined development workflows
- consistent deployments across environments
- less time spent getting code to production
- enhanced collaboration.

All the CI/CD strategies that Astro supports require utilization of a version control tool such as [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/). Implementation of version control is a longstanding software development best practice that enables:
- simultaneous collaboration
- easy review of code changes
- secure and risk-free experimentation on new features and fixes
- improved traceability and auditing.

With a version control system in place, you can configure automated deploys of your latest changes to Astro using CI/CD pipelines. How you choose to organize the code in your shared repository and deploy it to Astro should reflect the size and needs of your team.

### Option 1: one repo to one Deployment

Creating a single Git repository for each Astro project is the strategy Astronomer recommends for smaller teams (under 30 members) in organizations where a single team is responsible for both developing DAGs and maintaining Deployments on Astro.

Pro of this approach:
- Your code history and project configuration are centralized, making it easy for developers to contribute changes to DAGs and Deployment configuration while avoiding synchronization problems across files.

Cons of this approach:
- You can't take this approach and simultaneously collect DAGs used in multiple Deployments in a single repository.
- You can't take this approach and keep Deployment configuration code and DAG code separate, which is required when you want to [configure Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code) and when you want to restrict access to Deployment configuration.

### Option 2: one repo with multiple projects to multiple Deployments with CI/CD



### Option 3: multiple repos to one Deployment

Depending on your organization, you might need to keep Deployment configuration code and DAG code separate, requiring a many-to-one relationship. 

This approach is required when [configuring Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code) and when restricting access to Astro project settings, such as Python packages and worker configuration, to admins.

Astronomer recommends this approach when:
- You have strict security requirements for who can update specific project files.
- You want to minimize complexity for project contributors or manage Deployments more efficiently even if it means a more complex CI/CD pipeline.

Pros of this approach:
- You have more options when it comes to deploying code, including automated deployment.
- Managing Astro settings is potentially much easier, as this approach enables sharing configuration among Deployments.
- Accidental changes to Astro settings are minimized.

Cons of this approach:
- You must keep any local copies of an Astro project synchronized with *multiple repositories* in order to test Deployment code locally and ensure that updates from your configuration repo do not erase your DAGs.
- Team members might have inconsistencies in their local environments if they lack access to the configuration repo. For this reason, Astronomer recommends setting up a dev Deployment where DAG authors can see and modify project configurations for testing purposes when taking this approach.

:::info

This strategy requires [DAG-only deploys](https://www.astronomer.io/docs/astro/deploy-dags#enable-or-disable-dag-only-deploys-on-a-deployment) on the target Deployment and CI/CD pipeline setup for both Git repositories.

:::
