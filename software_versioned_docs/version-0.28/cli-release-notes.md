---
sidebar_label: 'Astronomer CLI'
title: 'Astronomer CLI Release Notes'
id: cli-release-notes
description: Release notes for the Astronomer CLI.
---

## Overview

This document provides a summary of all changes made to the [Astronomer CLI](cli-quickstart.md) for the v0.28.x series of Astronomer Software. For general product release notes, go to [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer Support](https://support.astronomer.io).

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
