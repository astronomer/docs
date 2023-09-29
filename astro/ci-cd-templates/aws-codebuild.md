---
sidebar_label: AWS CodeBuild
title: Astro CI/CD templates for AWS CodeBuild
id: aws-codebuild
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using AWS CodeBuild.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [AWS CodeBuild](https://aws.amazon.com/codebuild/).

The templates for AWS CodeBuild use [image deploy](template-overview.md#template-types) templates. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro and are interested in a DAG deploy CI/CD template, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](cli/develop-project.md#create-an-astro-project) hosted in a Git repository that AWS CodeBuild can access. See [Plan a build in AWS Codebuild](https://docs.aws.amazon.com/codebuild/latest/userguide/planning.html).
- An [Astro Deployment](create-deployment.md).
- A [Deployment API token](deployment-api-tokens.md), [Workspace API token](workspace-api-tokens.md), or [Organization API token](organization-api-tokens.md).
- Access to AWS CodeBuild. See [Getting started with CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/getting-started-overview.html).

Each CI/CD template implementation might have additional requirements.

## Single branch implementation

To automate code deploys from a single branch to a single Deployment using AWS CodeBuild, complete the following setup in the Git-based repository that hosts your Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRO_DEPLOYMENT_ID`: The ID for your Deployment.

    Be sure to set the value of your API token as secret.

2. At the root of your Git repository, add a [`buildspec.yml`](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example) file that includes the following script:

   ```yaml

   version: 0.2

   phases:
     install:
       runtime-versions:
         python: latest

     build:
       commands:
         - echo "${CODEBUILD_WEBHOOK_HEAD_REF}"
         - export ASTRO_API_TOKEN="${ASTRO_API_TOKEN}"
         - curl -sSL install.astronomer.io | sudo bash -s
         - astro deploy "${ASTRO_DEPLOYMENT_ID}" -f

    ```

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the Git repository where your Astro project is hosted. If you use GitHub, see [GitHub webhook events](https://docs.aws.amazon.com/codebuild/latest/userguide/github-webhook.html). When you configure the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.

## Multiple branch implementation

To automate code deploys across multiple Deployments using AWS CodeBuild, complete the following setup.

This setup requires two Deployments on Astro and two branches in your Git repository. The example assumes that one Deployment is a development environment, and that the other Deployment is a production environment. To learn more, see [Multiple environments](astro/set-up-ci-cd#multiple-environments).

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your production Deployment.
    - `DEV_ASTRO_API_TOKEN`: The value for your development Workspace or Organization API token.
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your development Deployment.

    Be sure to set the values for your API tokens as secret.

2. At the root of your Git repository, add a [`buildspec.yml`](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example) that includes the following script:

   ```yaml

   version: 0.2

   phases:
     install:
       runtime-versions:
         python: latest

     build:
       commands:
         - |
           if expr "${CODEBUILD_WEBHOOK_HEAD_REF}" : "refs/heads/main" >/dev/null; then
             export ASTRO_API_TOKEN="${PROD_ASTRO_API_TOKEN}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${PROD_DEPLOYMENT_ID}" -f
           fi
         - |
           if expr "${CODEBUILD_WEBHOOK_HEAD_REF}" : "refs/heads/dev" >/dev/null; then
             export ASTRO_API_TOKEN="${DEV_ASTRO_API_TOKEN}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${DEV_DEPLOYMENT_ID}" -f
           fi
    ```

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the Git repository where your Astro project is hosted. If you use GitHub, see [GitHub webhook events](https://docs.aws.amazon.com/codebuild/latest/userguide/github-webhook.html). When you configure the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to your development Deployment every time a commit or pull request is merged to the `dev` branch of your repository, and a code push to your production Deployment every time a commit or pull request is merged to the `main` branch of your repository.