---
sidebar_label: 'Teams'
title: 'Configure Teams on Astro'
id: manage-teams
description: Create, delete, and update Teams on Astro.
---

As an Organization Owner or Workspace Owner, you can use Teams to batch assign Organization and Workspace roles to groups of users. Organization Owners create, update, or delete Teams. Then, either Organization Owners or Workspace Owners can assign Teams to different Workspaces and define their [Workspace permissions](user-permissions.md#workspace-roles).

A _Team_ is a group of users in an Organization that share the same Organization and Workspace permissions. You can use Teams to securely assign permissions for a large group of users across multiple Workspaces. For example, you can create a Team of DAG authors, then assign that Team to each of your development Workspaces as a Workspace author.

You can also assign different roles for each Workspace. For example, you can have a group of DAG authors that has full Workspace Owner permissions for development Workspaces, and that same Team can have only Workspace Member permissions for production Workspaces.

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

:::cli

You can add a Team to multiple Workspaces programmatically using the Astro CLI. See [`astro workspace team add`](cli/astro-workspace-team-add.md) for example output and commands.

:::

## Add a Team to multiple Workspaces using the Astro CLI

You can use the Astro CLI and a shell script to add a Team to multiple Workspaces at once. The shell script reads from a text file which contains Team information. You can generate a text file for each Team that needs to be assigned to Workspaces and run a script to process the file. You must have Organization Owner or Workspace Owner level permissions to add Teams to Workspaces.

1. Create a text file named `teams.txt`.
2. Open the text file. On each line, add a Team ID, the Team's role, and the Workspace ID delimited by spaces. Your text file should look similar to the following:

    ```text
    uclk17xqgm124q01hkrgilsr49 WORKSPACE_MEMBER tbkj96wpfl913p90glqfgkrq398
    uclk17xqgm124q01hkrgilsr49 WORKSPACE_OWNER salk85voek802q89fkpefjqp287
    uclk17xqgm124q01hkrgilsr49 WORKSPACE_OPERATOR rzkj74undj791p78ejofeipo178
    vdml28yrhn235r12ilshjmts50 WORKSPACE_OWNER tbkj96wpfl913p90glqfgkrq398
    ```

3. Create a file named `add-teams.sh` and add the following script to it:

    ```bash
    #!/bin/bash

    # Check if a file was provided as an argument
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <file>"
        exit 1
    fi
    
    while read line; do
        team_id=$(echo "$line" | cut -d' ' -f1)
        role=$(echo "$line" | cut -d' ' -f2)
        workspace_id=$(echo "$line" | cut -d' ' -f3)
        echo "Inviting ${team_id} to ${workspace_id} as $role..."
        astro workspace team add "$team_id" --role "$role" --workspace-id "$workspace_id
    done < "$1"
    ```

4. (Optional) Log in to the Astro CLI using `astro login`, then run `astro workspace list` to ensure that you have access to the Workspaces where you want to add the users. 

5. Run the following command to execute the shell script:

    ```sh
    sh path/to/add-teams.sh path/to/teams.txt
    ```

6. (Optional) To use this script as part of a CI/CD pipeline, create an [Organization API token](organization-api-tokens.md) and specify the following environment variable in your CI/CD environment:

    - **Key**:  `ASTRO_API_TOKEN`
    - **Value**: `<your-api-token>`

## Teams and SCIM provisioning

To preserve a single source of truth for user group management, some Team management actions are limited when you [set up SCIM provisioning](set-up-scim-provisioning.md). Specifically, when you set up SCIM provisioning:

- You can't create new Teams.
- You can't add users to existing Teams.

For any Teams that were created before you set up SCIM provisioning, you can still complete the following actions:

- Update the Team's permissions.
- Remove users from the Team.
- Delete the Team.
