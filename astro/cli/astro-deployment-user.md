---
sidebar_label: "astro deployment user"
title: "astro deployment user"
id: astro-deployment-user
description: Manage Deployment users (Software only)
hide_table_of_contents: true
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Manage users in a Deployment on Astronomer Software. 

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
| `--role` (_Required_)          | The role assigned to the user                       | Possible values are `DEPLOYMENT_VIEWER`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_ADMIN`. The default value is `DEPLOYMENT_VIEWER` |

#### Related documentation

- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

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

- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

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

- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)
- 
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

- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)