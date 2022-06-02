---
sidebar_label: "astro dev logs"
title: "astro dev logs"
id: astro-dev-logs
description: Reference documentation for astro dev logs.
---

## Description

Show Webserver, Scheduler, and Celery worker logs from your local Airflow environment.

## Usage

```sh
astro dev logs
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-f`,`--follow` | Continue streaming most recent log output to your terminal. | ``|
| `-s`,`--scheduler`            | Show only Scheduler logs                                                                                  | ``                  |
| `-w`,`--webserver`            | Show only Webserver logs                                                                                  | ``                 |
| `-t`,`--triggerer`            | Show only Triggerer logs                                                                                  | ``                 |


## Examples

```sh
$ astro dev logs
# Show the most recent logs from both the Airflow Webserver and Scheduler
$ astro dev logs --follow
# Stream all new Webserver and Scheduler logs to the terminal
$ astro dev logs --follow --scheduler
# Stream only new Scheduler logs to the terminal
```

## Related Commands

- [`astro dev ps`](cli/astro-dev-ps.md)
- [`astro dev run`](cli/astro-dev-run.md)
