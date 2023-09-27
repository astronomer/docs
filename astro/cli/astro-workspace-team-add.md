---
sidebar_label: "astro workspace team add"
title: "astro workspace team add"
id: astro-workspace-team-add
description: Reference documentation for astro workspace team add.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info
The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.
:::

Add a Team to your current Workspace and grant it a Workspace role.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

```sh
astro workspace team add <options>
```

If you run the command with no options specified, the CLI lists Teams in your Organization and prompts you to select one. It then adds the Team to your cuurent Workspace with the Workspace Member role.

To add a Team to a specific Workspace, specify the Workspace using the `--workspace-id` flag. To find a Workspace ID, run `astro workspace list`.

## Options

| Option           | Description                                                               | Valid Values                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `--team-id`      | The ID for the Team to add to a Workspace. Bypasses the selection prompt. | Any valid Team ID. You can find available Team ID's by running `astro organization team list`.                                         |
| `-r`, `--role`   | The Team's role in the Workspace.                                         | Possible values are `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. Default is `WORKSPACE_MEMBER`. |
| `--workspace-id` | The ID for the Workspace where you want to add the Team.                  | Any valid Workspace ID. Default is the current Workspace context you are working in.                                                   |

</TabItem>

<TabItem value="software">

Manage Astronomer Software [Teams](https://docs.astronomer.io/software/import-idp-groups).

#### Usage

If you want to add a team to the current Workspace with the default role of Workspace Member, you can run `astro workspace team add <team-id>`, with the team ID that you want to add.

```sh
astro workspace team add <team-id>
```

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run `astro organization team list` and copy the value in the ID column

#### Options

| Option                   | Description                       | Possible Values                                                                                                                        |
| ------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `<team-id>` (_Required_) | The Team's ID                     | Any valid Team ID                                                                                                                      |
| `--role`                 | The Team's role in the Workspace. | Possible values are `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. Default is `WORKSPACE_MEMBER`. |

</TabItem>
</Tabs>

## Related commands

- [`astro workspace team remove`](cli/astro-workspace-team-remove.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
