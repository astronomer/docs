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

Run `astro organization role list` to view a list of the custom user roles in your Organization and their IDs.

If you want to view the default user roles and their IDs, you need to add the `--include-default-roles` flag. For example,

```sh

astro organization role list --include-default-roles

```

## Options

| Option                  | Description                                                                | Possible Values                  |
| ----------------------- | -------------------------------------------------------------------------- | -------------------------------- |
| --include-default-roles | Display the default [user roles](user-permissions.md) in the organization. | Any of the available user roles. |

## Output

| Output        | Description                     | Data Type |
| ------------- | ------------------------------- | --------- |
| `NAME`        | The name of the role.           | String    |
| `ID`          | The user ID.                    | String    |
| `DESCRIPTION` | A description of the user role. | String    |

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro organization switch`](cli/astro-organization-switch.md)
