---
sidebar_label: "astro workspace token create"
title: "astro workspace token create"
id: astro-workspace-token-create
description: Reference documentation for astro workspace token create.
hide_table_of_contents: true
---

Create a Workspace API token in your current Workspace.

## Usage

```sh
astro workspace token create
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--clean-output`   | Print only the token as output. Use this flag in automated workflows.                                                                                                      | None   |
| `--description` |The description for the token | Any string surrounded by quotations |
| `--expiration` | The expiration date for the token. By default there is no expiration date. | Any integer between 1 and 3650, used to represent days |
| `--name` | The name for the token. | Any string surrounded by quotations |
| `--role`  | The token's role in the Workspace.                | Possible values are either `WORKSPACE_MEMBER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Examples

```sh
astro workspace token create --name "My production API token" --role WORKSPACE_MEMBER
```

## Related commands

- [astro workspace token update](cli/astro-workspace-token-update.md)
- [astro workspace token rotate](cli/astro-workspace-token-rotate.md)
- [astro workspace switch](cli/astro-workspace-switch.md)