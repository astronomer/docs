---
sidebar_label: "astro deployment logs"
title: "astro deployment logs"
id: astro-deployment-logs
description: Reference documentation for astro deployment logs.
---

## Description

Show [scheduler logs](scheduler-logs.md) over the last 24 hours for a given Deployment on Astro. These scheduler logs are the same logs that appear in the **Logs** tab of the Cloud UI.

## Usage

```sh
astro deployment logs
```

## Options

| Option                   | Description                                     | Possible Values                     |
| ------------------------ | ----------------------------------------------- | ----------------------------------- |
| `<deployment-id>` | The Deployment to show logs for                        | Any valid Deployment ID |
| `-e`,`--error`           | Show only logs with a log level of `ERROR`      | ``                                  |
| `-w`,`--warn`            | Show only logs with a log level of `WARNING`    | ``                                  |
| `-i`,`--info`            | Show only logs with a log level of `INFO`       | ``                                  |
| `-c`,`--log-count`       | The number of log lines to show. The default is `500` | Any integer less than or equal to 500 |
| `--workspace-id` | Specify a Workspace to show logs for a Deployment outside of your current Workspace| Any valid Workspace ID                                            |

## Examples

```sh
$ astro deployment logs
# CLI prompts you for a Deployment to view logs for
$ astro deployment logs cl03oiq7d80402nwn7fsl3dmv
# View logs for a specific Deployment
$ astro deployment logs cl03oiq7d80402nwn7fsl3dmv --error --log-count=25
# For the same Deployment, show only the last 25 error-level logs
```

## Related Commands

- [`astro dev logs`](cli/astro-dev-logs.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev ps`](cli/astro-dev-ps.md)
