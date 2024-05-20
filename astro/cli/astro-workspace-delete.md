---
sidebar_label: "astro workspace delete"
title: "astro workspace delete"
id: astro-workspace-delete
description: Delete an Astro Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

The behavior and format of this command are the same for both Astro and Software.

:::

Delete an Astro Workspace.

## Usage

```sh
astro workspace delete <workspace-id>
```

You can find a Workspace's ID by running `astro workspace list`. Alternatively, in Astro, you can find a Workspace ID by opening the Workspace and going to **Workspace Settings** > **General** in the Astro UI. If you don't provide a Workspace ID, the CLI prompts you to pick from a list of Workspaces that you belong to in your current Organization.

## Related commands

- [`astro workspace update`](cli/astro-workspace-update.md)
- [`astro deployment delete`](cli/astro-deployment-delete.md)
