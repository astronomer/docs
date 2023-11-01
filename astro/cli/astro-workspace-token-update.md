---
sidebar_label: "astro workspace token update"
title: "astro workspace token update"
id: astro-workspace-token-update
description: Update a Workspace API token.
hide_table_of_contents: true
---

Update a Workspace API token in your current Workspace.

## Usage

```sh
astro workspace token update <flags>
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--clean-output`   | Print only the token as output. Use this flag in automated workflows.                                                                                                      | None   |
| `--description` | The description for the token | Any string surrounded by quotations |
| `--expiration` | The expiration date for the token. By default there is no expiration date. | Any integer between 1 and 3650, used to represent days |
| `--name` | The current name for the token. | Any string surrounded by quotations |
| `--new-name` | The updated name for the token. | Any string surrounded by quotations |
| `--role`  | The token's role in the Workspace.                | Possible values are either `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Examples

```sh
astro workspace token update --new-name "My updated API token" --role WORKSPACE_MEMBER
```

## Related commands

- [astro workspace token rotate](cli/astro-workspace-token-rotate.md)
- [astro workspace token delete](cli/astro-workspace-token-delete.md)
- [astro workspace switch](cli/astro-workspace-switch.md)