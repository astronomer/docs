---
sidebar_label: 'Configure Teams'
title: 'Configure Teams on Astro'
id: manage-teams
description: Create, delete, and update Teams on Astro.
---

_Teams_ are a group of users in an Organization that you can grant the same Workspace permissions, without needing to define them individually. Organization Owners create, update, or delete Teams. Then, either Organization Owners or Workspace Admins can assign Teams to different Workspaces and define their [Workspace permissions](astro/user-permissions.md#workspace-roles).

## Create a Team

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Access Management**.

2. Click **Teams**.

3. Click **+ Team** to create a new team.

4. Enter a **Team Name** and then click **Add users** to choose the Organization users you want to add to the team. 

    If you don't find the user you want to add, you might need to [add the user to your Organization](add-user.md#add-a-user-to-an-organization).

5. After you finish adding users to the Team, click **Add Team**.

You can now [add your Team to a Workspace](add-user.md#add-a-team-to-a-workspace) and define the Team users' permissions in the Workspace.

## Update existing Teams

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Access Management**.

2. Click **Teams**.

3. Click the name of the Team you want to update.

4. Update your Team:

    - Click **+ Member** to add an existing Organization member to your Team.
    - Click the delete icon to remove Team members.

## Add a Team to a Workspace

1. In the Cloud UI, select a Workspace and click **Workspace Settings** > **Access Management**.

2. Click **Teams**.

3. Click **+ Team**.

4. Select the **Team** you want to add and define their **Workspace Role**, which determines their [Workspace user permissions](/astro/user-permissions.md#workspace-roles).

## Teams and SCIM provisioning

To preserve a single source of truth for user group management, some Team management actions are limited when you [set up SCIM provisioning](set-up-scim-provisioning.md). Specifically, when you set up SCIM provisioning:

- You can't create new Teams.
- You can't add users to existing Teams.

For any Teams that were created before you set up SCIM provisioning, you can still complete the following actions:

- Update the Team's permissions.
- Remove users from the Team.
- Delete the Team.
