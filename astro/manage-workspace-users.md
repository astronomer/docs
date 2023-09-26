---
sidebar_label: 'Workspace users'
title: 'Manage users in your Astro Workspace'
id: manage-workspace-users
description: Add, edit, or remove users within a Workspace on Astro.
---

As a Workspace Owner or an Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Workspace.

To manage users at the Organization level, see [Manage Organization users](manage-organization-users.md). To manage groups of users, see [Manage Teams](manage-teams.md).

## Prerequisites

To add, edit, or remove Workspace users from a given Workspace, you need either Organization Owner permissions or Workspace Owner permissions for the Workspace.

## Add a user to a Workspace

1. In the Cloud UI, click **Workspace Settings** > **Access Management**.
   
2. In the **Users** tab, click **+ Member**.
   
3. Select the user's name and email address in the **Organization Member** list.
   
4. Select a role for the user and then click **Add member**. See [Workspace roles reference](user-permissions.md#workspace-roles).

After you add the user, their information appears in the **Users** tab as a new entry in the **Members** list. 

You can also add groups of users to a Workspace through Teams. See [Manage Teams](manage-teams.md).

## Update or remove a Workspace user

1. In the Cloud UI, go to **Workspace Settings** > **Access Management**.

2. Click **Edit** next to the user's name.

3. (Optional) Edit the user's name and role. See [Workspace roles](user-permissions.md).
   
4. If you've updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Add a group of users to a Workspace using the Astro CLI

You can use the Astro CLI and a shell script to add multiple users to a Workspace at once. The shell script reads from a text file which contains user information. You can generate a text file for each new batch of users that need to be assigned to a Workspace and run the script with the Astro CLI.

1. Create a text file named `users.txt`.
2. Open the text file. On each line, add a user's email and their role separated by a space. The following is an example of how you can write a list for inviting users to an Organization:

    ```text
    user1@astronomer.io WORKSPACE_MEMBER
    user2@astronomer.io WORKSPACE_OWNER
    user3@astronomer.io WORKSPACE_OPERATOR
    user4@astronomer.io WORKSPACE_OWNER
    ```

3. Create a file named `add-users.sh` and add the following script to it:

    ```bash
    #!/bin/bash

    # Check if a file was provided as an argument
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <file>"
        exit 1
    fi
    
    while read line; do
        email=$(echo "$line" | cut -d' ' -f1)
        role=$(echo "$line" | cut -d' ' -f2)
        echo "Inviting $email as $role..."
        astro workspace user add "$email" --role "$role"
    done < "$1"
    ```

4. Log in to the Astro CLI using `astro login`, then run `astro workspace list` to ensure that you're in the same Workspace where you want to add the users. If you're not in the right Workspace, run `astro workspace switch`.
5. Run the following command to execute the shell script:

    ```sh
    sh path/to/add-users.sh path/to/users.txt
    ```

6. (Optional) To use this script as part of a CI/CD pipeline, create an [Organization API token](organization-api-tokens.md) or [Workspace API token](workspace-api-tokens.md) and specify the environment variable `ASTRO_API_TOKEN=<your-token>` in your CI/CD environment. Note that you can use Workspace API tokens to manage users only at the Workspace level.

## See also

- [Manage Organization users](manage-organization-users.md)
- [Manage Teams](manage-teams.md)
- [Manage user permissions on Astro](user-permissions.md)
