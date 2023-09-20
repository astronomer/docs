---
sidebar_label: "astro dev init"
title: "astro dev init"
id: astro-dev-init
description: Initialize an Astro project to run a local Airflow environment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/docs/term-icon.png' }
---

Initialize an [Astro project](develop-project.md#create-an-astro-project) in an empty local directory. An Astro project contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. An Astro project can be either run locally with `astro dev start` or pushed to Astronomer with `astro deploy`.

## Usage

```sh
astro dev init
```

## Options

| Option                       | Description                                                                                       | Possible Values               |
| ---------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------- |
| `-v`, `--runtime-version`    | Initialize a project with a specific Runtime version                                              | Any supported Runtime version |
| `-n`,`--name`                | Name of your Astro project                                                                        | Any string                    |
| `--use-astronomer-certified` | Only for use on Astronomer Software. Initializes your project with an Astronomer Certified image. | None                          |

## Examples

```sh
$ astro dev init
# Initializes default project

$ astro dev init --name=MyProject
# Generates `config.yaml` file with `name=MyProject`

$ astro dev init --runtime-version=4.0.7
## Initializes project with Runtime 4.0.7
```

## Related Commands

- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
