---
sidebar_label: 'Manage Workspaces'
title: 'Manage Workspaces on Astro'
id: manage-workspaces
description: Create, delete, and update Workspaces on Astro.
---

Workspaces are collections of Deployments that can be accessed by a specific group of users. You can use Workspaces to group Deployments that share a business use case or environment trait.

Some common ways to implement Workspaces are:

- Using a **single Workspace** for an entire Organization, with all development and production pipelines hosted together.
- Using a **Workspace per environment**. For example, you might have a production Workspace that stores all of your production pipelines and a development Workspace that stores all of your development pipelines.
- Using a **Workspace per team**. For example, you might have a Workspace for your Data Science team and a separate Workspace for your Data Engineer team, with each team's Workspace hosting both production and development pipelines.
- Using a **Workspace per project**. For example, you might have a Workspace called "Sales Analytics Project" that hosts both production and development pipelines.

This document explains how to configure Workspace details. To manage Workspace users, see [Manage Astro users](add-user.md).

## Create a Workspace

:::info

To create a Workspace, you must have an [Organization-level](user-permissions.md#organization-roles) role.

:::

To create a Workspace, click the **Add Workspace** button from the **Overview** tab.

![Add Workspace button in the Cloud UI](/img/docs/add-workspace.png)

During this initial setup, you can configure a Workspace's name and description. All further Workspace configuration is completed in the Workspace view.

## Workspace view

To to enter your Workspace, click the Workspace in the **Overview** tab. When you click into a Workspace and see a list of that Workspace's Deployments, you are in the **Workspace view** of the Cloud UI. The Workspace view contains several pages for managing your Workspace which are accessible from a sidebar on the left of the screen:

- **Home**: View the status of your Deployments and select recently accessed Deployments. 
- **Deployments:** Create new Deployments and see key metrics about existing Deployments in the Workspace. For more information, see [Create a Deployment](create-deployment.md).
- **DAGs:** View metrics about individual DAGs across your Workspace. For more information, see [Deployment metrics](deployment-metrics.md#dag-runs).
- **Workspace Settings:** Update Workspace details, including Workspace user permissions, the Workspace name, and the Workspace description.

## Update Workspace details

1. In the Cloud UI, select a Workspace.
   
2. Click **Workspace Settings** and then click the **Details** tab.
   
3. Click **Edit Details**, update the Workspace name or description, and then click **Update**.

## Delete a Workspace

1. In the Cloud UI, select a Workspace.
   
2. Click **Workspace Settings**.
   
3. Click the option menu at the top of the page and select **Delete Workspace**. This option isn't available when there are active Deployments in the Workspace.

    ![Delete Workspace button](/img/docs/delete-workspace.png)

4. In the confirmation dialog, enter `delete` and then click **Yes, Continue**.

