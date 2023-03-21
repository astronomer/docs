---
sidebar_label: AWS Codebuild
title: AWS Codebuild CI/CD templates
id: aws-codebuild
description: Use pre-built templates to get started with automating code deploys from AWS Codebuild to Astro 
---

Use the following templates to automate code deploys to Astro using [AWS Codebuild](https://aws.amazon.com/codebuild/).

## Image-only templates

Image-only deploy templates build a Docker image and push it to Astro whenever you update any file in your Astro project.

### Single branch implementation

To automate code deploys from a single branch to a single Deployment using [AWS CodeBuild](https://aws.amazon.com/codebuild/), complete the following setup with a [supported Git-based repository](https://docs.aws.amazon.com/codebuild/latest/userguide/planning.html) hosting an Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

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

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the source provider where your Astro project is hosted, such as BitBucket or GitHub. When configuring the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.

### Multiple branch implementation

To automate code deploys across multiple Deployments using [AWS CodeBuild](https://aws.amazon.com/codebuild/), complete the following setup with a Git-based repository hosting an Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `PROD_ASTRONOMER_KEY_ID`: Your Production Deployment API key ID
    - `PROD_ASTRONOMER_KEY_SECRET`: Your Production Deployment API key secret
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your Production Deployment
    - `DEV_ASTRONOMER_KEY_ID`: Your Development Deployment API key ID
    - `DEV_ASTRONOMER_KEY_SECRET`: Your Development Deployment API key secret
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your Development Deployment

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

   3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the source provider where your Astro project is hosted, such as BitBucket or GitHub. When configuring the webhook, select an event type of `PUSH`.

Your `buildspec.yml` file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.