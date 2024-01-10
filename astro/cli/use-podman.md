---
sidebar_label: "Use Podman"
title: "Run the Astro CLI using Podman"
id: use-podman
toc_min_heading_level: 2
toc_max_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

The Astro CLI requires a container management engine to run Apache Airflow components on your local machine and deploy to Astro. For example, the `astro dev start` and `astro deploy` commands both require containers.

By default, the Astro CLI uses [Docker](https://www.docker.com/) as its container management engine. However, if your organization uses [Podman](https://podman.io/) to run and manage containers, you can configure the Astro CLI to use it instead. Podman is a secure, free, and open source alternative to Docker that doesn't require root access and orchestrates containers without using a centralized daemon.

## Configure the Astro CLI to use Podman

<Tabs
defaultValue="mac"
groupId= "configure-the-astro-cli-to-use-podman"
values={[
{label: 'Mac', value: 'mac'},
{label: 'WSL2 on Windows', value: 'windows'},
{label: 'Linux', value: 'linux'},
]}>
<TabItem value="mac">

Set up Podman on a Mac operating system so you can run Apache Airflow locally and deploy to Astro with Podman containers.

### Prerequisites

- Podman 3 or later. See [Getting started with Podman](https://podman.io/get-started/).
- A running Podman machine with at least 4 GB of RAM. To confirm that Podman is running, run `podman ps`.
- (M1 MacOS) Turn on rootful mode for Podman by using `podman machine set --rootful`. A [Podman bug](https://github.com/containers/podman/issues/15976) currently causes issues with volumes when running in rootless mode on M1.

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

- Podman 3 or later installed on Windows Subsystem for Linux version 2 (WSL 2) using Ubuntu 22.04 or later. See [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and [Getting started with Podman](https://podman.io/get-started/).
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

- Podman 3 or later. See [Getting started with Podman](https://podman.io/get-started/).
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

### Troubleshoot your Podman configuration

The following error can sometimes occur when the CLI tries to build your Astro Runtime image using Podman:

```bash
WARN[0010] SHELL is not supported for OCI image format, [/bin/bash -o pipefail -e -u -x -c] will be ignored. Must use `docker` format
```

To resolve this issue, run the following command to set the `BUILDAH_FORMAT` environment variable on your machine:

```dockerfile
export BUILDAH_FORMAT=docker
```

## Switch between Docker and Podman

After you set up the Astro CLI to use Podman on your local machine, the CLI automatically runs Podman containers whenever you run a command that requires them. To revert to the default behavior and run CLI commands in Docker containers, run the following command:

```sh
astro config set container.binary docker
```

If you need to switch back to using Podman again, run the following command:

```sh
astro config set container.binary podman
```