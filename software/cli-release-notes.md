---
sidebar_label: 'Astro CLI'
title: 'Astro CLI Release Notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](cli-quickstart.md) for the v0.28.x series of Astronomer Software. For general product release notes, go to [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer Support](https://support.astronomer.io).

## Astro CLI v1.0.0

Release date: May 25, 2022

### A Shared CLI for All Astronomer Users

:::danger Breaking Change

Astro CLI v1.0.0 includes breaking changes that might effect your existing CI/CD pipelines. Before upgrading the CLI, carefully read through [Upgrade to Astro CLI v1.0](upgrade-cli.md) to learn more about these breaking changes and how they can affect your pipelines.

:::

The Astro CLI is now a single CLI executable shared between Astro and Software users. With this new generation of the CLI, you can work between Astro and Software installations without having to switch out your essential tools.

To establish a shared framework between products, the syntax of several Software CLI commands has been updated. Due to the scale of these changes, all breaking changes related to using the CLI have been documented in [Upgrade to Astro CLI v1.0](upgrade-cli.md).

### New Command To Switch Between Astronomer Installations

You can now use the `astro context list` and `astro context switch` to show all Astronomer installations you have access to and switch between those installations. An Astronomer installation will appear as an available context if you have logged into it at least once. This command is primarily designed for users who need to work in both Astro and Astronomer Software installations.

These new commands replace `astro cluster list` and `astro cluster switch` respectively. For more information, see the [CLI Command Reference Guide](cli/astro-context-switch.md).

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
