---
sidebar_label: "astro dev init"
title: "astro dev init"
id: astro-dev-init
description: Reference documentation for astro dev init.
---

## Description

Initialize an [Astro project](create-project.md) in an empty local directory. An Astro project contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. An Astro project can be either run locally with `astro dev start` or pushed to Astronomer via `astro deploy`.

## Usage

```sh
astro dev init
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-v`, `runtime-version` | Initialize a project with a specific Runtime version | Any supported Runtime version |
| `-n`,`--name`            | Name of your Astronomer project                                                                                    | Any string                  |
| `--use-astronomer-certified`            | Only for use on Astronomer Software. Initializes your project with an Astronomer Certified image.                                                 | ``                 |

## Examples

```sh
$ astro dev init
# Initialized default project
$ astro dev init --name=MyProject
# Generated `config.yaml` file with `name=MyProject`
$ astro dev init --runtime-version=4.0.7
## Initialized project with Runtime 4.0.7
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
