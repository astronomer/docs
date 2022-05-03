---
sidebar_label: "astrocloud deployment logs"
title: "astrocloud deployment logs"
id: astrocloud-deployment-logs
description: Reference documentation for astrocloud deployment logs.
---

## Description

Show [Scheduler logs](scheduler-logs.md) over the last 24 hours for a given Deployment on Astro. These Scheduler logs are the same logs that appear in the **Logs** tab of the Cloud UI.

## Usage

```sh
astrocloud deployment logs
```

## Options

| Option                   | Description                                     | Possible Values                     |
| ------------------------ | ----------------------------------------------- | ----------------------------------- |
| `<deployment-id>` | The Deployment to show logs for                 | Any valid Deployment ID |
| `-e`,`--error`           | Show only logs with a log level of `ERROR`      | ``                                  |
| `-w`,`--warn`            | Show only logs with a log level of `WARNING`    | ``                                  |
| `-i`,`--info`            | Show only logs with a log level of `INFO`       | ``                                  |
| `-c`,`--log-count`       | The number of log lines to show. The default is`500` | Any integer                         |
| `--workspace-id` | Specify a Workspace to show logs for a Deployment outside of your current Workspace| Any valid Workspace ID                                            |

## Examples

```sh
$ astrocloud deployment logs
# CLI prompts you for a Deployment to view logs for
$ astrocloud deployment logs cl03oiq7d80402nwn7fsl3dmv
# View logs for a specific Deployment
$ astrocloud deployment logs cl03oiq7d80402nwn7fsl3dmv --error --log-count=25
# For the same Deployment, show only the last 25 error-level logs
```

## Related Commands

- [`astrocloud dev logs`](cli-reference/astrocloud-dev-logs.md)
- [`astrocloud dev run`](cli-reference/astrocloud-dev-run.md)
- [`astrocloud dev ps`](cli-reference/astrocloud-dev-ps.md)
