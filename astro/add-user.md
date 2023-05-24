---
sidebar_label: 'Manage users'
title: 'Manage Astro users'
id: add-user
description: Add, edit, or remove users in the Cloud UI.
---

As a Workspace Admin or Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Organization. Workspace Admins can remove users from a Workspace, and Organization Owners can remove users from an Organization.

## Prerequisites

- To add, edit, or remove Organization users, you need Organization Owner permissions.
- To add edit, or remove Workspace users, you need Workspace Admin permissions for a given Workspace. The user must also already be a part of the Organization that hosts the Workspace.
- To remove yourself from an Organization as an Organization Owner, one or more Organization Owners must be assigned to the Organization. If you're the only Organization Owner for your Organization, you'll need to assign another Organization Owner before removing yourself from the Organization.

For more information on user roles, see [Manage user permissions on Astro](user-permissions.md).

## Add a user to an Organization

If your Organization has a configured identity provider (IdP), assign users to Astro from your identity provider. By default, any users that you assign can join your Organization as an Organization Member without an invite. To change this behavior, see [Disable just-in-time provisioning](configure-idp.md#disable-just-in-time-provisioning).

If you want to invite a user to an Organization from a domain that you don't own, such as a third party consultant, or you want to invite someone from your company to Astro with a higher level role, follow these steps.

1. In the Cloud UI, go to **Settings** > **Access Management**.

2. Click **Invite member**:

3. Enter the user's email.

4. Set an Organization role for the user. See [Organization roles reference](user-permissions.md#organization-roles).

5. Click **Add member**.

    After you add the user, their information appears in **Access Management** as a new entry in the **Members** table. To access the Organization, the user needs to accept the invitation sent by email and then create an Astro account or log in.

## Update or remove an Organization user

See [User permissions](user-permissions.md) to view the permissions for each available Organization role.

1. In the Cloud UI, go to **Settings** > **Access Management**.
   
2. Find the user in the **Members** list and then click **Edit**.
   
3. Optional. Edit the user's role. See [Update Organization roles](user-permissions.md#update-organization-roles). 
   
4. If you updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Add a user to a Workspace

1. In the Cloud UI, select a Workspace.

2. Click **Workspace Settings**.
   
3. In the **Access Management** tab, click **Add Member**.

4. Select the user's name and email address in the **Organization Member** list.
   
5. Select a role for the user and then click **Add member**. See [Workspace roles reference](user-permissions.md#workspace-roles).

6. Click **Add member**.

    After you add the user, their information appears in the **Access Management** tab as a new entry in the **Members** list. To access the Workspace, the user needs to accept the invitation sent by email and log in.

## Update or remove a Workspace user

1. In the Cloud UI, select a Workspace.
   
2. Click **Workspace Settings**.

3. Click **Edit** next to the user name:

4. Optional. Edit the user's name and role. See [Update Workspace roles](user-permissions.md#update-workspace-roles).
   
5. If you've updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Make a Team

_Teams_ are a group of users in an Organization that you can grant the same Workspace permissions, without needing to define them individually. Organization Owners create or modify Teams across Workspaces. Then, either Organization Owners or Workspace Admins can assign Teams to different Workspaces and define their [Workspace permissions](astro/user-permissions.md#workspace-roles).

### Create a Team

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Access Management**.

2. Click **Teams**.

3. Click **+ Team** to create a new team.

4. Enter a **Team Name** and then click **Add users** to choose the Organization users you want to add to the team. 

    If you don't find the user you want to add, you might need to [add the user to your Organization](#add-a-user-to-an-organization).

5. After you finish adding users to the Team, click **Add Team**.

You can now [add your Team to a Workspace](#add-a-team-to-a-workspace) and define the Team users' permissions in the Workspace.

### Update existing Teams

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Access Management**.

2. Click **Teams**.

3. Click the name of the Team you want to update.

4. Update your Team:

    - Click **+ Member** to add an existing Organization member to your Team.
    - Click the delete icon to remove Team members.

### Add a Team to a Workspace

1. In the Cloud UI, select a Workspace and click **Workspace Settings** > **Access Management**.

2. Click **Teams**.

3. Click **+ Team**.

4. Select the **Team** you want to add and define their **Workspace Role**, which determines their [Workspace user permissions](/astro/user-permissions.md#workspace-roles).

## Add a group of users to Astro using the Astro CLI

You can use the Astro CLI and a shell script to add multiple users to an Organization or Workspace at a time using a shell script. The shell script reads from a text file that your team creates which contains user information. To automate adding users to Astro, generate the text file for each new batch of users that need to assigned to an Organization or Workspace and run the script with the Astro CLI.

1. Create a text file named `users.txt`.
2. Open the text file and add a list of user email addresses that you want to invite to an Organization or Workspace. Every email address should include the user's assigned role. The following is an example of how you can write a list for inviting users to an Organization:

    ```sh
    user1@astronomer.io ORGANIZATION_MEMBER
    user2@astronomer.io ORGANIZATION_OWNER
    user3@astronomer.io ORGANIZATION_BILLING_ADMIN
    user4@astronomer.io ORGANIZATION_OWNER
    ```

3. Create a file named `add-users.sh` and then add the following script to it:

    ```sh
    #!/bin/bash

    # Check if a file was provided as an argument
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <file>"
        exit 1
    fi
    
    # Read each line in the file and invite the user. 
    # Replace 'organization invite' with 'organization add' if you're inviting users to an Organization.
    while read line; do
        email=$(echo "$line" | cut -d' ' -f1)
        role=$(echo "$line" | cut -d' ' -f2)
        echo "Inviting $email as $role..."
        astro organization invite "$email" --role "$role"
    done < "$1"
    ```

    Replace the Astro CLI command with `astro workspace user add "$email" --role "$role"` if you're inviting a group of users to an Organization. Note that users must be first invited to an Organization before they can be added to a Workspace. 

4. Log in to the Astro CLI using `astro login`, and then run `astro organization list` or `astro workspace list` to ensure that you're in the same Organization or Workspace where you want to add the users. If you're not in the right context, run `astro organization switch` or `astro workspace switch`.
5. Run the following command to execute the shell script:

    ```sh
    sh path/to/add-users.sh path/to/users.txt
    ```
6. (Optional) To use this script as part of a CI/CD pipeline, create an [Organization API token](organization-api-tokens.md) or [Workspace API token](workspace-api-tokens.md) and specify the environment variable `ASTRO_API_TOKEN=<your-token>` in your CI/CD environment. Note that you can use Workspace API tokens to manage users only at the Workspace level.



