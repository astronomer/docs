---
sidebar_label: Azure DevOps
title: Azure DevOps CI/CD templates
id: azure-devops
description: Use pre-built templates to get started with automating code deploys from Azure DevOps to Astro 
---

Use the following template to automate [single branch deploys](template-overview.md#template-types) to Astro using [Azure DevOps](https://dev.azure.com/).

## Setup

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

