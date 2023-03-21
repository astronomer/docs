---
title: 'Create and manage Workspace API tokens'
sidebar_label: 'Workspace API tokens'
id: workspace-api-tokens
description: Create and manage Workspace API tokens to automate key Workspace actions like adding users and creating Deployments. 
---

Use Workspace API tokens to automate Workspace actions such as creating Deployments and managing users as part of your CI/CD pipelines. Using Workspace API tokens, you can automate:

- Creating and updating Deployments using a [Deployment file](manage-deployments-as-code.md)
- Adding batches of users to a Workspace in a CI/CD pipeline. See [Add a group of users to Astro using the Astro CLI](add-user.md#add-a-group-of-users-to-astro-using-the-astro-cli).
- Creating preview Deployments whenever you create a feature branch in your Astro project Git repository. 
- Performing Deployment-level actions on any Deployment in a Workspace, such as deploying code or making calls to the Airflow rest API. Workspace API tokens can complete the same actions as Deployment API keys for any Deployment in the Workspace. 

## Create a Workspace API token

1. In the Cloud UI, open your Workspace.
   
2. Go to **Workspace Settings** > **Access Management** > **API Tokens**.
   
3. Click **API Token**.
   
4. Configure the new Workspace API token:

    - **Name**: The name for the API token.
    - **Description**: Optional. The Description for the API token.
    - **Workspace Role**: The role that the API token can assume. See [User permissions](user-permissions.md#workspace-roles).
    - **Expiration**: The number of days that the API token can be used before it expires.

5. Click **Create API token**. A confirmation screen showing the token appears.
   
6. Copy the token and store it in a safe place. You will not be able to retrieve this value from Astro again. 

## Update or delete a Workspace API token

If you delete a Workspace API token, make sure that no existing CI/CD pipelines are using it. Once deleted, an API token cannot be recovered. If you unintentionally delete an API token, create a new one and update any CI/CD workflows that used the deleted API token.

1. In the Cloud UI, open your Workspace.
   
2. Go to **Workspace Settings** > **Access Management** > **API Tokens**.

3. Click **Edit** next to your API token.

4. Update the name, description, or Workspace role of your token, then click **Save Changes**.
   
5. Optional. To delete a Workspace API token, click **Delete API Token**, enter `Delete`, and then click **Yes, Continue**.

## Rotate a Workspace API token

Rotating a Workspace API token lets you renew a token without needing to reconfigure its name, description, and permissions. You can also rotate a token if you lose your current token value and need it for additional workflows. 

When you rotate a Workspace API token, you receive a new valid token that can be used in your existing workflows. The previous token value becomes invalid and any workflows using the old value stop working. 

1. In the Cloud UI, open your Workspace.
   
2. Go to **Workspace Settings** > **Access Management** > **API Tokens**.

3. Click **Edit** next to your API token.

4. Click **Rotate token**. The Cloud UI rotates the token and shows the new token value. 

5. Copy the new token value and store it in a safe place. You will not be able to retrieve this value from Astro again. 

6. In any workflows using the token, replace the old token value with the new value you copied. 

## Use a Workspace API token with the Astro CLI

To use a Workspace API token with Astro CLI, specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI.  

For example, to automate Astro CLI Workspace commands on a Mac, run the following command to set a temporary value for the environment variable:

```sh
export ASTRO_API_TOKEN=<your-token>
```

After you set the variable, you can run `astro deployment` and `astro workspace` commands for your Workspace without authenticating yourself to Astronomer. Astronomer recommends storing `ASTRO_API_TOKEN` as a secret before using it to automate the Astro CLI for production workflows.

:::info

If you have both `ASTRO_API_TOKEN` and `ASTRONOMER_KEY_ID`/`ASTRONOMER_KEY_SECRET` set in an environment, your Astro Workspace token takes precedence and is used for all Deployment actions in that Workspace. 

:::

### Use a Workspace API token for CI/CD

You can use Workspace API tokens and the Astro CLI to automate various Workspace and Deployment management actions in CI/CD. 

For all use cases, you must make the following environment variable available to your CI/CD environment:

```text
ASTRO_API_TOKEN=<your-token>
```

After you set this environment variable, you can run Astro CLI commands from CI/CD pipelines without needing to manually authenticate to Astro. For more information and examples, see [Automate code deploys with CI/CD](ci-cd.md).

