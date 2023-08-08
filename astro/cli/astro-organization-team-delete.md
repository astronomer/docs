---
sidebar_label: "astro organization team delete"
title: "astro organization team delete"
id: astro-organization-team-delete
description: Reference documentation for astro organization team delete command.
hide_table_of_contents: true
---

Delete a Team from your Organization.

## Usage

```sh
astro organization team delete <team-id>
```

To find a Team ID using the Astro CLI, run `astro organization team list`.

To find a Team ID In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings** > **Access Management** > **Teams** and open your Team. The Team ID is the string after the last slash in the page's URL. For example, the Team ID for `https://cloud.astronomer.io/settings/access/teams/clileesfx425o01kvybpzxcvxd5` is `clileesfx425o01kvybpzxcvxd5`.

## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
