---
sidebar_label: "astro config set"
title: "astro config set"
id: astro-config-set
description: Reference documentation for astro config set.
---

## Description

Update configurations for a locally hosted Astro project.

## Usage

Within your Astro project directory, run:

```sh
astro config set <option> <value>
```

## Options

| Option              | Description | Possible Values |
| ------------------- | ----------- | --------------- |
| `cloud.api.protocol`  | The type of protocol to use when calling the Airflow API in a local Airflow environment         | `http`, `https`             |
| `cloud.api.port`      | The port to use when calling the Airflow API in a local environment           | Any available port             |
| `context`           | The context for your Astro project          | Any available [context](cli/astro-context-list.md)             |
| `local.registry`     | The location of your local Docker container running Airflow             | Any available port             |
| `postgres.user`      | Your username for the Postgres metadata DB            | Any string             |
| `postgres.password`  | Your password for the Postgres metadata DB            | Any string             |
| `postgres.host`      | Your hostname for the Postgres metadata DB            | Any string             |
| `postgres.port`      | Your port for the Postgres metadata DB            | Any available port             |
| `project.name`       | The name of your Astro project         | Any string             |
| `webserver.port`     | The port for the Webserver in your local Airflow environment          | Any available port             |
| `show_warnings`      | Determines whether warning messages appear when starting up a local Airflow environment         | `true`, `false`             |

:::info

Some possible configurations are not documented here because they are used only on Astronomer Software.

:::

## Examples

```sh
## Set a username for your project's postgres user
$ astro config set postgres.user postgres
```

## Related Commands

- [astro config get](cli/astro-config-get.md)
