---
sidebar_label: 'Release notes'
title: 'Astro CLI release notes'
id: release-notes
---

<head>
  <meta name="description" content="This is where you’ll find information about the latest Astro command-line interface (CLI) commands and bug fixes. Check in regularly to know when issues are resolved and new commands are added." />
  <meta name="og:description" content="This is where you’ll find information about the latest Astro command-line interface (CLI) commands and bug fixes. Check in regularly to know when issues are resolved and new commands are added." />
</head>

<p>
    <a href="/astro-cli-release-notes.xml" target="_blank">
        <img src="/img/pic_rss.gif" width="36" height="14" alt="Subscribe to RSS Feed" />
    </a>
</p>

This document provides a summary of all changes made to the [Astro CLI](cli/overview.md). For general product release notes, go to [Astro Release Notes](release-notes.md). If you have any questions or a bug to report, contact [Astronomer support](https://cloud.astronomer.io/support).

## Astro CLI 1.15.1

Release date: May 19, 2023

### Bug fixes 

- Fixed an issue where you could not create a Deployment on a standard Hosted cluster.

## Astro CLI 1.15.0

Release date: May 18, 2023

### New commands to manage Airflow resources on Deployments

Use the following new Astro CLI commands to manage your Airflow variables, pools, connections, on Astro Deployments. These commands are particularly useful for automating the creation of new Deployments based on old ones, as you can now transfer all Airflow resources from a source Deployment to a target Deployment: 

- [`astro deployment connection list`](cli/astro-deployment-connection-list.md)
- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
- [`astro deployment connection copy`](cli/astro-deployment-connection-copy.md)
- [`astro deployment airflow-variable list`](cli/astro-deployment-airflow-variable-list.md)
- [`astro deployment airflow-variable create`](cli/astro-deployment-airflow-variable-create.md)
- [`astro deployment airflow-variable update`](cli/astro-deployment-airflow-variable-update.md)
- [`astro deployment airflow-variable copy`](cli/astro-deployment-airflow-variable-copy.md)
- [`astro deployment pool list`](cli/astro-deployment-pool-list.md)
- [`astro deployment pool create`](cli/astro-deployment-pool-create.md)
- [`astro deployment pool update`](cli/astro-deployment-pool-update.md)
- [`astro deployment pool copy`](cli/astro-deployment-pool-copy.md)

### Additional improvements

- You can now use the `--args` flag to specify pytest arguments to run with `astro dev pytest`. For example, you can run `astro dev pytest --args "-p pytest_cov"` to plugin the `pytest_cov` plugin with your pyests.
- You can now use Organization API tokens to automate Astro CLI tokens. Specify the Organization API token using the environment variable `ASTRO_API_TOKEN` in the environment where you run the Astro CLI. 
- You can now create a custom Docker/Podman compose file for your Astro project with the command `astro dev object export --compose`. After you modify the file, you can use it to start your project with `astro dev start --compose-file <compose-file-location>`.
- You can now set `postgres.repository` and `postgres.tag` with `astro config set`. You can use these configurations to customize the postgres database used in your local Airflow environments.
- The Astro CLI now automatically trims quotation marks from the beginning and end of environment variables being pushed to Astro.
- The command `astro user invite` has been deprecated.

### Bug fixes

- Fixed an issue were `astro deployment variable create/update` was not producing error when it failed to create an environment variable.
- Fixed an issue were Podman deploys were failing if the user didn't have the Docker CLI installed. 

## Astro CLI 1.14.1

Release date: April 20, 2023

### Bug fixes

- Fixed an issue where `astro workspace user list` didn't work when using a Workspace API token.

## Astro CLI 1.14.0

Release date: April 19, 2023

### New commands to manage Astro Workspaces

You can now manage Astro Workspaces from the Astro CLI using the following new commands:

- [`astro workspace create`](cli/astro-workspace-create.md)
- [`astro workspace update`](cli/astro-workspace-update.md)
- [`astro workspace delete`](cli/astro-workspace-delete.md)

To automate Workspace management, you can run these commands using a [Workspace API token](workspace-api-tokens.md).

## Astro CLI 1.13.2

Release date: April 11, 2023

### Bug fixes

- Fixed an issue where the CLI added the `dags` folder to `.dockerignore` whenever an image build was interrupted, resulting in DAGs not being deployed on the next image build.

## Astro CLI 1.13.0

Release date: March 30, 2023

:::caution

The command `astro user invite` will be deprecated in Astro CLI v1.15.0. Any use of this command in your projects or automation needs to be updated to [`astro organization user invite`](/cli/astro-organization-user-invite.md) before Astro CLI v1.15.0 is released.

:::

### New flag `--clean-output` for Deployment commands

You can now use the `-—clean-output` flag with the following commands to make sure that any output comes only from the command itself. 
- `astro deployment inspect`
- `astro deployment create`
- `astro deployment update`

This is helpful for users automating actions with deployment files, like using the Deploy Action template with [Github Actions](/astro/ci-cd-templates/github-actions.md).

### New environment variable `ASTRO_HOME`

The new environment variable `ASTRO_HOME` allows you to change the directory where the Astro CLI stores its global config file. This can be useful in environments where the CLI doesn’t have access to the HOME directory.

### Additional improvements

- The command `astro login` won’t ask for email input in the command line anymore. You can now provide your email address in the browser when you log in.


## Astro CLI 1.12.1

Release date: March 22, 2023

### Bug fixes 

- Fixed an issue where you couldn't authenticate to the Astro from the Astro CLI using single sign-on (SSO).

## Astro CLI 1.12.0

Release date: March 22, 2023

### Additional improvements

- You can now expose your local Airflow webserver and postgres database to all networks you're connected to using the following command:

    ```sh
    astro config set airflow.expose_port true
    ```

- When you trigger a DAG deploy to Astro, the CLI now includes the name of the DAG bundle version that it pushed. You can use this name to verify that your Deployment uses the correct version of your DAGs after a deploy.
- If you add the environment variable `ASTRO_API_TOKEN=<workspace-api-token>` to your environment, the Astro CLI will use the specified Workspace API token to perform Workspace and Deployment actions without requiring you to log in. 
- You can now disable [`astro run`](cli/astro-run.md) commands and exclude `astro-run-dag` from any images built by the CLI using the following command:

    ```sh
    astro config set disable_astro_run true
    ```
  
- In new Astro projects, `requirements.txt` now includes a commented list of the pre-installed provider packages on Astro Runtime. 

### Bug fixes

- Fixed an issue where the default DAG integrity test would sometimes generate an error for valid uses of `os.getenv(key,default)`.
- Fixed bugs in the default Astro project DAGs.

## Astro CLI 1.11.0

Release date: February 27, 2023

### Support for Podman

You can now configure the Astro CLI to run Airflow locally and deploy to Astro using [Podman](https://podman.io/). Podman is an alternative container engine to Docker that doesn't require root access and orchestrates containers without using a centralized daemon.

To configure the Astro CLI to use Podman, see [Run the Astro CLI using Podman](configure-cli.md#run-the-astro-cli-using-podman).

### Bug fixes 

- Fixed an issue where you couldn't run Astro CLI commands with a Deployment API key if you logged out of your personal account using `astro logout`.
- Fixed an issue where you couldn't set the minimum worker count for a worker queue to zero.
- Fixed an issue where running `astro deploy` would not return an error when you specified a Deployment name that didn't exist.
- Fixed an issue where you could not update a Deployment with a file using a Deployment API key.

## Astro CLI 1.10.0

Release date: February 2, 2023

### New commands to manage Astro users

To help you manage users in your Organization, Astro CLI 1.10.0 includes the following new commands:

- `astro organization user invite`: Invite a new user to your Astronomer Organization. 
- `astro organization user update`: Update a user's Organization role.
- `astro organization user list`: List all users in your Organization.
- `astro workspace user add`: Add a user to a Workspace.
- `astro workspace user update`: Update a user's role in a Workspace.
- `astro workspace user list`: List all users in a Workspace.
- `astro workspace user remove`: Remove a user from a Workspace.

:::info

`astro organization user invite` is identical to the existing `astro user invite` command. `astro user invite` will be deprecated in a future release.

:::

For more information, see the [`astro organization`](cli/astro-organization-user-invite.md) and [`astro workspace`](cli/astro-workspace-user-add.md) command references.

## Astro CLI 1.9.0

Release date: January 13, 2023

### Manage Astro Deployments as code

Astro CLI version 1.9 includes three new commands that make it possible to programmatically create and update Deployments:

- `astro deployment inspect --template`: Create a template file in YAML for an existing Deployment. This template file includes all information about the Deployment in its current state, including worker queue configurations, environment variables, and Astro Runtime version.
- `astro deployment create --deployment-file`: Create a new Deployment with the configurations specified in a template file.
- `astro deployment update --deployment-file`: Update an existing Deployment based on the values in a Deployment file.

You can use template and Deployment files to define Astro Deployments as code. For example, if your team regularly creates and deletes Deployments for testing, you can use template files to avoid manually copying configurations in the Cloud UI. For more information, see [Astro CLI command reference](cli/astro-deployment-create.md).

### New `--dag-file` flag for `astro run`

By default, the `astro run` command parses all of the DAGs in your `dags` directory even if you are only running one DAG.

In Astro CLI 1.9, you can instead use the `--dag-file` flag to run a specific DAG file without parsing all other DAGs in your directory. Specifying an individual DAG file makes it easier to troubleshoot errors for that DAG and results in faster execution of the command.

### Additional improvements

- When you run Airflow locally, you no longer need to enter credentials to log in to the Airflow UI.
- When you run Airflow locally, you can now access to the Airflow UI **Configurations** page (**Admin** > **Configurations**). This page shows the current configuration for your environment, including environment variables and Astro Runtime defaults.
- The Astro CLI now reminds you when a new version of the Astro CLI is available. To turn this feature off, run `astro config set -g upgrade_message false`.

## Astro CLI 1.8.4

Release date: December 12, 2022

### Additional improvements

- The `__pycache__/` directory is now included in the `.gitignore` file of an Astro project by default. `__pycache__/` includes compiled versions of DAG and Python files that are automatically generated and should not be committed to Git.
- Clarified the message that appears when you run `astro deployment update --dag-deploy enable` and DAG-only deploys were already enabled for the Deployment.

### Bug fixes

- Fixed an issue related to the [SQLAlchemy connection](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#sql-alchemy-conn) ([`sql_alchemy_conn`]) in local Airflow environments. Now, users running Airflow 2.3 or above do not see deprecation warnings for SQLAlchemy in logs for locally running Airflow components.

## Astro CLI 1.8.3

Release date: November 28, 2022

### Additional improvements

- Improved error handling for `astro login`.
- Added minor performance improvements to `astro run`

### Bug fixes

- Fixed an issue where `astro run` could not locate `airflow_settings.yaml` when running a local Airflow environment. 
- Fixed an issue were the Airflow settings file created by `astro dev object export` was not compatible with `astro run`.

## Astro CLI 1.8.1

Release date: November 23, 2022

### Bug fixes

- Fixed an issue where you could not use `astro deploy` if you did not have an `.env` file in your Astro project.

## Astro CLI 1.8.0

Release date: November 23, 2022

### New `astro run` command

You can now use the `astro run` command to run and debug a DAG from the command line without starting a local Airflow environment. When you run the command, the CLI compiles your DAG and runs it in a single Airflow worker container based on your Astro project configurations. You can see task success or failure, as well as task logs, directly in your terminal.

This command is an alternative to running `astro dev restart` every time you make a change to your DAG. Running DAGs without a scheduler or webserver improves the speed at which you can develop and test data pipelines.

To learn more, see [Run and Debug DAGs with Astro Run](test-and-troubleshoot-locally.md#run-and-debug-dags-with-astro-run).

### Additional improvements

- When you run `astro deploy` with an empty `dags` folder, the CLI excludes your `dags` folder when building and pushing an image of your project to Astro. This lets you manage your DAGs and project files in separate repositories when using [DAG-only deploys](deploy-code.md#deploy-dags-only).
- The `deployment inspect` command now includes a `dag-deploy-enabled` field, and the fields are now ordered in logical groupings instead of by alphabetical order.

### Bug fixes

- Fixed an issue where configurations specified in the `docker-compose.override.yaml` file of an Astro project were not properly applied. 
- Fixed an issue where `astro login` didn’t recognize some valid domains.

## Astro CLI 1.7.0

Release date: November 9, 2022 

### Deploy only DAGs with `astro deploy -—dags`

Use `astro deploy -—dags` with the Astro CLI to push only the `dags` directory of your Astro project to a Deployment on Astro. This is an additional option to `astro deploy`, which pushes all files in your Astro project every time you deploy your code to Astro.

Deploying only DAGs:

- Is significantly faster than running `astro deploy` when you only make changes to the `dags` directory.
- Does not cause your workers and schedulers to terminate and restart every time you make a change to a DAG and does not result in downtime for your Deployment.
- Enables your team to create separate CI/CD processes for deploying DAGs and deploying other changes to your Astro project.

When you make changes to other files in your Astro project that aren't in the `dags` directory, the `astro deploy` command is still required.

To use this feature, you must enable it for each Deployment. See [Deploy DAGs only](deploy-code.md#deploy-dags-only). For example CI/CD workflows with this feature enabled, see [CI/CD](set-up-ci-cd.md).

### New `astro deployment inspect` command

You can now run `astro deployment inspect` to return a Deployment's current state and configuration as a JSON or YAML object. This includes worker queue settings, Astro Runtime version, and more. Use this command to quickly understand the state of your Deployment as code and as an alternative to viewing it in the Cloud UI.

For more information, see the [CLI command reference](cli/astro-deployment-inspect.md).

### Additional improvements

- The outputs for `astro dev parse` and `astro dev pytest` commands have improved legibility by no longer including Docker container logs.
- The `astro organization switch` command now includes a `-—login-link` flag that you can use to manually log in if you don't have access to a web browser.
- You can now provide either an Organization name or ID when running `astro organization switch`.
- `astro dev start` now times out if the Airflow webserver does not become healthy within a set period of time. Use the `-—wait` flag to specify a wait time in seconds or minutes.

### Bug fixes

- Fixed an issue where `astro deploy` with `colima` was failing due to an issue with registry authentication
- Fixed an issue where `astro deployment list` didn't display the Workspace ID for a Deployment
  
## Astro CLI 1.6.1

Release date: November 3, 2022 

### Bug fixes 

- Fixed an issue where authenticating to Astronomer Software with `interactive=true` in your CLI configuration resulted in a 502 error.

## Astro CLI 1.6.0 

Release date: September 28, 2022 

### New commands to manage Airflow objects 

You can use the new `astro dev object` commands to better manage Airflow connections, variables, and pools between your local testing environment and Astro Deployments. 

- `astro dev object import` imports connections, variables, and pools from your Astro project `airflow_settings.yaml` into your locally running Airflow environment.
- `astro dev object export` exports connections, variables, and pools from your local airflow database to a file of your choosing. specify the `--env-export` flag to export Airflow connections and variables to your `.env` file as Astro environment variables. 

These commands enable you to:

- Update objects in a locally running Airflow environment without restarting it.
- Quickly move Airflow objects from a local testing environment to an Astro Deployment. 

### New commands to configure worker queues on Astro

You can now mange create, delete, and update worker queues on an Astro Deployment with the following new commands:

- `astro deployment worker-queue create` creates a new worker queue in a Deployment. 
- `astro deployment worker-queue update` updates an existing worker queue. 
- `astro deployment worker-queue delete` deletes an existing worker queue. 

### New commands to manage Organization

If you belong to multiple Astro Organizations, you can now use the CLI to switch between your Organizations: 

- `astro organization list` lists all Organizations you belong to
- `astro organization switch` allows you to switch between Organizations

To use these commands, you must be authenticated to your primary Organization through the CLI. 

### Additional improvements 

- The Astro CLI for Windows is now distributed as an `.exe` file.
- You can now define connections in the `conn_extra` field of `airflow_settings.yaml` as YAML blocks instead of stringified JSON objects. 
- You can now use the `--settings-file` flag with `astro dev start` to load and update Airflow objects in your environment from the configuration file of your choosing. 

### Bug fixes 

- Fixed an issue where the Astro CLI generated incorrect URLs for the Deployment dashboard
- Improved error handling and messaging when the Astro CLI doesn't recognize the image in a project's Dockerfile

## Astro CLI 1.5.1

Release date: September 23, 2022

### Bug fixes

- Fixes an issue where you could not push a deprecated version of Astro Runtime to a Deployment, even if that Deployment was already running that version. Instead of blocking deploys, the Astro CLI now shows only a warning.

## Astro CLI 1.5.0

Release date: September 2, 2022

### Additional improvements

- You can now use a new `--deployment-name` flag with all `astro deployment` commands to specify a Deployment by its name instead of its Deployment ID.
- You can now use a new `--wait` flag with `astro deployment create` to have the command wait until the new Deployment is healthy before completing.
- You can now use a new `--no-browser` flag with `astro dev start` if you don't want the Airflow UI to automatically open in a new tab on your browser when you run the command.
- The `astro dev restart` command no longer opens a new tab in your browser for the Airflow UI. When you use this command to apply changes to your DAGs, the Airflow UI should already be open.

### Bug fixes

- Fixed an issue where some environment variable values could be truncated when using `astro deployment variable create --load`.
- Fixed an issue where users with access to more than one Astro Organization could only log in to their primary Organization. Now, users can authenticate to multiple Organizations with a [token login](https://docs.astronomer.io/astro/cli/astro-login). Native support for organization commands is coming soon.

## Astro CLI 1.4.0

Release date: August 18, 2022

### New command to bash into local Airflow containers

You can now run bash commands in any locally running Airflow container using `astro dev bash`. You can use this to:

- Verify the packages installed in your Airflow environment.
- Run python commands and test python functions in your Airflow environment.
- Explore the local Airflow metadata database with a simple `postgres` command.

For more information, see the [CLI command reference](cli/astro-dev-bash.md).

### New command to invite a user to an Astro Organization

You can invite new users to an Astro Organization with the new `astro user invite` command. Previously, you could only invite users to Astro with the Cloud UI.

For more information, see the [CLI command reference](cli/astro-organization-user-invite.md).

### Additional improvements

- Create multiple environment variables more easily by passing a list of key and value pairs to `astro deployment variable create` and `astro deployment variable update`. For example, `astro deployment variable create KEY1=VAL1 KEY2=VAL2` creates variables for `KEY1` and `KEY2`. You can still create environment variables from a file with the `--load` flag.
- If Docker Desktop isn't already running on your machine, the CLI automatically starts it when you run `astro dev start`. Previously, the CLI showed an error and forced users to manually start Docker. Note that this feature only works on Mac OS.
- The Airflow UI now automatically opens in your default web browser after you run `astro dev start` as soon as the Airflow webserver is ready. Previously, you had to wait for the webserver to be ready and manually open or refresh your web browswer.

## Astro CLI 1.3.0

Release date: July 19, 2022

### Deploy a custom Docker image with new `--image-name` flag

You can now deploy your Astro project with a custom Docker image by running `astro deploy --image-name <custom-image>`, as long as the image is based on Astro Runtime and is available in a local Docker registry. Customizing your Runtime image lets you securely mount additional files and arguments in your project, which is required for setups such as [installing Python packages from private sources](develop-project.md#install-python-packages-from-private-sources).

Using this flag, you can automate deploying custom Runtime images from a CI/CD pipeline. You can also separate your build and deploy workflows in different pipelines.

The `--image-name` flag is also available for the following local development commands:

- `astro dev start`
- `astro dev restart`
- `astro dev parse`
- `astro dev pytest`

For more information about this command, see the [CLI command reference](cli/astro-deploy.md).

### New token login method for Astro

Astro CLI users can now log into Astro on a machine that does not have access to a browser by running `astro login --token-login`. This is an alternative to `astro login`, which automatically opens the Cloud UI in a browser on your machine.

If you run the command with this flag, the CLI provides a link to the Cloud UI that you can manually open in a web browser. You then copy an authentication token from the UI and enter it in the CLI. If you're using a browserless machine with the Astro CLI, this enables you to log in. For a browserless login, you can open the link and copy the token on a separate machine from the one running the Astro CLI.

For more information about this command, see the [CLI command reference](cli/astro-login.md).

### Skip parsing DAGs before deploys

By default, `astro deploy` automatically parses the DAGs in your Astro project for syntax and import errors. To develop more quickly, you can now configure the Astro CLI to automatically skip parsing DAGs before a deploy by updating one of the following configurations:

- Add `skip_parse: true` to your `.astro/config.yaml` file.
- Add `ASTRONOMER_SKIP_PARSE=true` as an environment variable to your local environment or CI/CD pipeline.

For more information on parsing DAGs, see [Parse DAGs](test-and-troubleshoot-locally.md#parse-dags). For more information about deploying to Astro, see [Deploy code](deploy-code.md).
### Additional improvements

- Upgraded the CLI to Go version 1.18, which includes improvements to both performance and the development experience. See the [Go Blog](https://go.dev/blog/go1.18).

### Bug fixes

- Fixed an issue where parsing DAGs during a deploy would kill a local project
- Fixed an issue where `astro dev parse` failed on DAGs using the `SnowflakeOperator`. If you use the `SnowflakeOperator`, delete `.astro/test_dag_integrity_default.py` from the `tests` directory of your Astro project and run `astro dev init` with the Astro CLI. This command will create a new file in your project that does not have this issue.

## Astro CLI 1.2.0

Release date: June 28, 2022

### Bug fixes

- Fixed an issue where `astro deploy` would kill a running project

## Astro CLI 1.1.0

Release date: June 13, 2022

### Deployment API keys now work with Deployment commands

You can now run the following commands with a Deployment API key:

- `astro deploy`
- `astro deployment list`
- `astro deployment logs`
- `astro deployment update`
- `astro deployment delete`
- `astro deployment variable list`
- `astro deployment variable create`
- `astro deployment variable update`

Previously, you could run only the `astro deploy` command with a Deployment API key. For more information on API keys, see [Manage Deployment API keys](api-keys.md).

### Easier way to determine Deployment ID on Deployment commands

The Astro CLI now follows a new process to determine which Deployment to run a command against. Specifically:

- The Astro CLI first checks if a Deployment ID is specified as an argument to the command. For example, `astro deployment update <deployment-id>`.
- If not found, it checks for a Deployment ID in the `./astro/config.yaml` file of your Astro project. In this file, you can set up to one Deployment ID as default. This is an alternative to manually specifying it or using a Deployment API key.
- If only one Deployment exists in your Workspace, the CLI automatically runs the command for that Deployment without requiring that you specify its Deployment ID.
- If a Deployment API key is set as an OS-level environment variable on your machine or in a CI/CD pipeline, the CLI automatically runs the command for that Deployment without requiring a Deployment ID.
- If multiple Deployments exist in your Workspace and a Deployment API key is not found, the CLI will prompt you to select a Deployment from a list of all Deployments in that Workspace.
- If the Astro CLI doesn't detect a Deployment across your system, it will prompt you to create one.

These changes make it easier to run and automate Deployment-level commands with the Astro CLI. Most notably, it means that you no longer need to specify a Deployment ID in cases where it can be automatically implied by our system.

If your CI/CD pipelines currently define one or more Deployment IDs, you may remove those IDs and their corresponding environment variables as they are no longer required. For up-to-date CI/CD templates, see [Automate code deploys with CI/CD](set-up-ci-cd.md).

### Bug fixes

- Fixed an issue where only Workspace Admins could create Deployments

## Astro CLI 1.0.1

Release date: June 6, 2022

### Bug fixes

- Fixed an issue where `astro deploy`, `astro dev parse`, and `astro dev pytest` failed for some users

## Astro CLI 1.0.0

Release date: June 2, 2022

### A shared CLI for all Astronomer users

The Astro CLI is now a single CLI executable built for all Astronomer products. This new generation of the CLI optimizes for a consistent local experience with Astro Runtime as well as the ability to more easily upgrade to Astro from other products hosted on Astronomer.

To establish a shared framework between products, the Astro CLI now uses a single `astro` executable:

```sh
# Before upgrade
astrocloud dev init

# After upgrade
astro dev init
```

Additionally, some commands have been standardized so that they can be shared between Astro and Astronomer Software users. As part of this change, `astro auth login` and `astro auth logout` have been renamed `astro login` and `astro logout`:

```sh
# Before upgrade
astrocloud auth login

# After upgrade
astro login
```

For Astro users, these are the only changes to existing CLI functionality. All other commands will continue to work as expected. We strongly recommend that all users upgrade. For instructions, see [Migrate from `astrocloud` to `astro`](cli/install-cli.md#migrate-from-astrocloud-to-astro).

:::caution Possible Breaking Change

If you currently have CI/CD pipelines that install the `astrocloud` executable of the Astro CLI, we encourage you to update them to use the latest version of `astro` to ensure reliability. All `astrocloud` commands will continue to work for some time but will be deprecated by Astronomer soon.

For updated CI/CD examples, see [CI/CD](set-up-ci-cd.md).
:::


### New Command To Set Astro Project Configurations

You can now use `astro config get` and `astro config set` to retrieve and modify the configuration of your Astro project as defined in the `.astro/config.yaml` file. The configuration in this file contains details about how your project runs in a local Airflow environment, including your Postgres username and password, your webserver port, and your project name.

For more information about these commands, see the [CLI command reference](cli/astro-config-set.md).

### New Command To Switch Between Astronomer Contexts

You can now use `astro context list` and `astro context switch` to show all the Astronomer contexts that you have access to and switch between them. An Astronomer context is defined as a base domain that you can use to access either Astro or an installation of Astronomer Software. A domain will appear as an available context if you have authenticated to it at least once.

This command is primarily for users who need to work in both Astro and Astronomer Software installations. If you're an Astro user with no ties to Astronomer Software, ignore this command. For more information, see the [CLI command reference ](cli/astro-context-switch.md).

For more information about these commands, see the [CLI command reference ](cli/astro-context-switch.md).

### Additional improvements

- Astro CLI documentation has been refactored. You can now find all information about the CLI, including installation steps and the command reference, under the [Astro CLI tab](cli/overview.md).
- The nonfunctional `--update` flag has been removed from `astro deployment variable create`. To update existing environment variables for a given Deployment, use `astro deployment variable update` instead.

## 1.5.0 (`astrocloud`)

Release date: April 28, 2022

### New command to update Deployment environment variables

A new `astro deployment variable update` command allows you to more easily update an existing environment variable by typing a new value directly into your command line or adding the updated variable to a `.env` file.

This command replaces the `—update` flag that was previously released with the `astro deployment variable create` command. For more information, see the [Astro CLI command reference](cli/astro-deployment-variable-create.md).

### Additional improvements

- When you run `astro workspace switch`, you can now specify a `<workspace-id>` as part of the command and avoid the prompt to manually select a Workspace
- You now need to provide an email address only the first time you run `astro login`. After you run that command once successfully, the Astro CLI will cache your email address in your `config.yaml` file and not prompt you to enter it again
- The `astro deploy` and `astro dev start` commands will now inform you if there is a new version of Astro Runtime available

### Bug fixes

- Fixed an issue were the `astro deployment variable create —load` command would fail if the specified `.env` file had a comment (e.g. `#  <comment>`) in it
- Fixed an issue were Deployment API keys would not work locally for some users

## 1.4.0 (`astrocloud`)

Release date: April 14, 2022

### New command to create and update environment variables

`astro deployment variable create` is a new Astro CLI command that allows you to create and update [environment variables](environment-variables.md) for a Deployment on Astro. New environment variables can be loaded from a file (e.g. `.env`) or specified as inputs to the CLI command itself. If you already set environment variables [via a `.env` file locally](develop-project.md#set-environment-variables-via-env-local-development-only), this command allows you to set environment variables on Astro from that file as well. More generally, this command makes it easy to automate creating or modifying environment variables instead of setting them manually in the Cloud UI.

For more information about this command and its options, see the [Astro CLI command reference](cli/astro-deployment-variable-create.md).

### New command to list and save Deployment environment variables

You can now list existing environment variables for a given Deployment and save them to a local `.env` file with a new `astro deployment variable list` command. This command makes it easy to export existing environment variables for a given Deployment on Astro and test DAGs with them in a local Airflow environment.

For more information about this command and its options, see the [Astro CLI command reference](cli/astro-deployment-variable-list.md).

### Additional improvements

- You can now specify a custom image name in your Astro project's `Dockerfile` as long as the image is based on an existing Astro Runtime image

## 1.3.4 (`astrocloud`)

Release date: April 11, 2022

### Additional improvements

- Improved the performance of `astro dev start`
- When you successfully push code to a Deployment with `astro deploy`, the CLI now provides URLs for accessing the Deployment's Cloud UI and Airflow UI pages.

## 1.3.3 (`astrocloud`)

Release date: March 31, 2022

### Additional improvements

- The `astro dev start` command should now be ~30 seconds faster
- When `astro dev parse` results in an error, the error messages now specify which DAGs they apply to
- If your DAGs don't pass the basic unit test that's included in your Astro project (`test_dag_integrity.py` ), running them with `astro dev pytest` will now provide more information about which part of your code caused an error

### Bug fixes

- Fixed an issue where running `astro dev parse/pytest` would occasionally result in an "orphaned containers" warning
- Fixed an issue where `astro dev parse/pytest` would crash when parsing projects with a large number of DAGs
- Fixed an issue were some `docker-compose.override.yml` files would cause `astro dev parse/pytest` to stop working

## 1.3.2 (`astrocloud`)

Release date: March 17, 2022

:::info

Astro CLI 1.3.2 is a direct patch replacement for 1.3.1, which is no longer available for download because it includes a critical bug related to `astro dev parse/pytest`. If you are currently using Astro CLI 1.3.1, then we recommend upgrading to 1.3.2+ as soon as possible to receive important bug fixes.

:::

### Support for identity-based login flow

To better integrate with Astro's identity-based login flow, the CLI now prompts you for your login email after you run `astro login`. Based on your email, the CLI assumes your Astro Organization and automatically brings you to your Organization's login flow via web browser.

### Additional improvements

- `astro deploy` now builds and tests only one image per deploy. This should result in improved deployment times in CI/CD pipelines which use this command.
- The `test` directory generated by `astro dev init` now includes more example pytests.

### Bug fixes

- Partially fixed `dev parse` permission errors on WSL. To fully fix this issue for an Astro project, you must delete the project's existing `.astro` directory and rerun `astro dev init`.
- Fixed an issue where running `astro dev parse/pytest` while a local Airflow environment was running would crash the Airflow environment. This issue was introduced in Astro CLI 1.3.1, which is no longer available for download.

## 1.3.0 (`astrocloud`)

Release date: March 3, 2022

### New command to parse DAGs for errors

`astro dev parse` is a new Astro CLI command that allows you to run a basic test against your Astro project to ensure that essential aspects of your code are properly formatted. This includes the DAG integrity test that is run with `astro dev pytest`, which checks that your DAGs are able to to render in the Airflow UI.

This command was built to replace the need to constantly run `astro dev restart` during troubleshooting to see if your DAGs render in the Airflow UI. Now, you can quickly run `astro dev parse` and see import and syntax errors directly in your terminal without having to restart all Airflow services locally. For more complex testing, we still recommend using `astro dev pytest`, which allows you to run other custom tests in your project.

For more information about `astro dev parse`, see the [CLI command reference](cli/astro-dev-parse.md). For more guidance on testing DAGs locally, see [Test DAGs locally](test-and-troubleshoot-locally.md#test-dags-locally).

### `astro deploy` parses DAGs by default

To better protect your Deployments from unexpected errors, `astro deploy` now automatically applies tests from `astro dev parse` to your Astro project before completing the deploy process. If any of these tests fail, the CLI will not push your code to Astro.

For more information about `astro deploy`, see [CLI command reference](cli/astro-deploy.md).

:::danger Breaking Change

For Deployments running Astro Runtime 4.1.0+, `astro deploy` will no longer complete the code push to your Deployment if your DAGs contain basic errors. If any files in your Astro project contain these errors, then certain deploys might stop working after you upgrade the Astro CLI to 1.3.0.

To maintain the CLI's original behavior, use `astro deploy --force`. This command forces a deploy even if errors are detected in your DAGs.

:::

### New command to update Deployment configurations

You can now use `astro deployment update` to update certain configurations for an existing Astro Deployment directly from the Astro CLI. The configurations that you can update are:

- Deployment name
- Deployment description
- Scheduler resources
- Scheduler replicas
- Worker resources

This is the same set of configurations that you can modify with the **Edit Configuration** view in the Cloud UI. For more information on modifying a Deployment, see [Configure a Deployment](configure-deployment-resources.md). For more information about this command, see [CLI command reference](cli/astro-deployment-update.md).

## 1.2.0 (`astrocloud`)

Release date: February 25, 2022

### Deploy to Astro with Deployment API keys for simpler CI/CD

You can now use [Deployment API keys](api-keys.md) to run `astro deploy` either from the CLI directly or via a CI/CD script. This update simplifies deploying code to Astro via CI/CD.

With an existing Deployment API key, you can set `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET` as OS-level environment variables. From there, you can now configure a CI/CD pipeline that:

- Installs the Astro CLI.
- Runs `astro deploy`.

When `astro deploy` is run, the CLI will now automatically look for and use the Deployment API key credentials that were set as environment variables to authorize and complete a code push.

Previously, any script that automated code pushes to Astro had to include a series of `cURL` requests to the Cloud API and could not use Deployment API keys to run an Astro CLI command. If your existing CI/CD pipelines still utilize this method, we recommend replacing those commands with an Astro CLI-based workflow. For more information and guiding examples, see [CI/CD](set-up-ci-cd.md).

### New command to run DAG unit tests with pytest

You can now run custom unit tests for all DAGs in your Astro project with `astro dev pytest`, a new Astro CLI command that uses [pytest](https://docs.pytest.org/en/7.0.x/index.html), a common testing framework for Python. As part of this change, new Astro projects created via `astro dev init` now include a `tests` directory, which includes one example pytest built by Astronomer.

When you run this command, the Astro CLI creates a local Python environment that includes your DAG code, dependencies, and Astro Runtime Docker image. The CLI then runs any pytests in the `tests` directory and shows you the results of those tests in your terminal. You can add as many custom tests to this directory as you'd like.

For example, you can use this command to run tests that check for:

- Python and Airflow syntax errors.
- Import errors.
- Dependency conflicts.
- Unique DAG IDs.

These tests don't require a fully functional Airflow environment in order to execute, which makes this Astro CLI command the fastest and easiest way to test DAGs locally.

In addition to running tests locally, you can also run pytest as part of the Astro deploy process. To do so, specify the `--pytest` flag when running `astro deploy`. This ensures that your code push to Astro automatically fails if any DAGs do not pass all pytests specified in the `tests` directory of your Astro project. For more information, see [Test DAGs locally with pytest](test-and-troubleshoot-locally.md#test-dags-locally-with-pytest).

### New command to view Deployment scheduler Logs

If you prefer to troubleshoot DAGs and monitor your Deployments from the command line, you can now run `astro deployment logs`, a new Astro CLI command that allows you to view the same scheduler logs that appear in the **Logs** tab of the Cloud UI.

When you run this command, all scheduler logs emitted by a Deployment over the last 24 hours appear in your terminal. Similarly to the Cloud UI, you can filter logs by log level using command flags. For more information about this command, see the [CLI command reference](cli/astro-deployment-logs.md).

### New commands to create and delete Deployments on Astro

You can now use the Astro CLI to create and delete Deployments on Astro with two new commands:

- `astro deployment create`
- `astro deployment delete`

These commands are functionally identical to the [Deployment configuration](configure-deployment-resources.md) and deletion process in the Cloud UI. For more information, see the [CLI command reference](cli/astro-deployment-create.md).

## 1.1.0 (`astrocloud`)

Release date: February 17, 2022

### New `astro dev restart` command to test local changes

For users making quick and continuous changes to an Astro project locally, the Astro CLI now supports a new `astro dev restart` command. This command makes local testing significantly easier and is equivalent to running `astro dev stop` followed by `astro dev start`.

### Support for the triggerer in local Airflow environments

The Astro CLI now supports the Apache Airflow [triggerer component](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html?) in a local environment. This means that you can test DAGs that use [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators) locally before pushing them to a Deployment on Astronomer. Additionally, triggerer logs appear alongside webserver and scheduler logs when you run `astro dev logs`.

The triggerer will only be created in local environments running Astro Runtime 4.0.0+.

### Additional improvements

- Postgres has been upgraded from 12.2 to [12.6](https://www.postgresql.org/docs/12/release-12-6.html) for local Airflow environments.

## 1.0.0 (`astrocloud`)

Release date: February 3, 2022

### Introducing the Astro CLI

The Astro CLI (`astrocloud`) is now generally available as the official command-line tool for Astro. It is a direct replacement of the previously released `./astro` executable.

The Astro CLI sets the foundation for more robust functionality in the future and includes several significant improvements to both the local development experience as well as use cases specific to Astro. These changes are summarized in the following sections.

The Astro CLI can be installed via Homebrew. Commands take the form of:

```sh
astro <command> # E.g. `astro dev start`
```

We strongly recommend that all users install the Astro CLI and delete the `./astro` executable from local directories as soon as possible. For guidelines, read [Install the Astro CLI](cli/install-cli.md). As of February 2022, `./astro` will no longer be maintained by our team. With that said, the release of the Astro CLI does not have any impact on your existing Deployments or DAGs.

### New authentication flow

The Astro CLI introduces an easy way to authenticate. Instead of requiring that users manually pass authentication tokens, the new CLI consists of a simple, browser-based login process.

Built with refresh tokens, the Astro CLI also does not require that users re-authenticate every 24 hours, as was the case with `./astro`. As long as you remain authenticated via the Cloud UI, your session via the Astro CLI will remain valid. You can expect to be asked to re-authenticate only once every few months instead of on a daily basis.

### Improved local development

Astro CLI 1.0.0 includes several improvements to the local development experience:

- You can now run `astrocloud dev start` with [Docker Buildkit](https://docs.docker.com/develop/develop-images/build_enhancements/) enabled. This resolves a [common issue](https://forum.astronomer.io/t/buildkit-not-supported-by-daemon-error-command-docker-build-t-airflow-astro-bcb837-airflow-latest-failed-failed-to-execute-cmd-exit-status-1/857) where users with Docker Buildkit enabled could not run this command.
- After running `astrocloud dev start`, the CLI no shows you the status of the webserver container as it spins up on your local machine. This makes it easier to know whether the Airflow UI is unavailable because the Airflow webserver container is still spinning up.

### Additional improvements

- `astrocloud deploy` now shows a list of your Deployments in the order by which they were created instead of at random.

## 1.0.4 (`./astro`)

Release date: December 9, 2021

### Improved example DAGs

The Astro CLI is built to enable developers to learn about, test, automate, and make the most of Apache Airflow both locally and on Astro. To that end, we've updated the CLI with two example DAGs that will be present for all users in the `/dags` folder that is automatically generated by `astro dev init`.

The file names are:
- `example-dag-basic.py`
- `example-dag-advanced.py`

The basic DAG showcases a simple ETL data pipeline and the advanced DAG showcases a series of more powerful Airflow features, including the TaskFlow API, jinja templating, branching and more. Both DAGs can be deleted at any time.

### Bug fixes

Fixed a broken documentation link and outdated description in the `airflow_settings.yaml` file, which you can use to programmatically set Airflow connections, variables, and pools locally.

## 1.0.3 (`./astro`)

Release date: November 5, 2021

- Bug Fix: Fixed an issue where users saw errors related to S3 in webserver logs when running locally (e.g. `Failed to verify remote log exists s3:///`).

## 1.0.2 (`./astro`)
Release date: October 25, 2021

- Improved help text throughout the CLI

## 1.0.1 (`./astro`)

Release date: October 15, 2021

- This release contains changes exclusively related to the Astro CLI developer experience.

## 1.0.0 (`./astro`)

Release date: September 28, 2021

- Improvement: `./astro dev init` now always pulls the latest version of Astro Runtime for new projects. This means that you no longer have to upgrade the CLI in order to take advantage of a new Runtime release. Note that you still need to manually [upgrade Runtime](upgrade-runtime.md) for existing projects.
- Improvement: Updated error messages throughout the CLI to be more clear and useful

## 0.2.9-beta (`./astro`)

Release date: September 20, 2021

- Improvement: Bumped the default Astro Runtime version for new projects to [`3.0.2`](runtime-release-notes.md#astro-runtime-302)
- Improvement: You can now use `./astro dev run` to run Airflow CLI commands
- Improvement: You can now use `./astro dev logs` to show logs for the Airflow scheduler and webserver when developing locally

## 0.2.8-beta (`./astro`)

Release date: August 31, 2021

- Improvement: Bumped the default Astro Runtime version for new projects to [`3.0.0`](runtime-release-notes.md#astro-runtime-300)
- Improvement: Updated help text throughout the CLI
- Improvement: Projects created with `./astro dev init` now include a README file

## 0.2.7-beta (`./astro`)

Release date: July 31, 2021

- Bug Fix: Fixed an issue where users could not push DAGs to Deployments on Astro via the CLI.

## 0.2.6-beta (`./astro`)

Release date: July 30, 2021

- Improvement: You can now run `./astro login` without specifying a domain (`astronomer.io` is always assumed).
