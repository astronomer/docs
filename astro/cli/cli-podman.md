---
sidebar_label: 'Run the CLI with Podman'
title: 'Run the Astro CLI in Podman containers'
id: cli-podman
description: Use Podman instead of Docker to run specific Astro CLI commands.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

If your Organization is already using [Podman](https://podman.io/) to run and manage containers, you can use it to run Airflow locally and deploy to Astronomer using the Astro CLI.

<Tabs
    defaultValue="mac"
    groupId= "cli-podman"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

Set up Podman on a Mac operating system so you can run the Astro CLI in Podman containers.

### Prerequisites

- A running instance of Podman 3 or later on your local machine. You can confirm that Podman is running using `podman ps`.

If you're interested in running a different version of Podman that's unsupported, contact [Astronomer support](https://cloud.astronomer.io/support).

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

2. Run the following command to pick up the Identity and connection URI for your `podman-machine-default`:

    ```sh
    podman system connection ls
    ```

    The output should look like the following:

    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```

    Copy the `Identity` and `URI` from `podman-machine-default*` for the next two steps.

3. Run the following command to set the connection URI from the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    Additionally run the following command if you're using Podman 3:

    ```sh
    astro config set -g duplicate_volumes false
    ```

</TabItem>

<TabItem value="windows">

Set up Podman on Windows so you can run the Astro CLI in Podman containers.

### Prerequisites

- A running instance of Podman 3 or later on Windows Subsystem for Linux version 2 (WSL 2) using Ubuntu 22.04 or later. You can confirm that Podman is running using `podman ps`.

If you're interested in running a different version of Podman that's unsupported, contact [Astronomer support](https://cloud.astronomer.io/support).

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

2. Run the following command to pick up the Identity and connection URI for your `podman-machine-default`:

    ```sh
    podman system connection ls
    ```

    The output should look like the following:

    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```

    Copy the `Identity` and `URI` from `podman-machine-default*` for the next two steps.

3. Run the following command to set the connection URI from the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    Additionally run the following command if you're using Podman 3:

    ```sh
    astro config set -g duplicate_volumes false
    ```

</TabItem>

<TabItem value="linux">

Set up Podman on Linux so you can run the Astro CLI in Podman containers.

### Prerequisites

- A running instance of Podman 3 or later on Ubuntu 22.04 or later. You can confirm that Podman is running using `podman ps`.

If you're interested in running a different version of Podman that's unsupported, contact [Astronomer support](https://cloud.astronomer.io/support).

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

2. Run the following command to pick up the Identity and connection URI for your `podman-machine-default`:

    ```sh
    podman system connection ls
    ```

    The output should look like the following:

    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```

    Copy the `Identity` and `URI` from `podman-machine-default*` for the next two steps.

3. Run the following command to set the connection URI from the Astro CLI:

    ```sh
    astro config set -g container.binary podman
    ```

    Additionally run the following command if you're using Podman 3:

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
