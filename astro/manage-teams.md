---
sidebar_label: 'Configure Teams'
title: 'Configure Teams on Astro'
id: manage-teams
description: Create, delete, and update Teams on Astro.
---

_Teams_ are a group of users in an Organization that you can grant the same Organization and Workspace permissions. Organization Owners create, update, or delete Teams. Then, either Organization Owners or Workspace Admins can assign Teams to different Workspaces and define their [Workspace permissions](astro/user-permissions.md#workspace-roles). This is a quicker and more secure way to assign roles to a large amount of users. 

## Create a Team

1. In the Cloud UI, click your Workspace name in the upper left corner, click **Organization Settings**, then click **Access Management**.

2. Click **Teams**.

3. Click **+ Team** to create a new Team.

4. Configure the following details about your Team:

    - **Team Name**: The name for your Team.
    - **Team description**: (Optional) The description for your Team.
    - **Organization role**: The Organization role for your Team. 
    - **Add users**: Choose the Organization users you want to add to the Team. 

    If you don't find the user you want to add, you might need to [add the user to your Organization](manage-organization-users.md#add-a-user-to-an-organization).

5. After you finish adding users to the Team, click **Add Team**.

You can now [add your Team to a Workspace](manage-teams.md#add-a-team-to-a-workspace) and define the Team users' permissions in the Workspace.

## Update existing Teams

1. In the Cloud UI, click your Workspace name in the upper left corner, click **Organization Settings**, then click **Access Management**.

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

## Add Teams to Workspaces with Astro CLI

You can add a Team to Workspaces programmatically with the Astro CLI instead of individually adding them with the Cloud UI. You must be logged into the correct Organization and Workspace 

### Prerequisites

- Install the [Astro CLI](install-cli.md).
- Create a [Team](#create-a-team)

### Add Teams to Workspaces

1. Log in to Astro. 

    ```sh
    astro login astronomer.io
    ```
2. Choose the Workspace where you want to add a Team.
    
    ```sh
    astro workspace
    ```
    :::tip

    If you do not see the Workspace listed, confirm which Organization you're currently working in with `astro organization list`. You can switch to the correct Organization with `astro organization switch`.

    :::

3. Retrieve the Team ID. 

    ```sh
    astro organization team list
    ```
    This command returns the Team ID, team name, creation date, and Organization Role the Team has.

4. Use the Team ID to assign the Team to a Workspace and optionally configure their [Workspace Role](/astro/user-permissions.md#workspace-roles).

    ```sh
    astro workspace team add <team-id> --role
    ```
    Available Role options include `WORKSPACE_MEMBER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`.

5. You can test that your Team assigned correctly by listing all Teams in your current Workspace.

    ```sh
    astro workspace team list
    ```

## Teams and SCIM provisioning

To preserve a single source of truth for user group management, some Team management actions are limited when you [set up SCIM provisioning](set-up-scim-provisioning.md). Specifically, when you set up SCIM provisioning:

- You can't create new Teams.
- You can't add users to existing Teams.

For any Teams that were created before you set up SCIM provisioning, you can still complete the following actions:

- Update the Team's permissions.
- Remove users from the Team.
- Delete the Team.
