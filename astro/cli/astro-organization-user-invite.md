---
sidebar_label: "astro organization user invite"
title: "astro organization user invite"
id: astro-organization-user-invite
description: Reference documentation for astro organization user invite command.
hide_table_of_contents: true
---

Invite users tp your current Astro Organization.

## Usage

Run `astro organization user invite` to invite a new user to your Astronomer Organization. You can use `astro organization user invite` to invite multiple users to an Organization at a time. See [Add a group of users to Astro using the Astro CLI](add-user.md#add-a-group-of-users-to-astro-using-the-astro-cli).

## Options 

| Option    | Description                                                                                                                                       | Valid Values                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<email>` | Specify the email for the user you want to invite or update. Use only with `astro organization user update` and `astro organization user invite`. | Any valid email                                                                                                                             |
| `--role`  | The user's role in the Organization. Use only with `astro organization user update` and `astro organization user invite`.                         | Valid values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.   The default is `ORGANIZATION_MEMBER` |

## Examples

```sh
# Invite a user to your Organization
astro organization user invite user@cosmicenergy.org --role ORGANIZATION_BILLING_ADMIN
```

## Related Commands

- [`astro organization-user-update`](cli/astro-organization-user-update.md)
