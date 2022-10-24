---
sidebar_label: 'Configure the CLI'
title: 'Configure the Astro CLI'
id: configure-cli
description: Make changes to your project and local Apache Airflow environment with the Astro CLI.
---

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
astro config set <configuration> <value>
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
| `context`           | The context for your Astro project          | Any available [context](cli/astro-context-list.md)             |
| `local.registry`     | The location of your local Docker container running Airflow             | Any available port             |
| `postgres.user`      | Your username for the Postgres metadata database            | Any string             |
| `postgres.password`  | Your password for the Postgres metadata database            | Any string             |
| `postgres.host`      | Your hostname for the Postgres metadata database            | Any string             |
| `postgres.port`      | Your port for the Postgres metadata database            | Any available port             |
| `project.name`       | The name of your Astro project         | Any string             |
| `webserver.port`     | The port for the webserver in your local Airflow environment          | Any available port             |
| `show_warnings`      | Determines whether warning messages appear when starting up a local Airflow environment         | `true`, `false`             |
