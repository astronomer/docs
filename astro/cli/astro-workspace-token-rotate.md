---
sidebar_label: "astro workspace token rotate"
title: "astro workspace token rotate"
id: astro-workspace-token-rotate
description: Rotate a Workspace API token.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
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

## Examples

```sh
astro workspace token rotate --name "My token" --force
```

## Related commands

- [astro workspace token update](cli/astro-workspace-token-update.md)
- [astro workspace token delete](cli/astro-workspace-token-delete.md)
- [astro workspace switch](cli/astro-workspace-switch.md)