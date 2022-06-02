---
sidebar_label: 'Astro CLI'
title: 'Astro CLI Release Notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.28.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer Support](https://support.astronomer.io).

<<<<<<< HEAD
## Astro CLI v0.29
=======
## Astro CLI v1.0.0

Release date: May 27, 2022

### A Shared CLI for All Astronomer Users

:::danger Breaking Change

Astro CLI v1.0.0 includes breaking changes that might effect your existing CI/CD pipelines. Before upgrading the CLI, carefully read through [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md) to learn more about these breaking changes and how they can affect your pipelines.

:::

The Astro CLI is now a single CLI executable built for all Astronomer products. This new generation of the Astro CLI is optimized for a consistent local development experience and provides more value to Astronomer Software customers. For organizations moving from Astronomer Software to [Astro](https://docs.astronomer.io/astro), this change makes the transition easier.

To establish a shared framework between products, the syntax of several Software CLI commands have been updated. Due to the quantity of these changes, all changes introduced in this release are documented in [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md). Astro CLI v1.0.0 is only compatible with Astronomer Software v0.28+.

### New Command To Switch Between Astronomer Installations

You can now use `astro context list` and `astro context switch` to show the Astronomer contexts that you can access and assume. An Astronomer context is a base domain that relates to either Astro or a particular Cluster on Astronomer Software. A domain appears as an available context if you have authenticated to it at least once.

These commands are intended for users who need to work across multiple Astronomer Software clusters or installations. They replace `astro cluster list` and `astro cluster switch`, respectively. For more information, see the [CLI Command Reference](cli-reference.md#astro-context-switch).

## 0.28.1
>>>>>>> 8445cc750d723feb84c890690df714b758506a85

Release date: June 1, 2022

### Create New Projects With Astro Runtime Images

`astro dev init` now initializes Astro projects with the latest Astro Runtime image by default. To use a specific Runtime version, you can run:

```sh
astro dev init --runtime-version <runtime-version>
```

If you want to continue using Astronomer Certified images in your new Astro projects, specify the new `--use-astronomer-certified` flag:

```sh
astro dev init --use-astronomer-certified
```

### Create Software Deployments with Astro Runtime

To support running Astro Runtime images on Astronomer Software Deployments, you can now specify a Runtime image version when creating new deployments using `astro deployment create`. To do so, you can run:

```sh
astro deployment create <flags> --runtime-version <your-runtime-version>
```

### Migrate Existing Software Deployments to Runtime

The Astro CLI includes a new command for migrating existing Software Deployments from Astronomer Certified to Astro Runtime. To initiate the process for migrating a Software Deployment to a Runtime image, you can run:

```sh
astro deployment runtime migrate --deployment-id=<deployment-id>
```

### Upgrade a Deployment's Runtime Version

The Astro CLI includes a new command for upgrading existing Software Deployments from one an older version of Runtime to a newer version. To initiate the process for upgrading a Software Deployment's runtime image, you can run:

```sh
astro deployment runtime upgrade --deployment-id=<deployment-id> --desired-runtime-version=<desired-runtime-version>
```

### Additional Improvements

- `astro deployment list` now shows each Deployment's image version.
- When running `astro dev start`, the containers running Airflow components now include your project directory in their names.
