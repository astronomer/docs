---
sidebar_label: 'Release Notes'
title: 'Astro CLI Release Notes'
id: release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](cli/get-started.md). For general product release notes, go to [Astro Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to [Astronomer Support](https://support.astronomer.io).

## Astro CLI v1.2.0

Release date: June 13, 2022

### Additional improvements 

- This release includes changes exclusively for Astronomer Software.  

## Astro CLI v1.1.0

Release date: June 13, 2022

### Deployment API Keys Now Work with Deployment Commands

You can now run the following commands with a Deployment API key:

- `astro deploy`
- `astro deployment list`
- `astro deployment logs`
- `astro deployment update`
- `astro deployment delete`
- `astro deployment variable list`
- `astro deployment variable create`
- `astro deployment variable update`

Previously, you could run only the `astro deploy` command with a Deployment API key. For more information on API keys, see [Manage Deployment API Keys](api-keys.md).

### Easier Way to Determine Deployment ID on Deployment Commands

The Astro CLI now follows a new process to determine which Deployment to run a command against. Specifically:

- The Astro CLI first checks if a Deployment ID is specified as an argument to the command. For example, `astro deployment update <deployment-id>`.
- If not found, it checks for a Deployment ID in the `./astro/config.yaml` file of your Astro project. In this file, you can set up to one Deployment ID as default. This is an alternative to manually specifying it or using a Deployment API key.
- If only one Deployment exists in your Workspace, the CLI automatically runs the command for that Deployment without requiring that you specify its Deployment ID.
- If a Deployment API key is set as an OS-level environment variable on your machine or in a CI/CD pipeline, the CLI automatically runs the command for that Deployment without requiring a Deployment ID.
- If multiple Deployments exist in your Workspace and a Deployment API key is not found, the CLI will prompt you to select a Deployment from a list of all Deployments in that Workspace.
- If the Astro CLI doesn't detect a Deployment across your system, it will prompt you to create one.

These changes make it easier to run and automate Deployment-level commands with the Astro CLI. Most notably, it means that you no longer need to specify a Deployment ID in cases where it can be automatically implied by our system.

If your CI/CD pipelines currently define one or more Deployment IDs, you may remove those IDs and their corresponding environment variables as they are no longer required. For up-to-date CI/CD templates, see [Automate Code Deploys with CI/CD](ci-cd.md).

### Bug Fixes

- Fixed an issue where only Workspace Admins could create Deployments

## Astro CLI v1.0.1

Release date: June 6, 2022

### Bug Fixes

- Fixed an issue where `astro deploy`, `astro dev parse`, and `astro dev pytest` failed for some users

## Astro CLI v1.0.0

Release date: June 2, 2022

### A Shared CLI for All Astronomer Users

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

For Astro users, these are the only changes to existing CLI functionality. All other commands will continue to work as expected. We strongly recommend that all users upgrade. For instructions, see [Migrate from `astrocloud` to `astro`](cli/configure-cli.md#migrate-from-astrocloud-to-astro).

:::caution Possible Breaking Change

If you currently have CI/CD pipelines that install the `astrocloud` executable of the Astro CLI, we encourage you to update them to use the latest version of `astro` to ensure reliability. All `astrocloud` commands will continue to work for some time but will be deprecated by Astronomer soon.

For updated CI/CD examples, see [CI/CD](ci-cd.md).
:::


### New Command To Set Astro Project Configurations

You can now use `astro config get` and `astro config set` to retrieve and modify the configuration of your Astro project as defined in the `.astro/config.yaml` file. The configuration in this file contains details about how your project runs in a local Airflow environment, including your Postgres username and password, your Webserver port, and your project name.

For more information about these commands, see the [CLI Command Reference](cli/astro-config-set.md).

### New Command To Switch Between Astronomer Contexts

You can now use `astro context list` and `astro context switch` to show all the Astronomer contexts that you have access to and switch between them. An Astronomer context is defined as a base domain that you can use to access either Astro or an installation of Astronomer Software. A domain will appear as an available context if you have authenticated to it at least once.

This command is primarily for users who need to work in both Astro and Astronomer Software installations. If you're an Astro user with no ties to Astronomer Software, ignore this command. For more information, see the [CLI Command Reference ](cli/astro-context-switch.md).

For more information about these commands, see the [CLI Command Reference ](cli/astro-context-switch.md).

### Additional Improvements

- Astro CLI documentation has been refactored. You can now find all information about the CLI, including installation steps and the command reference, under the [Astro CLI tab](cli/overview.md).
- The nonfunctional `--update` flag has been removed from `astro deployment variable create`. To update existing environment variables for a given Deployment, use `astro deployment variable update` instead.

## v1.5.0 (`astrocloud`)

Release date: April 28, 2022

### New Command to Update Deployment Environment Variables

A new `astro deployment variable update` command allows you to more easily update an existing environment variable by typing a new value directly into your command line or adding the updated variable to a `.env` file.

This command replaces the `—update` flag that was previously released with the `astro deployment variable create` command. For more information, see the [Astro CLI Command Reference](cli/astro-deployment-variable-create.md).

### Additional Improvements

- When you run `astro workspace switch`, you can now specify a `<workspace-id>` as part of the command and avoid the prompt to manually select a Workspace
- You now need to provide an email address only the first time you run `astro login`. After you run that command once successfully, the Astro CLI will cache your email address in your `config.yaml` file and not prompt you to enter it again
- The `astro deploy` and `astro dev start` commands will now inform you if there is a new version of Astro Runtime available

### Bug Fixes

- Fixed an issue were the `astro deployment variable create —load` command would fail if the specified `.env` file had a comment (e.g. `#  <comment>`) in it
- Fixed an issue were Deployment API Keys would not work locally for some users

## v1.4.0 (`astrocloud`)

Release date: April 14, 2022

### New Command to Create and Update Environment Variables

`astro deployment variable create` is a new Astro CLI command that allows you to create and update [environment variables](environment-variables.md) for a Deployment on Astro. New environment variables can be loaded from a file (e.g. `.env`) or specified as inputs to the CLI command itself. If you already set environment variables [via a `.env` file locally](develop-project.md#set-environment-variables-via-env-local-development-only), this command allows you to set environment variables on Astro from that file as well. More generally, this command makes it easy to automate creating or modifying environment variables instead of setting them manually via the Cloud UI.

For more information about this command and its options, see the [Astro CLI Command Reference](cli/astro-deployment-variable-create.md).

### New Command to List and Save Deployment Environment Variables

You can now list existing environment variables for a given Deployment and save them to a local `.env` file with a new `astro deployment variable list` command. This command makes it easy to export existing environment variables for a given Deployment on Astro and test DAGs with them in a local Airflow environment.

For more information about this command and its options, see the [Astro CLI Command Reference](cli/astro-deployment-variable-list.md).

### Additional Improvements

- You can now specify a custom image name in your Astro project's `Dockerfile` as long as the image is based on an existing Astro Runtime image

## v1.3.4 (`astrocloud`)

Release date: April 11, 2022

### Additional Improvements

- Improved the performance of `astro dev start`
- When you successfully push code to a Deployment via `astro deploy`, the CLI now provides URLs for accessing the Deployment's Cloud UI and Airflow UI pages.

## v1.3.3 (`astrocloud`)

Release date: March 31, 2022

### Additional Improvements

- The `astro dev start` command should now be ~30 seconds faster
- When `astro dev parse` results in an error, the error messages now specify which DAGs they apply to
- If your DAGs don't pass the basic unit test that's included in your Astro project (`test_dag_integrity.py` ), running them with `astro dev pytest` will now provide more information about which part of your code caused an error

### Bug Fixes

- Fixed an issue where running `astro dev parse/pytest` would occasionally result in an "orphaned containers" warning
- Fixed an issue where `astro dev parse/pytest` would crash when parsing projects with a large number of DAGs
- Fixed an issue were some `docker-compose.override.yml` files would cause `astro dev parse/pytest` to stop working

## v1.3.2 (`astrocloud`)

Release date: March 17, 2022

:::info

Astro CLI 1.3.2 is a direct patch replacement for 1.3.1, which is no longer available for download because it includes a critical bug related to `astro dev parse/pytest`. If you are currently using Astro CLI 1.3.1, then we recommend upgrading to 1.3.2+ as soon as possible to receive important bug fixes.

:::

### Support for Identity-Based Login Flow

To better integrate with Astro's identity-based login flow, the CLI now prompts you for your login email after you run `astro login`. Based on your email, the CLI assumes your Astro Organization and automatically brings you to your Organization's login flow via web browser.

### Additional Improvements

- `astro deploy` now builds and tests only one image per deploy. This should result in improved deployment times in CI/CD pipelines which use this command.
- The `test` directory generated by `astro dev init` now includes more example pytests.

### Bug Fixes

- Partially fixed `dev parse` permission errors on WSL. To fully fix this issue for an Astro project, you must delete the project's existing `.astro` directory and rerun `astro dev init`.
- Fixed an issue where running `astro dev parse/pytest` while a local Airflow environment was running would crash the Airflow environment. This issue was introduced in Astro CLI 1.3.1, which is no longer available for download.

## v1.3.0 (`astrocloud`)

Release date: March 3, 2022

### New Command to Parse DAGs for Errors

`astro dev parse` is a new Astro CLI command that allows you to run a basic test against your Astro project to ensure that essential aspects of your code are properly formatted. This includes the DAG integrity test that is run with `astro dev pytest`, which checks that your DAGs are able to to render in the Airflow UI.

This command was built to replace the need to constantly run `astro dev restart` during troubleshooting to see if your DAGs render in the Airflow UI. Now, you can quickly run `astro dev parse` and see import and syntax errors directly in your terminal without having to restart all Airflow services locally. For more complex testing, we still recommend using `astro dev pytest`, which allows you to run other custom tests in your project.

For more information about `astro dev parse`, see the [CLI Command Reference](cli/astro-dev-parse.md). For more guidance on testing DAGs locally, see [Test DAGs Locally](test-and-troubleshoot-locally.md#test-dags-locally).

### `astro deploy` Parses DAGs by Default

To better protect your Deployments from unexpected errors, `astro deploy` now automatically applies tests from `astro dev parse` to your Astro project before completing the deploy process. If any of these tests fail, the CLI will not push your code to Astro.

For more information about `astro deploy`, see [CLI Command Reference](cli/astro-deploy.md).

:::danger Breaking Change

For Deployments running Astro Runtime 4.1.0+, `astro deploy` will no longer complete the code push to your Deployment if your DAGs contain basic errors. If any files in your Astro project contain these errors, then certain deploys might stop working after you upgrade the Astro CLI to v1.3.0.

To maintain the CLI's original behavior, use `astro deploy --force`. This command forces a deploy even if errors are detected in your DAGs.

:::

### New Command to Update Deployment Configurations

You can now use `astro deployment update` to update certain configurations for an existing Astro Deployment directly from the Astro CLI. The configurations that you can update are:

- Deployment name
- Deployment description
- Scheduler resources
- Scheduler replicas
- Worker resources

This is the same set of configurations that you can modify with the **Edit Configuration** view in the Cloud UI. For more information on modifying a Deployment, see [Configure a Deployment](configure-deployment-resources.md). For more information about this command, see [CLI Command Reference](cli/astro-deployment-update.md).

## v1.2.0 (`astrocloud`)

Release date: February 25, 2022

### Deploy to Astro with Deployment API Keys for Simpler CI/CD

You can now use [Deployment API keys](api-keys.md) to run `astro deploy` either from the CLI directly or via a CI/CD script. This update simplifies deploying code to Astro via CI/CD.

With an existing Deployment API key, you can set `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET` as OS-level environment variables. From there, you can now configure a CI/CD pipeline that:

- Installs the Astro CLI.
- Runs `astro deploy`.

When `astro deploy` is run, the CLI will now automatically look for and use the Deployment API key credentials that were set as environment variables to authorize and complete a code push.

Previously, any script that automated code pushes to Astro had to include a series of `cURL` requests to the Cloud API and could not use Deployment API keys to run an Astro CLI command. If your existing CI/CD pipelines still utilize this method, we recommend replacing those commands with an Astro CLI-based workflow. For more information and guiding examples, see [CI/CD](ci-cd.md).

### New Command to Run DAG Unit Tests with pytest

You can now run custom unit tests for all DAGs in your Astro project with `astro dev pytest`, a new Astro CLI command that uses [pytest](https://docs.pytest.org/en/7.0.x/index.html), a common testing framework for Python. As part of this change, new Astro projects created via `astro dev init` now include a `tests` directory, which includes one example pytest built by Astronomer.

When you run this command, the Astro CLI creates a local Python environment that includes your DAG code, dependencies, and Astro Runtime Docker image. The CLI then runs any pytests in the `tests` directory and shows you the results of those tests in your terminal. You can add as many custom tests to this directory as you'd like.

For example, you can use this command to run tests that check for:

- Python and Airflow syntax errors.
- Import errors.
- Dependency conflicts.
- Unique DAG IDs.

These tests don't require a fully functional Airflow environment in order to execute, which makes this Astro CLI command the fastest and easiest way to test DAGs locally.

In addition to running tests locally, you can also run pytest as part of the Astro deploy process. To do so, specify the `--pytest` flag when running `astro deploy`. This ensures that your code push to Astro automatically fails if any DAGs do not pass all pytests specified in the `tests` directory of your Astro project. For more information, see [Test DAGs Locally with pytest](test-and-troubleshoot-locally.md#test-dags-locally-with-pytest).

### New Command to View Deployment Scheduler Logs

If you prefer to troubleshoot DAGs and monitor your Deployments from the command line, you can now run `astro deployment logs`, a new Astro CLI command that allows you to view the same Scheduler logs that appear in the **Logs** tab of the Cloud UI.

When you run this command, all Scheduler logs emitted by a Deployment over the last 24 hours appear in your terminal. Similarly to the Cloud UI, you can filter logs by log level using command flags. For more information about this command, see the [CLI Command Reference](cli/astro-deployment-logs.md).

### New Commands to Create and Delete Deployments on Astro

You can now use the Astro CLI to create and delete Deployments on Astro with two new commands:

- `astro deployment create`
- `astro deployment delete`

These commands are functionally identical to the [Deployment configuration](configure-deployment-resources.md) and deletion process in the Cloud UI. For more information, see the [CLI Command Reference](cli/astro-deployment-create.md).

## v1.1.0 (`astrocloud`)

Release date: February 17, 2022

### New `astro dev restart` Command to Test Local Changes

For users making quick and continuous changes to an Astro project locally, the Astro CLI now supports a new `astro dev restart` command. This command makes local testing significantly easier and is equivalent to running `astro dev stop` followed by `astro dev start`.

### Support for the Triggerer in Local Airflow Environments

The Astro CLI now supports the Apache Airflow [Triggerer component](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html?) in a local environment. This means that you can test DAGs that use [deferrable operators](deferrable-operators.md) locally before pushing them to a Deployment on Astronomer. Additionally, Triggerer logs appear alongside Webserver and Scheduler logs when you run `astro dev logs`.

The Triggerer will only be created in local environments running Astro Runtime 4.0.0+.

### Additional Improvements

- Postgres has been upgraded from 12.2 to [12.6](https://www.postgresql.org/docs/12/release-12-6.html) for local Airflow environments.

## v1.0.0 (`astrocloud`)

Release date: February 3, 2022

### Introducing the Astro CLI

The Astro CLI (`astrocloud`) is now generally available as the official command-line tool for Astro. It is a direct replacement of the previously released `./astro` executable.

The Astro CLI sets the foundation for more robust functionality in the future and includes several significant improvements to both the local development experience as well as use cases specific to Astro. These changes are summarized in the following sections.

The Astro CLI can be installed via Homebrew. Commands take the form of:

```sh
astro <command> # E.g. `astro dev start`
```

We strongly recommend that all users install the Astro CLI and delete the `./astro` executable from local directories as soon as possible. For guidelines, read [Install the Astro CLI](cli/get-started.md). As of February 2022, `./astro` will no longer be maintained by our team. With that said, the release of the Astro CLI does not have any impact on your existing Deployments or DAGs.

### New Authentication Flow

The Astro CLI introduces an easy way to authenticate. Instead of requiring that users manually pass authentication tokens, the new CLI consists of a simple, browser-based login process.

Built with refresh tokens, the Astro CLI also does not require that users re-authenticate every 24 hours, as was the case with `./astro`. As long as you remain authenticated via the Cloud UI, your session via the Astro CLI will remain valid. You can expect to be asked to re-authenticate only once every few months instead of on a daily basis.

### Improved Local Development

Astro CLI v1.0.0 includes several improvements to the local development experience:

- You can now run `astrocloud dev start` with [Docker Buildkit](https://docs.docker.com/develop/develop-images/build_enhancements/) enabled. This resolves a [common issue](https://forum.astronomer.io/t/buildkit-not-supported-by-daemon-error-command-docker-build-t-airflow-astro-bcb837-airflow-latest-failed-failed-to-execute-cmd-exit-status-1/857) where users with Docker Buildkit enabled could not run this command.
- After running `astrocloud dev start`, the CLI no shows you the status of the Webserver container as it spins up on your local machine. This makes it easier to know whether the Airflow UI is unavailable because the Airflow Webserver container is still spinning up.

### Additional Improvements

- `astrocloud deploy` now shows a list of your Deployments in the order by which they were created instead of at random.

## v1.0.4 (`./astro`)

Release date: December 9, 2021

### Improved Example DAGs

The Astro CLI is built to enable developers to learn about, test, automate, and make the most of Apache Airflow both locally and on Astro. To that end, we've updated the CLI with two example DAGs that will be present for all users in the `/dags` folder that is automatically generated by `astro dev init`.

The file names are:
- `example-dag-basic.py`
- `example-dag-advanced.py`

The basic DAG showcases a simple ETL data pipeline and the advanced DAG showcases a series of more powerful Airflow features, including the TaskFlow API, jinja templating, branching and more. Both DAGs can be deleted at any time.

### Bug Fixes

Fixed a broken documentation link and outdated description in the `airflow_settings.yaml` file, which you can use to programmatically set Airflow Connections, Variables, and Pools locally.

## v1.0.3 (`./astro`)

Release date: November 5, 2021

- Bug Fix: Fixed an issue where users saw errors related to S3 in Webserver logs when running locally (e.g. `Failed to verify remote log exists s3:///`).

## v1.0.2 (`./astro`)
Release date: October 25, 2021

- Improved help text throughout the CLI

## v1.0.1 (`./astro`)

Release date: October 15, 2021

- This release contains changes exclusively related to the Astro CLI developer experience.

## v1.0.0 (`./astro`)

Release date: September 28, 2021

- Improvement: `./astro dev init` now always pulls the latest version of Astro Runtime for new projects. This means that you no longer have to upgrade the CLI in order to take advantage of a new Runtime release. Note that you still need to manually [upgrade Runtime](upgrade-runtime.md) for existing projects.
- Improvement: Updated error messages throughout the CLI to be more clear and useful

## v0.2.9-beta (`./astro`)

Release date: September 20, 2021

- Improvement: Bumped the default Astro Runtime version for new projects to [`3.0.2`](runtime-release-notes.md#astro-runtime-302)
- Improvement: You can now use `./astro dev run` to run Airflow CLI commands
- Improvement: You can now use `./astro dev logs` to show logs for the Airflow Scheduler and Webserver when developing locally

## v0.2.8-beta (`./astro`)

Release date: August 31, 2021

- Improvement: Bumped the default Astro Runtime version for new projects to [`3.0.0`](runtime-release-notes.md#astro-runtime-300)
- Improvement: Updated help text throughout the CLI
- Improvement: Projects created with `./astro dev init` now include a README file

## v0.2.7-beta (`./astro`)

Release date: July 31, 2021

- Bug Fix: Fixed an issue where users could not push DAGs to Deployments on Astro via the CLI.

## v0.2.6-beta (`./astro`)

Release date: July 30, 2021

- Improvement: You can now run `./astro login` without specifying a domain (`astronomer.io` is always assumed).
