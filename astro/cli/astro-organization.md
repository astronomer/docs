---
sidebar_label: "astro organization"
title: "astro organization"
id: astro-organization
description: Reference documentation for astro organization commands.
hide_table_of_contents: true
---

Manage users in your current Astro Organization.

## Usage

This command includes three subcommands:

- `astro user list`: List all users in your Organization
- `astro user invite`: Invite a new user to your Astronomer Organization. The CLI prompts you for the user's email.
- `astro user update`: Update a user's Organization-level role.

## Options 

| Option    | Description                                                  | Possible Values                                                                                                                             |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<email>` | Specify the email for the user you want to invite or update. Use only with `astro user update` and `astro user invite`. | Any valid email                                                                                                                             |
| `--role`  | The user's role in the Organization. Use only with `astro user update` and `astro user invite`.                         | Possible values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.   Default is `ORGANIZATION_MEMBER` |

## Examples

```sh
# Invite a user to your Organization
astro user invite user@cosmicenergy.org --role ORGANIZATION_BILLING_ADMIN

# Update a user's role. The CLI prompts you for the user's email
astro user update --role ORGANIZATION_MEMBER
```

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro workspace`](cli/astro-workspace.md)
