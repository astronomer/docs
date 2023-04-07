---
sidebar_label: CircleCI
title: Astro CI/CD templates for CircleCI
id: circleci
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using CircleCI.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [CircleCI](https://circleci.com/).

The templates for CircleCI use the [image-only deploy](template-overview.md#template-types) process with a _single branch implementation_, which requires only one Astro Deployment.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro or you're interested in a multiple-branch implementation, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) hosted in a Git repository that CircleCI can access.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md).
- Access to [CircleCI](https://circleci.com/).

## Single branch implementation

To automate code deploys to a Deployment using CircleCI, complete the following setup in a Git-based repository that hosts an Astro project:

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

