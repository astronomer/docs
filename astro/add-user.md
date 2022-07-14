---
sidebar_label: 'Add a user'
title: 'Add a user to Astro'
id: add-user
description: Add a user to a either a Workspace or an Organization on Astro.
---

This guide provides steps for adding a user to an Astro Workspace. As a Workspace Admin or Organization Owner, you can add new team members to Astro and grant them user roles with permissions for specific actions across your Organization.

## Prerequisites

To add a user to Astro, you must have at least one of the following permissions:

- To invite a user to your Organization, you need Organization Owner permissions.
- To invite a user to a specific Workspace, you need Workspace Admin permissions for that Workspace. The user must also already be a part of the Organization that hosts the Workspace.

## Add a user to an Organization

To add a user to an Organization:

1. In the Cloud UI's Organization view, open the **People** tab.
2. Click **Invite member**:

    ![Organization user invite button](/img/docs/invite-org-user.png)

3. Enter the user's email.
4. Set an Organization role for the user.
5. Click **Add member**.

Once you add the user, their information will appear in the **Access** tab as a new entry in the **Members** table. The user needs to accept an invite to the Organization via email and either create an Astro account or log in before they can access the Organization.

## Add a user to a Workspace

To add an existing user from an Organization to a Workspace:

1. In the Cloud UI, open your Workspace and go to the **Access** tab.
2. Click **Add member**:

    ![Workspace user invite button](/img/docs/add-user.png)

3. Enter the user's email.
4. Set a Workspace role for the user. For a list of available roles and their permissions, see [Workspace roles](user-permissions.md#workspace-roles)
5. Click **Add member**.

Once you add the user, their information will appear in the **Access** tab as a new entry in the **Members** table. The user needs to accept an invite to the Workspace via email and log in before they can access the Workspace.
