---
sidebar_label: "astro workspace"
title: "astro workspace"
id: astro-workspace
description: Reference documentation for astro workspace.
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


Manage Workspaces on Astro.

## Usage

This command includes two subcommands:

```sh
# List all workspaces
astro workspace list 

# Switch between workspaces
astro workspace switch
```

</TabItem>
<TabItem value="software">


Manage Workspaces on Astronomer Software.

## Usage

This command has several subcommands. Read the following sections to learn how to use each subcommand.

### astro workspace create

Creates a new Workspace.

#### Usage

```sh
astro workspace create --label=<new-workspace-name>
```

#### Options

| Option                 | Description | Possible Values                        |
| ---------------------- | ----------- | -------------------------------------- |
| `--label` (_required_) |   The label or name for the new Workspace.  | Any string |
| `--description`        | The description for the new Workspace. | Any string |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)

### astro workspace delete

Deletes a Workspace.

#### Usage

Run `astro workspace delete <your-workspace-id>` to delete a Workspace. Your Workspace ID can be found by running `astro workspace list`. You must have Workspace Admin permissions to a Workspace in order to delete it.

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)

### astro workspace list

Generates a list of all Workspaces that you have access to.

#### Usage

Run `astro workspace list` to see the name and Workspace ID for each Workspace to which you have access.

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)

### astro workspace service-account create

Creates a service account for a given Workspace.

#### Usage

```sh
astro workspace service-account create --workspace-id=<your-workspace> --label=<your-label>
```

#### Options

| Option                      | Description                                                     | Possible Values                                                                                                            |
| --------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` (Required) | The Workspace you're creating a service account for.            | Any valid Workspace ID                                                                                                     |
| `--label` (Required)        | A label for the service account.                                | Any string                                                                                                                 |
| `--category`                | The Category for the service account. The default is `Not set`. | Any string                                                                                                                 |
| `role`                      | The User Role for the service account.                          | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. The default value is `WORKSPACE_VIEWER`. |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Deploy to Astronomer via CI/CD](https://docs.astronomer.io/software/ci-cd)

### astro workspace service-account delete

Deletes a service account for a given Workspace.

#### Usage

```sh
astro workspace service-account delete <your-service-account-id>
```

#### Options

| Option           | Description                                                                                                                                                                                                                               | Possible Values        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `--workspace-id` | The Workspace in which you want to delete a service account. If this flag is used instead of specifying `<your-service-account-id>`, you'll be prompted to select a service account from a list of all service accounts on the Workspace. | Any valid Workspace ID |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Deploy to Astronomer via CI/CD](ci-cd.md)

### astro workspace service-account get

Shows the name, ID, and API key for each service account on a given Workspace.

#### Usage

Run `astro deployment service-account get <service-account-id> --workspace-id=<your-workspace-id>` to get information on a single service account within a Workspace. To see a list of all service accounts on a Workspace, run `astro deployment service-account get --workspace-id=<your-workspace-id>`.

#### Options

| Option           | Description                                                                                                                       | Possible Values        |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `--workspace-id` | The Workspace you're getting the service account from. Use this flag as an alternative to specifying `<your-service-account-id>`. | Any valid Workspace ID |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Deploy to Astronomer via CI/CD](ci-cd.md)

### astro workspace switch

Switches the Workspace in which you're working.

#### Usage

```sh
astro workspace switch <workspace-id>
```

| Option         | Description                                                                                      | Possible Values |
| -------------- | ------------------------------------------------------------------------------------------------ | --------------- |
| `--paginated ` | Paginate the list of Workspaces. If `--page-size` is not specified, the default page size is 20. | None            |
| `--page-size`  | The page size for paginated lists.                                                               | Any integer     |

### astro workspace team add

Add a Team to a Workspace.

#### Usage

`astro workspace team add --workspace-id=<workspace_id> --team-id=<team-id> --role=<workspace_level_role>`

You can retrieve a Team's ID in one of two ways:

- Access the Team in the Software UI and copy the last part of the URL in your web browser. For example, if your Team is located at `BASEDOMAIN.astronomer.io/w/cx897fds98csdcsdafasdot8g7/team/cl4iqjamcnmfgigl4852flfgulye`, your Team ID would be `cl4iqjamcnmfgigl4852flfgulye`.
- Run [`astro workspace team list`](#astro-workspace-team-list) and copy the value in the `ID` column.

#### Options

| Option                        | Description                       | Possible Values                                                                   |
| ----------------------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| `--workspace-id` (_Required_) | The Workspace for the Team        | Any valid Workspace ID                                                            |
| `--team-id` (_Required_)      | The Team's ID                     | Any valid team ID                                                                 |
| `--role`                      | The Team's role in the Workspace. | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. |

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

### astro workspace update

Updates some of the basic information for your current Workspace.

#### Usage

```sh
astro workspace update 
```

At least one flag must be specified.

#### Options

| Option          | Description                     | Possible Values |
| --------------- | ------------------------------- | --------------- |
| `--label`       | The ID for the Workspace        | Any string      |
| `--description` | A description for the Workspace | Any string      |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)

### astro workspace user add

Creates a new user in your current Workspace. If the user has already authenticated to Astronomer, they will automatically be granted access to the Workspace. If the user does not have an account on Astronomer, they will receive an invitation to the platform via email.

#### Usage

```sh
astro workspace user add --email <user-email-address> 
```

#### Options

| Option                 | Description                                                                                                                                           | Possible Values                                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `--email` (_Required_) | The user's email                                                                                                                                      | Any valid email address                                                                                                 |
| `--workspace-id`       | The Workspace that the user is added to. Specify this flag if you want to create a user in a Workspace that is different than your current Workspace. | Any valid Workspace ID                                                                                                  |
| `--role`               | The role assigned to the user.                                                                                                                        | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, and `WORKSPACE_ADMIN`. Default value is `WORKSPACE_VIEWER`. |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

### astro workspace user remove

Removes an existing user from your current Workspace.

#### Usage

```sh
astro workspace user remove --email <user-email-address>
```

#### Options

| Option                 | Description       | Possible Values         |
| ---------------------- | ----------------- | ----------------------- |
| `--email` (_Required_) | The user's email. | Any valid email address |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

### astro workspace user list

Outputs a list of all users with access to your current Workspace.

#### Usage

```sh
astro workspace user list
```

#### Options

| Option           | Description                                                                                                                                             | Possible Values        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `--workspace-id` | The Workspace that you're searching in. Specify this flag if you want to search for users in a Workspace that is different than your current Workspace. | Any valid Workspace ID |
| `--email`        | The email for the user you're searching for.                                                                                                            | Any string             |
| `--name`         | The name of the user to search for.                                                                                                                     | Any string             |
| `--paginated `   | Paginate the list of users. If `--page-size` is not specified, the default page size is 20.                                                             | None                   |
| `--page-size`    | The page size for paginated lists.                                                                                                                      | Any integer            |


#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

### astro workspace user update

Updates a user's role in your current Workspace.

#### Usage

```sh
astro workspace user update --email <user-email-address>
```

#### Options

| Option    | Description                           | Possible Values                                                                                                       |
| --------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `--email` | The user's email.                     | Any valid email address                                                                                               |
| `--role`  | The role you're updating the user to. | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. Default value is `WORKSPACE_VIEWER` |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

</TabItem>
</Tabs>