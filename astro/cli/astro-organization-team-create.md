---
sidebar_label: "astro organization team create"
title: "astro organization team create"
id: astro-organization-team-create
description: Create a new Team in your Organization.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Create a new Team in your Organization.

## Usage

```sh
astro organization team create --name "<team-name>"
```

## Options 

| Option    | Description                                                                                                                                       | Valid Values                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `--name` | The Team's name. | String surrounded by quotation marks.                                                                                                                           |
| `--description` | A description for the Team. | String surrounded by quotation marks.                                                                                                                           |
| `--role`  | The Team's role in the Organization.  | Valid values are `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.  |

## Examples

```sh
# Invite a user to your Organization
astro organization team create --name "Billing Admins" --role ORGANIZATION_BILLING_ADMIN
```

## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
