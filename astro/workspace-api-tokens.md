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

## Create a Workspace API key

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

## Use a Workspace API token with the Astro CLI

To use a Deployment API key with the Astro CLI, you must make your API key ID and secret accessible to the Astro CLI by setting the following OS-level environment variables:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

For example, to update a Deployment using the Astro CLI on a Mac machine, set temporary OS-level environment variables with the following commands:

```sh
export ASTRONOMER_KEY_ID=<your-key-id>
export ASTRONOMER_KEY_SECRET=<your-key-secret>
```

After you set the variables, you can run `astro deployment update` for the Deployment and you don't have to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update a Deployment.

## Use an API key for CI/CD

If you deploy DAGs regularly to a production environment, Astronomer recommends using Deployment API keys to automate pushing code with a tool such as GitHub Actions or Circle CI.

For more information and examples, see [Automate code deploys with CI/CD](ci-cd.md).

## Delete an API key

If you delete an API key, make sure that no existing CI/CD pipelines are using it. Once deleted, an API key and secret cannot be recovered. If you unintentionally delete an API key, create a new one and update any CI/CD workflows that used the deleted API key.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **API Keys** tab.

3. Click **Edit** next to your API key.

    ![Edit API key button](/img/docs/edit-api-key.png)

4. Click **Delete API Key**, enter `Delete`, and then click **Yes, Continue**.
