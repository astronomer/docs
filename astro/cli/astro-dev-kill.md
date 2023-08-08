---
sidebar_label: "astro dev kill"
title: "astro dev kill"
id: astro-dev-kill
description: Reference documentation for astro dev kill.
hide_table_of_contents: true
---

Force-stop and remove all running containers for your local Airflow environment. Unlike [`astro dev stop`](astro-dev-stop.md), which only pauses running containers, `astro dev kill` deletes all data associated with your local Postgres database. This includes Airflow connections, logs, and task history.

For more information, read [Hard reset your local environment](cli/troubleshoot-your-local-airflow-environment.md#hard-reset-your-local-environment) or [Build and run a project locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev kill
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
