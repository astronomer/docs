---
title: 'Create and manage Workspace API tokens'
sidebar_label: 'Workspace API tokens'
id: workspace-api-tokens
description: Create and manage Workspace API tokens to automate key Workspace actions like adding users and creating Deployments. 
---

Use Workspace API tokens to automate Workspace actions such as creating Deployments and managing users as part of your CI/CD pipelines. Using Workspace API keys, you can:

- [Manage Deployments as code](manage-deployments-as-code.md) in a CI/CD pipeline.
- Add batches of users in a CI/CD pipeline. 
- Create preview Deployments. 

## Create a Workspace API token

1. In the Cloud UI, open your Workspace.
   
2. Go to **Workspace Settings** > **Access Management** > **API Tokens**.
   
3. Click **API Token**.
   
4. Configure the new Workspace API token:

    - **Name**: The name for the API token.
    - **Description**: The Description for the API token.
    - **Workspace Role**: The role that the API token can assume. See [User permissions](user-permissions.md#workspace-roles).
    - **Expiration**: The duration that the API token can be used before it expires.

5. Click **Create API token**. A confirmation screen showing the token appears.
   
6. Copy the token and store it in a safe place. You will not be able to retrieve this value from Astro again. 

## Update or delete a Workspace API token

If you delete an API key, make sure that no existing CI/CD pipelines are using it. Once deleted, an API token and secret cannot be recovered. If you unintentionally delete an API token, create a new one and update any CI/CD workflows that used the deleted API token.

1. In the Cloud UI, open your Workspace.
   
2. Go to **Workspace Settings** > **Access Management** > **API Tokens**.

3. Click **Edit** next to your API key.

4. Update the name, description, workspace role, or expiration date of your token, then click **Save Changes**.
   
5. Click **Delete API Key**, enter `Delete`, and then click **Yes, Continue**.

## Use a Workspace API token with the Astro CLI

To use a Workspace API token with the Astro CLI, you must make your API token available to the system running the Astro CLI using the `ASTRO_API_TOKEN` environment variable. 

For example, to automate Astro CLI Workspace commands on a Mac computer, run the following command to set a temporary value for the environment variable:

```sh
export ASTRO_API_TOKEN=<your-token>
```

After you set the variables, you can run `astro deployment` and `astro workspace` commands for your Workspace without authenticating yourself to Astronomer. Astronomer recommends storing `ASTRO_API_TOKEN` as a secret before using it to programmatically update a Deployment.

## Use an API key for CI/CD

You can use Workspace API keys to automate various actions in CI/CD. A few notable examples are:

- 

Regardless of your use case, you must make the following environment variable available to your CI/CD environment:

```
ASTRO_API_TOKEN=<your-token>
```

For more information and examples, see [Automate code deploys with CI/CD](ci-cd.md).

