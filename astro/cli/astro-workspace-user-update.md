---
sidebar_label: "astro workspace user update"
title: "astro workspace user update"
id: astro-workspace-user-update
description: Reference documentation for astro workspace user update.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Update the role of an existing user in your current Workspace. The CLI prompts you for the user's email.

## Usage

```sh
astro workspace user update --role <user-role>
```

## Options

| Option                | Description                                          | Valid Values                                                                     |
| --------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `<email>`             | The email address of the user whose role you want to update. | Any valid email                                                                  |
| `--role` (_Required_) | The user's role in the Workspace.                    | Valid values are `WORKSPACE_VIEWER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Related commands

- [`astro workspace user add`](cli/astro-workspace-user-add.md)
- [`astro organization user update`](cli/astro-organization-user-update.md)

</TabItem>
<TabItem value="software">

Update a user's permissions in your current Astronomer Workspace.

## Usage

```sh
astro workspace user update --email <user-email-address>
```

## Options

| Option                 | Description                           | Possible Values                                                                                                       |
| ---------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `--email` (_Required_) | The user's email.                     | Any valid email address                                                                                               |
| `--role`               | The role you're updating the user to. | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. Default value is `WORKSPACE_VIEWER` |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

</TabItem>
</Tabs>
