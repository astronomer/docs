---
sidebar_label: "astro dev start"
title: "astro dev start"
id: astro-dev-start
description: Reference documentation for astro dev start.
---

## Description

Build your Astro project into a Docker image and spin up local a local Docker container for each Airflow component.

This command can be used to rebuild an Astro project and run it locally. For more information, read [Build and run a project locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev start
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-e`,`--env` | Path to your environment variable file. Default is `.env` | Valid filepaths |


## Examples

```sh
$ astro dev start --env=/users/username/documents/myfile.env
```

## Related Commands

- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
