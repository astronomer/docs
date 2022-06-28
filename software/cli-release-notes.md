---
sidebar_label: 'Astro CLI'
title: 'Astro CLI release notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.29.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer support](https://support.astronomer.io).

## Astro CLI v0.29

Release date: June 1, 2022

### Create New Projects With Astro Runtime images

`astro dev init` now initializes Astro projects with the latest Astro Runtime image by default. To use a specific Runtime version, run:

```sh
astro dev init --runtime-version <runtime-version>
```

If you want to continue using Astronomer Certified images in your new Astro projects, specify the new `--use-astronomer-certified` flag:

```sh
astro dev init --use-astronomer-certified
```

For more information about Runtime vs. Certified, see [Differences Between Astro Runtime and Astronomer Certified](image-architecture.md#differences-between-astronomer-runtime-and-astronomer-certified)

### Create Software Deployments with Astro Runtime

To support running Astro Runtime images on Astronomer Software Deployments, you can now specify a Runtime image version when creating new deployments using `astro deployment create`. To do so, run:

```sh
astro deployment create <flags> --runtime-version=<your-runtime-version>
```

### Migrate Existing Software Deployments to Runtime

The Astro CLI includes a new command for migrating existing Software Deployments from Astronomer Certified to Astro Runtime. To initiate the process for migrating a Software Deployment to a Runtime image, run:

```sh
astro deployment runtime migrate --deployment-id=<deployment-id>
```

For more information, see the [CLI Reference Guide](cli-reference.md#astro-deployment-runtime-migrate).

### Upgrade a Deployment's Runtime Version

The Astro CLI includes a new command for upgrading existing Software Deployments to a newer version of Runtime. To upgrade a Software Deployment runtime image, run:

```sh
astro deployment runtime upgrade --deployment-id=<deployment-id> --desired-runtime-version=<desired-runtime-version>
```

For more information, see the [CLI Reference Guide](cli-reference.md#astro-deployment-runtime-upgrade).

### Additional improvements

- When running `astro dev start`, the containers running Airflow components now include your project directory in their names.
