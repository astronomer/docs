---
sidebar_label: "astro organization team list"
title: "astro organization team list"
id: astro-organization-team-list
description: List all Teams in your current Organization. 
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

List all Teams in your current Organization. 

## Usage

```sh
astro organization team list
```

## Output

| Column        | Description                                                                  | Data type     |
| ------------- | ---------------------------------------------------------------------------- | ------------- |
| `ID`          | The Team ID in the Organization.                                             | String        |
| `NAME`        | Team name.                                                                   | String        |
| `DESCRIPTION` | The description for the Team.                                           | String        |
| `IDP MANAGED` | Whether the Team is managed through an identity provider. | Boolean       |
| `CREATE DATE` | The date and time that the Team was created in the Organization.             | Date (`YYYY-MM-DDTHH:MM:SSZ`)         |

## Related commands

- [`astro workspace team add`](cli/astro-workspace-team-add.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
