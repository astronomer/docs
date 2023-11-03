---
sidebar_label: "astro dev ps"
title: "astro dev ps"
id: astro-dev-ps
description: List all running Docker containers in your local Airflow environment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

List all Docker containers running in your local Airflow environment, including the Airflow Webserver, Scheduler, and Postgres database. It outputs metadata for each running container, including `Container ID`, `Created`, `Status`, and `Ports`.

This command works similarly to [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/) and can only be run from a directory that is running an Astro project.

## Usage

```sh
astro dev ps
```

## Related Commands

- [`astro dev logs`](cli/astro-dev-logs.md)
- [`astro dev run`](cli/astro-dev-run.md)
