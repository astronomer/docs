---
sidebar_label: "astro dev logs"
title: "astro dev logs"
id: astro-dev-logs
description: Reference documentation for astro dev logs.
---

## Description

Show webserver, scheduler, and Celery worker logs from your local Airflow environment.

## Usage

```sh
astro dev logs
```

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-f`,`--follow` | Continue streaming most recent log output to your terminal. | ``|
| `-s`,`--scheduler`            | Show only scheduler logs                                                                                  | ``                  |
| `-w`,`--webserver`            | Show only webserver logs                                                                                  | ``                 |
| `-t`,`--triggerer`            | Show only triggerer logs                                                                                  | ``                 |


## Examples

```sh
$ astro dev logs
# Show the most recent logs from both the Airflow webserver and Scheduler
$ astro dev logs --follow
# Stream all new webserver and scheduler logs to the terminal
$ astro dev logs --follow --scheduler
# Stream only new scheduler logs to the terminal
```

## Related Commands

- [`astro dev ps`](cli/astro-dev-ps.md)
- [`astro dev run`](cli/astro-dev-run.md)
