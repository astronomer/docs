---
title: "Upgrade to Astro CLI version 1.0+"
sidebar_label: "Upgrade to Astro CLI version 1.0+"
id: upgrade-astro-cli
description: A list of all breaking changes and upgrade steps related to the major release of Astro CLI version 1.0+
---

Astro CLI version 1.0+ delivers several new features to Astronomer Software and establishes a shared CLI framework across all Astronomer products.

Several commands and their flags have been updated as part of this release, resulting in breaking changes for users of Astronomer Software. Use this document to learn about these breaking changes and prepare for your upgrade to Astro CLI version 1.0+.

This information applies only to users who are upgrading the Astro CLI from a pre-1.0 to a post-1.0 version. To install the latest version of the CLI for the first time, see [Install the CLI](https://docs.astronomer.io/astro/cli/install-cli).

## Upgrade checklist

Before installing Astro CLI version 1.0+, complete all of the following steps:

- Make sure you are running Astronomer Software version 0.28+. If you're not sure, ask your system administrator.
- Review the [Breaking changes](upgrade-astro-cli.md#breaking-changes) section in this document.
- Update any CI/CD pipelines or automated processes that use Astro CLI commands to ensure that these commands do not break after you upgrade.
- Review any custom shortcuts in your local CLI terminal to ensure that your shortcuts do not run any CLI commands that are no longer supported.

After you complete these steps, upgrade to Astro CLI version 1.0+ by following the instructions in [Install the CLI](https://docs.astronomer.io/astro/cli/install-cli).

## Features

### New `astro dev restart` command to test local changes

For users making continuous changes to an Astro project locally, the Astro CLI now supports a new `astro dev restart` command. With this new command, you no longer need to run `astro dev stop` followed by `astro dev start` when you're testing locally.

For more information, see [CLI command reference](https://docs.astronomer.io/astro/cli/astro-dev-restart).

### New command to run DAG unit tests with pytest

You can now run custom unit tests for all DAGs in your Astro project with `astro dev pytest`, a new Astro CLI command that uses [pytest](https://docs.pytest.org/en/7.1.x/contents.html#), a common testing framework for Python. As part of this change, new Astro projects created with `astro dev init` now include a `tests` directory, which includes one example unit test built by Astronomer.

In addition to running tests locally, you can also run `astro dev pytest` as part of the deploy process to Astronomer Software. For more information, see [CLI command reference](https://docs.astronomer.io/astro/cli/astro-dev-pytest).

### New command to parse DAGs for errors

The new `astro dev parse` command allows you to run a basic test against your Astro project to ensure that your DAGs are able to to render in the Airflow UI. This includes the DAG integrity test that is run with `astro dev pytest`, which checks that your DAGs are able to to render in the Airflow UI. Now, you can quickly run `astro dev parse` and see import and syntax errors directly in your terminal without having to restart all Airflow services locally.

For more complex testing, Astronomer recommends using `astro dev pytest` to run custom tests in your project. For more information on `astro dev parse`, see the [CLI command reference](https://docs.astronomer.io/astro/cli/astro-dev-parse).

## Breaking changes

This topic contains all information related to breaking changes included in Astro CLI version 1.0+ relative to version 0.28 and below.

This topic does not include information about new features and changes that are not breaking. For a summary of all changes, see the [CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

### `astro dev init`: New `--use-astronomer-certified` Flag Required for All New Projects Deployed to Software

When you create a new Astro project with the `astro dev init` command, you must now specify the `--use-astronomer-certified` flag if you want to [deploy the project](deploy-cli.md) to a Deployment on Astronomer Software. This flag initializes your project with the latest Astronomer Certified version.

If you don't specify this flag, the project is initialized with an Astro Runtime image. Support for Astro Runtime on Astronomer Software is coming soon.

```sh
# Before upgrade
astro dev init

# After upgrade
astro dev init --use-astronomer-certified
```

### `astro auth login` is now `astro login`

The previous `astro auth login` and `astro auth logout` commands have been simplified:

```sh
# Before upgrade
astro auth login <domain>
astro auth logout

# After upgrade
astro login <domain>
astro logout
```

### `astro workspace create/update` now takes all configurations as flags

When you specify configurations for a Workspace using `astro workspace create` or `astro workspace update`, you must now specify those properties with new flags.

```sh
# Before upgrade
astro workspace create label=my-workspace

# After upgrade
astro workspace create --label=my-workspace
```

### `astro workspace create/update`: `--desc` flag has been renamed to `--description`

The flag for specifying a description for a Workspace has been renamed from `--desc` to `--description`.

```sh
# Before upgrade
astro workspace create label=my-workspace --desc="my description"

# After upgrade
astro workspace create --label=my-workspace --description="my description"
```

### `astro workspace user add`: User email is now specified as a flag

You must now specify a new user's email using the `--email` flag when running `astro workspace `

```sh
# Before upgrade
astro workspace user add email-to-add@astronomer.io --role WORKSPACE_VIEWER
# After upgrade
astro workspace user add --email email-to-add@astronomer.io --role WORKSPACE_VIEWER
```

### `astro deploy` Now accepts a Deployment ID instead of a release name

To deploy code to a specific Deployment without manually selecting a Deployment from a list, you must now specify that Deployment's ID instead of its release name when running `astro deploy`.

```sh
# Before upgrade
astro deploy <release-name>

# After upgrade
astro deploy <deployment-id>
```

### `astro workspace sa get` is now `astro workspace sa list`

```sh
# Before upgrade
astro workspace sa get
# After upgrade
astro workspace sa list
```

### `astro deployment/workspace sa create`: `--role` only accepts full role names

The `--role` flag now accepts either `WORKSPACE_EDITOR`, `WORKSPACE_ADMIN`, or `WORKSPACE_VIEWER`.

```sh
# Before upgrade
astro workspace sa create --role viewer

# After upgrade
astro workspace sa create --role WORKSPACE_VIEWER
```

### `astro deployment create/update` now takes all properties as flags

You must now specify a Deployment's properties using flags when you run `astro deployment create` or `astro deployment update`.

```sh
# Before upgrade
astro deployment create my-deployment --executor=local

# After upgrade
astro deployment create --label=my-deployment --executor=local
```

### `astro deployment user list` Now Takes Deployment ID as a Flag

To list users that have access to a specific Deployment, you must now use the `--deployment-id` flag when running `astro deployment user list`.

```sh
# Before upgrade
astro deployment user list <deployment-id>

# After upgrade
astro deployment user list --deployment-id=<deployment-id>
```

### `astro deployment user add`: `--email` flag is now required

You must now specify a user's email using the `--email` flag when running `astro deployment user add`.

```sh
# Before upgrade
astro deployment user add <email> --deployment-id=<deployment-id>

# After upgrade
astro deployment user add --email=<email> --deployment-id=<deployment-id>
```

### `astro deployment user delete` is now `astro deployment user remove`

```sh
# Before upgrade
astro deployment user delete <email> --deployment-id=<deployment-id>

# After upgrade
astro deployment user remove <email> --deployment-id=<deployment-id>
```

### `astro logs <component>` is now deprecated

The `astro logs` command has been removed. This command has been unavailable for the last several CLI releases. Use `astro dev logs` to view logs locally or `astro deployment logs <component>` to view logs for a Deployment hosted on Astronomer Software.

### `astro cluster list/switch` is now `astro context list/switch`

```sh
# Before upgrade
astro cluster list

# After upgrade
astro context list
```

### `astro deployment sa create`: `--system-sa` and `--user-id` are deprecated

The `--system-sa` and `--user-id` flags have been deprecated for `astro deployment sa create`. These flags have not been functional for the last several CLI versions.

### `astro dev init`: shortcut for `--airflow-version` is now `-a`

The shortcut for specifying an Astronomer Certified version for `astro dev init` has been changed from `-v` to `-a`.

```sh
# Before upgrade
astro dev init -v=2.3.0

# After upgrade
astro dev init -a=2.3.0
```
