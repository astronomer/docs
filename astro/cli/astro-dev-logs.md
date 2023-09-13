---
sidebar_label: "astro dev logs"
title: "astro dev logs"
id: astro-dev-logs
description: Show logs for Airflow components.
hide_table_of_contents: true
---

Show webserver, scheduler, and triggerer logs from your local Airflow environment.

## Usage

```sh
astro dev logs
```

## Options

| Option             | Description                                                 | Possible Values |
| ------------------ | ----------------------------------------------------------- | --------------- |
| `-f`,`--follow`    | Continue streaming most recent log output to your terminal. | None            |
| `-s`,`--scheduler` | Show only scheduler logs                                    | None            |
| `-w`,`--webserver` | Show only webserver logs                                    | None            |
| `-t`,`--triggerer` | Show only triggerer logs                                    | None            |


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
