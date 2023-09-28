---
sidebar_label: "astro workspace team remove"
title: "astro workspace team remove"
id: astro-workspace-team-remove
description: Reference documentation for astro workspace team remove.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info
The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.
:::

Remove a Team from your current Workspace.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

```sh
astro workspace team remove <team-id> --workspace-id <workspace-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| ----------------------------- | -------------------------- | ---------------------- |
| `<team-id>` | The ID for the Team. Use to override CLI prompts. | Any valid Team ID. To retrieve a Team ID, run `astro workspace team list`. |
| `--workspace-id` | The Workspace for the Team Use to override CLI prompts. | Any valid Workspace ID |

</TabITem>
<TabItem value="software">

## Usage

```sh
astro workspace team remove <team-id> --workspace-id <workspace-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| ----------------------------- | -------------------------- | ---------------------- |
| `<team-id>` | The ID for the Team. | Any valid Team ID. To retrieve a Team ID, run `astro workspace list`. |
| `--workspace-id` (_Required_) | The Workspace for the Team. | Any valid Workspace ID |

</TabItem>
</Tabs>

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team remove`](cli/astro-organization-team-delete.md)
