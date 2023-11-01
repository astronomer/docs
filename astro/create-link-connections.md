---
sidebar_label: 'Create Astro connections'
title: 'Create connections in the Environment Manager'
id: create-link-connections
description: "Create Airflow connections for multiple Deployments in the Astro Environment Manager."
---

You can create and manage connections across Deployments with the Astro Environment Manager in the Cloud UI. This strategy of connection management behaves as if it is an Astro-managed secrets backend, which improves authentication management if you don't use a secrets backend and provides you with method to create a connection once and share it with multiple Airflow Deployments. 

Astro stores your connection configurations and authentication information in Hashicorp Vault and Kubernetes Secrets instead of requiring you to manage it in your own secrets backend. This means you can quickly and securely create connections once and share them to multiple Deployments without having to set up your own secrets backend or handle multiple sets of credentials for making connections to the same resource in multiple Deployments.

When you use the Cloud UI to create and manage connections, you can also:

- Share that connection with all or specific deployments within the workspace
- Choose to override certain fields in the connection at the Deployment level
- Share connections with local development environments when running `astro dev start`
- Use connections in branch-based deploys and PR previews

    ![Example of the Connections tab in the Astro Environment Manager page](/img/docs/connections-env-mgmt.png)

## Create a connection

There are two ways to access the **Environment** page where you can create and manage your connections.
- In your Deployment, go to the **Environment** tab. This view shows you all Cloud UI connections for your Deployment.
- From the main navigation, select **Environment**. This view shows you all the Cloud UI connections for your workspace. 

### Prerequisites

To make changes to connections, you need `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER` [user permissions](user-permissions.md)

### Setup

1. Open the **Environment Manager** page by either
    - Clicking **Environment** in the main menu to open the **Connections** page.
    - Opening the Deployment where you want to link your new connection. Click the **Environment** tab. Creating the connection from the Deployment automatically links the connection to the Deployment
2. Click the **Connection** tab.
3. Click **+ Connection** to add a new connection.
4. Find the service you want to connect from the list of available options.
5. Enter your information in the required fields.

    :::tip

    You can configure your connection with the credentials for a sandbox or development environment. Then, you can later configure your connection to be applied to all Deployments in the workspace by default. This means that when you create new Deployments, they automatically have access to your development environment. Later, you can edit the connection to point to your production resources by using [field overrides](#override-connection-fields).

    :::

6. Click **Create Connection** to make your new connection.

Now you can add connections to Deployments and override particular fields to customize behavior depending on the Deployment it's linked to.

## Link connections to Deployments

After you create a connection, then you can link it to Deployments.

### Prerequisites
- `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER` [user permissions](user-permissions.md)
- A Deployment on Astro. See [Create a Deployment](create-deployment.md)
- A local Astro project created with [the Astro CLI](cli/get-started-cli.md)
- Astro Runtime 9.3.0 or greater

### Step 1: Add link to connection

1. Click **Environment** in the main menu to open the **Connections** page.
2. Click the Connection you want to link to a Deployment.
3. Click **+ Link Deployment**.
4. Choose a Deployment from the list.
5. (Optional) Click **More options** and then add any field overrides for this Deployment. For example, you can specify a default schema to use.
6. Click **Link connection**.

### Step 2: (Optional) Add provider package

If you only added the connection in the Cloud UI and did not include the provider package name in your `requirements.txt` file in your project, you won't be able to use your connection. 

1. Open your project locally.
2. Add the provider package name to your project's `requirements.txt` file includes the provider package for the resource you connected to. Save your changes.
3. Run `astro deploy` to rebuild your containers and push the changes to your Deployment.

## Deployment sharing

You can configure whether Astro links connections to all Deployments in the workspace, or if you need to manually assign a connection to each individual Deployments. This means that you can configure a connection with default values for your sandbox or development environment and set the configuration so that all Deployments in a Workspace use the development environment by default. Then, when you create new Deployments, they automatically have a default connection to your development environment.

When you're ready for your Deployments to connect to your production environment, you can either replace the connection or [override the connection field](#override-connection-fields) values with your production resource information.

If you change the setting from **Restricted** to **Linked to all Deployments**, Astro respects any Connection Field Overrides that you might have configured for existing linked Deployments.

    ![Edit Deployment Sharing settings in the Environment Manager view](/img/docs/connection-restrict-link-all.png)

### Prerequisites
- `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER` [user permissions](user-permissions.md)
- A Deployment on Astro. See [Create a Deployment](create-deployment.md)
- A connection linked to a Deployment
- Astro Runtime 9.3.0 or greater

### Setup

1. Click **Environment** in the main menu to open the **Connections** page.
2. Click the Connection that you want to add per-Deployment field overrides to.
3. Click **Deployment Sharing** and toggle the setting to choose either:
    - **Restricted** - Only share connection individually to Deployments.
    - **Linked to all Deployments** - Link to all current and future workspaces in this Deployment.
4. (Optional) You can also change the default connection field values.
5. Click **Update connection** to save.

## Override connection fields

If you create a connection and link it to a Deployment, you can later edit the connection to specify field overrides. When you override a field, you specify particular values that you want to use for a specific Deployment, but not for others. This way, you can configure the connection and authentication a single time, but still have the flexibility to customize connection at the Deployment level.

For example, you might have created a connection to a Snowflake account, and then add field overrides to specify the default schemas or databases you want each Deployment to use. 

### Prerequisites
- `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER` [user permissions](user-permissions.md)
- A Deployment on Astro. See [Create a Deployment](create-deployment.md)
- A connection linked to a Deployment
- Astro Runtime 9.3.0 or greater

### Setup

1. Click **Environment** in the main menu to open the **Connections** page.
2. Click the Connection that you want to add per-Deployment field overrides to.
3. (Optional) Click **Deployment Sharing** and choose if you want to **Restrict** or **Link to all Deployments**. You can also change the default connection field values.Click **Update connection** to save.
4. Click **Edit** to open the connection configurations for a specific linked Deployment.
5. Add the override values to the fields you want to edit. You might need to open **More options** to find the full list of available fields.
6. Click **Update connection link**.

