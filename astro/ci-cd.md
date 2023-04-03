---
sidebar_label: 'CI/CD Templates'
title: 'Automate code deploys with CI/CD'
id: ci-cd
toc_min_heading_level: 2
toc_max_heading_level: 3
---

<head>
  <meta name="description" content="Learn how to create a continuous integration and continuous delivery (CI/CD) pipeline that triggers a deployment to Astro when your Airflow DAGs are modified." />
  <meta name="og:description" content="Learn how to create a continuous integration and continuous delivery (CI/CD) pipeline that triggers a deployment to Astro when your Airflow DAGs are modified." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use the Astronomer CI/CD templates to automate code deployment to Astro with popular CI/CD management tools, including GitHub Actions and Circle CI. To decide which template is right for you, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions).
- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) that is hosted in a place that your CI/CD tool can access.

## Template types

Templates allow you to configure automated workflows using popular CI/CD tools. Each template can be implemented without changes to produce a CI/CD pipeline. However, Astronomer recommends reconfiguring the templates to work with your own directory structures, tools, and processes.

There are two workflow types, image-only workflows and DAG-based workflows. The following templates are available for each workflow type: 

- Single branch: Deploys a single branch from your version control tool to Astro. This is the default template for all CI/CD tools. 
- Multiple branch: Deploys multiple branches to separate Deployments on Astro.
- Custom image: Deploys an Astro project with a customized Runtime image and additional build arguments.

### Image-only workflows  

The image-only workflow builds a Docker image and pushes it to Astro whenever you update any file in your Astro project. This type of template works well for development workflows that include complex Docker customization or logic.

CI/CD templates that use image-only workflows do the following:

- Access Deployment API key credentials. These credentials must be set as OS-level environment variables named `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
- Install the latest version of the Astro CLI.
- Run `astro deploy`. This creates a Docker image for your Astro project, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment.

This is equivalent to running the following shell script:

```sh
# Set Deployment API key credentials as environment variables
$ export ASTRONOMER_KEY_ID="<your-api-key-id>"
$ export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"
# Install the latest version of Astro CLI
$ curl -sSL install.astronomer.io | sudo bash -s
# Build your Astro project into a Docker image and push the image to your Deployment
$ astro deploy
```

### DAG-based workflows

The DAG-based workflow uses the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

CI/CD templates that use the DAG-based workflow do the following:

- Access Deployment API key credentials. These credentials must be set as OS-level environment variables named `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
- Install the latest version of the Astro CLI.
- Determine which files were updated by the commit:
    - If only DAG files in the `dags` folder have changed, run `astro deploy --dags`. This pushes your `dags` folder to your Deployment.
    - If any file not in the `dags` folder has changed, run `astro deploy`. This triggers two subprocesses. One that creates a Docker image for your Astro project, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment. A second that pushes your `dags` folder to your Deployment.

This is equivalent to the following shell script: 

```sh
# Set Deployment API key credentials as environment variables
export ASTRONOMER_KEY_ID="<your-api-key-id>"
export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"
export DAG_FOLDER="<path to dag folder ie. dags/>"
# Install the latest version of Astro CLI
curl -sSL install.astronomer.io | sudo bash -s
# Determine if only DAG files have changes
files=$(git diff --name-only HEAD^..HEAD)
dags_only=1
for file in $files; do
  if [[ $file != "$DAG_FOLDER"* ]]; then
    echo "$file is not a dag, triggering a full image build"
    dags_only=0
    break
  fi
done
# If only DAGs changed deploy only the DAGs in your 'dags' folder to your Deployment
if [ $dags_only == 1 ]
then
    astro deploy --dags
fi
# If any other files changed build your Astro project into a Docker image, push the image to your Deployment, and then push and DAG changes
if [ $dags_only == 0 ]
then
    astro deploy
fi
```

## GitHub Actions

The following templates use the Astronomer-maintained [Deploy Action](https://github.com/astronomer/deploy-action) to deploy code to Astronomer. See the [Deploy Action README](https://github.com/astronomer/deploy-action#readme) to learn more about using and customizing this action.

### GitHub Actions (Image-only deploys)

<Tabs
    defaultValue="standard"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRONOMER_KEY_ID` = `<your-key-id>`
   - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code

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
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
    ```

</TabItem>

<TabItem value="multibranch">

The following setup can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. The finished pipeline would deploy your code to Astro as demonstrated in the following diagram:

![Diagram showing how a multibranch CI/CD pipeline works](/img/docs/multibranch.png)

This setup assumes the following prerequisites:

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have unique [Deployment API keys and secrets](api-keys.md) for both of your Deployments.

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
   - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
   - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
   - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code (Multiple Branches)

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
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        env:
          ## Sets PROD Deployment API key credentials as environment variables
          ASTRONOMER_KEY_ID: ${{ secrets.PROD_ASTRONOMER_KEY_ID }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.PROD_ASTRONOMER_KEY_SECRET }}
        runs-on: ubuntu-latest
        steps:
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
    ```

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Prerequisites

To complete this setup, you need:

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Setup

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

  - `ASTRONOMER_KEY_ID` = `<your-key-id>`
  - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Additional build-time args

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
          uses: actions/checkout@v3
        - name: Create image tag
          id: image_tag
          run: echo ::set-output name=image_tag::astro-$(date +%Y%m%d%H%M%S)
        - name: Build image
          uses: docker/build-push-action@v2
          with:
            tags: ${{ steps.image_tag.outputs.image_tag }}
            load: true
            # Define your custom image's build arguments, contexts, and connections here using
            # the available GitHub Action settings:
            # https://github.com/docker/build-push-action#customizing .
            # This example uses `build-args` , but your use case might require configuring
            # different values.
            build-args: |
              <your-build-arguments>
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            image-name: ${{ steps.image_tag.outputs.image_tag }}
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
          uses: actions/checkout@v3
        - name: Create image tag
          id: image_tag
          run: echo ::set-output name=image_tag::astro-$(date +%Y%m%d%H%M%S)
        - name: Create SSH Socket
          uses: webfactory/ssh-agent@v0.5.4
          with:
            # GITHUB_SSH_KEY must be defined as a GitHub secret.
            ssh-private-key: ${{ secrets.GITHUB_SSH_KEY }}
        - name: (Optional) Test SSH Connection - Should print hello message.
          run: (ssh git@github.com) || true
        - name: Build image
          uses: docker/build-push-action@v2
          with:
            tags: ${{ steps.image_tag.outputs.image_tag }}
            load: true
            ssh: |
              github=${{ env.SSH_AUTH_SOCK }
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            image-name: ${{ steps.image_tag.outputs.image_tag }}
    ```

  :::info

  If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

  :::

</TabItem>
</Tabs>

### GitHub Actions (DAG-based deploys)

The following templates are examples of how to implement DAG-only deploys in GitHub Actions. They use the [Deploy Actions](https://github.com/astronomer/deploy-action) `dag-deploy-enabled` option to implement a DAG-based deploy workflow.

<Tabs
    defaultValue="standard"
    groupId= "github-actions-dag-based-deploy"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multiple branch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRONOMER_KEY_ID` = `<your-key-id>`
   - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code

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
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            dag-deploy-enabled: true
    ```

This Github Actions script checks the diff between your current commit and your `main` branch when a commit is pushed to `main`. Make sure to customize the script for your specific use case. 

</TabItem>

<TabItem value="multiple branch">

The following setup can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. The finished pipeline deploys your code to Astro as demonstrated in the following diagram:

![Diagram showing how a multiple branch CI/CD pipeline works](/img/docs/multibranch.png)

This setup assumes the following prerequisites:

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have unique [Deployment API keys and secrets](api-keys.md) for both of your Deployments.

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
   - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`
   - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
   - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code (Multiple Branches)

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
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            dag-deploy-enabled: true
        
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        env:
          ## Sets PROD Deployment API key credentials as environment variables
          ASTRONOMER_KEY_ID: ${{ secrets.PROD_ASTRONOMER_KEY_ID }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.PROD_ASTRONOMER_KEY_SECRET }}
        runs-on: ubuntu-latest
        steps:
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            dag-deploy-enabled: true
    ```

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Prerequisites

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Setup

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

  - `ASTRONOMER_KEY_ID` = `<your-key-id>`
  - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Additional build-time args

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
          uses: actions/checkout@v3
        - name: Create image tag
          id: image_tag
          run: echo ::set-output name=image_tag::astro-$(date +%Y%m%d%H%M%S)
        - name: Build image
          uses: docker/build-push-action@v2
          with:
            tags: ${{ steps.image_tag.outputs.image_tag }}
            load: true
            # Define your custom image's build arguments, contexts, and connections here using
            # the available GitHub Action settings:
            # https://github.com/docker/build-push-action#customizing .
            # This example uses `build-args` , but your use case might require configuring
            # different values.
            build-args: |
              <your-build-arguments>
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.1
          with:
            image-name: ${{ steps.image_tag.outputs.image_tag }}
            dag-deploy-enabled: true
    ```

  :::info

  If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

  :::

</TabItem>
</Tabs>

## AWS CodeBuild

<Tabs
    defaultValue="awscodebuildstandard"
    groupId= "aws-codebuild"
    values={[
        {label: 'Single branch', value: 'awscodebuildstandard'},
        {label: 'Multiple branch', value: 'awscodebuildmultibranch'},
    ]}>
<TabItem value="awscodebuildstandard">

To automate code deploys to a single Deployment using [AWS CodeBuild](https://aws.amazon.com/codebuild/), complete the following setup in a Git-based repository hosting an Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [buildspec.yml](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example) file that includes the following script:

   ```yaml

   version: 0.2

   phases:
     install:
       runtime-versions:
         python: latest

     build:
       commands:
         - echo "${CODEBUILD_WEBHOOK_HEAD_REF}"
         - export ASTRONOMER_KEY_ID="${ASTRONOMER_KEY_ID}"
         - export ASTRONOMER_KEY_SECRET="${ASTRONOMER_KEY_SECRET}"
         - curl -sSL install.astronomer.io | sudo bash -s
         - astro deploy "${ASTRONOMER_DEPLOYMENT_ID}" -f

    ```

3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the source provider where your Astro project is hosted, such as BitBucket or GitHub. When configuring the webhook, select an event type of `PUSH`.

Your buildspec.yml file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.

</TabItem>

<TabItem value="awscodebuildmultibranch">

To automate code deploys across multiple Deployments using [AWS CodeBuild](https://aws.amazon.com/codebuild/), complete the following setup in a Git-based repository hosting an Astro project:

1. In your AWS CodeBuild pipeline configuration, add the following environment variables:

    - `PROD_ASTRONOMER_KEY_ID`: Your Production Deployment API key ID
    - `PROD_ASTRONOMER_KEY_SECRET`: Your Production Deployment API key secret
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your Production Deployment
    - `DEV_ASTRONOMER_KEY_ID`: Your Development Deployment API key ID
    - `DEV_ASTRONOMER_KEY_SECRET`: Your Development Deployment API key secret
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your Development Deployment

2. At the root of your Git repository, add a [buildspec.yml](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example) that includes the following script:

   ```yaml

   version: 0.2

   phases:
     install:
       runtime-versions:
         python: latest

     build:
       commands:
         - |
           if expr "${CODEBUILD_WEBHOOK_HEAD_REF}" : "refs/heads/main" >/dev/null; then
             export ASTRONOMER_KEY_ID="${PROD_ASTRONOMER_KEY_ID}"
             export ASTRONOMER_KEY_SECRET="${PROD_ASTRONOMER_KEY_SECRET}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${PROD_DEPLOYMENT_ID}" -f
           fi
         - |
           if expr "${CODEBUILD_WEBHOOK_HEAD_REF}" : "refs/heads/dev" >/dev/null; then
             export ASTRONOMER_KEY_ID="${DEV_ASTRONOMER_KEY_ID}"
             export ASTRONOMER_KEY_SECRET="${DEV_ASTRONOMER_KEY_SECRET}"
             curl -sSL install.astronomer.io | sudo bash -s
             astro deploy "${DEV_DEPLOYMENT_ID}" -f
           fi
    ```

   3. In your AWS CodeBuild project, create a [webhook event](https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html) for the source provider where your Astro project is hosted, such as BitBucket or GitHub. When configuring the webhook, select an event type of `PUSH`.

Your buildspec.yml file now triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `main` branch of your repository.

</TabItem>
</Tabs>

## Azure DevOps

To automate code deploys to a Deployment using [Azure DevOps](https://dev.azure.com/), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following environment variables as [DevOps pipeline variables](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch):

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. Create a new YAML file in `astro-devops-cicd.yaml` at the root of the repository that includes the following configuration:

    ```
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

## Bitbucket

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


## CircleCI

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

## Drone

To automate code deploys to a Deployment using a Docker-based [Drone CI](https://www.drone.io/) pipeline, complete the following setup in a Git-based repository that hosts an Astro project.

This pipeline configuration requires:

- A functional Drone [server](https://docs.drone.io/server/overview/) and [Docker runner](https://docs.drone.io/runner/docker/overview/).
- A user with admin privileges to your Drone server.

1. Set the following environment variables as repository-level [secrets](https://docs.drone.io/secret/repository/) on Drone:

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your Drone server, open your Astro project repository and go to **Settings** > **General**. Under **Project Settings**, turn on the **Trusted** setting.

3. In the top level of your Git repository, create a file called `.drone.yml` that includes the following configuration:

    ```
    ---
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
        - astro deploy -f
        depends on:
        - wait

        environment:
          ASTRONOMER_KEY_ID:
            from_secret: ASTRONOMER_KEY_ID
          ASTRONOMER_KEY_SECRET:
            from_secret: ASTRONOMER_KEY_SECRET

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
    ```

## GitLab


:::info

If you use hosted runners, you might need certain tags or modifications based on your Gitlab runner. Speak with your Gitlab administrator and review the [Gitlab Documentation](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html) to customize this template for your use case.

:::

<Tabs
    defaultValue="gitlabstandard"
    groupId= "gitlab"
    values={[
        {label: 'Single branch', value: 'gitlabstandard'},
        {label: 'Multiple branch', value: 'gitlabmultibranch'},
    ]}>
<TabItem value="gitlabstandard">

To automate code deploys to a Deployment using [GitLab](https://gitlab.com/), complete the following setup in your GitLab repository that hosts an Astro project:

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. Go to the Editor option in your project's CI/CD section and commit the following:

   ```
   ---
    astro_deploy:
      stage: deploy
      image: docker:latest
      services:
       - docker:dind
      variables:
         ASTRONOMER_KEY_ID: ${ASTRONOMER_KEY_ID}
         ASTRONOMER_KEY_SECRET: ${ASTRONOMER_KEY_SECRET}
      before_script:
       - apk add --update curl && rm -rf /var/cache/apk/*
       - apk add bash
      script:
       - (curl -sSL install.astronomer.io | bash -s)
       - astro deploy -f
      only:
       - main
   ```

</TabItem>

<TabItem value="gitlabmultibranch">

To automate code deploys to Astro across multiple environments using [GitLab](https://gitlab.com/), complete the following setup in your GitLab repository that hosts an Astro project:

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
    - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
    - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
    - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`

:::caution

When you create environment variables that will be used in multiple branches, you may want to protect the branch they are being used in. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. For more information on protected branches, see [GitLab documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html#configure-a-protected-branch).

:::

2. Go to the Editor option in your project's CI/CD section and commit the following:

   ```
   ---
      astro_deploy_dev:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRONOMER_KEY_ID: ${DEV_ASTRONOMER_KEY_ID}
            ASTRONOMER_KEY_SECRET: ${DEV_ASTRONOMER_KEY_SECRET}
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
          - apk add jq
        script:
          - (curl -sSL install.astronomer.io | bash -s)
          - astro deploy -f
        only:
          - dev

      astro_deploy_prod:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRONOMER_KEY_ID: ${PROD_ASTRONOMER_KEY_ID}
            ASTRONOMER_KEY_SECRET: ${PROD_ASTRONOMER_KEY_SECRET}
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
          - apk add jq
        script:
          - (curl -sSL install.astronomer.io | bash -s)
          - astro deploy -f
        only:
          - main
   ```


</TabItem>
</Tabs>

## Jenkins

You can automate code deploys to a single Deployment (image-only), or implement DAG-only deploys with [Jenkins](https://www.jenkins.io/).

### Jenkins (Image-only deploys)

<Tabs
    defaultValue="jenkinsstandard"
    groupId= "jenkins"
    values={[
        {label: 'Single branch', value: 'jenkinsstandard'},
        {label: 'Multiple branch', value: 'jenkinsmultibranch'},
    ]}>
<TabItem value="jenkinsstandard">

To automate code deploys to a single Deployment using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astro project:

1. In your Jenkins pipeline configuration, add the following parameters:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

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
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    ./astro deploy
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

    This Jenkinsfile triggers a code push to Astro every time a commit or pull request is merged to the `main` branch of your repository.

</TabItem>

<TabItem value="jenkinsmultibranch">

To automate code deploys across multiple Deployments using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astro project:

1. In Jenkins, add the following environment variables:

    - `PROD_ASTRONOMER_KEY_ID`: Your Production Deployment API key ID
    - `PROD_ASTRONOMER_KEY_SECRET`: Your Production Deployment API key secret
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your Production Deployment
    - `DEV_ASTRONOMER_KEY_ID`: Your Development Deployment API key ID
    - `DEV_ASTRONOMER_KEY_SECRET`: Your Development Deployment API key secret
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your Development Deployment

    To set environment variables in Jenkins, on the Jenkins Dashboard go to **Manage Jenkins** > **Configure System** > **Global Properties** > **Environment Variables** > **Add**.

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    <pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Set Environment Variables') {
                steps {
                    script {
                        if (env.GIT_BRANCH == 'main') {
                            echo "The git branch is ${siteVariables.jenkinsenv}";
                            env.ASTRONOMER_KEY_ID = env.PROD_ASTRONOMER_KEY_ID;
                            env.ASTRONOMER_KEY_SECRET = env.PROD_ASTRONOMER_KEY_SECRET;
                            env.ASTRONOMER_DEPLOYMENT_ID = env.PROD_DEPLOYMENT_ID;
                        } else if (env.GIT_BRANCH == 'dev') {
                            echo "The git branch is ${siteVariables.jenkinsenv}";
                            env.ASTRONOMER_KEY_ID = env.DEV_ASTRONOMER_KEY_ID;
                            env.ASTRONOMER_KEY_SECRET = env.DEV_ASTRONOMER_KEY_SECRET;
                            env.ASTRONOMER_DEPLOYMENT_ID = env.DEV_DEPLOYMENT_ID;
                        } else {
                            echo "This git branch ${siteVariables.jenkinsenv} is not configured in this pipeline."
                        }
                    }
                }
            }
            stage('Deploy to Astronomer') {
                steps {
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    ./astro deploy
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

    This Jenkinsfile triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `dev` or `main` branch of your repository.

</TabItem>
</Tabs>

### Jenkins (DAG-based deploys)

Use the following template to implement DAG-only deploys with Jenkins.

1. In your Jenkins pipeline configuration, add the following parameters:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    <pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Dag Only Deploy to Astronomer') {
                when {
                    expression {
                        return env.GIT_BRANCH == "origin/main"
                    }
                }
                steps {
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    files=($(git diff-tree HEAD --name-only --no-commit-id))
                    find="dags"
                    if [[ ${siteVariables.jenkinsenv1} =~ (^|[[:space:]])"$find"($|[[:space:]]) && ${siteVariables.jenkinsenv2} -eq 1 ]]; then
                    ./astro deploy --dags;
                    else
                    ./astro deploy;
                    fi
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

