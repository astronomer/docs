---
sidebar_label: GitHub Actions
title: Astro CI/CD templates for GitHub Actions
id: github-actions
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using GitHub Actions.
---

GitHub Action templates use the Astronomer-maintained `deploy-action`, which is available in the [GitHub Marketplace](https://github.com/marketplace/actions/deploy-apache-airflow-dags-to-astro). This action automates the deploy process and includes additional features for more complex automation workflows. Specifically, the action can automatically:

- Choose a deploy type based on the files that were changed in a commit. This allows you to use the same template for DAG deploys and image deploys.
- Test DAGs as part of the deploy process and prevent deploying if any of the tests fail. These tests are defined in the `tests` directory of your Astro project.
- Create a preview Deployment to test your code before deploying to production. A Deployment preview is an Astro Deployment that mirrors the configuration of an existing Deployment.

See the [Deploy Action README](https://github.com/astronomer/deploy-action#readme) to learn more about using and customizing this action.

:::info

If you use GitHub Enterprise and cannot access the Astronomer Deploy Action, see [Private network templates](#private-network-templates).

:::

Read the following sections to choose the right template for your use case. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_. If your team builds custom Docker images, use the _custom image_ implementation. If you do not have access to Astronomer's `deploy-action`, use the [private network templates](#private-network-templates).

To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](cli/develop-project.md#create-an-astro-project) hosted in a GitHub repository.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API token](deployment-api-tokens.md), [Workspace API token](workspace-api-tokens.md), or [Organization API token](organization-api-tokens.md).
- Access to [GitHub Actions](https://github.com/features/actions).

Each CI/CD template implementation might have additional requirements.

:::warning

If you use a [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) to execute jobs from GitHub Actions, the Astro CLI's `config.yaml` file, which stores default deploy details, might be shared across your organization and hence multiple CI/CD pipelines. To reduce the risk of accidentally deploying to the wrong Deployment, ensure the following:

- Add `ASTRO_API_TOKEN` to your repository and include a check in your GitHub workflow to verify that it exists.
- Use Deployment API tokens, which are scoped only to one Deployment, instead of Workspace or Organization API tokens.
- Specify `deployment-id` or `deployment-name` in your action. For example, `astro deploy <deployment-id>` or `astro deploy -n <deployment-name>`.
- Add the command `astro logout` at the end of your workflow to ensure that your authentication token is cleared from the `config.yaml` file.

:::

## Deploy action templates

Templates that use the Astronomer `deploy-action` trigger both image deploys and DAG deploys. If you committed changes only to DAG files, the action triggers a DAG deploy. If you committed changes to any other file, the action triggers an image deploy.

- [GitHub Actions Template using Deploy Action](/ci-cd-templates/github-actions-deploy-action.md)

## Deployment preview templates

The Astronomer [Deploy Action](https://github.com/astronomer/deploy-action/tree/deployment-preview#deployment-preview-templates) includes several sub-actions that can be used together to create a complete [Deployment preview](ci-cd-templates/template-overview.md#preview-deployment-templates) pipeline.

The Deployment preview templates use GitHub secrets to manage the credentials needed for GitHub to authenticate to Astro. You can also use a secret to store the credentials for your [secrets backend](secrets-backend.md) so that preview Deployments have access to secret Airflow variables or connections for testing purposes. See [Deployment preview template with secrets backend implementation](#deployment-preview-template-with-secrets-backend-implementation).

### Standard Deployment preview template

The standard Deployment preview template uses GitHub secrets and an Astro Deployment API token to create a preview Deployment whenever you create a new feature branch off of your main branch.

- [Standard Deployment preview](/ci-cd-templates/github-actions-deployment-preview.md#standard-deployment-preview-template)

### Deployment preview with secrets backend

If you use a [secrets backend](secrets-backend.md) to manage Airflow objects such as variables and connections, you can configure your action to grant preview Deployments access to your secrets backend. This means that DAGs in the preview Deployment can access your secret Airflow objects for testing purposes.

This template makes use of the `AIRFLOW__SECRETS__BACKEND_KWARGS` environment variable to store information and credentials for your secrets backend.

- [Deployment preview with secrets backend](/ci-cd-templates/github-actions-deployment-preview.md#deployment-preview-template-with-secrets-backend-implementation)

## Private network templates

If you use GitHub Enterprise and can't use the public Astronomer [Deploy Action](https://github.com/astronomer/deploy-action) in the GitHub Marketplace, use the following templates to implement CI/CD.

You can configure your CI/CD pipelines to deploy a full project image or your `dags` directory to a preview environment.

- [Private network templates](/ci-cd-templates/github-actions-private-network.md)
