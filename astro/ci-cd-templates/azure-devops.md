---
sidebar_label: Azure DevOps
title: Astro CI/CD templates for Azure DevOps
id: azure-devops
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using Azure DevOps.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [Azure DevOps](https://dev.azure.com/).

The templates for Azure DevOps use the [image-only deploy](template-overview.md#template-types) process with a _single branch implementation_, which requires only one Astro Deployment.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro or you're interested in a multiple-branch implementation, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](create-project.md) hosted in a Git repository that Azure DevOps can access.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md).
- Access to [Azure DevOps](https://dev.azure.com/).

## Single branch implementation

Complete the following setup in an Azure repository that hosts an Astro project:

1. Set the following environment variables as [DevOps pipeline variables](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch):

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. Create a new Azure DevOps pipeline named `astro-devops-cicd.yaml` at the root of the repository that includes the following configuration:

    ```yaml
    trigger:
    - main

    pr: none

    stages:
    - stage: deploy
      jobs:
      - job: deploy_image
        pool:
          vmImage: 'Ubuntu-latest'
        steps:
        - script: |
            curl -sSL install.astronomer.io | sudo bash -s
            astro deploy
          env:
            ASTRONOMER_KEY_ID: $(ASTRONOMER_KEY_ID)
            ASTRONOMER_KEY_SECRET: $(ASTRONOMER_KEY_SECRET)
    ```

