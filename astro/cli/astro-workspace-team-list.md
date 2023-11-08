---
sidebar_label: "astro workspace team list"
title: "astro workspace team list"
id: astro-workspace-team-list
description: List Teams in a Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

List all Teams in your current Workspace as well as their level of [user permissions](https://docs.astronomer.io/astro/user-permissions) within the Workspace.

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
