---
sidebar_label: "astrocloud dev restart"
title: "astrocloud dev restart"
id: astrocloud-dev-restart
description: Reference documentation for astrocloud dev restart.
---

## Description

Stop your Airflow environment, rebuild your Astronomer project into a Docker image, and restart your Airflow environment with the new Docker image.

This command can be used to rebuild an Astronomer project and run it locally. For more information, read [Develop and Run a Project Locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astrocloud dev restart
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-e`,`--env` | Path to your environment variable file. Default is `.env` | Valid filepaths |


## Examples

```sh
$ astrocloud dev restart --env=/users/username/documents/myfile.env
```

## Related Commands

- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud dev stop`](cli-reference/astrocloud-dev-stop.md)
- [`astrocloud dev kill`](cli-reference/astrocloud-dev-kill.md)
- [`astrocloud dev init`](cli-reference/astrocloud-dev-init.md)
- [`astrocloud dev run`](cli-reference/astrocloud-dev-run.md)
- [`astrocloud dev logs`](cli-reference/astrocloud-dev-logs.md)
