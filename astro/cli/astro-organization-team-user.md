---
sidebar_label: "astro organization team user"
title: "astro organization team user"
id: astro-organization-team-user
description: Reference documentation for astro organization team user commands.
hide_table_of_contents: true
---

Manage users in an Astro Team. 

## Usage

This command has several subcommands

### astro organization user team add

Add a user to a Team.

#### Usage 

```sh
astro organization team user add 
```

#### Options 

| Option      | Description                                        | Valid Values     |
| ----------- | -------------------------------------------------- | ---------------- |
| `--team-id` | The ID of the Team where you want to add the user. | A valid Team ID. |
| `--user-id` | The user's ID.                                     | A valid user ID. |

### astro organization user team list

List all users in a Team

#### Usage 

```sh
astro organization team user list 
```

### astro organization user team remove

Remove a user from a Team.

#### Usage 

```sh
astro organization team user remove 
```

#### Options 

| Option      | Description                                        | Valid Values     |
| ----------- | -------------------------------------------------- | ---------------- |
| `--team-id` | The ID of the Team where you want to remove the user. | A valid Team ID. |
| `--user-id` | The user's ID.                                     | A valid user ID. |


## Related Commands

- [`astro organization user update`](cli/astro-organization-user-update.md)
- [`astro workspace user add`](cli/astro-workspace-user-add.md)
