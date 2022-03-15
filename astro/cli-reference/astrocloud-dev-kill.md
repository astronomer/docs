---
sidebar_label: "astrocloud dev kill"
title: "astrocloud dev kill"
id: astrocloud-dev-kill
description: Reference documentation for astrocloud dev kill.
---

## Description

Force-stop and remove all running containers for your local Airflow environment. Unlike [`astrocloud dev stop`](astrocloud-dev-stop.md), which only pauses running containers, `astro dev kill` will delete all data associated with your local Postgres database. This includes Airflow connections, logs, and task history.

For more information, read [Hard Reset Your Local Environment](test-and-troubleshoot-locally.md#hard-reset-your-local-environment) or [Build and Run a Project Locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astrocloud dev kill
```

## Related Commands

- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud dev stop`](cli-reference/astrocloud-dev-stop.md)
