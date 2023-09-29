---
sidebar_label: GitHub Actions
title: Astro CI/CD templates for GitHub Actions
id: github-actions
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using GitHub Actions.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

GitHub Action templates use the Astronomer-maintained `deploy-action`, which is available in the [GitHub Marketplace](https://github.com/marketplace/actions/deploy-apache-airflow-dags-to-astro). This action automates the deploy process and includes additional features for more complex automation workflows. Specifically, the action can automatically:

- Choose a deploy type based on the files that were changed in a commit. This allows you to use the same template for DAG deploys and image deploys.
- Test DAGs as part of the deploy process and prevent deploying if any of the tests fail. These tests are defined in the `tests` directory of your Astro project.
- Create a preview Deployment to test your code before deploying to production. A Deployment preview is an Astro Deployment that mirrors the configuration of an existing Deployment.

See the [Deploy Action README](https://github.com/astronomer/deploy-action#readme) to learn more about using and customizing this action. 

Read the following sections to choose the right template for your use case. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_. If your team builds custom Docker images, use the _custom image_ implementation. If you do not have access to Astronomer's `deploy-action`, use the [private network templates](#private-network-templates).

To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](cli/develop-project.md#create-an-astro-project) hosted in a GitHub repository.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API token](deployment-api-tokens.md), [Workspace API token](workspace-api-tokens.md), or [Organization API token](organization-api-tokens.md).
- Access to [GitHub Actions](https://github.com/features/actions).

Each CI/CD template implementation might have additional requirements.

:::caution

If you use a [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) to execute jobs from GitHub Actions, the Astro CLI's `config.yaml` file, which stores default deploy details, might be shared across your organization and hence multiple CI/CD pipelines. To reduce the risk of accidentally deploying to the wrong Deployment, ensure the following:

- Add `ASTRO_API_TOKEN` to your repository and include a check in your GitHub workflow to verify that it exists. 
- Use Deployment API tokens, which are scoped only to one Deployment, instead of Workspace or Organization API tokens.
- Specify `deployment-id` or `deployment-name` in your action. For example, `astro deploy <deployment-id> or `astro deploy -n <deployment-name>`.
- Add the command `astro logout` at the end of your workflow to ensure that your authentication token is cleared from the `config.yaml` file.

:::

## Deploy action templates

Templates that use the Astronomer `deploy-action` trigger both image deploys and DAG deploys. If you committed changes only to DAG files, the action triggers a DAG deploy. If you committed changes to any other file, the action triggers an image deploy.

<Tabs
    defaultValue="standard"
    groupId= "deploy-action-templates"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a single Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as a [GitHub secret](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code

    on:
      push:
        branches:
          - main

    env:
      ## Sets Deployment API credentials as environment variables
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.2
          deployment-id: <your-deployment-id>
    ```

</TabItem>

<TabItem value="multibranch">

The following template can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. 

#### Configuration requirements

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have at least one API token with access to both of your Deployments.

#### Implementation

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
   - `DEV_ASTRO_API_TOKEN`: The value for your development Workspace or Organization API token.

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
          ## Sets DEV Deployment API credential as an environment variable
          ASTRO_API_TOKEN: ${{ secrets.DEV_ASTRO_API_TOKEN }}
        runs-on: ubuntu-latest
        steps:
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.2
          with:
            deployment-id: <dev-deployment-id>
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        env:
          ## Sets Prod Deployment API credential as an environment variable
          ASTRO_API_TOKEN: ${{ secrets.PROD_ASTRO_API_TOKEN }}
        runs-on: ubuntu-latest
        steps:
        - name: Deploy to Astro
          uses: astronomer/deploy-action@v0.2
          with:
            deployment-id: <prod-deployment-id>
    ```

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Prerequisites

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Implementation

1. Set the following as a [GitHub secret](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

  - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

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
          ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
        steps:
        - name: Check out the repo
          uses: actions/checkout@v3
        - name: Create image tag
          id: image_tag
          run: echo ::set-output name=image_tag::astro-$(date +%Y%m%d%H%M%S)
        - name: Build image
          uses: docker/build-push-action@v2
          with:
            deployment-id: <your-deployment-id>
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
          uses: astronomer/deploy-action@v0.2
          with:
            deployment-id: <your-deployment-id>
            image-name: ${{ steps.image_tag.outputs.image_tag }}
    ```

    For example, to create a CI/CD pipeline that deploys a project which [installs Python packages from a private GitHub repository](cli/develop-project.md#install-python-packages-from-private-sources), you would use the following configuration:

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
          ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
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
          uses: astronomer/deploy-action@v0.2
          with:
            deployment-id: <your-deployment-id>
            image-name: ${{ steps.image_tag.outputs.image_tag }}
    ```

  :::info

  If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

  :::

</TabItem>
</Tabs>

## Deployment preview templates

The Astronomer [Deploy Action](https://github.com/astronomer/deploy-action/tree/deployment-preview#deployment-preview-templates) includes several sub-actions that can be used together to create a complete [Deployment preview](ci-cd-templates/template-overview.md#preview-deployment-templates) pipeline. 

### Prerequisites

- An Astro project hosted in a GitHub repository.
- A [Workspace API token](workspace-api-tokens.md).
- A [Deployment](create-deployment.md). 

### Deployment preview implementation

1. Copy and save the Deployment ID for your Astro deployment.
2. Set the following [GitHub secret](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in the repository hosting your Astro project:

  - Key: `ASTRO_API_TOKEN` 
  - Secret: `<your-token>`

3. In your project repository, create a new YAML file in `.github/workflows` named `create-deployment-preview.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Create preview Deployment

    on:
      create:
        branches:
          - "**"
    
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Create preview Deployment
          uses: astronomer/deploy-action@v0.2
          with:
            action: create-deployment-preview
            deployment-id: <main-deployment-id>
    ```

4. In the same folder, create a new YAML file named `deploy-to-preview.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to preview

    on:
      pull_request:
        branches:
          - main
    
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to preview
          uses: astronomer/deploy-action@v0.2
          with:
            action: deploy-deployment-preview
            deployment-id: <main-deployment-id>
    ```

5. In the same folder, create a new YAML file named `delete-preview-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Delete Preview Deployment

    on:
      delete:
        branches:
          - "**"
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Delete preview Deployment
          uses: astronomer/deploy-action@v0.2
          with:
            action: delete-deployment-preview
            deployment-id: <main-deployment-id>
    ```

6. In the same folder, create a new YAML file named `deploy-to-main-deployment.yml` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code to main Deployment

    on:
      push:
        branches:
          - main
    
    env:
      ## Set your API token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Deploy code to main Deployment
          uses: astronomer/deploy-action@v0.2
          with:
            deployment-id: <main-deployment-id>
    ```

    All four workflow files must have the same Deployment ID specified. The actions use this Deployment ID to create and delete preview Deployments based on your main Deployment.

## Private network templates

If you use GitHub Enterprise and can't use the public Astronomer [Deploy Action](https://github.com/astronomer/deploy-action) in the GitHub Marketplace, use the following templates to implement CI/CD.

<Tabs
    defaultValue="standard"
    groupId= "private-network-templates"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

2. In your project repository, create a new YAML file in `.github/workflows` that includes the following configuration:

    ```yaml
    name: Astronomer CI - Deploy code

    on:
      push:
        branches:
          - main

    env:
      ## Sets API token as an environment variable
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v3
        - name: Deploy to Astro
          run: |
            curl -sSL install.astronomer.io | sudo bash -s
            astro deploy <your-deployment-id>
    ```

</TabItem>

<TabItem value="multibranch">

The following setup can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment.

#### Prerequisites 

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have at least one API token with access to both of your Deployments.

#### Setup

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
   - `DEV_ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

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
          ## Sets DEV Deployment API token credential as an environment variable
          ASTRO_API_TOKEN: ${{ secrets.DEV_ASTRO_API_TOKEN }}
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v3
        - name: Deploy to Astro
          run: |
            curl -sSL install.astronomer.io | sudo bash -s
            astro deploy <your-dev-deployment-id>
      prod-push:
        if: github.event.action == 'closed' && github.event.pull_request.merged == true
        env:
          ## Sets PROD Deployment API token credential as an environment variable
          ASTRO_API_TOKEN: ${{ secrets.PROD_ASTRO_API_TOKEN }}
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v3
        - name: Deploy to Astro
          run: |
            curl -sSL install.astronomer.io | sudo bash -s
            astro deploy <your-prod-deployment-id>
    ```

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Prerequisites

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Setup

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

  - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

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
          ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
        steps:
        - name: Check out the repo
          uses: actions/checkout@v3
        - name: Create image tag
          id: image_tag
          run: echo ::set-output name=image_tag::astro-$(date +%Y%m%d%H%M%S)
        - name: Build image
          uses: docker/build-push-action@v4
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
          run: |
            curl -sSL install.astronomer.io | sudo bash -s
            astro deploy <your-deployment-id> --image-name ${{ steps.image_tag.outputs.image_tag }}
    ```

For example, to create a CI/CD pipeline that deploys a project which [installs Python packages from a private GitHub repository](cli/develop-project.md#install-python-packages-from-private-sources), you would use the following configuration:

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
        ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
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
        run: |
          curl -sSL install.astronomer.io | sudo bash -s
          astro deploy <your-deployment-id> --image-name ${{ steps.image_tag.outputs.image_tag }}
  ```

  
:::info

If you need guidance configuring a CI/CD pipeline for a more complex use case involving custom Runtime images, reach out to [Astronomer support](https://support.astronomer.io/).

:::


</TabItem>

</Tabs>