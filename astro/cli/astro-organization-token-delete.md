---
sidebar_label: "astro organization token delete"
title: "astro organization token delete"
id: astro-organization-token-delete
description: Delete an Organization API token.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available for Deployments on Astro.

:::

Delete an Organization API token.

## Usage

```sh
astro organization token delete
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--force`   | Delete or remove the API token without showing a warning.                                                                                                     | None.   |
| `--name` |The name of the token to delete. | Any string surrounded by quotations. |

## Related commands

- [astro organization token update](cli/astro-organization-token-update.md)
- [astro organization token rotate](cli/astro-organization-token-rotate.md)
- [astro organization switch](cli/astro-organization-switch.md)