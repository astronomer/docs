---
title: 'Organizing code for CI/CD'
sidebar_label: 'Organizing code for CI/CD'
id: repo-structure
---

Astro supports a range of options when it comes to configuring Continuous Integration and Continuous Delivery (CI/CD) pipelines for the code you deploy to Astro. Astronomer recommends weighing the pros and cons of each option, along with the needs of your team and structure of your organization, when organizing your Astro project code and developing your CI/CD pipelines.

## Feature overview

Astro supports a number of different CI/CD strategies:
- Maintain a single Git repository for all files in your Astro project.
- Separate your DAGs from other files and maintain multiple Git repositories for a single Astro project.
- Store your DAGs in a cloud provider solution, such as AWS S3, and the rest of your Astro project files in a dedicated Git repository.

Each approach has advantages and disadvantages depending on your team's needs and other factors. The guidance offered here is intended to help you choose the best strategy for your particular use case.

## Best practice guidance

In general, implementing Continuous Integration and Continuous Delivery (CI/CD) pipelines is a software development best practice that:
- enables faster feedback loops
- supports improved code quality
- streamlines development workflows
- enables consistent deployments across environments
- decreases the time spent getting code to production
- facilitates collaboration.

All the CI/CD strategies that Astro supports require utilization of a version control tool such as [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/). Implementation of version control is a longstanding software development best practice that enables:
- simultaneous collaboration
- easy review of code changes
- secure and risk-free experimentation on new features and fixes
- improved traceability and auditing.

With a version control system in place, you can configure automated deploys of your latest changes to Astro using CI/CD pipelines. How you choose to organize the code in your shared repository and deploy it to Astro should reflect the size and needs of your team.

### Option 1: one repo to one Deployment

Creating a single Git repository for each Astro project is the strategy Astronomer recommends for smaller teams (under 30 members).

Pro of this approach:
- Your code history and project configuration are centralized, making it easy for developers to contribute changes to DAGs and Deployment configuration while avoiding synchronization problems across files.

Cons of this approach:
- You can't take this approach and simultaneously collect DAGs used in multiple Deployments in a single repository.
- You can't take this approach and keep Deployment configuration code and DAG code separate, which is required in cases when you want to [configure Deployments programmatically](https://www.astronomer.io/docs/astro/manage-deployments-as-code) and when you want to restrict access to Deployment configuration.

### Option 2: one repo with multiple projects to multiple Deployments with CI/CD

### Option 3: multiple repos to one Deployment

