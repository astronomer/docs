---
sidebar_label: "astrocloud dev logs"
title: "astrocloud dev logs"
id: astrocloud-dev-ps
description: Reference documentation for astrocloud dev logs.
---

## Description

List all Docker containers running in your local Airflow environment, including the Airflow Webserver, Scheduler, and Postgres database. It outputs metadata for each running container, including `Container ID`, `Created`, `Status`, and `Ports`.

This command works similarly to [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/) and can only be run from a directory that is running an Astronomer Project.

## Usage

```sh
astrocloud dev ps
```

## Related Commands

- [`astrocloud dev logs`](cli-reference/astrocloud-dev-logs.md)
- [`astrocloud dev run`](cli-reference/astrocloud-dev-run.md)
