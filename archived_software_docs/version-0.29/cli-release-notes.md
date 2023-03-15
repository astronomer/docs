---
sidebar_label: 'Astro CLI'
title: 'Astro CLI release notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.29.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, contact [Astronomer Support](https://support.astronomer.io).

## Astro CLI v1.3.1

Release date: July 19, 2022

### Additional improvements

- Added support for building Runtime images locally on different system architectures, which eliminates the need for the build process to run in an emulation and improves the performance of `astro dev start`

## Astro CLI v1.3.0

Release date: July 19, 2022

### Deploy code to a custom image registry

You can now use the Astro CLI to build and deploy an image to a custom image registry. Based on the Helm configurations in your Kubernetes cluster, the Astro CLI automatically detects your custom image registry and pushes your image to it. It then calls the Houston API to update your Deployment to pull the new image from the registry.

For more information, see [Configure a custom registry for Deployment images](custom-image-registry.md).

### Additional improvements

- Upgraded the CLI to Go version 1.18, which includes improvements to both performance and the development experience. See the [Go Blog](https://go.dev/blog/go1.18).
- The CLI now provisions a triggerer when you create a Deployment using `astro deployment create`.

## Astro CLI v1.2.0

Release date: June 27, 2022

### A Shared CLI for All Astronomer Users

:::danger Breaking Change

Astro CLI v1.2.0 includes breaking changes that might effect your existing CI/CD pipelines. Before upgrading the CLI, carefully read through [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md) to learn more about these breaking changes and how they can affect your pipelines.

:::

The Astro CLI is now a single CLI executable built for all Astronomer products. This new generation of the Astro CLI is optimized for a consistent local development experience and provides more ways to interact with your Software Deployments. For organizations moving from Astronomer Software to [Astro](https://docs.astronomer.io/astro), this change makes the transition easier.

To establish a shared framework between products, the syntax of several Software CLI commands have been updated. Due to the quantity of these changes, all changes introduced in this release are documented in [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md).

### New Command To Switch Between Astronomer Installations

You can now use `astro context list` and `astro context switch` to show the Astronomer contexts that you can access and assume. An Astronomer context is a base domain that relates to either Astro or a particular Cluster on Astronomer Software. A domain appears as an available context if you have authenticated to it at least once.

These commands are intended for users who need to work across multiple Astronomer Software clusters or installations. They replace `astro cluster list` and `astro cluster switch`, respectively. For more information, see the [CLI Command Reference](cli-reference.md#astro-context-switch).

## Astro CLI v0.29.1

Release date: July 12, 2022

### Bug fixes

- Fixed an issue where `astro deploy` did not work when using Podman 4.0+

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
