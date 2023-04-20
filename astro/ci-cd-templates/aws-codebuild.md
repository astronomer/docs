---
sidebar_label: AWS CodeBuild
title: Astro CI/CD templates for AWS CodeBuild
id: aws-codebuild
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using AWS CodeBuild.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [AWS CodeBuild](https://aws.amazon.com/codebuild/).

The templates for AWS CodeBuild use the [image-only deploy](template-overview.md#template-types) process. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro and are interested in a DAG-based CI/CD template, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) hosted in a Git repository that AWS CodeBuild can access. See [Plan a build in AWS Codebuild](https://docs.aws.amazon.com/codebuild/latest/userguide/planning.html).
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md) for each Deployment.
- Access to AWS CodeBuild. See [Getting started with CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/getting-started-overview.html).

Each CI/CD template implementation might have additional requirements.

## Single branch implementation

To automate code deploys from a single branch to a single Deployment using AWS CodeBuild, complete the following setup in the Git-based repository that hosts your Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your Deployment

    Be sure to set the values for your API credentials as secret.

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
         - export ASTRONOMER_KEY_ID="${ASTRONOMER_KEY_ID}"
         - export ASTRONOMER_KEY_SECRET="${ASTRONOMER_KEY_SECRET}"
         - curl -sSL install.astronomer.io | sudo bash -s
         - astro deploy "${ASTRONOMER_DEPLOYMENT_ID}" -f

    ```

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the Git repository where your Astro project is hosted. If you use GitHub, see [GitHub webhook events](https://docs.aws.amazon.com/codebuild/latest/userguide/github-webhook.html). When you configure the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.

## Multiple branch implementation

To automate code deploys across multiple Deployments using AWS CodeBuild, complete the following setup.

This setup requires two Deployments on Astro and two branches in your Git repository. The example assumes that one Deployment is a development environment, and that the other Deployment is a production environment. To learn more, see [Multiple environments](astro/set-up-ci-cd#multiple-environments).

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `PROD_ASTRONOMER_KEY_ID`: Your production Deployment API key ID
    - `PROD_ASTRONOMER_KEY_SECRET`: Your production Deployment API key secret
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your production Deployment
    - `DEV_ASTRONOMER_KEY_ID`: Your development Deployment API key ID
    - `DEV_ASTRONOMER_KEY_SECRET`: Your development Deployment API key secret
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your development Deployment

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
             export ASTRONOMER_KEY_ID="${PROD_ASTRONOMER_KEY_ID}"
             export ASTRONOMER_KEY_SECRET="${PROD_ASTRONOMER_KEY_SECRET}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${PROD_DEPLOYMENT_ID}" -f
           fi
         - |
           if expr "${CODEBUILD_WEBHOOK_HEAD_REF}" : "refs/heads/dev" >/dev/null; then
             export ASTRONOMER_KEY_ID="${DEV_ASTRONOMER_KEY_ID}"
             export ASTRONOMER_KEY_SECRET="${DEV_ASTRONOMER_KEY_SECRET}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${DEV_DEPLOYMENT_ID}" -f
           fi
    ```

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the Git repository where your Astro project is hosted. If you use GitHub, see [GitHub webhook events](https://docs.aws.amazon.com/codebuild/latest/userguide/github-webhook.html). When you configure the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to your development Deployment every time a commit or pull request is merged to the `dev` branch of your repository, and a code push to your production Deployment every time a commit or pull request is merged to the `main` branch of your repository.