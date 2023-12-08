---
title: 'Create and manage Deployment API tokens'
sidebar_label: 'Deployment API tokens'
id: deployment-api-tokens
description: Use Deployment API tokens to automate code deploys and configuration changes to a Deployment.
---

A Deployment API token is a credential that you can use to programmatically access a specific Deployment. They are a direct replacement for [Deployment API keys](api-keys.md), which are deprecated. Using a Deployment API token, you can:

- [Push code](deploy-code.md) to a Deployment.
- Update the Deployment's [environment variables](environment-variables.md).
- Update a Deployment's configurations. See [Manage Deployments as code](manage-deployments-as-code.md).
- Make requests to update your Deployment's Airflow environment using the [Airflow REST API](airflow-api.md).

Use this document to learn how to create and manage API tokens. To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Deployment API token permissions

Unlike Workspace API tokens and Organization API tokens, Deployment API tokens are not scoped to a specific [user role](user-permissions.md). Deployment API tokens have the same permissions as the [Workspace Operator](user-permissions.md#workspace-roles) role, but only for Deployment-level operations. For example, an API token can create a Deployment [environment variable](environment-variables.md) but, unlike a Workspace Operator, it can't create an [Astro alert](alerts.md) because alerts apply to the whole Workspace.

## Create a Deployment API token

1. In the Cloud UI, open your Workspace, then open the Deployment you want to create an API token for.
   
2. Click **API Tokens**.
   
3. Click **+ API Token**.
   
4. Configure the new Deployment API token:

    - **Name**: The name for the API token.
    - **Description**: Optional. The Description for the API token.
    - **Expiration**: The number of days that the API token can be used before it expires.

5. Click **Create API token**. A confirmation screen showing the token appears.
   
6. Copy the token and store it in a safe place. You will not be able to retrieve this value from Astro again. 

## Update or delete a Deployment API token

If you delete a Deployment API token, make sure that no existing CI/CD workflows are using it. After it's deleted, an API token cannot be recovered. If you unintentionally delete an API token, create a new one and update any CI/CD workflows that used the deleted API token.

1. In the Cloud UI, open your Workspace, then open the Deployment that the API token belongs to.
   
2. Click **Edit** next to your API token.

3. Update the name or description of your token, then click **Save Changes**.
   
4. Optional. To delete a Deployment API token, click **Delete API Token**, enter `Delete`, and then click **Yes, Continue**.

## Rotate a Deployment API token

Rotating a Deployment API token lets you renew a token without needing to reconfigure its name, description, and permissions. You can also rotate a token if you lose your current token value and need it for additional workflows. 

When you rotate a Deployment API token, you receive a new valid token from Astro that can be used in your existing workflows. The previous token value becomes invalid and any workflows using those previous values stop working. 

1. In the Cloud UI, open your Workspace, then open the Deployment that the API token belongs to.
   
2. Click **Edit** next to your API token.

3. Click **Rotate token**. The Cloud UI rotates the token and shows the new token value. 

4. Copy the new token value and store it in a safe place. You will not be able to retrieve this value from Astro again. 

5. In any workflows using the token, replace the old token value with the new value you copied.

## Use a Deployment API token with the Astro CLI

To use a Deployment API token with Astro CLI, specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI:

```sh
export ASTRO_API_TOKEN=<your-token>
```

After you configure the `ASTRO_API_TOKEN` environment variable, you can run Astro CLI commands related to the deployment for which the Deployment API token was created. For example, `astro deployment inspect` or `astro deployment logs`.

:::info

If you have configured both a Deployment API token via `ASTRO_API_TOKEN` and Deployment API keys (deprecated) via `ASTRONOMER_KEY_ID`/`ASTRONOMER_KEY_SECRET`, the Deployment API token takes precedence. 

:::

When using a Deployment API token for automation, Astronomer recommends storing `ASTRO_API_TOKEN` as a secret.

### Use a Deployment API token for CI/CD

You can use Deployment API tokens and the Astro CLI to automate various Deployment management actions in CI/CD. 

For all use cases, you must make the following environment variable available to your CI/CD environment:

```text
ASTRO_API_TOKEN=<your-token>
```

After you set this environment variable, you can run Astro CLI commands from CI/CD pipelines without needing to manually authenticate to Astro. For more information and examples, see [Automate code deploys with CI/CD](set-up-ci-cd.md).
