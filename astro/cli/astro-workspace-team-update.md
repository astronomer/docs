---
sidebar_label: "astro workspace team update"
title: "astro workspace team update"
id: astro-workspace-team-update
description: Update a Team in a Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info
The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.
:::

Update a Team's permissions in a given Workspace.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

```sh
astro workspace team update <team-id> --workspace-id <workspace-id> --role=<system-role>
```

To find a Team ID using the Astro CLI, run `astro workspace team list`.

To find a Team ID in the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings** > **Access Management** > **Teams**. Search for your Team in the **Teams** table and copy its **ID**. The ID should look something like `clk17xqgm124q01hkrgilsr49`.

#### Options

| Option           | Description                                              | Possible Values                                                                                          |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `--workspace-id` | The Workspace for the Team. Use to override CLI prompts. | Any valid Workspace ID.                                                                                  |
| `<team-id>`      | The ID for the Team. Use to override CLI prompts.        | Any valid Team ID. To retrieve a Team ID, run `astro workspace team list`.                               |
| `--role`         | The Team's role in the Workspace.                        | Possible values are `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, and `WORKSPACE_OWNER`. |

</TabItem>
<TabItem value="software">

## Usage

```sh
astro workspace team update <team-id> --workspace-id <workspace-id> --role=<system-role>
```

To find a Team ID using the Astro CLI, run `astro workspace team list`. You can also access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.

#### Related documentation

- [Import identity provider groups into Astronomer Software](https://docs.astronomer.io/software/import-idp-groups).

#### Options

| Option                        | Description                       | Possible Values                                                                                                  |
| ----------------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` (_Required_) | The Workspace for the Team        | Any valid Workspace ID.                                                                                          |
| `<team-id>` (_Required_)      | The Team's ID.                    | Any valid Team ID.                                                                                               |
| `--role`                      | The Team's role in the Workspace. | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. Default is `WORKSPACE_VIEWER`. |

</TabItem>
</Tabs>

## Related commands

- [`astro workspace team remove`](cli/astro-workspace-team-remove.md)
- [`astro organization team create`](cli/astro-organization-team-create.md)
- [`astro workspace switch`](cli/astro-workspace-switch.md)
