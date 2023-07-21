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

For more information on user roles, see [Manage user permissions on Astro](user-permissions.md). To manage groups of users, see [Manage Teams](manage-teams.md).

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



