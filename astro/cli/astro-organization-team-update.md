---
sidebar_label: "astro organization team update"
title: "astro organization team update"
id: astro-organization-team-update
description: Update a Team in your Organization.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::info

This command is only available on Astro.

:::

Update a Team in your Organization.

## Usage

```sh
astro organization team update <flags>
```

## Options

| Option          | Description                             | Valid Values                                                                                       |
| --------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `<team-id>`     | The ID for the Team you want to update. | A valid Team ID.                                                                                   |
| `--name`        | The Team's name.                        | String surrounded by quotation marks.                                                              |
| `--description` | A description for the Team.             | String surrounded by quotation marks.                                                              |
| `-r`, `--role`  | The new role for the team.              | Possible values are `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, and `ORGANIZATION_OWNER`. |

## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
