---
sidebar_label: "astro organization user invite"
title: "astro organization user invite"
id: astro-organization-user-invite
description: Reference documentation for astro organization user invite command.
hide_table_of_contents: true
---

Invite users to your current Astro Organization.

:::caution

This command will replace `astro user invite`. Any instances in your projects or automation where you use `astro user invite` needs to be updated to `astro organization user invite` before support for `astro user invite` ends.

:::

## Usage

Run `astro organization user invite` to invite a new user to your Astronomer Organization. You can use `astro organization user invite` to invite multiple users to an Organization at a time. By default, new users are added as an `ORGANIZATION_MEMBER`. See [Add a group of users to Astro using the Astro CLI](add-user.md#add-a-group-of-users-to-astro-using-the-astro-cli). 

You must add new users to an Astro Organization before you can add them to specific Astro Workspaces. See [`astro workspace user add`](cli/astro-workspace-user-add.md). 

## Options 

| Option    | Description                                                                                                                                       | Valid Values                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<email>` | Specify the email for the user you want to invite or update. Use only with `astro organization user update` and `astro organization user invite`. | Any valid email                                                                                                                             |
| `--role`  | The user's role in the Organization. Use only with `astro organization user update` and `astro organization user invite`.  By default, new users are added as an `ORGANIZATION_MEMBER`.                        | Valid values are `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.  |

## Examples

```sh
# Invite a user to your Organization
astro organization user invite user@cosmicenergy.org --role ORGANIZATION_BILLING_ADMIN
```

## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
