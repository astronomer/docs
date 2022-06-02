---
sidebar_label: "astro dev stop"
title: "astro dev stop"
id: astro-dev-stop
description: Reference documentation for astro dev stop.
---

## Description

Pause all Docker containers running your local Airflow environment. Unlike `astro dev kill`, this command does not prune mounted volumes and delete data associated with your local Postgres database. If you run this command, Airflow connections and task history will be preserved.

This command can be used regularly with `astro dev start` to apply changes to your Astro project as you test and troubleshoot DAGs. For more information, read [Develop and Run a Project Locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev stop
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
