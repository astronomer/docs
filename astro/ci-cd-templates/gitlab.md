---
sidebar_label: GitLab
title: Astro CI/CD templates for GitLab
id: gitlab
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using GitLab.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a [GitLab](https://gitlab.com/) repository to Astro.

The templates for GitLab use the [image-only deploy](template-overview.md#template-types) process. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro and are interested in a DAG-based CI/CD template, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a GitLab repository.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).

Each CI/CD template implementation might have additional requirements.

## Image-only templates

### Single branch implementation

Use this template to push code to from a GitLab repository to Astro.

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

    For production Deployments, Astronomer recommends storing the value for your API token as either a [file-type variable](https://docs.gitlab.com/ee/ci/variables/#use-file-type-cicd-variables) or [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html).

2. Go to the **Editor** option in your project's CI/CD section and commit the following:

   ```
   ---
    astro_deploy:
      stage: deploy
      image: docker:latest
      services:
       - docker:dind
      variables:
         ASTRO_API_TOKEN: ${ASTRO_API_TOKEN}
      before_script:
       - apk add --update curl && rm -rf /var/cache/apk/*
       - apk add bash
      script:
       - (curl -sSL install.astronomer.io | bash -s)
       - astro deploy -f
      only:
       - main
   ```

### Multiple branch implementation

Use this template to push code to both a development and a production Deployment on Astro using GitLab.

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
    - `DEV_ASTRO_API_TOKEN`: The value for your development Workspace or Organization API token.

    For production Deployments, Astronomer recommends storing the value for your API token as either a [file-type variable](https://docs.gitlab.com/ee/ci/variables/#use-file-type-cicd-variables) or [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html).

  :::caution

  When you create environment variables that will be used in multiple branches, you might want to protect where you use them. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. For more information on protected branches, see [GitLab documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html#configure-a-protected-branch).

  :::

2. Go to the **Editor** option in your project's CI/CD section and commit the following:

   ```
   ---
      astro_deploy_dev:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRO_API_TOKEN: ${DEV_ASTRO_API_TOKEN}
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
          - apk add jq
        script:
          - (curl -sSL install.astronomer.io | bash -s)
          - astro deploy -f --deployment-name "<dev-deployment-name>"
        only:
          - dev

      astro_deploy_prod:
        stage: deploy
        image: docker:latest
        services:
          - docker:dind
        variables:
            ASTRO_API_TOKEN: ${PROD_ASTRO_API_TOKEN}
        before_script:
          - apk add --update curl && rm -rf /var/cache/apk/*
          - apk add bash
          - apk add jq
        script:
          - (curl -sSL install.astronomer.io | bash -s)
          - astro deploy -f --deployment-name "<prod-deployment-name>"
        only:
          - main
   ```

## DAG-based templates

The DAG-based template uses the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

### Single branch implementation

Use this template to push code to from a GitLab repository to Astro.

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

    For production Deployments, Astronomer recommends storing the value for your API token as either a [file-type variable](https://docs.gitlab.com/ee/ci/variables/#use-file-type-cicd-variables) or [external secret](https://docs.gitlab.com/ee/ci/secrets/index.html).

2. Go to the **Editor** option in your project's CI/CD section and commit the following:
   
    ```
    publish-dags:
      stage: publish
      image: docker:latest
      services:
       - docker:dind
      variables:
        ASTRO_API_TOKEN: ${ASTRO_API_TOKEN}
        DAG_FOLDER: "/dags"
      before_script:
        - apk add --update curl && rm -rf /var/cache/apk/*
        - apk add bash
        - apk add jq
      script:
        - (curl -sSL install.astronomer.io | bash -s)
        - files=$(git diff --name-only HEAD^..HEAD)
        - dags_only=1
        - for file in $files; do
        -  if [[ $file != "$DAG_FOLDER"* ]]; then
        -    echo "$file is not a dag, triggering a full image build"
        -    dags_only=0
        -    break
        -  fi
        - done
        - if [ $dags_only == 1 ]
        - then
        -   astro deploy --dags
        - fi
        - if [ $dags_only == 0 ]
        - then
        -   astro deploy -f
        - fi
      only:
        - main
    ```