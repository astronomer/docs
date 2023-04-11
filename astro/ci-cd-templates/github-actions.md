---
sidebar_label: GitHub Actions
title: Astro CI/CD templates for GitHub Actions
id: github-actions
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using GitHub Actions.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a GitHub repository using [GitHub Actions](https://github.com/features/actions).

The following templates for GitHub Actions are available:

- [Image-only deploy templates](template-overview.md#image-only-templates)
- [DAG-based deploy templates](template-overview.md#dag-based-templates)
- [Preview Deployment templates](template-overview.md#preview-deployment-templates)

Each template type supports multiple implementations. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_. If your team builds custom Docker images, use the _custom image_ implementation.

GitHub Action templates use the Astronomer-maintained [Deploy Action](https://github.com/astronomer/deploy-action) in the GitHub Marketplace. See the [Deploy Action README](https://github.com/astronomer/deploy-action#readme) to learn more about using and customizing this action.

For more information on each template or to configure your own, see [Template overview](template-overview.md). To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) hosted in a GitHub repository.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md).
- Access to [GitHub Actions](https://github.com/features/actions).

Each CI/CD template implementation might have additional requirements.

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

To automate code deploys to a single Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

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

The following template can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. 

#### Configuration requirements

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have unique [Deployment API keys and secrets](api-keys.md) for both of your Deployments.

#### Implementation

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

#### Configuration requirements

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Implementation

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

## DAG-based templates

The following templates are examples of how to implement DAG-based deploys in GitHub Actions. They use the [Deploy action](https://github.com/astronomer/deploy-action) `dag-deploy-enabled` option to implement a DAG-based deploy workflow.

<Tabs
    defaultValue="standard"
    groupId= "dag-based-templates"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

#### Implementation

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

<TabItem value="multibranch">

The following setup can be used to create a multiple branch CI/CD pipeline using GitHub Actions. A multiple branch pipeline can be used to test DAGs in a development Deployment and promote them to a production Deployment. The finished pipeline deploys your code to Astro as demonstrated in the following diagram:

![Diagram showing how a multiple branch CI/CD pipeline works](/img/docs/multibranch.png)

#### Configuration requirements:

- You have both a `dev` and `main` branch of an Astro project hosted in a single GitHub repository.
- You have respective `dev` and `prod` Deployments on Astro where you deploy your GitHub branches to.
- You have unique [Deployment API keys and secrets](api-keys.md) for both of your Deployments.

#### Implementation

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

#### Configuration requirements

- An Astro project that requires additional build-time arguments to build the Runtime image.

#### Implementation

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
      ## Set your Workspace API key token as a GitHub secret
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
      ## Set your Workspace API key token as a GitHub secret
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
      pull_request:
        branches:
          - main
    
    env:
      ## Set your Workspace API key token as a GitHub secret
      ASTRO_API_TOKEN: ${{ secrets.ASTRO_API_TOKEN }}
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Delete preview Deployment
          uses: astronomer/deploy-action@v0.2
          with:
            action: deploy-deployment-preview
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
      ## Set your Workspace API key token as a GitHub secret
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
