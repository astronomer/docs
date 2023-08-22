---
title: 'Create and manage Organization API tokens'
sidebar_label: 'Organization API tokens'
id: organization-api-tokens
description: Create and manage Organization API tokens to automate key actions across all Workspaces in your Organization, like adding users and creating Deployments. 
---

Use Organization API tokens to automate across all Workspaces in your Organization, such as creating Deployments and managing users as part of your CI/CD pipelines. Organization API keys are particularly helpful for automating:

- Creating Workspaces.
- Inviting users to an Organization or Workspace. See [Add a group of users to Astro using the Astro CLI](manage-workspace-users.md#add-a-group-of-users-to-a-workspace-using-the-astro-cli).
- Creating and updating Deployments using a [Deployment file](manage-deployments-as-code.md).
- Exporting audit logs.
- Gathering metadata about Deployments using the Airflow REST API.
- Completing any of the actions you can complete with a Workspace API token or Deployment API key across all Deployments in your Organization.

## Create an Organization API token

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Access Management** > **API Tokens**.
   
3. Click **+ API Token**.
   
4. Configure the new Organization API token:

    - **Name**: The name for the API token.
    - **Description**: Optional. The Description for the API token.
    - **Organization Role**: The role that the API token can assume. See [User permissions](user-permissions.md#organization-roles).
    - **Expiration**: The number of days that the API token can be used before it expires.

5. Click **Create API token**. A confirmation screen showing the token appears.
   
6. Copy the token and store it in a safe place. You will not be able to retrieve this value from Astro again. 

## Update or delete an Organization API token

If you delete an Organization API token, make sure that no existing automation workflows are using it. After it's deleted, an API token cannot be recovered. If you unintentionally delete an API token, create a new one and update any automation workflows that used the deleted API token.

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Access Management** > **API Tokens**.

3. Click **Edit** next to your API token.

4. Update the name, description, or Organization role of your token, then click **Save Changes**.
   
5. Optional. To delete an Organization API token, click **Delete API Token**, enter `Delete`, and then click **Yes, Continue**.

## Rotate an Organization API token

Rotating an Organization API token lets you renew a token without needing to reconfigure its name, description, and permissions. You can also rotate a token if you lose your current token value and need it for additional workflows. 

When you rotate an Organization API token, you receive a new valid token from Astro that can be used in your existing workflows. The previous token value becomes invalid and any workflows using those previous values stop working. 

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Access Management** > **API Tokens**.

3. Click **Edit** next to your API token.

4. Click **Rotate token**. The Cloud UI rotates the token and shows the new token value. 

5. Copy the new token value and store it in a safe place. You will not be able to retrieve this value from Astro again. 

6. In any workflows using the token, replace the old token value with the new value you copied. 

## Use an Organization API token with the Astro CLI

To use an Organization API token with Astro CLI, specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI.  

For example, to automate Astro CLI commands on a Mac, run the following command to set a temporary value for the environment variable:

```sh
export ASTRO_API_TOKEN=<your-token>
```

After you set the variable, you can run `astro deployment`, `astro workspace`, and `astro organization` commands for your Workspace without authenticating yourself to Astronomer. Astronomer recommends storing `ASTRO_API_TOKEN` as a secret before using it to automate the Astro CLI for production workflows.

:::info

If you have both `ASTRO_API_TOKEN` and `ASTRONOMER_KEY_ID`/`ASTRONOMER_KEY_SECRET` set in an environment, your Astro Workspace token takes precedence and is used for all Deployment actions in that Workspace. 

:::

### Use an Organization API token for CI/CD

You can use Organization API tokens and the Astro CLI to automate various Organization, Workspace, and Deployment management actions in CI/CD. 

For all use cases, you must make the following environment variable available to your CI/CD environment:

```text
ASTRO_API_TOKEN=<your-token>
```

After you set this environment variable, you can run Astro CLI commands from CI/CD pipelines without needing to manually authenticate to Astro. For more information and examples, see [Automate code deploys with CI/CD](set-up-ci-cd.md).

