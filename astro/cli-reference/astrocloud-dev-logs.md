---
sidebar_label: "astrocloud dev logs"
title: "astrocloud dev logs"
id: astrocloud-dev-logs
description: Reference documentation for astrocloud dev logs.
---

## Description

Show Webserver, Scheduler, and Celery worker logs from your local Airflow environment.

## Usage

```sh
astrocloud dev logs
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
$ astrocloud dev logs
# Show the most recent logs from both the Airflow Webserver and Scheduler
$ astrocloud dev logs --follow
# Stream all new Webserver and Scheduler logs to the terminal
$ astrocloud dev logs --follow --scheduler
# Stream only new Scheduler logs to the terminal
```

## Related Commands

- [`astrocloud dev ps`](cli-reference/astrocloud-dev-ps.md)
- [`astrocloud dev run`](cli-reference/astrocloud-dev-run.md)
