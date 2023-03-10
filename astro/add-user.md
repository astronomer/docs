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

If your Organization has a configured identity provider (IdP), assign users to Astro from your identity provider. By default, any users that you assign can join your Organization as an Organization Member without an invite. See [Configure just-in-time provisioning for single sign-on](manage-organization.md#configure-just-in-time-provisioning-for-single-sign-on).

If you want to invite a user to an Organization from a domain that you don't own, such as a third party consultant, or you want to invite someone from your company to Astro with a higher level role, follow these steps.

1. In the Cloud UI Organization view, click the **People** tab.

2. Click **Invite member**:

    ![Organization user invite button](/img/docs/invite-org-user.png)

3. Enter the user's email.

4. Set an Organization role for the user. See [User permissions](user-permissions.md).

5. Click **Add member**.

    After you add the user, their information appears in the **Access** tab as a new entry in the **Members** table. To access the Organization, the user needs to accept the invitation sent by email and then create an Astro account or log in.

## Update or remove an Organization user

See [User permissions](user-permissions.md) to view the permissions for each available Organization role.

1. In the Cloud UI, click the **People** tab.
   
2. Find the user in the **Members** list and then click **Edit**.
   
3. Optional. Edit the user's role. See [User permissions](user-permissions.md). 
   
4. If you updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Add a user to a Workspace

1. In the Cloud UI, select a Workspace.

2. Click **Workspace Settings**.
   
3. In the **Access** tab, click **Add Member**.

    ![Workspace user invite button](/img/docs/add-workspace-member.png)

4. Select the user's name and email address in the **Organization Member** list.
   
5. Select a role for the user and then click **Add member**. See [User permissions](user-permissions.md).

6. Click **Add member**.

    After you add the user, their information appears in the **Access** tab as a new entry in the **Members** list. To access the Workspace, the user needs to accept the invitation sent by email and log in.

## Update or remove a Workspace user

1. In the Cloud UI, select a Workspace.
   
2. Click **Workspace Settings**.

3. Click **Edit** next to the user name:

    ![Edit Workspace user button](/img/docs/edit-workspace-user.png)

4. Optional. Edit the user's name and role. See [User permissions](user-permissions.md).
   
5. If you've updated the user's role, click **Update member**. To delete the user, click **Remove member**.

## Add a group of users to Astro using the Astro CLI

You can use the Astro CLI and a shell script to add multiple users to an Organization or Workspace. Because the shell script reads from a text file, you can automate user management by generating the text file and running the shell script for each new batch of users that need to be assigned to an Organization or Workspace.

1. Create a text file named `users.txt`.
2. Open the text file and add a list of user email addresses that you want to invite to an Organization or Workspace. Every email address should include the user's assigned role. The following is an example of how you can write a list for inviting users to an Organization:

    ```sh
    user1@astronomer.io ORGANIZATION_VIEWER
    user2@astronomer.io ORGANIZATION_OWNER
    user3@astronomer.io ORGANIZATION_ADMIN
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