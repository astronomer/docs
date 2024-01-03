---
sidebar_label: "astro workspace switch"
title: "astro workspace switch"
id: astro-workspace-switch
description: Switch between Workspaces.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts.

:::

Switch between Workspaces.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>
<TabItem value="astro">

## Usage

```sh
astro workspace switch
```

## Options

| Option                    | Description                                                                                  | Valid Values           |
| ------------------------- | -------------------------------------------------------------------------------------------- | ---------------------- |
| `<workspace_id>` (Optional) | The ID of the Workspace you want to switch to. If not specified, the CLI prompts you to choose one. | Any valid Workspace ID |

## Example

Run `astro workspace switch <workspace-id>` to switch between Workspaces.

```sh
astro workspace switch clqw6uskr000008l9370y04jd
```

You can find a Workspace's ID by running `astro workspace list`, or by opening your Workspace and going to **Workspace Settings** > **General** in the Cloud UI. On Astro, if you don't provide a Workspace ID, the CLI prompts you to pick from a list of Workspaces that you belong to in your current Organization.

## Related commands

- [`astro workspace list`](cli/astro-workspace-list.md)

</TabItem>
<TabItem value="software">

## Usage

```sh
astro workspace switch <options>
```

## Options

| Option              | Description                                                                                  | Valid Values           |
| ------------------- | -------------------------------------------------------------------------------------------- | ---------------------- |
| `<workspace_id>`    | The ID of the workspace you want to switch to. Otherwise, the CLI prompts you to choose one. | Any valid Workspace ID |
| `-p`, `--paginated` | Choose whether or not to paginate the list of available Workspaces.           | `TRUE` or `FALSE`      |
| `-s`, `--page-size` | The length of the list per page when paginate is set to `TRUE`.                              | Any integer            |

## Example

Run `astro workspace switch <workspace-id>` to switch between Workspaces.

You can find a Workspace's ID by running `astro workspace list`.

## Related commands

- [`astro workspace list`](cli/astro-workspace-list.md)

</TabItem>
</Tabs>
