---
sidebar_label: "Configure the CLI"
title: "Configure the Astro CLI"
id: configure-cli
toc_min_heading_level: 2
toc_max_heading_level: 2
description: "Learn how to modify project-level settings by updating the .astro/config.yaml file."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


Every Astro project includes a file called `.astro/config.yaml` that supports various project-level settings, including:

- The name of your Astro project.
- The port for the Apache Airflow® webserver and Postgres metadata database.
- The username and password for accessing the Postgres metadata database.

In most cases, you only need to modify these settings in the case of debugging and troubleshooting the behavior of Airflow components in your local environment.

## Set a configuration

You can set Astro configurations at two different scopes: global and project.

For project-specific configurations, Astro stores the settings in a file named `.astro/config.yaml` in your project directory. This file is generated when you run `astro dev init` in your project folder. Global configurations, however, are stored in a central location with the Astro executable. If a configuration is set in a project configuration file, it always overrides any of the same configuration in the global configuration file.

### Set project configurations

Run the following command in an Astro project to set a configuration for that project:

```sh
astro config set <configuration-option> <value>
```

This command applies your configuration to `.astro/config.yaml` in your current Astro project. Configurations do not persist between Astro projects.

For example, to update the port of your local Airflow webserver to 8081 from the default of 8080, run:

```sh
astro config set webserver.port 8081
```

### Set global configurations

Use the `--global` flag with `astro config set [option] --global` to set a configuration for all current and new Astro projects on your machine. Your global Astro CLI configuration is saved in a central location on your machine. For example, the configurations are stored in `~/.astro/config.yaml` on Mac OS and `/home//.astro/config.yaml` on Linux.

Note that you can override global configurations by setting a [project-level configuration](#set-project-configuration). If an Astro project contains an `.astro/config.yaml` file, any configuration values in that file take precedence over the same global configuration values.

The following example shows how to set the local Airflow webserver port to `8081` for all Astro projects on your local machine:

```sh
astro config set -g webserver.port 8081
```

## Available CLI configurations

:::info

The Astronomer product you're using determines the format and behavior of the configuration commands. Select one of the following tabs to change product contexts.

:::

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>
<TabItem value="astro">

| Option                  | Description                                                                                                                                                                                                                                                                                      | Default value        | Valid values                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------- | -------------------------------------------------- |
| `airflow.expose_port`   | Determines whether to expose the webserver and postgres database of a local Airflow environment to all connected networks.                                                                                                                                                                       | `false`              | `true`, `false`                                    |
| `cloud.api.protocol`    | The type of protocol to use when calling the Airflow API in a local Airflow environment.                                                                                                                                                                                                         | `https`              | `http`, `https`                                    |
| `cloud.api.port`        | The port to use when calling the Airflow API in a local environment.                                                                                                                                                                                                                             | `443`                | Any available port                                 |
| `cloud.api.ws_protocol` | The type of WebSocket (ws) protocol to use when calling the Airflow API in a local Airflow environment.                                                                                                                                                                                          | `wss`                | `ws`, `wss`                                        |
| `container.binary`      | The name of the container engine.                                                                                                                                                                                                                                                                | `docker`             | `docker` or `podman`                               |
| `context`               | The context for your Astro project.                                                                                                                                                                                                                                                              | Empty string         | Any available [context](cli/astro-context-list.md) |
| `disable_astro_run`     | Determines whether to disable `astro run` commands and exclude `astro-run-dag` from any images built by the CLI.                                                                                                                                                                                 | `false`              | `true`, `false`                                    |
| `disable_env_objects`   | Determines whether the Astro CLI pulls connections set in the Astro UI to your local environment. When set to `true`, connections are not pulled to the local environment. Set to `false` to import connections from the Astro UI for local development. Can be set globally with the `-g` flag. | `true`               | `true`, `false`                                    |
| `duplicate_volumes`     | Determines if the Astro CLI creates duplicate volumes when running Airflow locally.                                                                                                                                                                                                              | `true`               | `true` or `false`                                  |
| `local.registry`        | The location of your local Docker container running Airflow.                                                                                                                                                                                                                                     | `localhost:5555`     | Any available port                                 |
| `postgres.user`         | The username for the Postgres metadata database.                                                                                                                                                                                                                                                 | `postgres`           | Any string                                         |
| `postgres.password`     | The password for the Postgres metadata database.                                                                                                                                                                                                                                                 | `postgres`           | Any string                                         |
| `postgres.host`         | The hostname for the Postgres metadata database.                                                                                                                                                                                                                                                 | `postgres`           | Any string                                         |
| `postgres.port`         | The port for the Postgres metadata database.                                                                                                                                                                                                                                                     | `5432`               | Any available port                                 |
| `postgres.repository`   | Image repository to pull the Postgres image from                                                                                                                                                                                                                                                 | `docker.io/postgres` | Any Postgres image in a repository                 |
| `postgres.tag`          | The tag for your Postgres image                                                                                                                                                                                                                                                                  | `12.6`               | Any valid image tag                                |
| `project.name`          | The name of your Astro project.                                                                                                                                                                                                                                                                  | Empty string         | Any string                                         |
| `show_warnings`         | Determines whether warning messages appear when starting a local Airflow environment. For example, when set to `true`, you'll receive warnings when a new version of Astro Runtime is available and when your Astro project doesn't have any DAGs.                                               | `true`               | `true`, `false`                                    |
| `skip_parse`            | Determines whether the CLI parses DAGs before pushing code to a Deployment.                                                                                                                                                                                                                      | `false`              | `true`, `false`                                    |
| `upgrade_message`       | Determines whether a message indicating the availability of a new Astro CLI version displays in the Astro CLI.                                                                                                                                                                                   | `true`               | `true`, `false`                                    |
| `webserver.port`        | The port for the webserver in your local Airflow environment.                                                                                                                                                                                                                                    | `8080`               | Any available port                                 |

</TabItem>

<TabItem value="software">

| Option                    | Description                                                                                                                                                                                                                                        | Default value | Valid values                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ----------------------------------- |
| `houston.dial_timeout`    | The time in seconds to wait for a Houston connection.                                                                                                                                                                                              | `10`          | Any integer                         |
| `houston.skip_verify_tls` | Determines whether the Transport Layer Security (TLS) certificate is verified when connecting to Houston.                                                                                                                                          | `false`       | `true`, `false`                     |
| `interactive`             | Determines whether responses are paginated in the Astro CLI when pagination is supported.                                                                                                                                                          | `false`       | `true`, `false`                     |
| `page_size`               | Determines the size of the paginated response when `interactive` is set to `true`.                                                                                                                                                                 | `20`          | Any integer                         |
| `postgres.user`           | The username for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`    | Any string                          |
| `postgres.password`       | The password for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`    | Any string                          |
| `postgres.host`           | The hostname for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`    | Any string                          |
| `postgres.port`           | The port for the Postgres metadata database.                                                                                                                                                                                                       | `5432`        | Any available port                  |
| `project.name`            | The name of your Astro project.                                                                                                                                                                                                                    | Empty string  | Any string                          |
| `show_warnings`           | Determines whether warning messages appear when starting a local Airflow environment. For example, when set to `true`, you'll receive warnings when a new version of Astro Runtime is available and when your Astro project doesn't have any DAGs. | `true`        | `true`, `false`                     |
| `upgrade_message`         | Determines whether a message indicating the availability of a new Astro CLI version displays in the Astro CLI.                                                                                                                                     | `true`        | `true`, `false`                     |
| `verbosity`               | Determines the Astro CLI log level type.                                                                                                                                                                                                           | `warning`     | `debug`, `info`, `warning`, `error` |
| `webserver.port`          | The port for the webserver in your local Airflow environment.                                                                                                                                                                                      | `8080`        | Any available port                  |

</TabItem>
</Tabs>


