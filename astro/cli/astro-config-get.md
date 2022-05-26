---
sidebar_label: "astro config get"
title: "astro config get"
id: astro-config-get
description: Reference documentation for astro config get.
---

## Description

View the current configuration of your Astro project as defined in the `.astro/config.yaml` file. The configuration in this file contains details about how your project runs in a local Airflow environment, including your Postgres username and password, your Webserver port, and your project name.

## Usage

Within your Astro project directory, run:

```sh
astro config get <option>
```

## Options

| Option              | Description                                                                             |
| ------------------- | --------------------------------------------------------------------------------------- |
| `cloud.api.protocol`  | The type of protocol to use when calling the Airflow API in a local Airflow environment |
| `cloud.api.port`      | The port to use when calling the Airflow API in a local environment                     |
| `context`           | The context for your Astro project                                                      |
| `local.registry`     | The location of your local Docker container running Airflow                             |
| `postgres.user`      | Your username for the local Airflow metadata database                                           |
| `postgres.password`  | Your password for the local Airflow metadata database                                              |
| `postgres.host`      | The host for the local Airflow metadata database                                                   |
| `postgres.port`      | The port for the local Airflow metadata database                                                    |
| `project.name`       | The name of your Astro project                                                       |
| `webserver.port`     | The port for the Webserver in your local Airflow environment                           |
| `show_warnings`      | Determines whether warning messages appear when starting up a local Airflow environment |

:::info

Some possible configurations are not documented here because they are used only on Astronomer Software.

:::

## Examples

```sh
## View the username for your project's postgres user
$ astro config get postgres.user
```

## Related Commands

- [astro config set](cli/astro-config-set.md)
