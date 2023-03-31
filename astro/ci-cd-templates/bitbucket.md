---
sidebar_label: BitBucket
title: BitBucket CI/CD templates
id: bitbucket
description: Use pre-built templates for BitBucket to automate your Apache Airflow code deploys to Astro  
---

Templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools. 
 
You can use this template for [BitBucket](https://bitbucket.org/product) to automate code deploys to Astro with Image-only deploy templates [Image-only deploy templates](template-overview.md#template-types) create an automated workflow that builds a Docker image and then pushes it to Astro whenever you update any file in your Astro project. A _Single branch implementation_ allows you to deploy code to one Astro Deployment. 

See [Template overview](template-overview.md) to decide which template is right for you. To learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

This pipeline configuration requires the following:

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A [BitBucket](https://bitbucket.org/product) pipeline configuration.
- An [Astro project](create-project.md) hosted in a Git repository that your CI/CD tool can access.

## Single branch implementation

To automate code deploys to a Deployment using [Bitbucket](https://bitbucket.org/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables as [Bitbucket pipeline variables](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/):

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

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

