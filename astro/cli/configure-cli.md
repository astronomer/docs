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

| Option              | Description | Possible Values |
| ------------------- | ----------- | --------------- |
| `cloud.api.protocol`  | The type of protocol to use when calling the Airflow API in a local Airflow environment         | `http`, `https`             |
| `cloud.api.port`      | The port to use when calling the Airflow API in a local environment           | Any available port             |
| `cloud.api.ws_protocol`   | The type of WebSocket (ws) protocol to use when calling the Airflow API in a local Airflow environment           | `http`, `https`             |
| `cloud.api.token`    | The type of API token to use when calling the Airflow API in a local Airflow environment           | Any available API token             |
| `context`            | The context for your Astro project          | Any available [context](cli/astro-context-list.md)             |
| `contexts`           | The contexts for your Astro project          | Any available [context](cli/astro-context-list.md)             |
| `local.astrohub`     | The location of your local Astro project          | `http://localhost:8871/v1`             |
| `local.core`         | The location of your local Airflow scheduler          | `http://localhost:8888/v1alpha1`             |
| `local.public_astrohub`  | The location of your local, public Astro project          | `http://localhost:8871/graphql`             |
| `local.registry`     | The location of your local Docker container running Airflow             | Any available port             |
| `local.houston`      | The location of your local Houston API instance             | Any string             |
| `local.platform`      | The location of your local platform             | Any string             |
| `postgres.user`      | Your username for the Postgres metadata database            | Any string             |
| `postgres.password`  | Your password for the Postgres metadata database            | Any string             |
| `postgres.host`      | Your hostname for the Postgres metadata database            | Any string             |
| `postgres.port`      | Your port for the Postgres metadata database            | Any available port             |
| `project.name`       | The name of your Astro project         | Any string             |
| `project.workspace`       | The name of your Astro project workspace         | Any string             |
| `webserver.port`     | The port for the webserver in your local Airflow environment          | Any available port             |
| `show_warnings`      | Determines whether warning messages appear when starting a local Airflow environment         | `true`, `false`             |
| `verbosity`          | The verbosity or complexity of warning messages that appear when starting a local Airflow environment         | Any string             |
| `houston.dial_timeout`  | The time in minutes to wait until a Houston API call times out         | Any string             |
| `houston.skip_verify_tls`  | Determines whether Transport Layer Security (TLS) verification is ignored when executing a Houston API call         | `true`, `false`             |
| `skip_parse`  | Determines whether parsing is ignored when executing a Houston API call         | `true`, `false`             |
| `interactive`  | Determines whether parsing is interactive         | `true`, `false`             |
| `page_size`  | Determines the page size of the Astro CLI         | Any string             |
| `upgrade_message`  | Determines whether a message indicating the availability of an Astro CLI upgrade displays in the Astro CLI         | `true`, `false`             |
