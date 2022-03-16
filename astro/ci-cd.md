---
sidebar_label: 'CI/CD'
title: 'Automate Code Deploys with CI/CD'
id: ci-cd
description: Create a CI/CD pipeline that triggers a deploy to Astro based on changes to your Airflow DAGs.
---

import {siteVariables} from '@site/src/versions';

## Overview

This guide provides setup steps for configuring a CI/CD pipeline to deploy DAGs on Astro.

There are many benefits to deploying DAGs and other changes to Airflow via a CI/CD workflow. Specifically, you can:

- Deploy new and updated DAGs in a way that streamlines the development process amongst team members.
- Decrease the maintenance cost of integrating changes, allowing your team to quickly respond in case of an error or failure.
- Enforce continuous, automating testing, which increases code quality and protects your DAGs in production.

## Prerequisites

To set up CI/CD for a given Deployment, you need:

- A [Deployment API key ID and secret](api-keys.md)
- A Deployment ID. To find this, open your Deployment in the Cloud UI and copy the unique string at the end of the URL. For example, `cktogz2eg847343yzo9pru1b0d` is the Deployment ID in `https://cloud.astronomer.io/<workspace-ID>/deployments/cktogz2eg847343yzo9pru1b0d`. You can also find this value by running `astrocloud deployment list` via the Astro CLI.
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions).
- An [Astro project](create-project.md) that is hosted in a place that your CI/CD tool can access.

## CI/CD Templates

The following section provides basic templates for configuring individual CI pipelines using popular CI/CD tools. Each template can be implemented as-is to produce a simple CI/CD pipeline, but we recommend reconfiguring the templates to work with your own directory structures, workflows, and best practices. More templates are coming soon.

At a high level, these CI/CD pipelines will:

1. Access Deployment API key credentials. These credentials must be set as OS-level environment variables called `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
2. Install the latest version of the Astro CLI.
3. Run `astrocloud deploy`. This builds your Astro project into a Docker image, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment.

This workflow is equivalent to the following bash script:

```sh
# Set Deployment API key credentials as environment variables
$ export ASTRONOMER_KEY_ID="<your-api-key-id>"
$ export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"

# Install the Astro CLI
$ brew install astronomer/cloud/astrocloud@1.2.0

# Build your Astro project into a Docker image and push the image to your Deployment
$ astrocloud deploy <your-deployment-id>
```

:::info

The following templates use `brew install` to install the latest version of the Astro CLI for every deploy. For a more stable CI/CD pipeline, you can install only a specific version of the CLI by tagging a specific version in the command:

```sh
brew install astronomer/cloud/astrocloud@<version-number>
```

:::

### GitHub Actions

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRONOMER_KEY_ID` = `<your-key-id>`
   - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
   - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. Create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy Code

    on:
      push:
        branches:
          - main

    env:
      ## Sets Deployment API key credentials as environment variables
      ASTRONOMER_KEY_ID: ${{ secrets.ASTRONOMER_KEY_ID }}
      ASTRONOMER_KEY_SECRET: ${{ secrets.ASTRONOMER_KEY_SECRET }}

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v2.3.4
        - name: Deploy to Astro
          run: |
            brew install astronomer/cloud/astrocloud
            astrocloud deploy ${{ secrets.ASTRONOMER_DEPLOYMENT_ID }}
    ```

### Jenkins

To automate code deploys to a single Deployment using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astronomer project:

1. In your Jenkins pipeline configuration, add the following environment variables:

    - `ASTRONOMER_DEPLOYMENT_ID`: Your Astro Deployment ID
    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script, making sure to replace `<deployment-id>` with your own Deployment ID:

    <pre><code parentName="pre">{`pipeline {
      agent any
        stages {
          stage('Deploy to Astronomer') {
           when {
            expression {
              return env.GIT_BRANCH == "origin/main"
            }
           }
           steps {
             script {
                   sh 'curl https://goreleaserdev.blob.core.windows.net/goreleaser-test-container/releases/${siteVariables.cliVersion}/cloud-cli_${siteVariables.cliVersion}_Linux_x86_64.tar.gz -o astrocloudcli.tar.gz'
                   sh 'tar xzf astrocloudcli.tar.gz'
                   sh './astrocloud deploy ${siteVariables.deploymentid} -f'
             }
           }
         }
       }
     post {
       always {
         cleanWs()
       }
      }
    }
    `}</code></pre>

    This Jenkinsfile triggers a code push to Astro every time a commit or pull request is merged to the `main` branch of your repository.

### CircleCI

To automate code deploys to a Deployment using [CircleCI](https://circleci.com/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables in a [CircleCI context](https://circleci.com/docs/2.0/contexts/):

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
    - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. Create a new YAML file in `.circleci/config.yml` that includes the following configuration:

    <pre><code parentName="pre">{`# Use the latest 2.1 version of CircleCI pipeline process engine.
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
                echo export ASTRONOMER_KEY_ID=${siteVariables.keyid} >> $BASH_ENV
                echo export ASTRONOMER_KEY_SECRET=${siteVariables.keysecret} >> $BASH_ENV
          - run:
              name: "Deploy to Astro"
              command: |
                curl https://goreleaserdev.blob.core.windows.net/goreleaser-test-container/releases/v${siteVariables.cliVersion}/cloud-cli_${siteVariables.cliVersion}_Linux_x86_64.tar.gz -o astrocloudcli.tar.gz
                tar xzf astrocloudcli.tar.gz
                ./astrocloud deploy ${siteVariables.deploymentid} -f

    # Invoke jobs via workflows
    # See: https://circleci.com/docs/2.0/configuration-reference/#workflows
    workflows:
      version: 2.1
      build-and-deploy-prod:
        jobs:
          - build_image_and_deploy:
              context:
                 - cs-poc
             filters:
               branches:
                 only:
                   - main
    `}</code></pre>
