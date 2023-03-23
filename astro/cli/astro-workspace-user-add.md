---
sidebar_label: "astro workspace user add"
title: "astro workspace user add"
id: astro-workspace-user-add
description: Reference documentation for astro workspace.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on which Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Add an existing Organization user to your current Astronomer Workspace. You must be a Workspace Admin to perform this action.

You can use this command to invite multiple users to a Workspace at a time. See [Add a group of users to Astro using the Astro CLI](add-user.md#add-a-group-of-users-to-astro-using-the-astro-cli)

## Usage

```sh
astro workspace user add <email> 
```

## Options

| Option    | Description                                          | Valid Values                                                                               |
| --------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `<email-address>` | The email address of the user that you want to add to the Workspace. | Any valid email address                                                                            |
| `--role`  | The user's role in the Workspace.                    | Possible values are either `WORKSPACE_VIEWER`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER`. |

## Related commands

- [`astro workspace user update`](cli/astro-workspace-user-update.md)
- [`astro organization user invite`](cli/astro-organization-user-invite.md)
- [`astro organization user update`](cli/astro-organization-user-update.md)

</TabItem>
<TabItem value="software">

Creates a new user in your current Workspace. If the user has already authenticated to Astronomer, they will automatically be granted access to the Workspace. If the user does not have an account on Astronomer, they will receive an email invitation to the platform.

## Usage

```sh
astro workspace user add --email <user-email-address> 
```

## Options

| Option                 | Description                                                                                                                                           | Possible Values                                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `--email` (_Required_) | The user's email                                                                                                                                      | Any valid email address                                                                                                 |
| `--workspace-id`       | The Workspace that the user is added to. Specify this flag if you want to create a user in a Workspace that is different than your current Workspace. | Any valid Workspace ID                                                                                                  |
| `--role`               | The role assigned to the user.                                                                                                                        | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, and `WORKSPACE_ADMIN`. Default value is `WORKSPACE_VIEWER`. |

## Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

</TabItem>
</Tabs>