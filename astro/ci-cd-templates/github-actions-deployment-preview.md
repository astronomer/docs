---
sidebar_label: Preview Deployment templates
title: GitHub Actions templates for preview Deployments
id: github-actions-deployment-preview
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to a preview Deployment using GitHub Actions.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

The Astronomer [deploy action](https://github.com/astronomer/deploy-action/tree/deployment-preview#deployment-preview-templates) includes several sub-actions that can be used together to create a complete [Deployment preview](ci-cd-templates/template-overview.md#preview-deployment-templates) pipeline.

The Deployment preview templates use GitHub secrets to manage the credentials needed for GitHub to authenticate to Astro. You can also use a secret to store the credentials for your [secrets backend](secrets-backend.md) so that preview Deployments have access to secret Airflow variables or connections during tests. See [Deployment preview template with secrets backend implementation](#deployment-preview-template-with-secrets-backend-implementation).

Because Deployment preview templates use the `deploy-action` template, which is available in the [GitHub Marketplace](https://github.com/marketplace/actions/deploy-apache-airflow-dags-to-astro). This action automates the deploy process and includes additional features for more complex automation workflows. Specifically, the action can automatically:

- Choose a deploy type based on the files that were changed in a commit. This allows you to use the same template for DAG deploys and image deploys.
- Test DAGs as part of the deploy process and prevent deploying if any of the tests fail. These tests are defined in the `tests` directory of your Astro project.
- Create a preview Deployment to test your code before deploying to production. A Deployment preview is an Astro Deployment that mirrors the configuration of an existing Deployment.

This means that the `deploy-action` triggers both image deploys and DAG deploys depending on the type of file changes that you made. If you committed changes only to DAG files, the action triggers a DAG deploy. If you committed changes to any other file, the action triggers an image deploy. See the [Deploy Action README](https://github.com/astronomer/deploy-action#readme) to learn more about using and customizing this action.

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

Each implementation might have additional requirements.

:::warning

If you use a [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) to execute jobs from GitHub Actions, the Astro CLI's `config.yaml` file, which stores default deploy details, might be shared across your organization and hence multiple CI/CD pipelines. To reduce the risk of accidentally deploying to the wrong Deployment, ensure the following:

- Add `ASTRO_API_TOKEN` to your repository and include a check in your GitHub workflow to verify that it exists.
- Use Deployment API tokens, which are scoped only to one Deployment, instead of Workspace or Organization API tokens.
- Specify `deployment-id` or `deployment-name` in your action. For example, `astro deploy <deployment-id>` or `astro deploy -n <deployment-name>`.
- Add the command `astro logout` at the end of your workflow to ensure that your authentication token is cleared from the `config.yaml` file.

:::

## Standard Deployment preview template

The standard Deployment preview template uses GitHub secrets and an Astro Deployment API token to create a preview Deployment whenever you create a new feature branch off of your main branch.

### Prerequisites

- An Astro project hosted in a GitHub repository.
- A [Workspace API token](workspace-api-tokens.md).
- A [Deployment](create-deployment.md).

### Setup

1. Copy and save the Deployment ID for your Astro deployment.
2. Set the following [GitHub secret](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in the repository hosting your Astro project:

  - Key: `ASTRO_API_TOKEN`
  - Secret: `<your-token>`

3. In your project repository, create a new YAML file in `.github/workflows` named `create-deployment-preview.yml` that includes the following configuration.

    ```yaml
    name: Astronomer CI - Create preview Deployment

    on:
      create:
        branches:
          - "**"

    env:
      ## Sets Deployment API key credentials as environment variables or GitHub Secret depending on your configuration
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Create preview Deployment
          uses: astronomer/deploy-action@v0.4
          with:
            action: create-deployment-preview
            deployment-id: <main-deployment-id>
    ```

4. In the same folder, create a new YAML file named `deploy-to-preview.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to preview

    on:
      pull_request:
        branches:
          - main

    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to preview
          uses: astronomer/deploy-action@v0.4
          with:
            action: deploy-deployment-preview
            deployment-id: <main-deployment-id>
    ```

5. In the same folder, create a new YAML file named `delete-preview-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Delete Preview Deployment

    on:
      delete:
        branches:
          - "**"
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Delete preview Deployment
          uses: astronomer/deploy-action@v0.4
          with:
            action: delete-deployment-preview
            deployment-id: <main-deployment-id>
    ```

6. In the same folder, create a new YAML file named `deploy-to-main-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to main Deployment

    on:
      push:
        branches:
          - main

    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to main Deployment
          uses: astronomer/deploy-action@v0.4
          with:
            deployment-id: <main-deployment-id>
    ```

    All four workflow files must have the same Deployment ID specified. The actions use this Deployment ID to create and delete preview Deployments based on your main Deployment.

## Deployment preview template with secrets backend implementation

If you use a [secrets backend](secrets-backend.md) to manage Airflow objects such as variables and connections, you can configure your action to grant preview Deployments access to your secrets backend. This means that DAGs in the preview Deployment can access your secret Airflow objects for testing purposes.

This template makes use of the `AIRFLOW__SECRETS__BACKEND_KWARGS` environment variable to store information and credentials for your secrets backend.

### Prerequisites

- An Astro project hosted in a GitHub repository.
- A [Workspace API token](workspace-api-tokens.md).
- A [Deployment](create-deployment.md).
- A [secrets backend](secrets-backend.md).

### Setup

1. Copy and save the Deployment ID for your Astro deployment.
2. Set the following [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in the repository hosting your Astro project. This includes your Astro API Token, so that GitHub has permissions to deploy code to your Deployments or Workspaces, and your secrets backend information stored in `AIRFLOW__SECRETS__BACKEND_KWARGS`. See [Configure a secrets backend](secrets-backend.md) for more information about configuring your secrets backend as an environment variable.

    - **Key 1**: `ASTRO_API_TOKEN`
    - **Secret 1**: `<your-token>`
    - **Key 2**: `AIRFLOW__SECRETS__BACKEND_KWARGS`
    - **Secret 2**: `<your-kwargs>`

3. In your project repository, create a new YAML file in `.github/workflows` named `create-deployment-preview.yml` that includes the following configuration.

    ```yaml
    name: Astronomer CI - Create preview Deployment with Secrets Backend

    on:
      create:
        branches:
          - "**"

    env:
      ## Sets Deployment API key credentials as environment variables
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - steps:
          - name: Create Deployment Preview
            uses: astronomer/deploy-action@v0.3
            with:
              action: create-deployment-preview
              deployment-name: "test"
              id: create-dep-prev
          - name: Create Secret Variables
            run: |
              astro deployment variable update --deployment-id ${{steps.create-dep-prev.outputs.preview-id}} AIRFLOW__SECRETS__BACKEND_KWARGS=${{ secrets.AIRFLOW__SECRETS__BACKEND_KWARGS }} --secret
    ```

4. In the same folder, create a new YAML file named `deploy-to-preview.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to preview

    on:
      pull_request:
        branches:
          - main

    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to preview
          uses: astronomer/deploy-action@v0.4
          with:
            action: deploy-deployment-preview
            deployment-id: <main-deployment-id>
    ```

5. In the same folder, create a new YAML file named `delete-preview-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Delete Preview Deployment

    on:
      delete:
        branches:
          - "**"
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Delete preview Deployment
          uses: astronomer/deploy-action@v0.4
          with:
            action: delete-deployment-preview
            deployment-id: <main-deployment-id>
    ```

6. In the same folder, create a new YAML file named `deploy-to-main-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to main Deployment

    on:
      push:
        branches:
          - main

    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to main Deployment
          uses: astronomer/deploy-action@v0.4
          with:
            deployment-id: <main-deployment-id>
    ```

    All four workflow files must have the same Deployment ID specified. The actions use this Deployment ID to create and delete preview Deployments based on your main Deployment.
