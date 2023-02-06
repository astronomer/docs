---
sidebar_label: 'Configure the CLI'
title: 'Configure the Astro CLI'
id: configure-cli
---

<head>
  <meta name="description" content="Learn how to modify project-level settings by updating the .astro/config.yaml file. Modifying project-level settings can help you debug and troubleshoot the behavior of Airflow components in your local environment." />
  <meta name="og:description" content="Learn how to modify project-level settings by updating the .astro/config.yaml file. Modifying project-level settings can help you debug and troubleshoot the behavior of Airflow components in your local environment." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Every Astro project includes a file called `.astro/config.yaml` that supports various project-level settings, including:

- The name of your Astro project.
- The port for the Airflow webserver and Postgres metadata database.
- The username and password for accessing the Postgres metadata database.

In most cases, you only need to modify these settings in the case of debugging and troubleshooting the behavior of Airflow components in your local environment.

## Set a configuration

Run the following command in an Astro project:

```sh
astro config set <configuration-option> <value>
```

This command applies your configuration to `.astro/config.yaml` in your current Astro project. Configurations do not persist between Astro projects.

For example, to update the port of your local Airflow webserver to 8081 from the default of 8080, run:

```sh
astro config set webserver.port 8081
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

| Option              | Description | Default value | Valid values |
| ------------------- | ----------- | --------------- |---------------  |
| `cloud.api.protocol`  | The type of protocol to use when calling the Airflow API in a local Airflow environment.         | `https` |`http`, `https`             |
| `cloud.api.port`      | The port to use when calling the Airflow API in a local environment.           | `443` | Any available port             |
| `cloud.api.ws_protocol`   | The type of WebSocket (ws) protocol to use when calling the Airflow API in a local Airflow environment.           | `wss` | `ws`, `wss`             |
| `context`            | The context for your Astro project.          | Empty string | Any available [context](cli/astro-context-list.md)             |
| `local.registry`     | The location of your local Docker container running Airflow.             | `localhost:5555` | Any available port             |
| `postgres.user`      | The username for the Postgres metadata database.            | `postgres` | Any string             |
| `postgres.password`  | The password for the Postgres metadata database.            | `postgres` | Any string             |
| `postgres.host`      | The hostname for the Postgres metadata database.            | `postgres` |Any string             |
| `postgres.port`      | The port for the Postgres metadata database.            | `5432` | Any available port             |
| `project.name`       | The name of your Astro project.         | Empty string | Any string             |
| `show_warnings`      | Determines whether warning messages appear when starting a local Airflow environment. For example, when set to `true`, you'll receive warnings when a new version of Astro Runtime is available and when your Astro project doesn't have any DAGs.        | `true` | `true`, `false`             |
| `skip_parse`         | Determines whether the CLI parses DAGs before pushing code to a Deployment.         | `false` | `true`, `false`            | 
| `upgrade_message`    | Determines whether a message indicating the availability of a new Astro CLI version displays in the Astro CLI.         | `true` | `true`, `false`             |
| `webserver.port`     | The port for the webserver in your local Airflow environment.          | `8080` | Any available port             |

</TabItem>

<TabItem value="software">

| Option              | Description | Default value   | Valid values   |
| ------------------- | ----------- | --------------- | --------------- |
| `houston.dial_timeout`       |  The time in seconds to wait for a Houston connection.        | `10` |  Any integer           |
| `houston.skip_verify_tls`       |  Determines whether the Transport Layer Security (TLS) certificate is verified when connecting to Houston.       | `false` | `true`, `false`             |
| `interactive`        | Determines whether responses are paginated in the Astro CLI when pagination is supported.         | `false` |  `true`, `false`           |
| `page_size`          | Determines the size of the paginated response when `interactive` is set to `true`.                      | `20` | Any integer             |
| `postgres.user`      | The username for the Postgres metadata database.            | `postgres` | Any string             |
| `postgres.password`  | The password for the Postgres metadata database.            | `postgres` | Any string             |
| `postgres.host`      | The hostname for the Postgres metadata database.            | `postgres` | Any string             |
| `postgres.port`      | The port for the Postgres metadata database.            | `5432` | Any available port             |
| `project.name`       | The name of your Astro project.         | Empty string | Any string             |
| `show_warnings`      | Determines whether warning messages appear when starting a local Airflow environment. For example, when set to `true`, you'll receive warnings when a new version of Astro Runtime is available and when your Astro project doesn't have any DAGs.         | `true` | `true`, `false`             |
| `upgrade_message`    | Determines whether a message indicating the availability of a new Astro CLI version displays in the Astro CLI.        | `true` | `true`, `false`             |
| `verbosity`      | Determines the Astro CLI log level type.             | `warning` | `debug`, `info`, `warning`, `error`             |
| `webserver.port`     | The port for the webserver in your local Airflow environment.          |  `8080`| Any available port             |

</TabItem>
</Tabs>
