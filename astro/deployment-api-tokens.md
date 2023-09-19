---
title: 'Create and manage Deployment API tokens'
sidebar_label: 'Deployment API tokens'
id: deployment-api-tokens
description: Use Deployment API tokens to automate code deploys and configuration changes to a Deployment.
---

:::caution

This feature is in [Public Preview](https://docs.astronomer.io/astro/feature-previews).

:::

A Deployment API token is a credential that you can use to programmatically access a specific Deployment. Using a Deployment API token, you can:

- [Push code](deploy-code.md) to a Deployment.
- Update the Deployment's [environment variables](environment-variables.md).
- Update a Deployment's configurations. See [Manage Deployments as code](manage-deployments-as-code.md).
- Make requests to update your Deployment's Airflow environment using the [Airflow REST API](airflow-api.md).

Use this document to learn how to create and manage API tokens. To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Deployment API token permissions

Unlike Workspace API tokens and Organization API tokens, Deployment API tokens are are not scoped to a specific [user role](user-permissions.md). Generally speaking, Deployment API tokens have the same permissions as the Workspace Operator role, but only for Deployment-level operations. For example, an API token can create a Deployment [environment variable](environment-variables.md) but, unlike a Workspace Operator, it can't create an [Astro alert](alerts.md) because alerts apply to the whole Workspace.

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

If you delete a Deployment API token, make sure that no existing CI/CD pipelines are using it. After it's deleted, an API token cannot be recovered. If you unintentionally delete an API token, create a new one and update any CI/CD workflows that used the deleted API token.

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