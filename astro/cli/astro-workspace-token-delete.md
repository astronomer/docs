---
sidebar_label: "astro workspace token delete"
title: "astro workspace token delete"
id: astro-workspace-token-delete
description: Delete a Workspace API token.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available for Deployments on Astro.

:::

Delete a Workspace API token or remove an Organization API token in your current Workspace.

## Usage

```sh
astro workspace token delete
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--force`   | Delete or remove the API token without showing a warning.                                                                                                     | None   |
| `--name` |The name of the token to delete. | Any string surrounded by quotations |

## Related commands

- [astro workspace token update](cli/astro-workspace-token-update.md)
- [astro workspace token rotate](cli/astro-workspace-token-rotate.md)
- [astro workspace switch](cli/astro-workspace-switch.md)