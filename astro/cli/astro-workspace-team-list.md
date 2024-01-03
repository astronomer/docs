---
sidebar_label: "astro workspace team list"
title: "astro workspace team list"
id: astro-workspace-team-list
description: List Teams in a Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts.

:::

List all Teams in your current Workspace, as well as their level of user permissions within the Workspace.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

```sh
astro workspace team list
```

## Output

| Output        | Description                                                      | Data Type                     |
| ------------- | ---------------------------------------------------------------- | ----------------------------- |
| `ID`          | The Team ID.                                                     | String                        |
| `Role`        | The Team's role in the Workspace.                                | String                        |
| `Name`        | The name of the Team.                                            | String                        |
| `Description` | The Team description.                                            | Boolean                       |
| `Create Date` | The date and time that the Team was created in the Organization. | Date (`YYYY-MM-DDTHH:MM:SSZ`) |

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro organization team list`](cli/astro-organization-team-list.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)

</TabItem>
<TabItem value="software">

## Usage

```sh
astro workspace team list <options>
```

## Options

| Option           | Description                                      | Valid Values           |
| ---------------- | ------------------------------------------------ | ---------------------- |
| `<workspace_id>` | The Workspace you want to list Teams for. | Any valid Workspace ID |

## Output

| Output        | Description                                                      | Data Type                     |
| ------------- | ---------------------------------------------------------------- | ----------------------------- |
| `ID`          | The Team ID.                                                     | String                        |
| `Role`        | The Team's role in the Workspace.                                | String                        |
| `Name`        | The name of the Team.                                            | String                        |
| `Description` | The Team description.                                            | Boolean                       |
| `Create Date` | The date and time that the Team was created in the Organization. | Date (`YYYY-MM-DDTHH:MM:SSZ`) |

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro organization team list`](cli/astro-organization-team-list.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)

</TabItem>
</Tabs>
