---
title : 'Example use-cases to manage Deployments as code'
sidebar_label: 'Example use-cases'
id: deployments-as-code-examples
description: View example workflows and templates for managing Deployments as code.
---


This page provides some example use-cases in detail that you can implement using Astro CLI, your version-control system (VCS) and your CI/CD process. In these examples, we are using GitHub as the VCS and GitHub Actions as the CI/CD process.

### Create ephemeral Deployments based on branch name

To ensure smooth transition of your new or changed DAGs from a lower environment to a production environment, it is imperative to have some processes or controls on how your team tests. You can enforce this easily using Astro's ability to output your Deployment configuration as code. 

For example, if you want your team to test the new or updated DAGs using the same set of configurations as in your production Deployment, follow these steps:

1. Create a [reference template file](#generate-a-deployment-template-file) for your production Deployment.

2. Check-in your Deployment template file to your GitHub repository's `main` branch.

3. Follow GitHub documentation to [create environment variables](https://docs.github.com/en/actions/learn-github-actions/variables) for [API token or API key](./automation-authentication.md#api-based-access) and the ID of your dev Workspace.

4. Create a new GitHub action which does the following:
  a. On creation of a new `dev` branch, use the template reference file from the `main` branch to add the Deployment name, update the `workspace_id` to your dev Workspace, and any other values.
  b. [Create a new Deployment](#create-a-deployment-from-a-template-file).
  c. [Deploy your code](astro/deploy-code.md).

5. When the testing is complete, on merge of `dev` branch to `staging` or `main`, you can [delete the Deployment](cli/astro-deployment-delete.md) on Astro

This process will help you save costs by auto-creating and removing the test Deployments and also ensure your test environment is similar to your production environment.

### Smart deploys from a mono-repo setup

Automation of your CI/CD process depends on how your organization manages your Airflow DAGs in a version-control system, such as using a single repository for all your Airflow DAGs or using multiple repostitories for different teams, and how it segregates various Airflow environments.

Let's consider a scenario:

- You have a mono-repo and two Airflow environments, one for staging and one for production. 
- All team members use `dev` prefixed branches to build their DAGs and test locally.

To auto-detect if you need DAG-based deploy or image-based deploy to staging, follow these steps:

1. Create a GitHub action to copy all DAGs from the `dags` directory to a `astro_deploy` branch. This should get triggered when a Pull Request (PR) is created to `staging` branch from a `dev` prefixed branch.
2. Create a GitHub action to check if only the files in `dags` directory have changed or other files have also changed. This should get triggered when changes are pushed to `astro deploy` branch. When changes are detected only in `dags` directory, then trigger DAG-based deploy. Otherwise, if there are changes to files outside the `dags` directory, then trigger an image-based deploy.
3. Create a GitHub action to deploy changes from `astro_deploy` branch to `main` branch. This should get triggered when a PR is created to `main` from `astro_deploy`. This Github action will do an image-based deploy to your production environment.


### i am not very happy with my diagram, wondering if we do this in Figma ?
![Flow diagram for CI/CD with DAG-based and image-based deploys](/img/docs/ci_cd_dag_and_image.png)