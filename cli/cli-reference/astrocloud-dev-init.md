---
sidebar_label: "astrocloud dev init"
title: "astrocloud dev init"
id: astrocloud-dev-init
description: Reference documentation for astrocloud dev init.
---

## Description

Initialize an [Astro project](create-project.md) in an empty local directory. An Astro project contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. An Astro project can be either run locally with `astro dev start` or pushed to Astronomer via `astro deploy`.

## Usage

```sh
astrocloud dev init
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-v`, `runtime-version` | Initialize a project with a specific Runtime version | Any supported Runtime version |
| `-n`,`--name`            | Name of your Astronomer project                                                                                    | Any string                  |

## Examples

```sh
$ astrocloud dev init
# Initialized default project
$ astrocloud dev init --name=MyProject
# Generated `config.yaml` file with `name=MyProject`
$ astrocloud dev init --runtime-version=4.0.7
## Initialized project with Runtime 4.0.7
```

## Related Commands

- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud dev stop`](cli-reference/astrocloud-dev-stop.md)
- [`astrocloud dev init`](cli-reference/astrocloud-dev-init.md)
- [`astrocloud dev run`](cli-reference/astrocloud-dev-run.md)
- [`astrocloud dev logs`](cli-reference/astrocloud-dev-logs.md)
