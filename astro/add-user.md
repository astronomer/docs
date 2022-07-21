---
sidebar_label: 'Add and remove users'
title: 'Add and remove Astro users'
id: add-user
description: Add or remove users in the Cloud UI.
---

As a Workspace Admin or Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Organization. Workspace Admins can remove users from a Workspace, and Organization Owners can remove users from an Organization.

## Prerequisites

- To add or remove Organization users, you need Organization Owner permissions.
- To add or remove Workspace users, you need Workspace Admin permissions for that Workspace. The user must also already be a part of the Organization that hosts the Workspace.
- To remove a user from an Organization, one or more Organization Owners must be assigned to the Organization. If you're the only Organization Owner for your Organization, you'll need to assign another Organization Owner before removing yourself from the Organization. 

For more information on user roles, see [Manage user permissions on Astro](user-permissions.md).
## Add a user to an Organization

1. In the Cloud UI's Organization view, open the **People** tab.
2. Click **Invite member**:

    ![Organization user invite button](/img/docs/invite-org-user.png)

3. Enter the user's email.
4. Set an Organization role for the user.
5. Click **Add member**.

    After you add the user, their information appears in the **Access** tab as a new entry in the **Members** table. To access the Organization, the user needs to accept the invitation sent by email and then create an Astro account or log in.

## Add a user to a Workspace

1. In the Cloud UI, select a Workspace.
2. Click **Access** in the left menu.
3. Click **Add member**.

    ![Workspace user invite button](/img/docs/add-user.png)

4. Enter the user's email.
5. Set a Workspace role for the user. For a list of available roles and their permissions, see [Workspace roles](user-permissions.md#workspace-roles)
6. Click **Add member**.

    After you add the user, their information appears in the **Access** tab as a new entry in the **Members** table. To access the Workspace, the user needs to accept the invitation sent by email and log in.

## Remove users from a Workspace

1. In the Cloud UI, select a Workspace.
2. Click **Access** in the left menu.

   ![Access tab](/img/docs/access-tab.png)

3. Click **Edit** next to the user you want to remove.
4. Click **Remove member**.
5. Click **Yes, Continue** to confirm the removal.

## Remove users from an Organization

Remove a user from an Organization when their role changes, or they leave the Organization. When you remove a user from an Organization, they are automatically removed from all of the Workspaces they had access to within the Organization.

1. In the Cloud UI, click the **People** tab.
2. Click Edit next to the user you want to remove.
3. Click **Remove member**.
4. Click **Yes, Continue** to confirm the removal.