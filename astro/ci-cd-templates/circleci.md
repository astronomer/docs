---
sidebar_label: CircleCI
title: CircleCI CI/CD templates
id: circleci
description: Use pre-built templates to get started with automating code deploys from CircleCI to Astro 
---

Use the following template to automate [single branch deploys](template-overview.md#template-implementations) to Astro using [CircleCI](https://circleci.com/).

## Setup

To automate code deploys to a Deployment using [CircleCI](https://circleci.com/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables in a [CircleCI context](https://circleci.com/docs/2.0/contexts/):

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. Create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    ```
    # Use the latest CircleCI pipeline process engine version.
    # See: https://circleci.com/docs/2.0/configuration-reference
    version: 2.1

    orbs:
      docker: circleci/docker@2.0.1
      github-cli: circleci/github-cli@2.0.0

    # Define a job to be invoked later in a workflow.
    # See: https://circleci.com/docs/2.0/configuration-reference/#jobs
    jobs:

      build_image_and_deploy:
        docker:
          - image: cimg/base:stable
        # Add steps to the job
        # See: https://circleci.com/docs/2.0/configuration-reference/#steps
        steps:
          - setup_remote_docker:
              version: 20.10.11
          - checkout
          - run:
              name: "Setup custom environment variables"
              command: |
                echo export ASTRONOMER_KEY_ID=${ASTRONOMER_KEY_ID} >> $BASH_ENV
                echo export ASTRONOMER_KEY_SECRET=${ASTRONOMER_KEY_SECRET} >> $BASH_ENV
          - run:
              name: "Deploy to Astro"
              command: |
                curl -sSL install.astronomer.io | sudo bash -s
                astro deploy -f

    # Invoke jobs with workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      build-and-deploy-prod:
        jobs:
          - build_image_and_deploy:
              context:
                 - <YOUR-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - main
    ```

