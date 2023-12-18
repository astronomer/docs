---
sidebar_label: 'Create connections in Astro'
title: 'Create Airflow connections in the Cloud UI'
id: create-and-link-connections
description: "Create Airflow connections and link them to multiple Deployments in the Astro Environment Manager."
---

You can create and manage Airflow connections for Deployments with the Astro Environment Manager in the Cloud UI. The Environment Manager uses an Astro-managed secrets backend to store connection configurations as Kubernetes Secrets.

Using the Environment Manager, you can quickly and securely create connections once and share them to multiple Deployments without having to set up your own secrets backend. You can also create a connection once and use it across multiple Airflow Deployments.

For example, you can configure a connection with the credentials for a sandbox or development environment. Then, you can later configure your connection to be applied to all Deployments in the workspace by default. This means that when you create new Deployments, they automatically have access to your development environment. Later, you can edit the connection to point to your production resources by using [field overrides](#override-connection-fields).

Compared to creating a connection in the Airflow UI, when you create a connection in the Cloud UI, you can:

- Share the connection with multiple Deployments within the Workspace.
- Override fields in the connection for individual Deployments.
- Use configured connections in local Airflow environments. See [Import and export connections and variables](import-export-connections-variables.md#from-the-astro-cloud-ui).
- Use connections in branch-based deploys and PR previews.

Workspace Owners and Operators can create and assign connections, while Workspace Authors can view configured connections and use them in Deployments. If your Organization has **Environment Secrets Fetching** enabled, you can additionally use configured connections, including ones that contain secrets, in local development environments. See [Import and export connections and variables](import-export-connections-variables.md#from-the-astro-cloud-ui).

![Example of the Connections tab in the Astro Environment Manager page](/img/docs/connections-env-mgmt.png)

## Prerequisites

- Workspace Operator or Workspace Owner [user permissions](user-permissions.md)
- A Deployment on Astro. See [Create a Deployment](create-deployment.md)
- Astro Runtime 9.3.0 or greater

## Create a connection

You can create connections both at the Deployment and Workspace level. When you create a connection at the Deployment level, the connection details are available only to that specific Deployment. When you create a connection at the Workspace level, you can apply the connection to several Deployments and override specific fields as needed for each Deployment.

To create a connection at the Workspace level:

1. In the Cloud UI, click **Environment** in the left menu to open the **Connections** page.
2. Click **+ Connection** to add a new connection.
3. Find the service you want to connect from the list of available options.
5. Enter the information for your connection in the listed fields.
6. Click **Create Connection**.
7. Make your connection accessible to Deployments. See [Link connections to Deployments](#link-connections-to-deployments).

To create a connection at the Deployment level:

1. In the Cloud UI, select a Deployment, then click the **Environment** tab within the Deployment menu.
3. Click **+ Connection** to add a new connection.
4. Find the service you want to connect from the list of available options.
5. Enter your information in the required fields.
6. Click **Create Connection** to make your new connection.

After you create a connection, you can reference its **Connection ID** from DAG code like you would with any Airflow connection created through the Airflow UI.

## Link connections to Deployments

After you create a connection at the Workspace level, you can link it to multiple Deployments. Linking connections is useful for standardizing external resource usage across your entire team.

For the most flexibility, you can set default connections and override the connection details per-Deployment based on details like the Deployment's usage and environment type (production or development).

### Step 1: Link the connection

1. In the Cloud UI, click **Environment** in the left menu to open the **Connections** page.
2. Click the connection you want to link to a Deployment.
3. Click **+ Link Deployment**.
4. Choose a Deployment from the list that appears.
5. (Optional) Click **More options** and then add any field overrides for this Deployment. For example, if your connection requests access to a development database by default, you can override its details to instead request access to a production database.
6. Click **Link connection**.

### Step 2: (Optional) Add provider packages to your Deployment

Some connection types require installing dependencies on your Deployment through provider packages. If your connection type requires a provider package and the provider package is neither [included in Astro Runtime](https://docs.astronomer.io/astro/runtime-image-architecture#provider-packages) nor included in the `requirements.txt` file of your Astro project, Airflow won't be able to use your connection.

1. Open the local Astro project for your Deployment.
2. Add the required provider package name to your project's `requirements.txt`. Save your changes.
3. Run `astro deploy` to rebuild your project image and push the changes to your Deployment.

## Configure connection sharing for a Workspace

You can configure Astro to link Workspace-level connections to all Deployments in the Workspace by default.

This is useful, for example, when you need to configure a connection for development environments that all Deployments in a Workspace should start with. Then, when you create new Deployments, they automatically have a default connection to your development resources.

When you're ready to connect your Deployments to production resources, you can either replace the connection or [override the connection field](#override-connection-fields) values with your production resource information.

If you change the setting from **Restricted** to **Linked to all Deployments**, Astro respects any connection field overrides that you might have configured for existing linked Deployments.

![Edit Deployment Sharing settings in the Environment Manager view](/img/docs/connection-restrict-link-all.png)

1. Click **Environment** in the main menu to open the **Connections** page.
2. Click the connection that you want to add per-Deployment field overrides to.
3. Click **Deployment Sharing** and toggle the setting to choose either:
    - **Restricted**: Only share the connection individually to Deployments.
    - **Linked to all Deployments**: Link to all current and future Deployments in this Workspace.
4. (Optional) Change the default connection field values.
5. Click **Update connection** to save.

## Override connection fields

If you create a connection at the Workspace level and link it to a Deployment, you can later edit the connection within the Deployment to specify field overrides. When you override a field, you specify values that you want to use for a one Deployment, but not for others. This way, you can configure the connection and authentication a single time, but still have the flexibility to customize connection at the Deployment level.

For example, you might have created a connection to a Snowflake account, and then add field overrides to specify the default schemas or databases you want each Deployment to use.

1. Click **Environment** in the main menu to open the **Connections** page.
2. Click the connection that you want to add per-Deployment field overrides to.
3. (Optional) Click **Deployment Sharing** and choose if you want to **Restrict** or **Link to all Deployments**. You can also change the default connection field values. Click **Update connection** to save.
4. Click **Edit** to open the connection configurations for a specific linked Deployment.
5. Add the override values to the fields you want to edit. You might need to open **More options** to find the full list of available fields.
6. Click **Update connection link**.