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

To find a Team ID In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings** > **Access Management** > **Teams** and open your Team. The Team ID is the string after the last slash in the page's URL. For example, the Team ID for `https://cloud.astronomer.io/settings/access/teams/clileesfx425o01kvybpzxcvxd5` is `clileesfx425o01kvybpzxcvxd5`.

## Options

| Option    | Description                                          | Valid Values                                                                               |
| --------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `--role`  | The Team's role in the Workspace.                    | Possible values are either `WORKSPACE_MEMBER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Related commands

- [`astro workspace team remove`](cli/astro-workspace-team-remove.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
