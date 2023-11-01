---
sidebar_label: "astro workspace service-account"
title: "astro workspace service-account"
id: astro-workspace-service-account
description: Manage Workspace service accounts (Software only)
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

## Usage

This command has several subcommands.

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
| `role`                      | The User Role for the service account.                          | Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, `WORKSPACE_ADMIN`. The default value is `WORKSPACE_VIEWER`. |

#### Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Configure CI/CD on Astronomer Software](https://docs.astronomer.io/software/ci-cd)

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
- [Configure CI/CD on Astronomer Software](https://docs.astronomer.io/software/ci-cd)

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
- [Configure CI/CD on Astronomer Software](https://docs.astronomer.io/software/ci-cd)