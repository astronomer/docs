---
sidebar_label: 'Astro CLI'
title: 'Astro CLI release notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.30.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, contact [Astronomer Support](https://support.astronomer.io).

## Astro CLI 1.6.1

Release date: November 3, 2022

### Bug fixes

- Fixed an issue where authenticating to Astronomer Software with `interactive=true` in your CLI configuration resulted in a 502 error.

## Astro CLI 1.6.0

Release date: September 28, 2022

### New commands to manage Airflow objects

You can use the new `astro dev object` commands to better manage Airflow connections, variables, and pools between your local testing environment and Astro Deployments.

- `astro dev object import` imports connections, variables, and pools from your Astro project `airflow_settings.yaml` into your locally running Airflow environment without restarting it.
- `astro dev object export` exports connections, variables, and pools from your local airflow database to a file of your choosing.

### Additional improvements

- You can now define connections in the `conn_extra` field of `airflow_settings.yaml` as YAML blocks instead of stringified JSON objects.
- The Astro CLI for Windows is now distributed as an `.exe` file.

### Bug fixes

- Fixed an issue where `astro dev start` did not properly load Airflow object configurations from `airflow_settings.yaml`
- Fixed an issue where `astro deployment user list` listed incorrect roles for some users

## Astro CLI 1.5.0

Release date: September 2, 2022

### New flags for paginating Workspace, Team, and user lists

You can now paginate longer lists of Workspaces, Teams, and users by using the `--paginated` flag with any of the following commands:

- `astro workspace user list`
- `astro workspace switch`
- `astro team list`

By default, paginated lists show 20 items per page. To change the number of items per page, set the `--page-list` flag.

To permanently set these flags, run the following commands:

```sh
# Always paginate lists when possible
astro config set -g interactive true
# Always show the specified number of items per page
astro config set -g page_size <page_size>
```

### Additional improvements

- You can now use the `--no-browser` flag with `astro dev start` to run Airflow on a browserless machine.
- You can now use the `--roles` flag with `astro team get` to see the role of that Team in each Workspace and Deployment it belongs to.
- You can now use the `--all` flag with `astro team get` to view all available information for each user in the Team.
- `astro dev restart` no longer automatically opens a browser tab with the Airflow UI.

## Astro CLI v1.4.0

Release date: August 18, 2022

### New command to run commands in local Airflow containers

You can now run bash commands in any locally running Airflow container using `astro dev bash`.

### New commands to manage Teams

Several new commands have been introduced to help you manage Teams on Astronomer Software.

#### Manage teams across a Software installation:

- `astro team get`: Get the information for an existing Team
- `astro team list`: View all Teams across an installation
- `astro team update`: Update a Team's permissions

#### Manage teams across a Workspace

- `astro workspace team add`: Add a Team to a given Workspace
- `astro workspace team remove`: Remove a Team from a given Workspace
- `astro workspace team update`: Update a Team's permissions for a given Workspace
- `astro workspace team list`: List all Teams in a given Workspace

#### Manage teams across a Deployment

- `astro deployment team add`: Add a Team to a given Deployment
- `astro deployment team remove`: Remove a Team from a given Deployment
- `astro deployment team update`: Update a Team's permissions for a given Deployment
- `astro deployment team list`: List all Teams in a Workspace

### Additional improvements

- If Docker isn't already running, the CLI automatically starts it after you run `astro dev start`. Note that this feature only works on Mac OS.
- The Airflow webserver now automatically opens in your default web browser after you run `astro dev start`.
