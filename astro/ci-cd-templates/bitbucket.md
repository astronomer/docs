---
sidebar_label: Bitbucket
title: Astro CI/CD templates for Bitbucket
id: bitbucket
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using BitBucket. 
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [Bitbucket](https://bitbucket.org/product).

The templates for Bitbucket use the [image-only deploy](template-overview.md#template-types) process with a _single branch implementation_, which requires only one Astro Deployment.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro or you're interested in a multiple-branch implementation, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a Git repository that Bitbucket can access.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- Access to [Bitbucket](https://bitbucket.org/product).

## Single branch implementation

To automate code deploys to a Deployment using [Bitbucket](https://bitbucket.org/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variable as a [Bitbucket pipeline variable](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/):

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

    For production Deployments, be sure to set the value of your API token as **secured**.

2. Create a new YAML file in `bitbucket-pipelines.yml` at the root of the repository that includes the following configuration:

    ```
    pipelines:
      pull-requests: # The branch pattern under pull requests defines the *source* branch.
        dev:
          - step:
              name: Deploy to Production
              deployment: Production
              script:
                - curl -sSL install.astronomer.io | sudo bash -s
                - astro deploy
              services:
                - docker
    ```

