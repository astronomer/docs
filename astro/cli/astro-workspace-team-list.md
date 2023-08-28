---
sidebar_label: "astro workspace team list"
title: "astro workspace team list"
id: astro-workspace-team-list
description: Reference documentation for astro workspace team list.
hide_table_of_contents: true
---

List all Teams in your current Workspace as well as their level of [user permissions](https://docs.astronomer.io/astro/user-permissions) within the Workspace. 

## Usage

```sh
astro workspace team list
```

## Output

| Output        | Description                                                                  | Data Type     |
| ------------- | ---------------------------------------------------------------------------- | ------------- |
| `ID`          | The Team ID.                                                                 | String        |
| `Role`        | The type of user permissions all Team members have.                          | String        |
| `Name       ` | Name of the Team.                                                            | String        |
| `Description` | An optional description of the Team.                                         | Boolean       |
| `Create Date` | The date and time that the Team was created in the Organization.             | Date          |

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro organization team list`](cli/astro-organization-team-list.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
