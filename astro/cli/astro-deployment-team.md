---
sidebar_label: "astro deployment team"
title: "astro deployment team"
id: astro-deployment-team
description: Manage Deployment Teams.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.

:::

Manage Deployment-level Teams.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

This command includes four subcommands: `add`, `list`, `update`, and `remove`.

```sh
astro deployment team add --deployment-id=<your-deployment-id> <team-id> --role --workspace-id
astro deployment team list <deployment-id> <team-id> --role --workspace-id
astro deployment team update --deployment-id=<your-deployment-id> <team-id> --role --workspace-id
astro deployment team remove --deployment-id=<your-deployment-id> <team-id> --role --workspace-id
```

To find a Team ID using the Astro CLI, run `astro organization team list`.

To find a Team ID in the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings** > **Access Management** > **Teams**. Search for your Team in the **Teams** table and copy its **ID**. The ID should look something like `clk17xqgm124q01hkrgilsr49`.

## Options

| Option                         | Description                 | Possible Values                                                 |
| ------------------------------ | --------------------------- | --------------------------------------------------------------- |
| `--deployment-id` (_Required_) | The Deployment for the Team | Any valid Deployment ID                                         |
| `<team-id>` (_Required_)       | The Team's ID               | Any valid Team ID                                               |
| `--role`                       | The role for the team.      | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. |
| `--workspace-id`             | The Workspace from which to remove the user  | Any valid Workspace ID  |


</TabItem>
<TabItem value="software">

## Usage

This command includes four subcommands: `add`, `list`, `update`, and `remove`:

```sh
astro deployment team add --deployment-id=<your-deployment-id> <team-id>
astro deployment team list <deployment-id>
astro deployment team update --deployment-id=<your-deployment-id> <team-id>
astro deployment team remove --deployment-id=<your-deployment-id> <team-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID is `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](cli/astro-workspace-team-list.md) and copy the value in the `ID` column.

## Options

| Option                         | Description                       | Possible Values                                                                                                            |
| ------------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `--deployment-id` (_Required_) | The Deployment for the Team       | Any valid Deployment ID                                                                                                    |
| `<team-id>` (_Required_)       | The Team's ID                     | Any valid Team ID                                                                                                          |
| `--role`                       | The Team's role in the Deployment | Possible values are either `DEPLOYMENT_VIEWER`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_ADMIN`. Default is `DEPLOYMENT_VIEWER` |

</TabItem>
</Tabs>
