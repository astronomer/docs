---
sidebar_label: 'CI/CD'
title: 'Automate Code Deploys with CI/CD'
id: ci-cd
description: Create a CI/CD pipeline that triggers a deploy to Astro based on changes to your Airflow DAGs.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
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
- A Deployment ID. To find this, open your Deployment in the Cloud UI and copy the unique string at the end of the URL. For example, `cktogz2eg847343yzo9pru1b0d` is the Deployment ID in `https://cloud.astronomer.io/<workspace-ID>/deployments/cktogz2eg847343yzo9pru1b0d`. You can also find this value by running `astro deployment list` via the Astro CLI.
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions).
- An [Astro project](create-project.md) that is hosted in a place that your CI/CD tool can access.

## CI/CD Templates

The following section provides basic templates for configuring individual CI pipelines using popular CI/CD tools. Each template can be implemented as-is to produce a simple CI/CD pipeline, but we recommend reconfiguring the templates to work with your own directory structures, workflows, and best practices. More templates are coming soon.

At a high level, these CI/CD pipelines will:

1. Access Deployment API key credentials. These credentials must be set as OS-level environment variables called `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
2. Install the latest version of the Astro CLI.
3. Run `astro deploy`. This creates a Docker image for your Astro project, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment.

This workflow is equivalent to the following bash script:

```sh
# Set Deployment API key credentials as environment variables
$ export ASTRONOMER_KEY_ID="<your-api-key-id>"
$ export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"

# Install the latest version of Astro CLI
$ brew install astronomer/tap/astro

# Build your Astro project into a Docker image and push the image to your Deployment
$ astro deploy <your-deployment-id>
```

:::info

The following templates use [Astro CLI v1.0+](cli/release-notes.md) to deploy via CI/CD. These templates will not work if you use the `astrocloud` executable. To upgrade, see [Install the Astro CLI](cli/configure-cli.md).

:::

### GitHub Actions

<Tabs
    defaultValue="standard"
    values={[
        {label: 'Standard', value: 'standard'},
        {label: 'Multi-branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRONOMER_KEY_ID` = `<your-key-id>`
   - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
   - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

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
            brew install astronomer/tap/astro
            astro deploy ${{ secrets.ASTRONOMER_DEPLOYMENT_ID }}
    ```

</TabItem>

<TabItem value="multibranch">

The following setup can be used to create a multi-branch CI/CD pipeline using GitHub Actions. A multi-branch pipeline makes can be used to test DAGs in a development Deployment and promote them to a production Deployment. The finished pipeline would deploy your code to Astro as demonstrated in the following diagram:

![Diagram showing how a multibranch CI/CD pipeline works](/img/docs/multibranch.png)

This setup assumes the following prerequisites:

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have unique [Deployment API keys and secrets](api-keys.md) for both of your Deployments.

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
   - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
   - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`
   - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
   - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
   - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy Code (Multiple Branches)

    on:
      push:
        branches: [dev]
      pull_request:
        types:
          - closed
        branches: [main]

    jobs:
      dev-push:
        if: github.ref == 'refs/heads/dev'
        env:
          ## Sets DEV Deployment API key credentials as environment variables
          ASTRONOMER_KEY_ID: ${{ secrets.DEV_ASTRONOMER_KEY_ID }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.DEV_ASTRONOMER_KEY_SECRET }}
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v2.3.4
        - name: Deploy to Astro
          run: |
            brew install astronomer/tap/astro
            astro deploy ${{ secrets.DEV_ASTRONOMER_DEPLOYMENT_ID }}
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        env:
          ## Sets PROD Deployment API key credentials as environment variables
          ASTRONOMER_KEY_ID: ${{ secrets.PROD_ASTRONOMER_KEY_ID }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.PROD_ASTRONOMER_KEY_SECRET }}
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v2.3.4
        - name: Deploy to Astro
          run: |
            brew install astronomer/tap/astro
            astro deploy ${{ secrets.PROD_ASTRONOMER_DEPLOYMENT_ID }}
    ```

</TabItem>

<TabItem value="custom">

If your Astro project uses a custom Runtime image with additional build-time arguments, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Prerequisites

To complete this setup, you need:

- An Astro project that builds a custom Runtime image.

#### Setup

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

  - `ASTRONOMER_KEY_ID` = `<your-key-id>`
  - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
  - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Custom base image

    on:
      push:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest
        env:
          ASTRONOMER_KEY_ID: ${{ secrets.ASTRO_ACCESS_KEY_ID_DEV }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.ASTRO_SECRET_ACCESS_KEY_DEV }}
        steps:
        - name: Check out the repo
          uses: actions/checkout@v2
        - name: Build Dockerfile.build image
          uses: docker/build-push-action@v2
          with:
            # This image tag must match the image tag in the FROM line of your `Dockerfile`.
            tags: custom-<astro-runtime-image>
            load: true
            file: Dockerfile.build
            # Define your custom image's build arguments, contexts, and connections here using
            # the available GitHub Action settings:
            # https://github.com/docker/build-push-action#customizing .
            # This example uses `build-args` , but your use case might require configuring
            # different values.
            build-args: |
              <your-build-arguments>
        - name: Deploy to Astro
          run: |
            brew install astronomer/tap/astro
            astro deploy ${{ secrets.ASTRONOMER_DEPLOYMENT_ID }}
    ```

    For example, to create a CI/CD pipeline that deploys a project which [installs Python packages from a private GitHub repository](develop-project.md#install-python-packages-from-private-sources), you would use the following configuration:

    ```yaml
    name: Astronomer CI - Custom base image

    on:
      push:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest
        env:
          ASTRONOMER_KEY_ID: ${{ secrets.ASTRO_ACCESS_KEY_ID_DEV }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.ASTRO_SECRET_ACCESS_KEY_DEV }}
        steps:
        - name: Check out the repo
          uses: actions/checkout@v2
        - name: Create SSH Socket
          uses: webfactory/ssh-agent@v0.5.4
          with:
            # GITHUB_SSH_KEY must be defined as a GitHub secret.
            ssh-private-key: ${{ secrets.GITHUB_SSH_KEY }}
        - name: (Optional) Test SSH Connection - Should print hello message.
          run: (ssh git@github.com) || true
        - name: Build Dockerfile.build image
          uses: docker/build-push-action@v2
          with:
            # This image tag must match the image tag in the FROM line of your `Dockerfile`.
            tags: custom-<astro-runtime-image>
            load: true
            file: Dockerfile.build
            ssh: |
              github=${{ env.SSH_AUTH_SOCK }
        - name: Deploy to Astro
          run: |
            brew install astronomer/tap/astro
            astro deploy ${{ secrets.ASTRONOMER_DEPLOYMENT_ID }}
    ```

  :::info

  If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

  :::

</TabItem>
</Tabs>

### Jenkins

To automate code deploys to a single Deployment using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astro project:

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
                   sh 'curl -sSL install.astronomer.io | sudo bash -s'
                   sh 'astro deploy ${siteVariables.deploymentid} -f'
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
                curl -sSL install.astronomer.io | sudo bash -s
                astro deploy ${siteVariables.deploymentid} -f

    # Invoke jobs via workflows
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
    `}</code></pre>

### Drone

To automate code deploys to a Deployment using a Docker-based [Drone CI](https://www.drone.io/) pipeline, complete the following setup in a Git-based repository that hosts an Astro project.

#### Prerequisites

This pipeline configuration requires:

- A functional Drone [server](https://docs.drone.io/server/overview/) and [Docker runner](https://docs.drone.io/runner/docker/overview/).
- A user with admin privileges to your Drone server.

1. Set the following environment variables as repository-level [secrets](https://docs.drone.io/secret/repository/) on Drone:

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
    - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. In your Drone server, open your Astro project repository and go to **Settings** > **General**. Under **Project Settings**, turn on the **Trusted** setting.

3. In the top level of your Git repository, create a file called `.drone.yml` that includes the following configuration:

    <pre><code parentName="pre">{`---
    kind: pipeline
    type: docker
    name: deploy

    steps:
      - name: install
        image: debian
        commands:
        - apt-get update
        - apt-get -y install curl
        - curl -sSL install.astronomer.io | sudo bash -s
      - name: wait
        image: docker:dind
        volumes:
        - name: dockersock
          path: /var/run
        commands:
        - sleep 5
      - name: deploy
        image: docker:dind
        volumes:
        - name: dockersock
          path: /var/run
        commands:
        - astro deploy ${siteVariables.deploymentiddrone} -f
        depends on:
        - wait

        environment:
          ASTRONOMER_KEY_ID:
            from_secret: ASTRONOMER_KEY_ID
          ASTRONOMER_KEY_SECRET:
            from_secret: ASTRONOMER_KEY_SECRET
          ASTRONOMER_DEPLOYMENT_ID:
            from_secret: ASTRONOMER_DEPLOYMENT_ID

    services:
    - name: docker
      image: docker:dind
      privileged: true
      volumes:
      - name: dockersock
        path: /var/run

    volumes:
    - name: dockersock
      temp: {}

    trigger:
      branch:
      - main
      event:
      - push
    `}</code></pre>

### GitLab

To automate code deploys to a Deployment using [GitLab](https://gitlab.com/), complete the following setup in your GitLab repository that hosts an Astro project:

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`
    - `ASTRONOMER_DEPLOYMENT_ID` = `<your-astro-deployment-id>`

2. Go to the Editor option in your project's CI/CD section and commit the following:

   <pre><code parentName="pre">{`---
      astro_deploy:
      stage: deploy
      image: docker:latest
      services:
       - docker:dind
      variables:
         ASTRONOMER_KEY_ID: $ASTRONOMER_KEY_ID
         ASTRONOMER_KEY_SECRET: $ASTRONOMER_KEY_SECRET
      before_script:
       - apk add --update curl && rm -rf /var/cache/apk/*
       - apk add bash
      script:
       - curl -sSL install.astronomer.io | bash -s
       - astro deploy $ASTRONOMER_DEPLOYMENT_ID -f
      only:
       - main
   `}</code></pre>

### GitLab (Multiple Branches)

To automate code deploys to Astro across multiple environments using [GitLab](https://gitlab.com/), complete the following setup in your GitLab repository that hosts an Astro project:

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
    - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
    - `DEV_ASTRONOMER_DEPLOYMENT_ID` = `<your-dev-astro-deployment-id>`
    - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
    - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
    - `PROD_ASTRONOMER_DEPLOYMENT_ID` = `<your-prod-astro-deployment-id>`

:::caution

When you create environment variables that will be used in multiple branches, you may want to protect the branch they are being used in. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. For more information on protected branches, see [GitLab documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html#configure-a-protected-branch).

:::

2. Go to the Editor option in your project's CI/CD section and commit the following:

   <pre><code parentName="pre">{`---
      astro_deploy_dev:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRONOMER_KEY_ID: $DEV_ASTRONOMER_KEY_ID
            ASTRONOMER_KEY_SECRET: $DEV_ASTRONOMER_KEY_SECRET
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
        script:
          - curl -sSL install.astronomer.io | bash -s
          - astro deploy $DEV_ASTRONOMER_DEPLOYMENT_ID -f
        only:
          - dev

      astro_deploy_prod:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRONOMER_KEY_ID: $PROD_ASTRONOMER_KEY_ID
            ASTRONOMER_KEY_SECRET: $PROD_ASTRONOMER_KEY_SECRET
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
        script:
          - curl -sSL install.astronomer.io | bash -s
          - astro deploy $PROD_ASTRONOMER_DEPLOYMENT_ID -f
        only:
          - main
   `}</code></pre>
