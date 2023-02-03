---
sidebar_label: 'CI/CD'
title: 'Configure CI/CD on Astronomer Software'
id: ci-cd
description: Automate the deploy process to your Airflow Deployment on Astronomer Software.
---

Users can push code and deploy to an Airflow Deployment on Astronomer using a Continuous Integration/Continuous Delivery (CI/CD) tool.

There are many benefits to deploying DAGs and other changes to Airflow via a CI/CD workflow. Specifically, you can:

- Deploy new and updated DAGs in a way that streamlines the development process amongst team members.
- Decrease the maintenance cost of integrating changes, allowing your team to quickly respond in case of an error or failure.
- Enforce continuous, automating testing, which increases code quality and protects your DAGs in production.

This guide will walk you through configuring a CI/CD pipeline on Astronomer.

### Example CI/CD workflow

Consider an Astro project hosted on GitHub and deployed to Astronomer. In this scenario, a set of `dev` and `main` branches of an Astro project are hosted on a single GitHub repository, and `dev` and `prod` Airflow Deployments are hosted on an Astronomer Workspace.

Using CI/CD, you can automatically deploy DAGs to your Airflow Deployment on Astronomer by pushing or merging code to a corresponding branch in GitHub. The general setup would look something like this:

1. Create two Airflow Deployments within your Astronomer Workspace, one for `dev` and one for `prod`.
2. Create a repository in GitHub that hosts project code for all Airflow Deployments within your Astronomer Workspace.
3. In your GitHub code repository, create a `dev` branch off of your `main` branch.
4. Configure your CI/CD tool to deploy to your `dev` Airflow Deployment whenever you push to your `dev` branch, and to deploy to your `prod` Airflow Deployment whenever you merge your `dev` branch into `main`.

That would look something like this:

![CI/CD Workflow Diagram](/img/software/ci-cd-flow.png)

### CI/CD on Astronomer

Automating the deploy process to Astronomer starts with creating a Service Account, which will assume a user role and some set of permissions to your Workspace or Deployment.

From there, you'll write a script that allows your service account to do the following:

- Build and tag a Docker Image
- Authenticate to a Docker Registry
- Push your image to that Docker Registry

From there, a webhook triggers an update to your Airflow Deployment using the CI/CD tool of your choice. The Astro CLI completes an authentication and push for every manual `$ astro deploy` command.

The rest of this guide describes how to create a service account and what your CI/CD script should look like based on the tool you're using.

:::info

If you're using BuildKit with the [Buildx plugin](https://github.com/docker/buildx), you need to add the `--provenance=false` flag to your `docker buildx build` commands.

:::

## Prerequisites

Before completing this setup, make sure you:

- Have access to a running Airflow Deployment on Astronomer.
- Installed the [Astro CLI](https://github.com/astronomer/astro-cli).
- Are familiar with your CI/CD tool of choice.

## Step 1: Create a service account

In order to authenticate your CI/CD pipeline to Astronomer's private Docker registry, you'll need to create a service account and grant it an appropriate set of permissions. You can do so via the Software UI or CLI. Once created, you can always delete this service account at any time. In both cases, creating a service account will generate an API key that will be used for the CI/CD process.

Note that you're able to create Service Accounts at the:

- Workspace Level
- Airflow Deployment Level

Creating a service account at the Workspace level allows you to deploy to *multiple* Airflow deployments with one code push, while creating them at the Deployment level ensures that your CI/CD pipeline only deploys to one particular deployment on Astronomer.

Read below for guidelines on how to create a service account via the CLI and via the Software UI.

### Create a service account using the CLI

#### Deployment level service account

To create a Deployment Level Service account via the CLI, first run:

```bash
astro deployment list
```

This will output the list of running Airflow deployments you have access to, and their corresponding UUID.

With that UUID, run:

```bash
astro deployment service-account create -d <deployment-id> --label <service-account-label> --role <deployment-role>
```

#### Workspace level service account

To create a Workspace Level Service account via the CLI, first run:

```bash
astro workspace list
```

This will output the list of running Astronomer Workspaces you have access to, and their corresponding UUID.

With that UUID, run:

```bash
astro workspace service-account create -w <workspace-id> --label <service-account-label> --role <workspace-role>
```

### Create a service account using the Software UI

If you prefer to provision a service account through the Software UI, start by logging into Astronomer.

#### Go to your Deployment's "Configure" page

From the Software UI, navigate to: `Deployment` > `Service Accounts`

![New Service Account](/img/software/ci-cd-new-service-account.png)

#### Configure your service account

Upon creating a Service Account, make sure to:

* Give it a Name
* Give it a Category (optional)
* Grant it a User Role

> **Note:** In order for a service account to have permission to push code to your Airflow Deployment, it must have either the "Editor" or "Admin" role. For more information on Workspace roles, refer to our ["Roles and Permissions"](workspace-permissions.md) doc.

![Name Service Account](/img/software/ci-cd-name-service-account.png)

#### Copy the API key

Once you've created your new Service Account, grab the API key that was immediately generated. Depending on your use case, you might want to store this key in an Environment Variable or secret management tool of choice.

> **Note:** This API key will only be visible during the session.

![Service Account](/img/software/ci-cd-api-key.png)

## Step 2: Authenticate and push to Docker

The first step of this pipeline will authenticate against the Docker registry that stores an individual Docker image for every code push or configuration change:

```bash
docker login registry.${BASE_DOMAIN} -u _ -p $${API_KEY_SECRET}
```

In this example:

- `BASE_DOMAIN` = The domain at which your Software instance is running
- `API_KEY_SECRET` = The API key that you got from the CLI or the UI and stored in your secret manager

### Building and pushing an image

Once you are authenticated you can build, tag and push your Airflow image to the private registry, where a webhook will trigger an update to your Airflow Deployment on the platform.

> **Note:** To deploy successfully to Astronomer, the version in the `FROM` statement of your project's Dockerfile must be the same as the version of Airflow specified in your Astronomer Deployment. For more information on upgrading, read [Upgrade Airflow](manage-airflow-versions.md).

#### Registry address

*Registry Address* tells Docker where to push images to. On Astronomer Software, your private registry is located at `registry.${BASE_DOMAIN}`.

#### Release name

*Release Name* refers to the release name of your Airflow Deployment. It will follow the pattern of `spaceyword-spaceyword-4digits` (e.g. `infrared-photon-7780`).

#### Tag name

*Tag Name*: Each deploy to Astronomer generates a Docker image with a corresponding tag. If you deploy via the CLI, the tag will by default read `deploy-n`, with `n` representing the number of deploys made to that Airflow Deployment. If you're using CI/CD, you get to customize this tag. We typically recommend specifying the source and the build number in the name.

In the example below, we use the prefix `ci-` and the ENV `${DRONE_BUILD_NUMBER}`. This guarantees that we always know which CI/CD build triggered the build and push.

Example:

```bash
docker build -t registry.${BASE_DOMAIN}/${RELEASE_NAME}/airflow:ci-${DRONE_BUILD_NUMBER} .
```

If you would like to see a more complete working example please visit our [full example using Drone-CI](https://github.com/astronomer/airflow-example-dags/blob/main/.drone.yml).

### Run unit tests

For CI/CD pipelines that push code to a production Deployment, Astronomer recommends adding a unit test after the image build step to ensure that you don't push a Docker image with breaking changes. To run a basic unit test, add a step in your CI/CD pipeline that executes `docker run` and then runs `pytest tests` in a container that is based on your newly built image before it's pushed to your registry.

For example, you can add the following command as a step in a [Drone](ci-cd.md#DroneCI) pipeline:

> **Note:** `BASE_DOMAIN` and `RELEASE_NAME` are pre-configured environment variables in the CI/CD tool, and `DRONE_BUILD_NUMBER` is an environment variable provided by the job execution in DroneCI.

```bash
docker run --rm registry.${BASE_DOMAIN}/${RELEASE_NAME}/airflow:ci-${DRONE_BUILD_NUMBER} /bin/bash -c "pytest tests"
```

## Step 3: Configure your CI/CD pipeline

Depending on your CI/CD tool, configuration will be slightly different. This section will focus on outlining what needs to be accomplished, not the specifics of how.

At its core, your CI/CD pipeline will first authenticate to Astronomer's private registry and then build, tag and push your Docker image to that registry.

## Example implementation

The following setup is an example implementation of CI/CD using GitHub Actions. These steps cover both the implementation and the workflow necessary to create a fully functional CI/CD pipeline.

1. Create a GitHub repository for an Astro project. Ensure your repo has a development branch and a main branch. In this example, the branches are named `dev` and `main`.
2. Create two [Deployment-level service accounts](ci-cd.md#step-1-create-a-service-account): One for your Dev Deployment and one for your Production Deployment.
3. Follow instructions in [GitHub documentation](https://docs.github.com/en/actions/reference/encrypted-secrets) to add your service accounts as secrets to your repository. In the example below, these secrets are named `SERVICE_ACCOUNT_KEY` and `SERVICE_ACCOUNT_KEY_DEV`.
4. Go to the Actions tab of your GitHub repo and create a new action with a `main.yml` file. To achieve the recommended workflow described in [Overview](ci-cd.md#overview), use the following action:

    ```yaml
    name: Astronomer CI - Deploy code
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
        runs-on: ubuntu-latest
        steps:
        - name: Check out the repo
          uses: actions/checkout@v3
        - name: Log in to registry
          uses: docker/login-action@v1
          with:
            registry: registry.${BASE_DOMAIN}
            username: _
            password: ${{ secrets.SERVICE_ACCOUNT_KEY_DEV }}
        - name: Build image
          run: docker build -t registry.${BASE_DOMAIN}/<dev-release-name>/airflow:ci-${{ github.sha }} .
        - name: Run tests
          run: docker run --rm registry.${BASE_DOMAIN}/<dev-release-name>/airflow:ci-${{ github.sha }} /bin/bash -c "pytest tests"
        - name: Push image
          run: docker push registry.${BASE_DOMAIN}/<dev-release-name>/airflow:ci-${{ github.sha }}
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        runs-on: ubuntu-latest
        steps:
        - name: Check out the repo
          uses: actions/checkout@v3
        - name: Log in to registry
          uses: docker/login-action@v1
          with:
            registry: registry.${BASE_DOMAIN}
            username: _
            password: ${{ secrets.SERVICE_ACCOUNT_KEY }}
        - name: Build image
          run: docker build -t registry.${BASE_DOMAIN}/<prod-release-name>/airflow:ci-${{ github.sha }} .
        - name: Run tests
          run: docker run --rm registry.${BASE_DOMAIN}/<prod-release-name>/airflow:ci-${{ github.sha }} /bin/bash -c "pytest tests"
        - name: Push image
          run: docker push registry.${BASE_DOMAIN}/<prod-release-name>/airflow:ci-${{ github.sha }}
    ```

    Ensure the branches match the names of the branches in your repository, and replace `<dev-release-name>` and `<prod-release-name>` with the respective release names of your development and production Airflow Deployments on Astronomer.

5. Test the GitHub Action by making a change on your `dev` branch and committing that change. This should update your development Airflow Deployment on Astronomer, which you can confirm in the Software UI. If that update was successful, try opening a pull request and then merging `dev` into `main` to update your production Airflow Deployment. If both updates were successful, you now have a functioning, scalable CI/CD pipeline that can automatically deploy code to multiple Airflow Deployments.

> **Note:** The prod-push action as defined here will only run after merging a pull request from the `dev` branch as we recommend.
>
>To further restrict this pipeline, you can add branch protection settings in GitHub to limit whether your users can push directly to the `main` branch within your repository or your CI tool, or you can modify the action as needed.

The following sections provide basic templates for configuring single CI/CD pipelines using popular CI/CD tools. Each template can be implemented to produce a simple CI/CD pipeline similar to the one above, but they can also be reconfigured to manage any number of branches or Deployments based on your needs.

## DroneCI

```yaml
pipeline:
  build:
    image: quay.io/astronomer/ap-build:latest
    commands:
      - docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${DRONE_BUILD_NUMBER} .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      event: push
      branch: [ master, release-* ]

  test:
    image: quay.io/astronomer/ap-build:latest
    commands:
      - docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${DRONE_BUILD_NUMBER} /bin/bash -c "pytest tests"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      event: push
      branch: [ master, release-* ]

  push:
    image: quay.io/astronomer/ap-build:latest
    commands:
      - echo $${SERVICE_ACCOUNT_KEY}
      - docker login registry.$BASE_DOMAIN -u _ -p $SERVICE_ACCOUNT_KEY
      - docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${DRONE_BUILD_NUMBER}
    secrets: [ SERVICE_ACCOUNT_KEY ]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      event: push
      branch: [ master, release-* ]
```

## CircleCI

```yaml
# Python CircleCI 2.0 configuration file
#
# Check https://circleci.com/docs/2.0/language-python/ for more details
#
version: 2
jobs:
  build:
    machine: ubuntu-2004:202008-01
    steps:
      - checkout
      - restore_cache:
          keys:
          - v1-dependencies-{{ checksum "requirements.txt" }}
          # fallback to using the latest cache if no exact match is found
          - v1-dependencies-
      - run:
          name: Install test deps
          command: |
            # Use a virtual env to encapsulate everything in one folder for
            # caching. And make sure it lives outside the checkout, so that any
            # style checkers don't run on all the installed modules
            python -m venv ~/.venv
            . ~/.venv/bin/activate
            pip install -r requirements.txt
      - save_cache:
          paths:
            - ~/.venv
          key: v1-dependencies-{{ checksum "requirements.txt" }}
      - run:
          name: run linter
          command: |
            . ~/.venv/bin/activate
            pycodestyle .
  deploy:
    docker:
      - image:  docker:18.09-git
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Push to Docker Hub
          command: |
            TAG=0.1.$CIRCLE_BUILD_NUM
            docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$TAG .
            docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$TAG /bin/bash -c "pytest tests"
            docker login registry.$BASE_DOMAIN -u _ -p $SERVICE_ACCOUNT_KEY
            docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$TAG

workflows:
  version: 2
  build-deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only:
                - master
```

## Jenkins Script

```yaml
pipeline {
    agent any
    stages {
        stage('Deploy to astronomer') {
            when { branch 'master' }
            steps {
                script {
                    sh 'docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BUILD_NUMBER} .'
                    sh 'docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BUILD_NUMBER} /bin/bash -c "pytest tests'
                    sh 'docker login registry.$BASE_DOMAIN -u _ -p $SERVICE_ACCOUNT_KEY'
                    sh 'docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BUILD_NUMBER}'
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
```

## Bitbucket

If you are using [Bitbucket](https://bitbucket.org/), this script should work (courtesy of our friends at [Das42](https://www.das42.com/))

```yaml
image: quay.io/astronomer/ap-build:latest

pipelines:
  branches:
    master:
      - step:
          name: Deploy to production
          deployment: production
          script:
            - echo ${SERVICE_ACCOUNT_KEY}
            - docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BITBUCKET_BUILD_NUMBER} .
            - docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BITBUCKET_BUILD_NUMBER} /bin/bash -c "pytest tests"
            - docker login registry.$BASE_DOMAIN -u _ -p $SERVICE_ACCOUNT_KEY
            - docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${BITBUCKET_BUILD_NUMBER}
          services:
            - docker
          caches:
            - docker
```

## Gitlab

```yaml
astro_deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  script:
    - echo "Building container.."
    - docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:CI-$CI_PIPELINE_IID .
    - docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:CI-$CI_PIPELINE_IID /bin/bash -c "pytest tests"
    - docker login registry.$BASE_DOMAIN -u _ -p $SERVICE_ACCOUNT_KEY
    - docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:CI-$CI_PIPELINE_IID
  only:
    - master
```

## AWS Codebuild

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: latest

  pre_build:
    commands:
      - echo Logging in to dockerhub ...
      - docker login "registry.$BASE_DOMAIN" -u _ -p "$API_KEY_SECRET"
      - export GIT_VERSION="$(git rev-parse --short HEAD)"
      - echo "GIT_VERSION = $GIT_VERSION"
      - pip install -r requirements.txt

  build:
    commands:
      - docker build -t "registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$GIT_VERSION" .
      - docker run --rm "registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$GIT_VERSION" /bin/bash -c "pytest tests"
      - docker push "registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-$GIT_VERSION"
```

## GitHub Actions CI/CD

GitHub supports a growing set of native CI/CD features in ["GitHub Actions"](https://github.com/features/actions), including a "Publish Docker" action that works well with Astronomer.

To use GitHub Actions on Astronomer, create a new action in your repo at `.github/workflows/main.yml` with the following:

```yaml
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out the repo
      uses: actions/checkout@v3
    - name: Log in to registry
      uses: docker/login-action@v1
      with:
        registry: registry.$BASE_DOMAIN
        username: _
        password: ${{ secrets.SERVICE_ACCOUNT_KEY }}
    - name: Build image
      run: docker build -t registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${{ github.sha }} .
    - name: Run tests
      run: docker run --rm registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${{ github.sha }} /bin/bash -c "pytest tests"
    - name: Push image
      run: docker push registry.$BASE_DOMAIN/$RELEASE_NAME/airflow:ci-${{ github.sha }}
```

> **Note:** Make sure to replace `$RELEASE_NAME` in the example above with your deployment's release name and to store your service account Key in your GitHub repo's secrets according to [this GitHub guide]( https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables).

## Azure DevOps

In this example configuration, you can automatically deploy your Astro project from a GitHub repository using an [Azure Devops](https://azure.microsoft.com/en-us/services/devops/) pipeline connected to the GitHub repository.

:::tip

To see an example GitHub project that utilizes this configuration, visit [Astronomer's GitHub](https://github.com/astronomer/cs-tutorial-azuredevops)

:::

To set up this workflow, make sure you have:

- A GitHub repository hosting your Astro project.
- An Azure DevOps account with permissions to create new pipelines.

1. Create a new file called `astro-devops-cicd.yaml` in your Astro project repository with the following configuration:

    ```yaml
    # Control which branches have CI triggers:
    trigger:
    - main

    # To trigger the build/deploy only after a PR has been merged:
    pr: none

    # Optionally use Variable Groups & Azure Key Vault:
    #variables:
    #- group: Variable-Group
    #- group: Key-Vault-Group

    stages:
    - stage: build
      jobs:
      - job: run_build
        pool:
          vmImage: 'Ubuntu-latest'
        steps:
        - script: |
            echo "Building container.."
            docker build -t registry.$(BASE-DOMAIN)/$(RELEASE-NAME)/airflow:$(Build.SourceVersion) .
            docker run --rm registry.$(BASE-DOMAIN)/$(RELEASE-NAME)/airflow:$(Build.SourceVersion) /bin/bash -c "pytest tests"
            docker login registry.$(BASE-DOMAIN) -u _ -p $(SVC-ACCT-KEY)
            docker push registry.$(BASE-DOMAIN)/$(RELEASE-NAME)/airflow:$(Build.SourceVersion)
    ```

2. Follow the steps in [Azure documentation](https://docs.microsoft.com/en-us/azure/devops-project/azure-devops-project-github#configure-access-to-your-github-repo-and-select-a-framework) to link your GitHub Repo and Action to an Azure pipeline. When prompted for the source code for your pipeline, specify that you have an existing Azure Pipelines YAML file and provide the setup tool with the file path to your `astro-devops-cicd.yaml` file.
3. Finish and save your Azure pipeline setup.
4. In Azure, [add environment variables](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch) for the following values:

    - `BASE-DOMAIN`: Your base domain for Astronomer
    - `RELEASE-NAME`: The release name for your Deployment
    - `SVC-ACCT-KEY`: The service account you created on Astronomer for CI/CD

    We recommend marking `SVC-ACCT-KEY` as secret.

Once you complete this setup, any merges on the main branch of your GitHub repo will trigger the pipeline and deploy your changes to Astronomer.
