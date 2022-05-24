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
| `CloudAPIProtocol`  | The type of protocol to use when calling the Airflow API in a local Airflow environment         | `http`, `https`             |
| `CloudAPIPort`      | The port to use when calling the Airflow API in a local environment           | Any available port             |
| `Context`           | The context for your Astro project          | Any available [context](cli/astro-context-list.md)             |
| `LocalRegistry`     | The location of your local Docker container running Airflow             | Any available port             |
| `PostgresUser`      | Your username for the Postgres metadata DB            | Any string             |
| `PostgresPassword`  | Your password for the Postgres metadata DB            | Any string             |
| `PostgresHost`      | Your hostname for the Postgres metadata DB            | Any string             |
| `PostgresPort`      | Your port for the Postgres metadata DB            | Any available port             |
| `ProjectName`       | The name of your Astro project         | Any string             |
| `WebserverPort`     | The port for the Webserver in your local Airflow environment          | Any available port             |
| `ShowWarnings`      | Determines whether warning messages appear when starting up a local Airflow environment         | `true`, `false`             |

## Examples

```sh
## Set a username for your project's postgres user
$ astro config set PostgresUser postgres
```

## Related Commands

- [astro config get](cli/astro-config-get.md)
