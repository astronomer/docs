---
sidebar_label: 'astro team'
title: 'astro team'
id: astro-team
description: Reference documentation for astro team.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Manage system-level Teams on Astronomer Software. See [Import identity provider groups into Astronomer Software](https://docs.astronomer.io/software/import-idp-groups).

## Usage 

This command has several subcommands. Read the following sections to learn how to use each subcommand.

### astro team get 

View information for a single Team. 

#### Usage  

```sh
astro team get <team-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-a`, `--all` | View all information about the Team | None  |
| `-r`, `--roles` | View role details for the Team  | None  |
| `-u`, `--users` | View all users in the Team  | None  |

### astro team list 

List all Teams on Astronomer Software.

#### Usage  

```sh
astro team list 
```

#### Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-a`, `--all` | View all information about the Team | None  |
| `-p` `--paginated ` | Paginate the list of Teams. If `--page-size` is not specified, the default page size is 20. | None            |
| `-s` `--page-size`  | The page size for paginated lists.                                                               | Any integer     |

### astro team update 

Update an Astro Team's system-level role.

#### Usage  

```sh
astro team update <team-id> --role=<system-role>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID is `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-r` `--role`       | The Team's system-level role | Possible values are `SYSTEM_VIEWER`, `SYSTEM_EDITOR`, or `SYSTEM_ADMIN`. |