---
sidebar_label: AWS Codebuild
title: AWS Codebuild CI/CD templates
id: aws-codebuild
description: Use pre-built templates for AWS Codebuild to automate your Apache Airflow code deploys to Astro 
---

Astro CI/CD templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools. Use the following templates to automate deploys to Astro using [AWS Codebuild](https://aws.amazon.com/codebuild/).

The following templates use [AWS Codebuild](https://aws.amazon.com/codebuild/) to automate code deploys to Astro. The templates create an automated workflow that builds a Docker image and then pushes it to Astro as an [image-only deploy](template-overview.md#template-types) whenever you update any file in your Astro project. You can choose whether to deploy to a single Deployment, called _Single branch implementation_, or multiple Deployments, called _Multiple branch implementation_.

These templates do not use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) in Astro to set up [DAG-based workflows](astro/ci-cd#dag-based-workflows). Updated templates are coming soon. To learn more about CI/CD on Astro, see [Template overview](template-overview.md) and [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

- A Git-based repository. See [Plan a build in AWS Codebuild](https://docs.aws.amazon.com/codebuild/latest/userguide/planning.html).
- At least 1 Astro Deployment and at least 1 branch in a Git-based repository. The number of Deployments and environments depends on your CI/CD strategy. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md) for each Deployment.
- Access to AWS CodeBuild. See [Getting started with CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/getting-started-overview.html).
- An [Astro project](create-project.md) hosted in a Git repository that AWS CodeBuild can access.

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