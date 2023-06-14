---
sidebar_label: "astro workspace token rotate"
title: "astro workspace token rotate"
id: astro-workspace-token-rotate
description: Reference documentation for astro workspace token rotate.
hide_table_of_contents: true
---

Rotate a Workspace API token in your current Workspace.

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

## Usage

```sh
astro workspace token rotate --name "My token" --force
```

## Related commands

- [astro workspace token update](cli/astro-workspace-token-update)
- [astro workspace token delete](cli/astro-workspace-token-delete)
- [astro workspace switch](cli/astro-workspace-switch)