---
sidebar_label: "astro organization user list"
title: "astro organization user list"
id: astro-organization-user-list
description: Manage users in your Organization.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Manage users in your current Astro Organization.

## Usage

Run `astro organization user list` to list all users, their email, ID, organization role, and account creation date in your Organization.

## Output

| Output              | Description                                                                                                                                                  | Data Type                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| `FULLNAME`          | The full name of the user.                                                                                                                                   | String                        |
| `EMAIL`             | The email address associated with the user account.                                                                                                          | String                        |
| `ID`                | The user ID.                                                                                                                                                 | String                        |
| `ORGANIZATION ROLE` | The level of permissions granted to the user at the Organization level. Can be `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`. | String                        |
| `IDP MANAGED`       | Whether or not the user is managed through an identity provider (IdP).                                                                                       | Boolean                       |
| `CREATE DATE`       | The date the user profile was created.                                                                                                                       | Date (`YYYY-MM-DDTHH:MM:SSZ`) |

## Related Commands

- [`astro organization user update`](cli/astro-workspace-switch.md)
