---
sidebar_label: 'Manage Workspaces'
title: 'Manage Workspaces on Astro'
id: manage-workspaces
description: Create, delete, and update Workspaces on Astro.
---

## Overview

This guide provides steps for creating and managing Workspaces on Astro.

Workspaces are collections of Deployments that can all be accessed by a specific group of users. You can use Workspaces to group Deployments that all share a trait. For example, you can create one Workspace that stores all of your production pipelines and another Workspace that stores all of your development pipelines.

## Create a Workspace

:::info

To create a Workspace, you must have an [Organization-level](user-permissions.md#organization-roles) role.

:::

To create a Workspace, click the **Add Workspace** button from the **Overview** tab.

![Add Workspace button in the Cloud UI](/img/docs/add-workspace.png)

During this initial setup, you can configure a Workspace's name and description. All further Workspace configuration is completed in the Workspace view.

## Workspace View

To to enter your Workspace, click the Workspace in the **Overview** tab. When you click into a Workspace and see a list of that Workspace's Deployments, you are in the **Workspace view** of the Cloud UI. The Workspace view contains several pages for managing your Workspace which are accessible from a sidebar on the left of the screen:

- **Deployments:** Create new Deployments and see key metrics about existing Deployments in the Workspace. For more information, see [Create a Deployment](create-deployment.md).
- **DAGs:** View metrics about individual DAGs across your Workspace. For more information, see [Deployment metrics](deployment-metrics.md#dag-runs).
- **Logs:** View scheduler logs for Deployments in the Workspace. For more information, see [View logs](view-logs.md).
- **Access:** Manage user access to the Workspace.
- **Workspace Settings:** Update or delete Workspace details.

## Manage Workspace Users

As a Workspace Admin, you can add or remove users from your Workspace at any time. Before adding a user, make sure that the user is an existing member of your Organization. If the user is not, [invite them to Astro](add-user.md#add-a-user-to-an-organization) before following the steps below.

To add a user to a Workspace:

1. In the Workspace view, go to the **Access** page.
2. Click **Add member**.
3. Specify the user's email and role within the Workspace. For more information about Workspace roles and permissions, see [User permissions](user-permissions.md).

Once added, the user will see the Workspace listed on the **Overview** page of the Cloud UI. They will also appear as an active Workspace member in the **Access** tab. For more information about inviting users to Astronomer, see [Add a user](add-user.md).

### Update or Remove a Workspace User

To update a Workspace user's access to the Workspace:

1. In the Workspace view, go to the **Access** page.
2. Click the **Edit** button next to the user's entry in the **Member** table:

    ![Edit Workspace user button](/img/docs/edit-workspace-user.png)

From here, you can either update a user's Workspace role or remove the user from the Workspace.

## Update a Workspace

To update a Workspace's name or description, go to the **Workspace Settings** page in the Workspace view. To save any changes to your Workspace, click **Update Workspace**.

### Delete a Workspace

To delete a Workspace, click the **Delete Workspace** button in the **Workspace Settings** page. Note that you can delete a Workspace only if there are no active Deployments in the Workspace.
