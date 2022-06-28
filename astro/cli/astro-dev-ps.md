---
sidebar_label: "astro dev ps"
title: "astro dev ps"
id: astro-dev-ps
description: Reference documentation for astro dev ps.
---

## Description

List all Docker containers running in your local Airflow environment, including the Airflow webserver, scheduler, and Postgres database. It outputs metadata for each running container, including `Container ID`, `Created`, `Status`, and `Ports`.

This command works similarly to [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/) and can only be run from a directory that is running an Astro project.

## Usage

```sh
astro dev ps
```

## Related Commands

- [`astro dev logs`](cli/astro-dev-logs.md)
- [`astro dev run`](cli/astro-dev-run.md)
