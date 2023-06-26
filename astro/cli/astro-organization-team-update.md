---
sidebar_label: "astro organization team update"
title: "astro organization team update"
id: astro-organization-team-update
description: Reference documentation for astro organization team create command.
hide_table_of_contents: true
---

Update a Team in your Organization.

## Usage

```sh
astro organization team update <flags>
```

## Options 

| Option    | Description                                                                                                                                       | Valid Values                                                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<team-id>` | The ID for the Team you want to update. | A valid Team ID.                                                                                                                           |
| `--name` | The Team's name. | String surrounded by quotation marks.                                                                                                                           |
| `--description` | A description for the Team. | String surrounded by quotation marks.                                                                                                                           |

## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
