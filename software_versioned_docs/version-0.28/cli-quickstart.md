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

Alternatively, you can run the CLI with Podman 3.1.0+. For more information, read [Run the CLI with Podman](cli-podman.md).

## Step 1: Install the Astronomer CLI

There are two ways to install any version of the Astronomer CLI:

- [Homebrew](https://brew.sh/)
- cURL

> **Note:** Both methods only work for Unix (Linux+Mac) based systems. If you're running on Windows 10, follow [this guide](cli-install-windows-10.md) to get set up with Docker for WSL.

### Install with Homebrew

If you have Homebrew installed, run:

```sh
brew install astronomer/tap/astro
```

To install a specific version of the Astronomer CLI, you'll have to specify `@major.minor.patch`. To install v0.27.0, for example, run:

```sh
brew install astronomer/tap/astro@0.27.0
```

### Install with cURL

To install the latest version of the Astronomer CLI, run:

```
curl -sSL https://install.astronomer.io | sudo bash
```

To install a specific version of the Astronomer CLI, specify `-s -- major.minor.patch` as a flag at the end of the cURL command. To install v0.27.0, for example, run:

```
curl -sSL https://install.astronomer.io | sudo bash -s -- v0.27.0
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
Astronomer CLI Version: 0.27.0
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

## Astronomer CLI and Platform Versioning

To ensure that you can continue to develop locally and deploy successfully, you should always upgrade to the latest minor version of the Astronomer CLI when you upgrade to the latest version of Astronomer. If you're on Astronomer v0.27+, for example, Astronomer CLI v0.27+ is required.

While upgrading to a new minor version of Astronomer requires upgrading the Astronomer CLI, subsequent patch versions will remain compatible. For instance, consider a system where Astronomer is on v0.27.2 and the Astronomer CLI is on v0.27.0. While we encourage users to always run the latest available version of all components, these patch versions of Astronomer and the Astronomer CLI remain compatible because they're both in the v0.27 series.

### Check Running Versions of Astronomer and the Astronomer CLI

To check your working versions of Astronomer (`Astro Server Version`) and the Astronomer CLI (`Astronomer CLI`), run:

```sh
astro version
```

This command will output something like the following:

```sh
$ astro version
Astronomer CLI Version: 0.27.0
Astro Server Version: 0.27.0
Git Commit: 748ca2e9de1e51e9f48f9d85eb8315b023debc2f
```

Here, the listed versions of Astronomer and the Astronomer CLI are compatible because they're both in the v0.27 series. If the minor versions for the two components do not match, you'll receive an error message in your command line with instructions to either upgrade or downgrade the Astronomer CLI accordingly. If you're running v0.16.10 of Astronomer and v0.27.0 of the Astronomer CLI, for example, you'll be instructed to downgrade the CLI to the latest in the v0.16 series. If you have access to more than one Astronomer Software installation, `Astro Server Version` will correspond to the `<base-domain>` that you're currently authenticated into.

## Next Steps

After installing and trying out the Astronomer CLI, we recommend reading through the following guides:

* [CLI Release Notes](cli-release-notes.md)
* [Create a Project](create-project.md)
* [Astronomer CLI Reference Guide](cli-reference.md)
* [Deploy DAGs via the Astronomer CLI](deploy-cli.md)
