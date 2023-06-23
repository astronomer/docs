---
sidebar_label: CircleCI
title: Astro CI/CD templates for CircleCI
id: circleci
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using CircleCI.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[CircleCI](https://circleci.com/) is a continuous integration and continuous delivery platform that can be used to implement DevOps practices. This document provides sample CI/CD templates to automate deploying Apache Airflow DAGs from a GitHub repository to Astro using CircleCI.

If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_. If your team builds custom Docker images, use the _custom image_ implementation.

Refer to [Template overview](template-overview.md) to see generic templates expressed as simple shell scripts or configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a Git repository that CircleCI can access.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- A [CircleCI](https://circleci.com/vcs-authorize/) account.

## Image-only templates

[Image-only deploy templates](template-overview.md#template-types) build a Docker image and push it to Astro whenever you update any file in your Astro project.

<Tabs
    defaultValue="standard"
    groupId= "image-only-templates"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a Deployment using CircleCI, complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables in a [CircleCI context](https://circleci.com/docs/2.0/contexts/):

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRO_DEPLOYMENT_ID`: The ID for your Deployment.

2. Create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    ```yaml
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
              name: "Deploy to Astro"
              command: |
                curl -sSL install.astronomer.io | sudo bash -s
                astro deploy ${ASTRO_DEPLOYMENT_ID} -f

    # Invoke jobs with workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      wf-build-and-deploy:
        jobs:
          - build_image_and_deploy:
              context:
                - <YOUR-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - <YOUR-BRANCH-NAME>
    ```

</TabItem>

<TabItem value="multibranch">

The following template can be used to create a multiple branch CI/CD pipeline using CircleCI. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. 

#### Configuration requirements

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.

#### Implementation

1. Set the following environment variables in both your production and development [CircleCI contexts](https://circleci.com/docs/2.0/contexts/):

   - `ASTRO_API_TOKEN` = `<your-workspace-or-organization-api-token-with-access-to-prod-deployment>`
   - `ASTRO_DEPLOYMENT_ID` = `<your-prod-deployment-id>`

2. Create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    ```yaml
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
              name: "Deploy to Astro"
              command: |
                curl -sSL install.astronomer.io | sudo bash -s
                astro deploy ${ASTRO_DEPLOYMENT_ID} -f

    # Invoke jobs with workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      wf_build-and-deploy:
        jobs:
          - build_image_and_deploy:
              context:
                - <YOUR-PROD-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - <YOUR-PRODUCTION-BRANCH-NAME>
        jobs:
          - build_image_and_deploy:
              context:
                - <YOUR-DEV-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - <YOUR-DEVELOPMENT-BRANCH-NAME>
    ```

Read more about multiple workflows in the [CircleCI documentation](https://circleci.com/docs/schedule-pipelines-with-multiple-workflows/).

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments in `docker build` command and then use the `image tag` to deploy to Astro. See [`docker build`](https://docs.docker.com/build/guide/build-args/) for reference.

#### Prerequisites

- An Astro project that uses additional build-time arguments in its Astro Runtime image.

#### Implementation

1. Set the following environment variables in a [CircleCI context](https://circleci.com/docs/2.0/contexts/):

   - `ASTRO_API_TOKEN` = `<your-workspace-or-organization-api-token-with-access-to-prod-deployment>`
   - `ASTRO_DEPLOYMENT_ID` = `<your-deployment-id>`

2. Create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    ```yaml
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
            name: "Build image and deploy"
            command: |
              set -e
              echo "export image_tag=astro-$(date +%Y%m%d%H%M%S)" >> $BASH_ENV
              source "$BASH_ENV"
              docker build -t ${image_tag} --build-arg="<your-build-arg>=<your-build-arg-value>" .
              curl -sSL install.astronomer.io | sudo bash -s
              astro deploy --image-name ${image_tag} ${ASTRO_DEPLOYMENT_ID} -f

    # Invoke jobs with workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      build-and-deploy-prod:
        jobs:
          - build_image_and_deploy_prod:
              context:
                - <YOUR-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - <YOUR-BRANCH-NAME>
    ```

  :::info

  If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

  :::

</TabItem>
</Tabs>

## DAG-based templates

A [DAG-based template](template-overview#dag-based-templates) uses the `--dags` flag in the Astro CLI `astro depoy` command to push only DAGs to your Deployment. This CI/CD pipeline deploys your DAGs only when files in your `dags` folder are modified whereas it deploys the rest of your Astro project as a Docker image when other files or directories are also modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

### Configuration requirements

For each Deployment that you use with DAG-based templates, you must [enable DAG deploys](deploy-code.md#deploy-dags-only).

### Single branch implementation

To automate code deploys to a Deployment using [CircleCI](https://circleci.com/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables in a [CircleCI context](https://circleci.com/docs/2.0/contexts/):

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRO_DEPLOYMENT_ID`: The ID for your Deployment.

2. In your project repository, create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    ```yaml
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
              name: "Build image and deploy"
              command: |
                curl -sSL install.astronomer.io | sudo bash -s
                files=($(git diff-tree HEAD --name-only --no-commit-id))
                echo ${files}
                find="dags"
                if [[ ${files[*]} =~ (^|[[:space:]])"$find"($|[[:space:]]) && ${#files[@]} -eq 1 ]]; then
                  echo "only deploying dags"
                  astro deploy ${ASTRO_DEPLOYMENT_ID} --dags -f;
                else
                  echo "image deploy"
                  astro deploy ${ASTRO_DEPLOYMENT_ID} -f;
                fi

    # Invoke jobs with workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      wf-build-and-deploy:
        jobs:
          - build_image_and_deploy:
              context:
                - <YOUR-CIRCLE-CI-CONTEXT>
              filters:
                branches:
                  only:
                    - <YOUR-BRANCH-NAME>
    ```

This script checks the diff between your current commit and the HEAD of your branch to which you are pushing the changes to. If the changes are only in `dags` then it will perform `dag-only` deploy else do an image based deploy. Make sure to customize the script to use your specific branch and context. 

You can customize this script to work for multiple branches as shown in the [image-based multi-branch deploy template](circleci?tab=multibranch#image-only-templates) by creating separate `job` and `workflow` for each branch.

