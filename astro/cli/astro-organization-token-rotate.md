---
sidebar_label: "astro organization token rotate"
title: "astro organization token rotate"
id: astro-organization-token-rotate
description: Reference documentation for astro organization token rotate.
hide_table_of_contents: true
---

Rotate an Organization API token.

## Usage

```sh
astro workspace token rotate <flags>
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--clean-output`   | Print only the token as output. Use this flag in automated workflows.                                                                                                      | None   |
| `--force` | Rotate the token without showing a warning |  None |
| `--name` | The name for the token. | Any string surrounded by quotations |

## Examples

```sh
astro organization token rotate --name "My token" --force
```

## Related commands

- [astro organization token update](cli/astro-workspace-token-update.md)
- [astro organization token delete](cli/astro-workspace-token-delete.md)
- [astro organization switch](cli/astro-workspace-switch.md)