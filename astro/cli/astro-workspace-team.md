---
sidebar_label: "astro workspace team"
title: "astro workspace team"
id: astro-workspace-team
description: Reference documentation for astro workspace team.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Manage Astronomer Software [Teams](https://docs.astronomer.io/software/import-idp-groups).

## Usage

This command includes several subcommands.

### astro workspace team add

Add a Team to a Workspace.

#### Usage

`astro workspace team add --team-id=<team-id> --role=<workspace_level_role>`

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| Option                        | Description                       | Possible Values                                                                   |
| ----------------------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| `--team-id` (_Required_)      | The Team's ID                     | Any valid team ID                                                                 |
| `--role`                      | The Team's role in the Workspace. | Possible values are `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. Default is `WORKSPACE_MEMBER`. |

### astro workspace team list

View a list of all Teams in a Workspace.

#### Usage

```sh
astro workspace team list
```

#### astro workspace team remove

Update a Team from a given Workspace.

#### Usage

```sh
astro workspace team remove <team-id> --workspace-id <workspace-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| Option                        | Description                | Possible Values        |
| ----------------------------- | -------------------------- | ---------------------- |
| `--workspace-id` (_Required_) | The Workspace for the Team | Any valid Workspace ID |

### astro workspace team update

Update a Team's permissions in a given Workspace.

#### Usage

```sh
astro workspace team update <team-id> --workspace-id <workspace-id> --role=<system-role>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Related documentation 

- [Import identity provider groups into Astronomer Software](https://docs.astronomer.io/software/import-idp-groups).

#### Options

| Option                        | Description                       | Possible Values                                                                   |
| ----------------------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| `--workspace-id` (_Required_) | The Workspace for the Team        | Any valid Workspace ID                                                            |
| `<team-id>` (_Required_)      | The Team's ID                     | None                                                                              |
| `--role`                      | The Team's role in the Workspace. | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. |
