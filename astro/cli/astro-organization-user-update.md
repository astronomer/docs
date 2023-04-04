---
sidebar_label: "astro organization user update"
title: "astro organization user update"
id: astro-organization-user-update
description: Reference documentation for astro organization user update.
hide_table_of_contents: true
---

Update user Organization roles in your current Astro Organization.

## Usage

Run `astro organization user update` to update a user's Organization role. The CLI prompts you for the user email address associated with their account.

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
- [`astro organization user invite`](cli/astro-organization-user-invite.md)
- [`astro organization user list`](cli/astro-organization-user-list.md)
