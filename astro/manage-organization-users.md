---
sidebar_label: 'Manage Organization users'
title: 'Manage Organization users'
id: manage-organization-users
description: Add, edit, or remove users at the Organization level in the Cloud UI.
---

As aan Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Organization.

To manage users at the Workspace level, see [Manage Workspace users](manage-workspace-users.md). To manage groups of users, see [Manage Teams](manage-teams.md).

## Prerequisites

- To add, edit, or remove Organization users, you need Organization Owner permissions.
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
   
3. Optional. Edit the user's role. See [Organization roles](user-permissions.md). 
   
4. If you updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Add a group of users to Astro using the Astro CLI

You can use the Astro CLI and a shell script to add multiple users to an Organization at a time using a shell script. The shell script reads from a text file that your team creates which contains user information. To automate adding users to Astro, generate the text file for each new batch of users that need to assigned to an Organization and run the script with the Astro CLI.

1. Create a text file named `users.txt`.
2. Open the text file and add a list of user email addresses that you want to invite to your Organization. Every email address should include the user's assigned role. The following is an example of how you can write a list for inviting users to an Organization:

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
    
    while read line; do
        email=$(echo "$line" | cut -d' ' -f1)
        role=$(echo "$line" | cut -d' ' -f2)
        echo "Inviting $email as $role..."
        astro organization invite "$email" --role "$role"
    done < "$1"
    ```

4. Log in to the Astro CLI using `astro login`, and then run `astro organization list` to ensure that you're in the same Organization where you want to add the users. If you're not in the right context, run `astro organization switch`.
5. Run the following command to execute the shell script:

    ```sh
    sh path/to/add-users.sh path/to/users.txt
    ```

6. (Optional) To use this script as part of a CI/CD pipeline, create an [Organization API token](organization-api-tokens.md) and specify the environment variable `ASTRO_API_TOKEN=<your-token>` in your CI/CD environment.

## See also

- [Manage Workspace users](manage-workspace-users.md)
- [Manage Teams](manage-teams.md)
- [Manage user permissions on Astro](user-permissions.md)