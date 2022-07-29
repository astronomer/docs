---
sidebar_label: 'Astro CLI'
title: 'Astro CLI Release Notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.28.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer Support](https://support.astronomer.io).

## Astro CLI v1.1.0

Release date: June 13, 2022

### Additional improvements

- This release exclusively contains changes for [Astro users](https://docs.astronomer.io/astro/cli/release-notes).

## Astro CLI v1.0.0

Release date: June 2, 2022

### A Shared CLI for All Astronomer Users

:::danger Breaking Change

Astro CLI v1.0.0 includes breaking changes that might effect your existing CI/CD pipelines. Before upgrading the CLI, carefully read through [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md) to learn more about these breaking changes and how they can affect your pipelines.

:::

The Astro CLI is now a single CLI executable built for all Astronomer products. This new generation of the Astro CLI is optimized for a consistent local development experience and provides more value to Astronomer Software customers. For organizations moving from Astronomer Software to [Astro](https://docs.astronomer.io/astro), this change makes the transition easier.

To establish a shared framework between products, the syntax of several Software CLI commands have been updated. Due to the quantity of these changes, all changes introduced in this release are documented in [Upgrade to Astro CLI v1.0](upgrade-astro-cli.md). Astro CLI v1.0.0 is only compatible with Astronomer Software v0.28+.

### New Command To Switch Between Astronomer Installations

You can now use `astro context list` and `astro context switch` to show the Astronomer contexts that you can access and assume. An Astronomer context is a base domain that relates to either Astro or a particular Cluster on Astronomer Software. A domain appears as an available context if you have authenticated to it at least once.

These commands are intended for users who need to work across multiple Astronomer Software clusters or installations. They replace `astro cluster list` and `astro cluster switch`, respectively. For more information, see the [CLI command reference](cli-reference.md#astro-context-switch).

## Astro CLI v0.28.2

Release date: July 12, 2022

### Bug fixes

- Fixed an issue where `astro deploy` did not work when using Podman 4.0+

## 0.28.1

Release date: March 14, 2022

### Additional Improvements

- You can now use the new `--no-cache` flag with `astro dev start` and `astro deploy`. This flag prevents your container engine from building your project with cached images from previous builds.
- New Deployments created via `astro deployment create` now use the Celery Executor by default.

### Bug fixes

- Fixed an issue where `astro dev logs` and `astro dev start` didn't work when using custom Docker container names
- Fixed an issue where `astro deploy` did not work when using Podman in specific circumstances
- Fixed an issue where `airflow_settings.yaml` was not properly imported to the Airflow UI when running Astro in a local Podman environment
- Fixed an issue where updating a Deployment's deployment type via `astro deployment update` would generate an error in the Software UI
- Added a timeout for failing to connect to Houston

## 0.28.0

Release date: February 15, 2022

### Additional Improvements

- After successfully pushing code to a Deployment via `astro deploy`, the CLI now provides a URL that you can use to directly access that Deployment via the UI.
- You can now retrieve Triggerer logs using `astro deployment logs triggerer`.

### Bug Fixes

- Fixed an issue where some objects specified in `airflow_settings.yaml` were not rendered after running `astro dev start`
- Fixed an issue where environment variables in `docker-compose.override.yml` were not correctly applied after running `astro dev start`
