---
sidebar_label: "astrocloud dev stop"
title: "astrocloud dev stop"
id: astrocloud-dev-stop
description: Reference documentation for astrocloud dev stop.
---

## Description

Pause all Docker containers running your local Airflow environment. Unlike `astro dev kill`, this command does not prune mounted volumes and delete data associated with your local Postgres database. If you run this command, Airflow connections and task history will be preserved.

This command can be used regularly with `astro dev start` to apply changes to your Astronomer project as you test and troubleshoot DAGs. For more information, read [Develop and Run a Project Locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astrocloud dev stop
```

## Related Commands

- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud dev kill`](cli-reference/astrocloud-dev-kill.md)
