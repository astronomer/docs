---
sidebar_label: "astro organization role list"
title: "astro organization role list"
id: astro-organization-role-list
description: Reference documentation for the astro organization role list command.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::publicpreview
:::

:::info

This command is only available on Astro.

:::

View a list of all the roles in your Organizations.

## Usage

Run `astro organization role list` to view a list of the [user roles](user-permissions.md) in your Organization and their IDs.

## Output

| Output        | Description                                                   | Data Type |
| ------------- | ------------------------------------------------------------- | --------- |
| `NAME`        | The name of the Organizations that you have access to.        | String    |
| `ID`          | The user ID.                                                  | String    |
| `DESCRIPTION` | A description of the user role you can assign permissions to. | String    |

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro organization switch`](cli/astro-organization-switch.md)
