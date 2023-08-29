---
sidebar_label: "astro organization team list"
title: "astro organization team list"
id: astro-organization-team-list
description: Reference documentation for astro organization team list.
hide_table_of_contents: true
---

List all Teams in your current Organization. 

## Usage

```sh
astro organization team list
```

## Output

| Output        | Description                                                                  | Data Type     |
| ------------- | ---------------------------------------------------------------------------- | ------------- |
| `ID`          | The Team ID in the Organization.                                             | String        |
| `NAME`        | Team name.                                                                   | String        |
| `DESCRIPTION` | The description for the Workspace.                                           | String        |
| `IDP MANAGED` | Wheather a Team's members have their access managed by an identity provider. | Boolean       |
| `CREATE DATE` | The date and time that the Team was created in the Organization.             | Date          |

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
