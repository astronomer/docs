---
sidebar_label: 'Configure the CLI'
title: 'Configure the Astro CLI'
id: configure-cli
toc_min_heading_level: 2
toc_max_heading_level: 2
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

| Option                  | Description                                                                                                                                                                                                                                        | Default value    | Valid values                                       |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------------------- |
| `airflow.expose_port`   | Determines whether to expose the webserver and postgres database of a local Airflow environment to all connected networks.                                                                                                                         | `false`          | `true`, `false`                                    |
| `cloud.api.protocol`    | The type of protocol to use when calling the Airflow API in a local Airflow environment.                                                                                                                                                           | `https`          | `http`, `https`                                    |
| `cloud.api.port`        | The port to use when calling the Airflow API in a local environment.                                                                                                                                                                               | `443`            | Any available port                                 |
| `cloud.api.ws_protocol` | The type of WebSocket (ws) protocol to use when calling the Airflow API in a local Airflow environment.                                                                                                                                            | `wss`            | `ws`, `wss`                                        |
| `context`               | The context for your Astro project.                                                                                                                                                                                                                | Empty string     | Any available [context](cli/astro-context-list.md) |
| `disable_astro_run`     | Determines whether to disable `astro run` commands and exclude `astro-run-dag` from any images built by the CLI.                                                                                                                                    | `false`          | `true`, `false`                                    |
| `local.registry`        | The location of your local Docker container running Airflow.                                                                                                                                                                                       | `localhost:5555` | Any available port                                 |
| `postgres.user`         | The username for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`       | Any string                                         |
| `postgres.password`     | The password for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`       | Any string                                         |
| `postgres.host`         | The hostname for the Postgres metadata database.                                                                                                                                                                                                   | `postgres`       | Any string                                         |
| `postgres.port`         | The port for the Postgres metadata database.                                                                                                                                                                                                       | `5432`           | Any available port                                 |
| `project.name`          | The name of your Astro project.                                                                                                                                                                                                                    | Empty string     | Any string                                         |
| `show_warnings`         | Determines whether warning messages appear when starting a local Airflow environment. For example, when set to `true`, you'll receive warnings when a new version of Astro Runtime is available and when your Astro project doesn't have any DAGs. | `true`           | `true`, `false`                                    |
| `skip_parse`            | Determines whether the CLI parses DAGs before pushing code to a Deployment.                                                                                                                                                                        | `false`          | `true`, `false`                                    |
| `upgrade_message`       | Determines whether a message indicating the availability of a new Astro CLI version displays in the Astro CLI.                                                                                                                                     | `true`           | `true`, `false`                                    |
| `webserver.port`        | The port for the webserver in your local Airflow environment.                                                                                                                                                                                      | `8080`           | Any available port                                 |

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


## Run the Astro CLI using Podman

The Astro CLI requires a container management engine to run Apache Airflow components on your local machine and deploy to Astro. For example, the `astro dev start` and `astro deploy` commands both require containers.

By default, the Astro CLI uses [Docker](https://www.docker.com/) as its container management engine. However, if your organization uses [Podman](https://podman.io/) to run and manage containers, you can configure the Astro CLI to use it instead. Podman is a secure, free, and open source alternative to Docker that doesn't require root access and orchestrates containers without using a centralized daemon.

<Tabs
    defaultValue="mac"
    groupId= "cli-podman"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'WSL2 on Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

Set up Podman on a Mac operating system so you can run Apache Airflow locally and deploy to Astro with Podman containers.

### Prerequisites

- Podman 3 or later. See [Getting started with Podman](https://podman.io/getting-started/).
- A running Podman machine with at least 4 GB of RAM. To confirm that Podman is running, run `podman ps`.
- If you use an M1 Mac, turn on rootful mode for Podman by using `podman machine set --rootful`.

:::tip

If you receive an error after running `podman ps`, there is likely a problem with your Podman connection. You might need to set the system-level `DOCKER_HOST` environment variable to be the location of your Podman service socket:

1. Run the following command to identify the connection URI for `podman-machine-default`:

    ```sh
    podman system connection ls
    ```
    
    The output should look like the following:
    
    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```
    
2. Copy the value in the `URI` column from `podman-machine-default*`. This is typically `unix:///run/podman/podman.sock`, but it can vary based on your installation.

3. Set your `DOCKER_HOST` environment variable to the value of the URI.

:::

### Setup

1. Run the following command to confirm that Podman has access to Astro images at `docker.io`:

    ```sh
    podman run --rm -it postgres:12.6 whoami
    ```

    If this command fails, use [Podman Desktop](https://podman-desktop.io/) to change Podman's default image registry location to `docker.io`. See [Provide pre-defined registries](https://podman-desktop.io/blog/podman-desktop-release-0.11#provide-pre-defined-registries-1201).

2. Run the following command to set Podman as your container management engine for the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    If you're using Podman 3, additionally run the following command:

    ```sh
    astro config set -g duplicate_volumes false
    ```

</TabItem>

<TabItem value="windows">

Set up Podman on Windows so you can run Apache Airflow locally and deploy to Astro with Podman containers.

### Prerequisites

- Podman 3 or later installed on Windows Subsystem for Linux version 2 (WSL 2) using Ubuntu 22.04 or later. See [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and [Getting started with Podman](https://podman.io/getting-started/).
- A running Podman machine with at least 4 GB of RAM. To confirm that Podman is running, run `podman ps` in your Linux terminal. 
- The Astro CLI Linux distribution installed on WSL 2. See [Install the Astro CLI on Linux](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli).

:::tip

If you receive an error after running `podman ps`, there is likely a problem with your Podman connection. You might need to set the system-level `DOCKER_HOST` environment variable to be the location of your Podman service socket:

1. In a WSL 2 terminal, run the following command to identify the connection URI for `podman-machine-default`:

    ```sh
    podman system connection ls
    ```
    
    The output should look like the following:
    
    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```
    
2. Copy the value in the `URI` column from `podman-machine-default*`. This is typically `unix:///run/podman/podman.sock`, but it can vary based on your installation.

3. Set your `DOCKER_HOST` environment variable to the value of the URI.

:::

### Setup

1. In a WSL 2 terminal, run the following command to confirm that Podman has access to Astro images at `docker.io`:

    ```sh
    podman run --rm -it postgres:12.6 whoami
    ```

    If this command fails, run the following command to change Podman's default image registry location to `docker.io`:

    ```sh
    cat << EOF | sudo tee -a /etc/containers/registries.conf.d/shortnames.conf
    "postgres" = "docker.io/postgres"
    EOF
    ```

2. Run the following command to set Podman as your container management engine for the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    If you're using Podman 3, additionally run the following command:

    ```sh
    astro config set -g duplicate_volumes false
    ```

</TabItem>

<TabItem value="linux">

Set up Podman on Linux so you can run Apache Airflow locally and deploy to Astro with Podman containers.

### Prerequisites

- Podman 3 or later. See [Getting started with Podman](https://podman.io/getting-started/).
- A running Podman machine with at least 4 GB of RAM. To confirm that Podman is running, run `podman ps`. 

:::tip

If you receive an error after running `podman ps`, there is likely a problem with your Podman connection. You might need to set the system-level `DOCKER_HOST` environment variable to be the location of your Podman service socket:

1. Run the following command to identify the connection URI for `podman-machine-default`:

    ```sh
    podman system connection ls
    ```
    
    The output should look like the following:
    
    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```
    
2. Copy the value in the `URI` column from `podman-machine-default*`. This is typically `unix:///run/podman/podman.sock`, but it can vary based on your installation.

3. Set your `DOCKER_HOST` environment variable to the value of the URI.

:::

### Setup

1. Run the following command to confirm that Podman has access to Astro images at `docker.io`:

    ```sh
    podman run --rm -it postgres:12.6 whoami
    ```

    If this command fails, run the following command to change Podman's default image registry location to `docker.io`:

    ```sh
    cat << EOF | sudo tee -a /etc/containers/registries.conf.d/shortnames.conf
    "postgres" = "docker.io/postgres"
    EOF
    ```

2. Run the following command to set Podman as your container management engine for the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    If you're using Podman 3, additionally run the following command:

    ```sh
    astro config set -g duplicate_volumes false
    ```

</TabItem>

</Tabs>

## Switch between Docker and Podman

After you set up the Astro CLI to use Podman on your local machine, the CLI automatically runs Podman containers whenever you run a command that requires them. To revert to the default behavior and run CLI commands in Docker containers, run the following command:

```sh
astro config set container.binary docker
```

If you need to switch back to using Podman again, run the following command:

```sh
astro config set container.binary podman
```
