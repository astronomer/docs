---
sidebar_label: "astro organization switch"
title: "astro organization switch"
id: astro-organization-switch
description: Switch your current Organization.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available for Deployments on Astro.

:::

Switch the Astro Organization where you're currently working.

## Usage

Run `astro organization switch` to switch between Organizations. In the Astro CLI, you can first run `astro organization list` to see a list of Organizations that you can access and their IDs.

| Option    | Description                                                                                                                                      | Possible Values                                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<organization-id>` | Specify the Astro Organization ID that you want to switch to. | Any valid Organization ID                                                                      |


## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro organization list`](cli/astro-organization-list.md)
