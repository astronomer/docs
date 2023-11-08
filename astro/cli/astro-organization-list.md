---
sidebar_label: "astro organization list"
title: "astro organization list"
id: astro-organization-list
description: Reference documentation for the astro organization list command.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

View a list of Organizations that you can access on Astro and their IDs.

## Usage

Run `astro organization list` to view a list of Organizations that you can access on Astro and their IDs. Only the Organizations you have been invited to by an Organization Owner appear on this list.

## Output

| Output | Description                                            | Data Type |
| ------ | ------------------------------------------------------ | --------- |
| `NAME` | The name of the Organizations that you have access to. | String    |
| `ID`   | The Organization ID.                                   | String    |

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro organization switch`](cli/astro-organization-switch.md)
