---
sidebar_label: "astro organization"
title: "astro organization"
id: astro-organization
description: Reference documentation for astro organization commands.
hide_table_of_contents: true
---

Manage users in your current Astro Organization.

## Usage

This command includes five subcommands:

- `astro organization user list`: List all users in your Organization.
- `astro organization user invite`: Invite a new user to your Astronomer Organization.
- `astro organization user update`: Update a user's Organization role.
- `astro organization list`: View a list of Organizations that you can access on Astro. Only the Organizations you have been invited to by a System Admin appear on this list.
- `astro organization switch`: Switch to a different Organization that you have access to in Astro.

You can use `astro organization user invite` to invite multiple users to an Organization at a time. See [Add a group of users to Astro using the Astro CLI](add-user.md#add-a-group-of-users-to-astro-using-the-astro-cli).

## Options 

| Option    | Description                                                                                                                                       | Valid Values                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<email>` | Specify the email for the user you want to invite or update. Use only with `astro organization user update` and `astro organization user invite`. | Any valid email                                                                                                                             |
| `--role`  | The user's role in the Organization. Use only with `astro organization user update` and `astro organization user invite`.                         | Valid values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.   The default is `ORGANIZATION_MEMBER` |

## Examples

```sh
# Invite a user to your Organization
astro organization user invite user@cosmicenergy.org --role ORGANIZATION_BILLING_ADMIN

# Update a user's role. The CLI prompts you for the user's email
astro organization user update --role ORGANIZATION_MEMBER
```

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
