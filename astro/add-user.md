---
sidebar_label: 'Add a User'
title: 'Add a User to a Workspace'
id: add-user
description: Add a user to a Workspace on Astro.
---

## Overview

As a Workspace Admin, you can add team members to your Astro Workspace. From here, you can grant them user roles with permissions for specific actions across the Workspace and the Deployments within it.

This guide provides steps for adding a user to an Astro Workspace.

## Prerequisites

To add a user to a Workspace, you must have:

- An [Organization on Astro](install-aws.md).
- Workspace Admin permissions.

## Step 1: Invite the User to Astro

:::info

If your organization integrated an [external Identity Provider (IdP)](configure-idp.md) such as Okta or Azure AD, invite your user to Astro via your IDP's own user management system.

:::

If the user you want to add doesn't already have an account on Astro, tell them to go to https://cloud.astronomer.io and sign up. Once they create an account, they will automatically assume the Organization Member role and see the following screen on their first login:

<div class="text--center">
  <img src="/img/docs/welcome-user.png" alt="Successful account creation screen" />
</div>

Make note of the user's account email for the next step.

## Step 2: Add the User

To add a user with an Astro account to your Workspace:

1. In the Cloud UI, open your Workspace and go to the **Access** tab.
2. Click **Add member**:

    <div class="text--center">
      <img src="/img/docs/add-user.png" alt="Add member button in the access menu" />
    </div>

3. Enter the user's email from Step 1.
4. Set a Workspace role for the user. For a list of available roles and their permissions, see [Workspace Roles](user-permissions.md#workspace-roles)
5. Click **Add member**.

Once you add the user, their information will appear in the **Access** tab as a new entry in the **Members** table.

:::caution

If you attempt to invite a user that does not have an account on Astro, you will see an error in the Cloud UI that reads:

```
An error occurred
<user-email-address> is not a user in your Organization. This user must first create an account at https://cloud.astronomer.io before they can be invited to a Workspace.
```

If you see this error:
- Complete Step 1 above. Ask the user to sign up at https://cloud.astronomer.io. Once their account is created, add the user to your Workspace.
- Make sure that the user's email address is consistent with the email address you're using to add them to your Workspace. The emails must match.

:::
