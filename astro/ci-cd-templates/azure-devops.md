---
sidebar_label: Azure DevOps
title: Azure DevOps CI/CD templates
id: azure-devops
description: Use pre-built templates for Azure DevOps to automate your Apache Airflow code deploys to Astro 
---

Use the following template to automate [single branch deploys](template-overview.md#template-implementations) to Astro using .

Templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools. 
 
You can use this template for [Azure DevOps](https://dev.azure.com/) to automate code deploys to Astro with Image-only deploy templates using a Single branch implementation. [Image-only deploy templates](template-overview.md#template-types) create an automated workflow that builds a Docker image and then pushes it to Astro whenever you update any file in your Astro project. A _Single branch implementation_ allows you to deploy code to one Astro Deployment. 

See [Template overview](template-overview.md) to decide which template is right for you. To learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

This pipeline configuration requires the following:

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A [Azure DevOps](https://dev.azure.com/) account.
- An [Astro project](create-project.md) hosted in an Azure repository that your CI/CD tool can access.

## Single branch implementation

Complete the following set up in an Azure repository that hosts an Astro project:

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

