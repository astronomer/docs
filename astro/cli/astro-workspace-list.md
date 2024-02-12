---
sidebar_label: "astro workspace list"
title: "astro workspace list"
id: astro-workspace-list
description: List Workspaces.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

The behavior and format of this command are the same for both Astro and Software.

:::

Generates a list of all Workspaces within your current Organization that you have access to.

## Usage

Run `astro workspace list` to see the name and Workspace ID for each Workspace to which you have access.

## Output

| Output | Description                                                              | Data Type |
| ------ | ------------------------------------------------------------------------ | --------- |
| `NAME` | The name of the Workspaces in your Organization that you have access to. | String    |
| `ID`   | The Workspace ID.                                                        | String    |

## Related commands

- [`astro workspace switch`](cli/astro-workspace-switch.md)
