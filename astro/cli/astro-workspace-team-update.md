---
sidebar_label: "astro workspace team update"
title: "astro workspace team update"
id: astro-workspace-team-update
description: Reference documentation for astro workspace team update.
hide_table_of_contents: true
---

Update a Team's role in your current Workspace.

## Usage

```sh
astro workspace team update <team-id> 
```

To find a Team ID using the Astro CLI, run `astro organization team list`.

To find a Team ID in the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings** > **Access Management** > **Teams**. Search for your Team in the **Teams** table and copy its **ID**. The ID should look something like `clk17xqgm124q01hkrgilsr49`.

## Options

| Option    | Description                                          | Valid Values                                                                               |
| --------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `--role`  | The Team's role in the Workspace.                    | Possible values are either `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Related commands

- [`astro workspace team remove`](cli/astro-workspace-team-remove.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
