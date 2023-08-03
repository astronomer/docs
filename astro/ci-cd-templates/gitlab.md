---
sidebar_label: GitLab
title: Astro CI/CD templates for GitLab
id: gitlab
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using GitLab.
---

Use the following CI/CD templates to automate deployment of your Astro project from a [GitLab](https://gitlab.com/) repository to Astro.

The templates for GitLab use the [image-only deploy](template-overview.md#template-types) and smart deploys, which is a combination of image-based and [DAG-only deploy](astro/deploy-code).

If you have one Deployment and one environment on Astro, use the [single branch implementation](#single-branch-implementation). If you have multiple Deployments that support development and production environments, use the [multiple branch implementation](#multiple-branch-implementation). If you want your CI/CD process to automatically decide which deploy strategy to choose, see [smart deploy templates](#smart-deploy-templates)

To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a GitLab repository.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).

Each CI/CD template implementation might have additional requirements.

## Image-only templates

### Single branch implementation

Use this template to push code to from a GitLab repository to Astro.

1. In your GitLab project, [follow GitLab's documentation](https://docs.gitlab.com/ee/ci/variables/#for-a-project) to set the following environment variables for a project:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `DEPLOYMENT_ID`: The ID of your Astro Deployment. You can copy this **ID** from your Deployment's home page in the Cloud UI.

    Astronomer recommends to always mask the value of your API token to prevent it from getting printed in plain-text in the logs. You can also set API token as an [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html) for an extra layer of security.

2. Go to **Build** > **Pipeline Editor**, paste and commit the following:

  ```yaml
  astro_deploy:
    stage: deploy
    image: docker:latest
    services:
      - docker:dind
    
    variables:
        ASTRO_API_TOKEN: ${ASTRO_API_TOKEN}
        DEPLOYMENT_ID: ${DEPLOYMENT_ID}

    before_script:
      - apk add --update curl && rm -rf /var/cache/apk/*
      - apk add bash
    script:
      - (curl -sSL install.astronomer.io | bash -s)
      - astro deploy -f $DEPLOYMENT_ID
    only:
      - main
  ```

### Multiple branch implementation

Use this template to push code to a development and a production Deployment in Astro based on your GitLab project's branch name.

1. In your GitLab project, [follow GitLab's documentation](https://docs.gitlab.com/ee/ci/variables/#for-a-project) to set the following environment variables for a project:

    - `PROD_ASTRO_API_TOKEN`: The value of your production Workspace or Organization API token.
    - `PROD_DEPLOYMENT_ID`: The ID of your Astro Deployment. You can copy this **ID** from your production Deployment's home page in the Cloud UI.
    - `DEV_ASTRO_API_TOKEN`: The value of your development Workspace or Organization API token.
    - `DEV_DEPLOYMENT_ID`: The ID of your Astro Deployment. You can copy this **ID** from your development Deployment's home page in the Cloud UI.

    Astronomer recommends to always mask the value of your API token to prevent it from getting printed in plain-text in the logs. You can also set API token as an [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html) for an extra layer of security.

  :::tip

  When you create a CI/CD variable that will be used in multiple branches, you might want to protect where you use them. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. See GitLab's documentation on [protected branches](https://docs.gitlab.com/ee/user/project/protected_branches.html) and [protected tags](https://docs.gitlab.com/ee/user/project/protected_tags.html) for more details. 

  :::

2. Go to the **Editor** option in your project's CI/CD section and commit the following:

  ```yaml
  astro_deploy_dev:
    stage: deploy
    image: docker:latest
    services:
      - docker:dind
    variables:
        ASTRO_API_TOKEN: ${DEV_ASTRO_API_TOKEN}
        DEPLOYMENT_ID: ${DEV_DEPLOYMENT_ID}
    before_script:
      - apk add --update curl && rm -rf /var/cache/apk/*
      - apk add bash
    script:
      - (curl -sSL install.astronomer.io | bash -s)
      - astro deploy -f $DEPLOYMENT_ID
    only:
      - dev

  astro_deploy_prod:
    stage: deploy
    image: docker:latest
    services:
      - docker:dind
    variables:
        ASTRO_API_TOKEN: ${PROD_ASTRO_API_TOKEN}
        DEPLOYMENT_ID: ${PROD_DEPLOYMENT_ID}
    before_script:
      - apk add --update curl && rm -rf /var/cache/apk/*
      - apk add bash
      - apk add jq
    script:
      - (curl -sSL install.astronomer.io | bash -s)
      - astro deploy -f $DEPLOYMENT_ID
    only:
      - main
  ```

## Smart deploy templates

The DAG-based template uses the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](astro/deploy-code.md).

### Single branch implementation

Use this template to push code to from a GitLab repository to Astro.

1. In your GitLab project, [follow GitLab's documentation](https://docs.gitlab.com/ee/ci/variables/#for-a-project) to set the following environment variables for a project:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `DEPLOYMENT_ID`: The ID of your Astro Deployment. You can copy this **ID** from your Deployment's home page in the Cloud UI.

    Astronomer recommends to always mask the value of your API token to prevent it from getting printed in plain-text in the logs. You can also set API token as an [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html) for an extra layer of security.

2. Go to the **Editor** option in your project's CI/CD section and commit the following:
   
    ```yaml
    astro_smart_deploy:
      stage: deploy
      image: docker:latest
      services:
        - docker:dind
      variables:
        ASTRO_API_TOKEN: ${ASTRO_API_TOKEN}
        DAG_FOLDER: "dags"
        DEPLOYMENT_ID: ${DEPLOYMENT_ID}
      before_script:
        - apk add --update curl && rm -rf /var/cache/apk/*
        - apk add git
        - apk add bash
      script:
        - (curl -sSL install.astronomer.io | bash -s)
        - files=$(git diff --name-only $(git rev-parse HEAD~1) -- .)
        - dags_only=1
        - echo "$DAG_FOLDER"
        - echo "$files"
        - for file in $files; do
        -   echo "$file"
        -   if [[ "$file" != "$DAG_FOLDER"* ]]; then
        -     echo "$file is not a dag, triggering a full image build"
        -     dags_only=0
        -     break
        -   else
        -     echo "just a DAG"
        -   fi
        - done
        - if [[ $dags_only == 1 ]]; then
        -   echo "doing dag-only deploy"
        -   astro deploy --dags $DEPLOYMENT_ID
        - elif [[ $dags_only == 0 ]]; then
        -   echo "doing image deploy"
        -   astro deploy -f $DEPLOYMENT_ID
        - fi
      only:
        - main
    ```