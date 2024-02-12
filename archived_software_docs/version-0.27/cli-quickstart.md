---
title: "Astronomer CLI Quickstart"
sidebar_label: "Astronomer CLI Quickstart"
id: cli-quickstart
description: Establish a local testing environment and deploy to Astronomer Software from the CLI.
---

## Overview

Astronomer's [open source CLI](https://github.com/astronomer/astro-cli) is the easiest way to run Apache Airflow on your machine.

From the CLI, both Astronomer and non-Astronomer users can create a local Apache Airflow instance with a dedicated Webserver, Scheduler and Postgres Database. Once you initialize a project on Astronomer, you can easily customize your image (e.g. add Python or OS-level packages, plugins etc.) and push that image to run on your local machine.

If you're an Astronomer Software user, you might use the Astronomer CLI to do the following:

- Authenticate to Astronomer
- List Astronomer Workspaces and Deployments you have access to
- Deploy to an Airflow Deployment on Astronomer
- Create Astronomer Service Accounts, Users and Deployments
- Append annotations to your Deployment's Pods

This guide provides steps for installing the CLI, initializing an Astronomer project, and deploying to an Airflow instance on your local machine. For more information on specific CLI workflows and features, read the [Astronomer CLI Reference Guide](cli-reference.md).

## Prerequisites

The Astronomer CLI requires:

- [Docker](https://www.docker.com/) (v18.09 or higher).
- [Docker Engine](https://docs.docker.com/engine/) (v0.13.1 or higher).

Alternatively, you can run the CLI with Podman 3.1.0+. For more information, read [Run the CLI with Podman](https://docs.astronomer.io/astro/cli/use-podman).

## Step 1: Install the Astronomer CLI

There are two ways to install any version of the Astronomer CLI:

- [Homebrew](https://brew.sh/)
- cURL

> **Note:** Both methods only work for Unix (Linux+Mac) based systems. If you're running on Windows 10, follow [this guide](cli-install-windows-10.md) to get set up with Docker for WSL.

### Install with Homebrew

To install the latest supported version of the Astronomer CLI, run:

```sh
brew install astro@0.27.4
```

### Install with cURL

To install the latest supported version of the Astronomer CLI, run:

```sh
curl -sSL https://install.astronomer.io | sudo bash -s -- v0.27.4
```

#### Install the CLI on macOS Catalina+:

As of macOS Catalina, Apple [replaced bash with ZSH](https://www.theverge.com/2019/6/4/18651872/apple-macos-catalina-zsh-bash-shell-replacement-features) as the default shell. Our CLI install cURL command currently presents an incompatibility error with ZSH, sudo and the pipe syntax.

If you're running macOS Catalina and beyond, do the following:

1. Run `sudo -K` to reset/un-authenticate
2. Run the following to install the CLI properly:

```
curl -sSL https://install.astronomer.io | sudo bash -s < /dev/null
```

## Step 2: Confirm the Install

To make sure that you have the Astronomer CLI installed on your machine, run:

```bash
astro version
```

If the installation was successful, you should see the version of the CLI that you installed in the output:

```
Astro CLI Version: 0.27.0
Git Commit: c4fdeda96501ac9b1f3526c97a1c5c9b3f890d71
```

For a breakdown of subcommands and corresponding descriptions, you can always run `$ astro` or `$ astro --help`.

```
astro is a command line interface for working with the Astronomer Platform.

Usage:
  astro [command]

Available Commands:
  auth            Manage astronomer identity
  cluster         Manage Astronomer EE clusters
  completion      Generate autocompletions script for the specified shell (bash or zsh)
  config          Manage astro project configurations
  deploy          Deploy an airflow project
  deployment      Manage airflow deployments
  dev             Manage airflow projects
  help            Help about any command
  upgrade         Check for newer version of Astronomer CLI
  user            Manage astronomer user
  version         Astronomer CLI version
  workspace       Manage Astronomer workspaces

Flags:
  -h, --help   help for astro

Use "astro [command] --help" for more information about a command.
```

## Step 3: Initialize an Airflow Project

Once the Astronomer CLI is installed, the next step is to initialize an Airflow project on Astronomer. To do so:

1. Create a new directory on your machine by running the following command:

    ```sh
    mkdir <directory-name> && cd <directory-name>
    ```

2. Create the necessary project files in your new directory by running the following command:

    ```sh
    astro dev init
    ```

    This will generate the following files in that directory:
    ```py
    .
    ├── dags # Where your DAGs go
    │   └── example-dag.py # An example DAG that comes with the initialized project
    ├── Dockerfile # For Astronomer's Docker image and runtime overrides
    ├── include # For any other files you'd like to include
    ├── plugins # For any custom or community Airflow plugins
    ├── airflow_settings.yaml # For your Airflow Connections, Variables and Pools (local only)
    ├── packages.txt # For OS-level packages
    └── requirements.txt # For any Python packages
    ```

    These files make up the Docker image you'll then push to the Airflow instance on your local machine or to an Airflow Deployment on Astronomer Software.

## Step 4: Start Airflow Locally

You can now push your project to a local instance of Airflow. To do so:

1. Start Airflow on your local machine by running the following command in your project directory:

    ```
    astro dev start
    ```

    This command will spin up 3 Docker containers on your machine, each for a different Airflow component:

    - **Postgres:** Airflow's Metadata Database
    - **Webserver:** The Airflow component responsible for rendering the Airflow UI
    - **Scheduler:** The Airflow component responsible for monitoring and triggering tasks

2. Verify that all 3 Docker containers were created by running:

    ```
    docker ps
    ```

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with `admin` for both your Username and Password.

   You should also be able to access your Postgres Database at: `localhost:5432/postgres`. For guidelines on accessing your Postgres database both locally and on Astronomer, refer to the [Access Airflow Database](access-airflow-database.md) guide.

   > **Note**: Running `$ astro dev start` will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432.
   >
   > If you already have either of those ports allocated, you can either [stop existing docker containers](https://forum.astronomer.io/t/docker-error-in-cli-bind-for-0-0-0-0-5432-failed-port-is-already-allocated/151) or [change the port](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).

## Step 5: Authenticate to Astronomer

To authenticate to Astro via the Astronomer CLI, run:

```
astro auth login BASEDOMAIN
```

If you created your account with a username and password, you'll be prompted to enter them directly in your terminal. If you did so via Google or GitHub, you'll be prompted to grab a temporary token from the Software UI in your browser.

If you do not yet have an account on Astronomer, ask a Workspace Admin on your team to send you an invitation.

> **Note:** Once you run this command once, it should stay cached and allow you to just run `$ astro auth login` to authenticate more easily in the future.

## Apply Changes to your Airflow Project

As you develop locally, it's worth noting that some changes made to your image are automatically applied, while other changes made to a certain set of files require rebuilding your image in order for them to render.

### Code Changes

All changes made to the following files will be picked up as soon as they're saved to your code editor:

- `dags`
- `plugins`
- `include`

Once you save your changes, refresh the Airflow Webserver in your browser to see them render.

### Other Changes

All changes made to the following files require rebuilding your image:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

This includes changing the Airflow image in your `Dockerfile` and adding Python Packages to `requirements.txt` or OS-level packages to `packages.txt`.

To rebuild your image after making a change to any of these files, first run the following command:

```
astro dev stop
```

Then, restart the Docker containers by running:

```
astro dev start
```

> **Note:** As you develop locally, it may be necessary to reset your Docker containers and metadata DB for testing purposes. To do so, run [`astro dev kill`](cli-reference.md#astro-dev-kill) instead of [`astro dev stop`](cli-reference.md#astro-dev-stop) when rebuilding your image. This deletes all data associated with your local Postgres metadata database, including Airflow Connections, logs, and task history.

## Astronomer CLI and Platform Versioning

To ensure that you can continue to develop locally and deploy successfully, you should always upgrade to the latest minor version of the Astronomer CLI when you upgrade to the latest version of Astronomer. If you're on Astronomer v0.27+, for example, Astronomer CLI v0.27+ is required.

While upgrading to a new minor version of Astronomer requires upgrading the Astronomer CLI, subsequent patch versions will remain compatible. For instance, consider a system where Astronomer is on v0.27.2 and the Astronomer CLI is on v0.27.0. While we encourage users to always run the latest available version of all components, these patch versions of Astronomer and the Astronomer CLI remain compatible because they're both in the v0.27 series.

### Check Running Versions of Astronomer and the Astronomer CLI

To check your working versions of Astronomer (`Astro Server Version`) and the Astronomer CLI (`Astro CLI`), run:

```sh
astro version
```

This command will output something like the following:

```sh
$ astro version
Astro CLI Version: 0.27.0
Astro Server Version: 0.27.0
Git Commit: 748ca2e9de1e51e9f48f9d85eb8315b023debc2f
```

Here, the listed versions of Astronomer and the Astronomer CLI are compatible because they're both in the v0.27 series. If the minor versions for the two components do not match, you'll receive an error message in your command line with instructions to either upgrade or downgrade the Astronomer CLI accordingly. If you're running v0.16.10 of Astronomer and v0.27.0 of the Astronomer CLI, for example, you'll be instructed to downgrade the CLI to the latest in the v0.16 series. If you have access to more than one Astronomer Software installation, `Astro Server Version` will correspond to the `<base-domain>` that you're currently authenticated into.

For more information on Astronomer and Astronomer CLI releases, refer to:

* [CLI Release Changelog](https://github.com/astronomer/astro-cli/releases)
* [Astronomer Release Notes](release-notes.md)

## Next Steps

After installing and trying out the Astronomer CLI, we recommend reading through the following guides:

* [CLI Release Notes](cli-release-notes.md)
* [Astronomer CLI Reference Guide](cli-reference.md)
* [Deploy DAGs via the Astronomer CLI](deploy-cli.md)
* [Deploy DAGs via NFS Volume](deploy-nfs.md)
* [Customize Your Image](customize-image.md)
* [Upgrade Apache Airflow on Astronomer](manage-airflow-versions.md)
* [Deploy to Astronomer via CI/CD](ci-cd.md)

As always, don't hesitate to reach out to [Astronomer Support](https://support.astronomer.io/hc/en-us) or post in our [Astronomer Forum](https://forum.astronomer.io/) for additional questions.
