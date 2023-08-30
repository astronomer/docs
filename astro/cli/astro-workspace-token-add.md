---
sidebar_label: "astro workspace token add"
title: "astro workspace token add"
id: astro-workspace-token-add
description: Reference documentation for astro workspace token add.
hide_table_of_contents: true
---

Add an Organization API token to your current Workspace and grant it Workspace permissions.

## Usage

```sh
astro workspace token add
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--org-token-name`   | The name of the Organization API token you want to add to your Workspace.                                                                                                      | Any string enclosed in quotations    |
| `--enforce-ci-cd` | The Workspace role to grant to the Organization API token. | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |

## Related commands

- [astro workspace token update](cli/astro-workspace-token-update.md)
- [astro workspace token rotate](cli/astro-workspace-token-rotate.md)
- [astro workspace switch](cli/astro-workspace-switch.md)