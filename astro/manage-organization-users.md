---
sidebar_label: 'Manage Organization users'
title: 'Manage users in an Astro Organization'
id: manage-organization-users
description: Add, edit, or remove users at the Organization level in the Cloud UI.
---

As an Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Organization.

To manage users at the Workspace level, see [Manage Workspace users](manage-workspace-users.md). To manage groups of users, see [Manage Teams](manage-teams.md).

## Prerequisites

- Organization Owner permissions.

For more information on user roles, see [Manage user permissions on Astro](user-permissions.md). 

## Add a user to an Organization

If your Organization has [configured an identity provider (IdP) with Astro](configure-idp#configure-your-sso-identity-provider), assign users to Astro from your identity provider. By default, any users that you assign can join your Organization as an Organization Member without an invite. To change this behavior, see [Disable just-in-time provisioning](configure-idp.md#disable-just-in-time-provisioning).

You can also manually add users to an Organization. You must manually add users in the following circumstances:

- You don't have an IdP configured.
- You disabled just-in-time provisioning.
- You want to invite a user to an Organization from a domain that you don't own, such as a third party consultant.
- You want to invite someone from your company to Astro as a role other than Organization Member.

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Settings** > **Access Management**.
      
3. Click **Invite member**:

4. Enter the user's email.

5. Select an Organization role for the user. See [Organization roles reference](user-permissions.md#organization-roles).

6. Click **Invite member**.

After you add the user, their information appears in the **Users** tab in **Access Management**. To access Astro, the user needs to accept the invitation sent by email and then create an Astro account.

## Update or remove an Organization user

See [User permissions](user-permissions.md) to view the permissions for each available Organization role.

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Settings** > **Access Management**.

3. Find the user in the **Users** list and then click **Edit**.
   
4. (Optional) Edit the user's role. See [Organization roles](user-permissions.md). 
   
5. If you updated the user's role, click **Update member**. To delete the user, click **Remove member**.

:::info

To remove yourself from an Organization as an Organization Owner, one or more Organization Owners must be assigned to the Organization. If you're the only Organization Owner for your Organization, you'll need to assign another Organization Owner before removing yourself from the Organization.

:::

## Add a group of users to Astro using the Astro CLI

You can use the Astro CLI and a shell script to add multiple users to an Organization at once. The shell script reads from a text file which contains user information. You can generate the text file for each new batch of users that need to assigned to an Organization and run the script using the Astro CLI.

1. Create a text file named `users.txt`.
2. Open the text file. On each line, add a user's email and their role separated by a space. The following is an example of how you can write a list for inviting users to an Organization:

    ```text
    user1@astronomer.io ORGANIZATION_MEMBER
    user2@astronomer.io ORGANIZATION_OWNER
    user3@astronomer.io ORGANIZATION_BILLING_ADMIN
    user4@astronomer.io ORGANIZATION_OWNER
    ```

3. Create a file named `add-users.sh` and then add the following script to it:

    ```bash
    #!/bin/bash

    # Check if a file was provided as an argument
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <file>"
        exit 1
    fi
    # Loop through the file to read each user email address and the role, and use Astro CLI to invite them  
    while read line; do
        email=$(echo "$line" | cut -d' ' -f1)
        role=$(echo "$line" | cut -d' ' -f2)
        echo "Inviting $email as $role..."
        astro organization invite "$email" --role "$role"
    done < "$1"
    ```

4. Log in to the Astro CLI using `astro login`, and then run `astro organization list` to ensure that you're in the same Organization where you want to add the users. If you're not in the right Organization, run `astro organization switch`.
5. Run the following command to execute the shell script:

    ```bash
    sh path/to/add-users.sh path/to/users.txt
    ```

6. (Optional) To use this script as part of a CI/CD pipeline, create an [Organization API token](organization-api-tokens.md) and specify the environment variable `ASTRO_API_TOKEN=<your-token>` in your CI/CD environment.

## See also

- [Manage Workspace users](manage-workspace-users.md)
- [Manage Teams](manage-teams.md)
- [Manage user permissions on Astro](user-permissions.md)