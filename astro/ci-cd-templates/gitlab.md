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

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) hosted in a GitLab repository.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md) for each Deployment.

Each CI/CD template implementation might have additional requirements.

### Single branch implementation

Use this template to push code to from a GitLab repository to Astro.

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

### Multiple branch implementation

Use this template to push code to both a development and a production Deployment on Astro using GitLab.

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
    - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
    - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
    - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`

:::caution

When you create environment variables that will be used in multiple branches, you might want to protect where you use them. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. For more information on protected branches, see [GitLab documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html#configure-a-protected-branch).

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
