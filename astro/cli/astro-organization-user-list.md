---
sidebar_label: "astro organization user list"
title: "astro organization user list"
id: astro-organization-user-list
description: Reference documentation for astro organization user list command.
hide_table_of_contents: true
---

Manage users in your current Astro Organization.

## Usage

Run `astro organization user list` to list all users, their email, ID, organization role, and account creation date in your Organization. 

## Output

| Output               | Description                                                                                        | Data Type                                  |
| -------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `FULLNAME`               | The full name of the user.  | String                                    |
| `EMAIL` | The email address associated with the user account or email addressed used to invite the user to the Organization. | String |
| `ID` | The user ID. | String |
| `ORGANIZATION ROLE` | The level of permissions granted to the user at the Organization level. Can be `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`. | String |
| `CREATE DATE` | The date the user profile was created. | Date (`YYYY-MM-DDTHH:MM:SSZ`) |


## Related Commands

- [`astro organization user update`](cli/astro-workspace-switch.md)
