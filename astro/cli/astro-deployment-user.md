---
sidebar_label: "astro deployment user"
title: "astro deployment user"
id: astro-deployment-user
description: Manage Deployment users.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.

:::

Manage Deployment-level users.

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>

<TabItem value="astro">

## Usage

This command has several subcommands. Read the following sections to learn how to use each subcommand.

### astro deployment user add

Give an existing user in a Workspace access to a Deployment within that Workspace. You must be a Deployment Admin for the given Deployment to run this command.

#### Usage

```sh
astro deployment user add --email=<user-email-address> --deployment-id=<user-deployment-id> --workspace-id=<user-workspace-id> --role=<user-role>
```

#### Options

| Option                         | Description                                         | Possible values                                                                                                               |
| ------------------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `--deployment-id` (_Required_) | The ID for the Deployment that the user is added to | Any valid Deployment ID                                                                                                       |
| `-e`,`--email` (_Required_)    | The user's email                                    | Any valid email address                                                                                                       |
| `--role` (_Required_)          | The role assigned to the user                       | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `--workspace-id`               | The workspace assigned to the Deployment            | Any valid Workspace ID                                                                                                        |

### astro deployment user list

View a list of all Workspace users who have access to a given Deployment.

#### Usage

```sh
astro deployment user list --deployment-id=<deployment-id>
```

#### Options

| Option                       | Description                                 | Possible values         |
| ---------------------------- | ------------------------------------------- | ----------------------- |
| `--deployment-id` (Required) | The Deployment whose users you want to view | Any valid Deployment ID |
| `--workspace-id`             | The Workspace whose users you want to view  | Any valid Workspace ID  |

### astro deployment user remove

Remove access to a Deployment for an existing Workspace user, the command line prompts you for the user email address or user ID for the user you want to remove. To grant that same user a different set of permissions instead, modify their existing Deployment-level role by running `astro deployment user update`. You must be a Deployment Admin to run this command.

#### Usage

```sh
astro deployment user remove --deployment-id=<deployment-id> --email=<user-email-address> --workspace-id=<workspace-id>
```

#### Options

| Option                       | Description                                  | Possible values         |
| ---------------------------- | -------------------------------------------- | ----------------------- |
| `--deployment-id` (Required) | The Deployment from which to remove the user | Any valid Deployment ID |
| `-e`,`--email` (_Required_)  | The user's email                             | Any valid email address |
| `--workspace-id`             | The Workspace from which to remove the user  | Any valid Workspace ID  |

### astro deployment user update

Update a user's role in a given Deployment.

#### Usage

```sh
astro deployment user update --email=<email=address> --deployment-id=<deployment-id> --role=
```

#### Options

| Option                       | Description                          | Possible values          |
| ---------------------------- | ------------------------------------ | ------------------------ |
| `--deployment-id` (Required) | The Deployment that you're searching | Any valid Deployment ID. |
| `-e`,`--email` (_Required_)  | The user's email                     | Any valid email address  |
| `--role` | The role for the user. | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default value is `DEPLOYMENT_ADMIN`. |

#### Related documentation

- [Manage User Permissions on Astronomer](https://www.astronomer.io/docs/software/workspace-permissions)

</TabItem>
<TabItem value="software">

## Usage

This command has several subcommands. Read the following sections to learn how to use each subcommand.

### astro deployment user add

Give an existing user in a Workspace access to a Deployment within that Workspace. You must be a Deployment Admin for the given Deployment to run this command.

#### Usage

```sh
astro deployment user add --email=<user-email-address> --deployment-id=<user-deployment-id> --role<user-role>
```

#### Options

| Option                         | Description                                         | Possible values                                                                                                               |
| ------------------------------ | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `--deployment-id` (_Required_) | The ID for the Deployment that the user is added to | Any valid Deployment ID                                                                                                       |
| `-e`,`--email` (_Required_)    | The user's email                                    | Any valid email address                                                                                                       |
| `--role` (_Required_)          | The role assigned to the user                       | 1DEPLOYMENT_ADMIN1 or the custom role name. Default is `DEPLOYMENT_ADMIN`. |

#### Related documentation

- [Manage User Permissions on Astronomer](https://www.astronomer.io/docs/software/workspace-permissions)

### astro deployment user remove

Remove access to a Deployment for an existing Workspace user. To grant that same user a different set of permissions instead, modify their existing Deployment-level role by running `astro deployment user update`. You must be a Deployment Admin to run this command.

#### Usage

```sh
astro deployment user remove --deployment-id=<deployment-id> --email=<user-email-address>
```

#### Options

| Option                       | Description                                  | Possible values         |
| ---------------------------- | -------------------------------------------- | ----------------------- |
| `--email` (Required)         | The user's email                             | Any valid email address |
| `--deployment-id` (Required) | The Deployment from which to remove the user | Any valid Deployment ID |

#### Related documentation

- [Manage User Permissions on Astronomer](https://www.astronomer.io/docs/software/workspace-permissions)

### astro deployment user list

View a list of all Workspace users who have access to a given Deployment.

#### Usage

```sh
astro deployment user list --deployment-id=<deployment-id>
```

#### Options

| Option                       | Description                                 | Possible values         |
| ---------------------------- | ------------------------------------------- | ----------------------- |
| `--deployment-id` (Required) | The Deployment that you're searching in     | Any valid Deployment ID |
| `--email`                    | The email for the user you're searching for | Any valid email address |
| `--name`                     | The name of the user to search for          | Any string              |

#### Related documentation

- [Manage User Permissions on Astronomer](https://www.astronomer.io/docs/software/workspace-permissions)

### astro deployment user update

Update a user's role in a given Deployment.

#### Usage

```sh
astro deployment user update --deployment-id=<deployment-id>
```

#### Options

| Option                       | Description                          | Possible values                                                                                                                |
| ---------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `--deployment-id` (Required) | The Deployment that you're searching | Any valid Deployment ID.                                                                                                       |
| `--role`                     | The role for the user.               | Possible values are `DEPLOYMENT_VIEWER`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_ADMIN`. The default value is `DEPLOYMENT_VIEWER`. |

#### Related documentation

- [Manage User Permissions on Astronomer](https://www.astronomer.io/docs/software/workspace-permissions)

</TabItem>
</Tabs>
