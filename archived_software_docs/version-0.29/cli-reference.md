---
sidebar_label: 'CLI reference guide'
title: 'Astro CLI reference guide'
id: cli-reference
description: A list of every command and setting in the Astro CLI.
---

The Astronomer [open source CLI](https://github.com/astronomer/astro-cli) is the easiest way to run Apache Airflow® on your local machine. From the CLI, you can create a local Apache Airflow instance with a dedicated Webserver, Scheduler and Postgres Database. If you're an Astronomer customer, you can use the Astro CLI to create and manage users, Workspaces, Airflow Deployments, service accounts, and more.

This document contains information about all commands and settings available in the Astro CLI, including examples and flags. It does not contain detailed guidelines on each command, but each section provides resources for additional information in a **Related documentation** section if it's available.

## Installation

To install the CLI, see [Install the CLI](install-cli.md)

### Prerequisites

The Astro CLI installation process requires [Docker](https://www.docker.com/) (v18.09 or higher).

### Install with Homebrew

If you have Homebrew installed, run:

```sh
brew install astro
```

### Install with cURL

To install the latest version of the Astro CLI, run:

```
curl -sSL https://install.astronomer.io | sudo bash
```

#### Note for MacOS Catalina Users:

As of macOS Catalina, Apple [replaced bash with ZSH](https://www.theverge.com/2019/6/4/18651872/apple-macos-catalina-zsh-bash-shell-replacement-features) as the default shell. Our CLI install cURL command currently presents an incompatibility error with ZSH, sudo and the pipe syntax.

If you're running macOS Catalina and beyond, do the following:

1. Run `sudo -K` to reset/un-authenticate
2. Run the following to install the CLI properly:

```
curl -sSL https://install.astronomer.io | sudo bash -s < /dev/null
```

### Confirm the install

To make sure that you have the Astro CLI installed on your machine, run:

```bash
astro version
```

If the installation was successful, you should see the version of the CLI that you installed in the output:

```
Astro CLI Version: 1.2.0
Git Commit: c4fdeda96501ac9b1f3526c97a1c5c9b3f890d71
```

For a breakdown of subcommands and corresponding descriptions, you can always run `astro` or `astro --help`.

```
astro is a command line interface for working with the Astronomer Platform.

Usage:
  astro [command]

Available Commands:
  auth            Manage astronomer identity
  cluster         Manage Astronomer EE clusters
  completion      Generate autocompletions script for the specified shell (bash or zsh)
  config          Manage astro project configurations
  deploy          Deploy an airflow project
  deployment      Manage airflow deployments
  dev             Manage airflow projects
  help            Help about any command
  upgrade         Check for newer version of Astro CLI
  user            Manage astronomer user
  version         Astro CLI version
  workspace       Manage Astronomer workspaces

Flags:
  -h, --help   help for astro

Use "astro [command] --help" for more information about a command.
```

Once you've successfully installed the CLI, use the remainder of this guide to learn more about the CLI's available commands.

## astro completion

Generates autocompletion scripts for Astronomer.

### Usage

Use `astro completion <subcommand>` to generate autocompletion scripts, which can be used to automate workflows on Astronomer that require multiple CLI commands.

> **Note:** If you're running on MacOS, make sure to install [Bash Completion](https://github.com/scop/bash-completion) before creating autocompletion scripts. To do so via Homebrew, run:

    ```sh
    brew install bash-completion
    ```

### Subcommands

| Subcommand | Usage                                                                                                                                                      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash`     | Run `astro completion bash` to show the bash shell script for autocompletion in Astronomer. Use this output to modify or view your autocompletion scripts. |
| `zsh`      | Run `astro completion zsh` to show the zsh shell script for autocompletion in Astronomer. Use this output to modify or view your autocompletion scripts.   |

## astro config

Modifies certain platform-level settings on Astronomer Software without needing to manually adjust them in your `config.yaml` file.

### Usage

Run `astro config get <setting-name>` to list the value for a particular setting in your `config.yaml` file. To update or override a value, run `astro config set <setting-name> <value>`.

The settings that you can update via the command line are:

- `cloud.api.protocol`
- `cloud.api.port`
- `cloud.api.ws_protocol`
- `cloud.api.token`
- `container.engine`
- `context`
- `contexts`
- `houston.dial_timeout`
- `local.houston`
- `local.orbit`
- `postgres.user`
- `postgres.password`
- `postgres.host`
- `postgres.port`
- `project.deployment`
- `project.name`
- `project.workspace`
- `webserver.port`
- `show_warnings`

### Subcommands

| Subcommand | Usage                                                     |
| ---------- | --------------------------------------------------------- |
| `get`      | Show current values for the above configuration settings. |
| `set`      | Updates a setting in your platform to a new value.        |

### Related documentation

- [Apply a config change](apply-platform-config.md)

## astro context delete

Delete the locally stored information for a given Astronomer installation. After running this command, the domain for the installation that you specify no longer appears when you run `astro context list`, and you can't use the `astro context switch` command to move to the installation.

If you use this command to reauthenticate to an installation that you previously deleted, installation information is available when you use the `astro context list` and `astro context switch` commands.

### Usage

```sh
astro context delete <basedomain>
```

## astro context list

View a list of domains for all Astronomer installations that you have access to. Astronomer installations appear on this list if you have authenticated to it at least once using `astro login`.

### Usage

```sh
astro context list
```

## astro context switch

Switch to a different Astronomer installation. You can switch to a given Astronomer installation if you have authenticated to it at least once using `astro login`.

After you switch to a different Astronomer installation, you might need to run `astro login` to reauthenticate to the installation.

### Usage

```sh
astro context switch <basedomain>
```

## astro deploy

Deploys code in your Airflow project directory to any Airflow Deployment on Astronomer.

### Usage

Run `astro deploy <your-deployment-release-name> [flags]` in your terminal to push a local Apache Airflow® project as a Docker image to your Airflow Deployment on Astronomer.

If you have the appropriate Workspace and Deployment-level permissions, your code is packaged into a Docker image, pushed to Astronomer's Docker Registry, and applied to your Airflow webserver, scheduler(s), and worker(s).

To identify your Deployment's release name, go to **Settings** > **Basics** > **Release Name** in the Software UI or run `astro deployment list`.

If you run `astro deploy` without specifying `your-deployment-release-name`, the Astro CLI lists all Airflow Deployments in your Workspace.

### Options

| Option             | Value Type | Usage                                                                               |
| ---------------- | ---------- | ----------------------------------------------------------------------------------- |
| `--force`        | None       | Forces deploy even if there are uncommitted changes.                                |
| `--prompt`       | None       | Forces prompt for choosing a target Deployment.                                     |
| `--pytest`       | None       | Deploy code to Astro only if the specified Pytests are passed.                      |
| `--save`         | None       | Saves this directory/Deployment combination for future deploys.                     |
| `--test`         | None       | A valid filepath within your Astro project to an alternative pytest file or directory. |
| `--workspace-id` | String     | Lists available Deployments in your Workspace and prompts you to pick one.          |
| `--no-cache`     | None       | Do not use any images from the container engine's cache when building your project. |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine                                      | A valid name for a pre-built Docker image based on Astro Runtime |

### Related documentation

- [Deploy to Astronomer via the CLI](deploy-cli.md)

## astro deployment

Manages various Deployment-level actions on Astronomer.

### Usage

Run `astro deployment <subcommand>` in your terminal to create, delete, or manage an Airflow Deployment on Astronomer. See the following entries of this guide for more information on each subcommand.

When managing an existing Deployment using subcommands such as `delete` and `logs`, you additionally need to specify a Deployment in your command. In this case, you would run `astro deployment <subcommand> --deployment-id=<deployment-id>`.

### Related documentation

- [Configure an Apache Airflow® Deployment on Astronomer](manage-workspaces.md)

## astro deployment airflow upgrade

Initializes the Airflow version upgrade process on any Airflow Deployment on Astronomer.

### Usage

Run `astro deployment airflow upgrade --deployment-id` to initialize the Airflow upgrade process. To finalize the Airflow upgrade process, complete all of the steps as described in [Upgrade Apache Airflow® on Astronomer](manage-airflow-versions.md).

If you do not specify `--desired-airflow-version`, this command creates a list of available Airflow versions that you can select. The Astro CLI lists only the available Airflow versions that are later than the version currently specified in your `Dockerfile`.


### Options

| Option                        | Value Type | Usage                                                                                                                    |
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `--deployment-id`           | String     | The ID of the Deployment for which you want to upgrade Airflow. To find your Deployment ID, run `astro deployment list`. |
| `--desired-airflow-version` | String     | The Airflow version you're upgrading to (for example, `2.2.0`).                                                                |


### Related documentation

- [Upgrade Apache Airflow® on Astronomer](manage-airflow-versions.md)
- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro deployment create

Creates a new Airflow Deployment in your current Astronomer Workspace.

### Usage

Run `astro deployment create <new-deployment-name> [flags]` to create a new Deployment in your Astronomer Workspace. This is equivalent to using the **New Deployment** button in the Software UI.

### Options

| Option                    | Value Type | Usage                                                                                                                                                                                                         |
| ----------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--airflow-version`     | String     | The Astronomer Certified version for the new Deployment.                                                                                                                                                                   |
| `--runtime-version`     | String     | The Astro Runtime version for the new Deployment.                                                                                                                                                                   |
| `--cloud-role`          | String     | Append an AWS or GCP IAM role to your Airflow Deployment's webserver, scheduler, and worker Pods.                                                                                                             |
| `--executor`            | String     | The executor type for the Deployment. Can be `local`, `celery`, or `kubernetes`. If no executor is specified, then `celery` is used.                                                                          |
| `--release-name`        | String     | A custom release name for the Airflow Deployment. Applies only to Deployments on Astronomer Software.                                                                                                         |
| `--dag-deployment-type` | String     | The DAG deploy method for the Deployment. Can be either `image` or `volume`. The default is `image`.                                                                                                    |
| `--nfs-location`        | String     | The location for an NFS volume mount, specified as: `<IP>:/<path>`. Must be specified when `--dag-deployment-type=volume`. Input is automatically prepended with `nfs:/` - do not include this in your input. |
| `--triggerer-replicas`  | Integer    | The number of replica triggerers to provision for the Deployment.                                                                                                                                             |

### Related documentation

- [Configure an Apache Airflow® Deployment on Astronomer](manage-workspaces.md)
- [Integrate IAM roles](integrate-iam.md)

## astro deployment delete

Deletes an Airflow Deployment from an Astronomer Workspace. This is equivalent to the **Delete Deployment** action in the Software UI.

### Usage

`astro deployment delete <your-deployment-id>`

## astro deployment list

Generates a list of Airflow Deployments in your current Astronomer Workspace.

### Usage

`astro deployment list [flags]`

### Options

| Option    | Value Type | Usage                                                                                          |
| ------- | ---------- | ---------------------------------------------------------------------------------------------- |
| `--all` | None       | Generates a list of running Airflow Deployments across all Workspaces that you have access to. |

## astro deployment logs

Returns logs from your Airflow Deployment's scheduler, webserver, triggerer, and Celery workers.

### Usage

You can run any of the following commands depending on which logs you want to stream:

- `astro deployment logs scheduler [flags]`
- `astro deployment logs webserver [flags]`
- `astro deployment logs workers [flags]`
- `astro deployment logs triggerer [flags]`

### Options

| Option       | Value Type                                    | Usage                                                               |
| ---------- | --------------------------------------------- | ------------------------------------------------------------------- |
| `--follow` | None                                          | Subscribes to watch more logs.                                      |
| `--search` | String                                        | Searches for the specified string within the logs you're following. |
| `--since`  | Lookback time in `h` or `m` (e.g. `5m`, `2h`) | Limits past logs to those generated in the lookback window.         |

### Related documentation

- [Deployment Logs](deployment-logs.md)

## astro deployment runtime migrate

Migrate an existing existing Software Deployment from Astronomer Certified to Astro Runtime.

### Usage

Run `astro deployment runtime migrate --deployment-id=<your-deployment-id>` to initialize the migration process.

### Options

| Option                        | Value Type | Usage                                                                                                                    |
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `--deployment-id`           | String     | The ID of the Deployment that you want to migrate. To find your Deployment ID, run `astro deployment list`. |
| `--desired-runtime-version` | String     | The Runtime version you're migrating to (for example, `5.0.0`).                                                                |

## astro deployment runtime upgrade

Initializes the Runtime version upgrade process on any Software Deployment.

### Usage

Run `astro deployment airflow upgrade --deployment-id=<your-deployment-id>` to initialize the upgrade process. To finalize the upgrade process, complete all of the steps as described in [Upgrade Apache Airflow® on Astronomer](manage-airflow-versions.md).

If you do not specify `--desired-runtime-version`, this command creates a list of available Runtime versions that you can select. The Astro CLI lists only the available Runtime versions that are later than the version currently specified in your `Dockerfile`.


### Options

| Option                        | Value Type | Usage                                                                                                                    |
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `--deployment-id`           | String     | The ID of the Deployment for which you want to upgrade Airflow. To find your Deployment ID, run `astro deployment list`. |
| `--desired-runtime-version` | String     | The Runtime version you're upgrading to (for example, `5.0.0`).                                                                |

## astro deployment service-account create

Creates a Deployment-level service account on Astronomer, which you can use to configure a CI/CD pipeline or otherwise interact with the Astronomer Houston API.

### Usage

`astro deployment service-account create --deployment-id=<your-deployment-id> --label=<your-service-account-label> [flags]`

### Options

| Option                         | Value Type | Usage                                                                                                                           |
| ---------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `--category`                 | String     | The category for the new service account as displayed in the Software UI. This is optional, and the default value is `Not set`. |
| `--deployment-id` (Required) | String     | The Deployment you're creating a service account for.                                                                           |
| `--label` (Required)         | String     | The name or label for the new service account.                                                                                  |
| `--role`                     | String     | The User Role for the new service account. Select `viewer`, `editor`, or `admin`. The default is `viewer`.                |


### Related documentation

- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro deployment service-account delete

Deletes a service account for a given Deployment.

### Usage

`astro deployment service-account delete <your-service-account-id> [flags]`

### Options

| Option                        | Value Type | Usage                                                                                                                                                                                         |
| --------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--deployment-id`(Required) | String     | The Airflow Deployment in which the service account is configured. Use this flag as an alternative to specifying `<your-service-account-id>`. To get this value, run `astro deployment list`. |

### Related documentation

- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro deployment service-account list

Shows the name, ID, and API key for each service account in a specific Deployment.

### Usage

Run `astro deployment service-account list <service-account-id> --deployment-id=<your-deployment-id>` to get information on a single deployment-level service account. To see a list of all service accounts on a Deployment, run `astro deployment service-account list --deployment-id=<your-deployment-id>`.

### Options

| Option                         | Value Type | Usage                        |
| ---------------------------- | ---------- | ---------------------------- |
| `--deployment-id` (Required) | String     | `--deployment-id` (Required) | String | The Deployment ID of the Deployment in which your service account is configured. |

### Related documentation

- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro deployment update

Updates various parts of an Airflow Deployment on Astronomer, including metadata, deployment methods, and executor type. Can also be used to append IAM roles to the webserver, scheduler, and worker pods for Deployments running on Amazon EKS or Google GCP.

### Usage

Run `astro deployment update <your-deployment-id> [flags]` to update a Deployment. The Deployment ID can be found by running `astro deployment list`.

> **Note:** Only the `--cloud-role` flag is specified with a `--`. Additional flags should be written without a leading `--`.

### Options

| Option           | Value Type | Usage                                                                                   |
| -------------- | ---------- | --------------------------------------------------------------------------------------- |
| `--cloud-role` | String     | The ARN for the IAM role.                                                               |
| `--dag-deployment-type` | String     | The DAG deploy method for the Deployment. Can be either `image` or `volume`. The default value is `image`.                                                               |
| `--nfs-location` | String     | The location for an NFS volume mount, specified as: `<IP>:/<path>`. Must be specified when `--dag-deployment-type=volume`. Input is automatically prepended with `nfs:/` - do not include this in your input.                                  |
| `label`        | String     | The label for the Deployment.                                                           |
| `description`  | String     | The description for a Deployment.                                                       |
| `version`      | String     | The Airflow version for the Deployment (e.g. `v2.0.0`).                                 |
| `releaseName`  | String     | The release name for the Deployment (e.g. `planetary-fusion-1382`).                     |
| `alert_emails` | String     | An email address which receives Airflow alerts from the Deployment.                     |
| `type`         | String     | The type of Deployment. Can be either `airflow` or `flower`.                            |
| `executor`     | String     | The executor type for the Deployment. Can be either `local`, `kubernetes`, or `celery`. |

### Related documentation

- [Integrate IAM roles](integrate-iam.md)
- []

## astro deployment user add

Gives an existing user in a Workspace access to an Airflow Deployment within that Workspace. You must be a Deployment Admin for the given Deployment to complete this action.

### Usage

`astro deployment user add --email=<user-email-address> --deployment-id=<user-deployment-id> --role<user-role>`

### Options

| Option                         | Value Type | Usage                                                                                                                                            |
| ---------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--deployment-id` (Required) | String     | The ID for the Deployment that the user is added to. To find this value, run `astro deployment list`.                                        |
| `--email` (Required)         | String     | The user's email.                                                                                                                          |
| `--role` (Required)          | String     | The role assigned to the user. Can be `DEPLOYMENT_VIEWER`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_ADMIN`. The default value is `DEPLOYMENT_VIEWER`. |

### Related documentation

- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro deployment user remove

Removes access to an Airflow Deployment for an existing Workspace user. To grant that same user a different set of permissions instead, modify their existing Deployment-level role by running `astro deployment user update`. You must be a Deployment Admin to perform this action.

### Usage

`astro deployment user remove --deployment-id=<deployment-id> --email=<user-email-address>`

### Options

| Option                         | Value Type | Usage                                              |
| ---------------------------- | ---------- | -------------------------------------------------- |
| `--email` (Required)         | String     | The user's email.                            |
| `--deployment-id` (Required) | String     | The Deployment that the user will be removed from. |

### Related documentation

- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro deployment user list

Outputs a list of all Workspace users who have access to a given Deployment. Use the optional flags to list specific users based on their name, email, or ID.

### Usage

`astro deployment user list --deployment-id=<deployment-id> [flags]`

### Options

| Option                         | Value Type | Usage                                        |
| ---------------------------- | ---------- | -------------------------------------------- |
| `--deployment-id` (Required) | String     | The Deployment that you're searching in.     |
| `--email`                    | String     | The email for the user you're searching for. |
| `--name`                     | String     | The name of the user to search for.          |

### Related documentation

- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro deployment user update

Updates a user's role in a given Deployment.

### Usage

`astro deployment user update --deployment-id=<deployment-id> [flags]`

### Options

| Option                         | Value Type | Usage                                                                                                                                                                                              |
| ---------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--deployment-id` (Required) | String     | The Deployment that you're searching in.                                                                                                                                                           |
| `--role`                     | String     | The role you're updating the user to. Possible values are `DEPLOYMENT_VIEWER`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_ADMIN`. If `--role` is not specified, `DEPLOYMENT_VIEWER` is the default value. |  |

### Related documentation

- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro dev

This set of commands allow you to create and manage a local Airflow environment on your machine. Access to the Astronomer platform is not required.

### Usage

`astro dev <subcommand> [flags]`

Refer to the following sections for information on each subcommand.

## astro dev init

Initializes a new Astro project in your working directory. The set of files generated by this command are required to run Airflow locally and can be pushed to a Deployment on Astronomer.

:::info

To deploy your project to a Software Deployment, either specify the `--use-astronomer-certified` flag when you run `astro dev init`, or update the image in your project's `Dockerfile` to a supported Astronomer Certified image. For more information, see [Deploy DAGs via Astro CLI](deploy-cli.md).

:::

### Usage

`astro dev init [flags]`

When you run this command, the following skeleton files are generated in your current directory:

```python
.
├── dags # Where your DAGs go
│   └── example-dag.py # An example DAG that comes with the initialized project
├── Dockerfile # For Astronomer's Docker image and runtime overrides
├── include # For any other files you'd like to include
├── plugins # For any custom or community Apache Airflow® plugins
├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
├── packages.txt # For OS-level packages
└── requirements.txt # For any Python packages
```

### Options

| Option                         | Value Type                                                                                                                                                      | Usage                                                                                              |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `--airflow-version`     | String     | The Airflow version for the new Deployment. If you use this flag, do not use `--runtime-version`.                                                                                                                                                                    |
| `--runtime-version`        | String     | The Runtime version for the new Deployment. If you use this flag, do not use `--airflow-version`.                                                                                                         |
| `--use-astronomer-certified` | `` | Create the new project with the latest version of Astronomer Certified. If you don't use this flag, your project is created with the latest version of Astronomer Runtime. |
| `--name`                     | String                                                                                                                                                          | The name for the Airflow project.                                                                  |

## astro dev kill

Forces running containers in your local Airflow environment to stop. Unlike `astro dev stop`, which only pauses running containers, `astro dev kill` will delete all data associated with your local Postgres metadata database, including Airflow connections, logs, and task history.

This command is most often used to restart a cluster when testing new DAGs or settings in a non-production environment. After using `astro dev kill`, you can restart your environment with `astro dev start`.

### Usage

In your project directory, run `astro dev kill` to delete all data associated with your Airflow Deployment's Postgres metadata database.

## astro dev logs

Shows logs for the scheduler or webserver in your local Airflow environment.

### Usage

Run `astro dev logs [flags]` to start tracking logs for your scheduler, webserver, or triggerer in your CLI terminal window.

### Options

| Option          | Value Type | Usage                                              |
| ------------- | ---------- | -------------------------------------------------- |
| `--follow`    | None       | Continues to show the latest outputs from the log. |
| `--scheduler` | None       | Outputs only scheduler logs.                       |
| `--webserver` | None       | Outputs only webserver logs.                       |
| `--triggerer` | None       | Outputs only triggerer logs.                       |

## astro dev parse

Parse the DAGs in a locally hosted Astro project to quickly check them for errors.

### Usage

`astro dev parse`

### Options

| Option          | Value Type | Usage                                              |
| ------------- | ---------- | -------------------------------------------------- |
| `--env`       | string     | The filepath to your environment variables. (The default is `.env`)  |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine                                      | A valid name for a pre-built Docker image based on Astro Runtime |

## astro dev ps

Lists all running Docker containers for your local Airflow environment. This command can only be used in a project directory and works similarly to `docker ps`.

### Usage

`astro dev ps`

## astro dev pytest

Run unit tests for your data pipelines with `pytest`, a testing framework for Python. When you run this command, the Astro CLI creates a local Python environment that includes your DAG code, dependencies, and Astronomer Certified Docker image. The CLI then runs any pytests in the `tests` directory of your Astro project and shows you the results of those tests in your terminal.

### Usage

`astro dev pytest` to run specfic Pytests on your DAGs. Use `astro dev pytest <pytest-filepath>` to specify a specific test.

### Options

| Option          | Value Type | Usage                                              |
| ------------- | ---------- | -------------------------------------------------- |
|`<pytest-filepath>`| String | Any valid filepath within the `tests` directory. |
| `--env`       | string     | The filepath to your environment variables. (The default is `.env`)  |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine                                      | A valid name for a pre-built Docker image based on Astro Runtime |

## astro dev restart

Stop your Airflow environment, rebuild your Astro project into a Docker image, and restart your Airflow environment with the new Docker image.

You can use this command to rebuild an Astro project and run it locally.

### Usage

astro dev restart

### Options

| Option          | Value Type | Usage                                              |
| ------------- | ---------- | -------------------------------------------------- |
| `--env`       | string     | The filepath to your environment variables. The default is `.env`  |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine                                      | A valid name for a pre-built Docker image based on Astro Runtime |

## astro dev run

Runs a single [Apache Airflow® CLI command](https://airflow.apache.org/docs/apache-airflow/stable/cli-ref.html) on your local Airflow environment. This command only applies to local development and is not supported for Airflow Deployments on Astronomer.

### Usage

`astro dev run`

### Related documentation

- [Access to the Apache Airflow® CLI](customize-image.md#access-to-the-airflow-cli)

## astro dev start

Initializes a local Airflow environment on your machine by creating a Docker container for each of Airflow's core components:

- Postgres
- Scheduler
- Webserver
- Triggerer

### Usage

`astro dev start [flags]`

### Options

| Option         | Value Type | Usage                                                                               |
| ------------ | ---------- | ----------------------------------------------------------------------------------- |
| `--env`      | String     | Specifies the filepath containing environment variables for the Airflow cluster.    |
| `--no-cache` | None       | Do not use any images from the container engine's cache when building your project. |

## astro dev stop

Stops all running Docker containers on your local Airflow environment. Running this command followed by `astro dev start` is required to push certain types of changes to your Astro project. Unlike `astro dev kill`, this command does not prune mounted volumes and will preserve data associated with your local Postgres metadata database.

### Usage

`astro dev stop`

## astro dev upgrade-check

Runs a script that checks whether all files in your local Astro project are compatible with Airflow 2.0 by reviewing your DAG code, deployment-level configurations, and environment variables, as well as metadata from the Airflow database. You must be on Airflow 1.10.14+ and in your Astro project directory to run this command.

### Usage

`astro dev upgrade-check`

### Related documentation

- [Running the Apache Airflow® Upgrade Check Package](https://airflow.apache.org/docs/apache-airflow/stable/upgrade-check.html#upgrade-check)

## astro login/ logout

Logs you in and out of an installation on Astronomer Software.

### Usage

Run `astro login <base-domain>` or `astro logout <base-domain>` to log in or out of your Astronomer platform respectively. This is equivalent to using the login screen of the Software UI.

If you have access to more than one Astronomer installation, each installation has a unique `<base-domain>`. When moving between platforms, make sure to log out of one `<base domain>` before logging into another.

## astro upgrade

Checks for the latest version of the Astro CLI, but does not perform the upgrade.

### Usage

`astro upgrade`

> **Note:** This command only checks whether or not a new version of the Astro CLI is available. To upgrade the Astro CLI to the latest version, run:
>
> ```sh
> brew install astro
> ```

## astro user create

Creates a new user on Astronomer. An invitation email will be sent to the email address you specify. Once this user creates an account on Astronomer, they are able to join an existing Workspace or create a new Workspace.

### Usage

`astro user create [flags]`

### Options

| Option         | Value Type | Usage                                                                                                                                     |
| ------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `--email`    | String     | Specifies the email address for the new user. If not specified, you'll be prompted to enter an address during runtime.                    |
| `--password` | String     | Specifies a password for the new user to access Astronomer with. If not specified, you'll be prompted to enter a password during runtime. |

### Related documentation

- [Manage Workspace Permissions on Astronomer](workspace-permissions.md)
- [Manage Users on Astronomer Software](manage-platform-users.md)

## astro version

Displays the running versions of both the Astro CLI and the Astronomer platform to which you are authenticated. Astronomer recommends upgrading when the minor versions of the Astro CLI and your Astronomer platform don't match.

### Usage

Run `astro version` to see both your CLI version and Astronomer platform version.

## astro workspace

Manages various Workspace-level actions on Astronomer.

### Usage

`astro workspace <subcommand> [flags]`

For more information on each subcommand, refer to the following sections.

## astro workspace create

Creates a new Workspace.

### Usage

`astro workspace create --name=<new-workspace-name> [flags]`

### Options

| Option                  | Value Type | Usage                                  |
| --------------------- | ---------- | -------------------------------------- |
| `--label` (_required_) | String     | The label/name for the new Workspace.        |
| `--description`       | String     | The description for the new Workspace. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)

## astro workspace delete

Deletes a Workspace.

### Usage

Run `astro workspace delete <your-workspace-id>` to delete a Workspace. Your Workspace ID can be found by running `astro workspace list`. You must have Workspace Admin permissions to a Workspace in order to delete it.

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)

## astro workspace list

Generates a list of all Workspaces that you have access to.

### Usage

Run `astro workspace list` to see the name and Workspace ID for each Workspace to which you have access.

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)

## astro workspace service-account create

Creates a service account for a given Workspace.

### Usage

`astro workspace service-account create --workspace-id=<your-workspace> --label=<your-label> [flags]`

### Options

| Option                        | Value Type | Usage                                                                                                                                                |
| --------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` (Required) | String     | The Workspace you're creating a service account for.                                                                                                 |
| `--label` (Required)        | String     | A label for the service account.                                                                                                                     |
| `--category`                | String     | The Category for the service account. The default is `Not set`.                                                                                |
| `role`                      | String     | The User Role for the service account. Can be `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. The default value is `WORKSPACE_VIEWER`. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro workspace service-account delete

Deletes a service account for a given Workspace.

### Usage

`astro workspace service-account delete <your-service-account-id> [flags]`

### Options

| Option             | Value Type | Usage                                                                                                                                                                                                                                     |
| ---------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` | String     | The Workspace in which you want to delete a service account. If this flag is used instead of specifying `<your-service-account-id>`, you'll be prompted to select a service account from a list of all service accounts on the Workspace. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro workspace service-account get

Shows the name, ID, and API key for each service account on a given Workspace.

### Usage

Run `astro deployment service-account get <service-account-id> --workspace-id=<your-workspace-id>` to get information on a single service account within a Workspace. To see a list of all service accounts on a Workspace, run `astro deployment service-account get --workspace-id=<your-workspace-id>`.

### Options

| Option             | Value Type | Usage                                                                                                                             |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` | String     | The Workspace you're getting the service account from. Use this flag as an alternative to specifying `<your-service-account-id>`. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Deploy to Astronomer via CI/CD](ci-cd.md)

## astro workspace switch

Switches the Workspace in which you're working.

### Usage

`astro workspace switch <workspace-id>`

## astro workspace update

Updates some of the basic information for your current Workspace.

### Usage

`astro workspace update [flags]`

At least one flag must be specified.

> **Note:** Unlike other commands, do not specify flags for this command with a leading `--`.

### Options

| Option            | Value Type | Usage                            |
| --------------- | ---------- | -------------------------------- |
| `--label`       | String     | The ID for the Workspace.        |
| `--description` | String     | A description for the Workspace. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)

## astro workspace user add

Creates a new user in your current Workspace. If the user has already authenticated to Astronomer, they will automatically be granted access to the Workspace. If the user does not have an account on Astronomer, they will receive an invitation to the platform via email.

### Usage

`astro workspace user add --email <user-email-address> [flags]`

### Options

| Option                   | Value Type | Usage                                                                                                                                                                     |
| ---------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--email` (_Required_) | String     | The user's email.                                                                                                                                                         |
| `--workspace-id`       | String     | The Workspace that the user is added to. Specify this flag if you want to create a user in a Workspace that is different than your current Workspace.                            |
| `--role`               | String     | The role assigned to the user. Can be `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. If `--role` is not specified, the default role is `WORKSPACE_VIEWER`. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro workspace user remove

Removes an existing user from your current Workspace.

### Usage

`astro workspace user remove --email <user-email-address>`

### Options

| Option                   | Value Type | Usage             |
| ---------------------- | ---------- | ----------------- |
| `--email` (_Required_) | String     | The user's email. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro workspace user list

Outputs a list of all users with access to your current Workspace.

### Usage

`astro workspace user list [flags]`

### Options

| Option             | Value Type | Usage                                                                                                                                       |
| ---------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `--workspace-id` | String     | The Workspace that you're searching in. Specify this flag if you want to search for users in a Workspace that is different than your current Workspace. |
| `--email`        | String     | The email for the user you're searching for.                                                                                                |
| `--name`         | String     | The name of the user to search for.                                                                                                         |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Manage User Permissions on Astronomer](workspace-permissions.md)

## astro workspace user update

Updates a user's role in your current Workspace.

### Usage

`astro workspace user update --email <user-email-address> [flags]`

### Options

| Option      | Value Type | Usage                                                                                                                                                                                                       |
| --------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--email` | String     | The user's email.                                                                                                                                                                                     |
| `--role`  | String     | The role you're updating the user to. Possible values are `WORKSPACE_VIEWER`, `WORKSPACE_EDITOR`, or `WORKSPACE_ADMIN`. If `--role` is not specified, the user is updated to `WORKSPACE_VIEWER` by default. |

### Related documentation

- [Manage Workspaces and Deployments on Astronomer](manage-workspaces.md)
- [Manage User Permissions on Astronomer](workspace-permissions.md)
