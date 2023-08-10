---
sidebar_label: "astro workspace team add"
title: "astro workspace team add"
id: astro-workspace-team-add
description: Reference documentation for astro workspace team add.
hide_table_of_contents: true
---

Add a Team to your current Workspace and grant it a Workspace role.

## Usage

```sh
astro workspace team add <team-id> 
```

To find a Team ID using the Astro CLI, run `astro organization team list`.

To find a Team ID in the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Access Management** > **Teams** and open your Team. The Team ID is the string after the last slash in the page's URL. For example, the Team ID for `https://cloud.astronomer.io/settings/access/teams/clileesfx425o01kvybpzxcvxd5` is `clileesfx425o01kvybpzxcvxd5`.

## Options

| Option    | Description                                          | Valid Values                                                                               |
| --------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `--role`  | The Team's role in the Workspace.                    | Possible values are either `WORKSPACE_MEMBER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Related commands

- [`astro workspace team remove`](cli/astro-workspace-team-remove.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
