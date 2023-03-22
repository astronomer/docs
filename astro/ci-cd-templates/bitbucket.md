---
sidebar_label: BitBucket
title: BitBucket CI/CD templates
id: bitbucket
description: Use pre-built templates to get started with automating code deploys from BitBucket to Astro 
---

Use the following template to automate [single branch deploys](template-overview.md#template-implementations) to Astro using [BitBucket](https://bitbucket.org/product).

## Setup

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

