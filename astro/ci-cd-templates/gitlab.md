---
sidebar_label: GitLab
title: GitLab CI/CD templates
id: gitlab
description: Use pre-built templates for GitLab to automate your Apache Airflow code deploys to Astro  
---

Templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools. 

The following templates use [GitLab](https://gitlab.com/) to automate code deploys to Astro with Image-only deploy templates. [Image-only deploy templates](template-overview.md#template-types) create an automated workflow that builds a Docker image and then pushes it to Astro whenever you update any file in your Astro project. You can choose whether to deploy to a single Deployment, called _Single branch implementation_, or multiple Deployments, called _Multiple branch implementation_. 

See [Template overview](template-overview.md) to decide which template is right for you and to learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).


## Prerequisites

The following prerequisites are required for both single branch and multiple branch implementations.

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A [GitLab](https://gitlab.com/) repository.
- An [Astro project](create-project.md) hosted in a GitLab repository that your CI/CD tool can access.


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

Use this template to push code to both a development and a production Deployment on Astro using [GitLab](https://gitlab.com/).

1. In GitLab, go to **Project Settings** > **CI/CD** > **Variables** and set the following environment variables:

    - `DEV_ASTRONOMER_KEY_ID` = `<your-dev-key-id>`
    - `DEV_ASTRONOMER_KEY_SECRET` = `<your-dev-key-secret>`
    - `PROD_ASTRONOMER_KEY_ID` = `<your-prod-key-id>`
    - `PROD_ASTRONOMER_KEY_SECRET` = `<your-prod-key-secret>`

:::caution

When you create environment variables that will be used in multiple branches, you may want to protect where you use them. Otherwise, uncheck the `Protect variable` flag when you create the variable in GitLab. For more information on protected branches, see [GitLab documentation](https://docs.gitlab.com/ee/user/project/protected_branches.html#configure-a-protected-branch).

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
