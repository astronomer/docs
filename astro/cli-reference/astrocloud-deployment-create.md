---
sidebar_label: "astrocloud deployment create"
title: "astrocloud deployment create"
id: astrocloud-deployment-create
description: Reference documentation for astrocloud deployment create.
---

## Description

Create a Deployment on Astro. This command is functionally identical to [creating a Deployment](configure-deployment.md) via the Cloud UI.

## Usage

```sh
astrocloud deployment create
```

## Options

| Option                      | Description                                                                        | Possible Values                                                          |
| --------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `-c`, `--cluster-id`        | The Cluster in which you want to create a Deployment                                                                      | The name of any Cluster that you can create Deployments in               |
| `-d`,`--description`        | The description for the Deployment                                    | Any string. Multiple-word descriptions should be specified in quotations (`"`) |
| `-n`,`--name`        | The Deployment's name                                                       | Any string. Multiple-word descriptions should be specified in quotations |
| `-v`,`--runtime-version`    | The Astro Runtime version for the Deployment                                                   | Any supported version of Astro Runtime. Major, minor, and patch versions must be specified.                                                |
| `-s`,`--scheduler-au`       | The number of AU to allocate towards the Deployment's Scheduler(s). The default is`5`.     | Integer between `0` and `30`                                             |
| `-a`,`--worker-au`          | The number of AU to allocate towards the Deployment's worker(s). The default is `10`.      | Integer between `0` and `175`                                            |
| `-r`,`--scheduler-replicas` | The number of Scheduler replicas for the Deployment. The default is `1`. | Integer between `0` and `4`                                              |
| `--workspace-id` | The Workspace in which to create a Deployment. If not specified, your current Workspace is assumed. | Any valid Workspace ID                                            |

## Examples

```sh
$ astrocloud deployment create
# CLI prompts you for a Deployment name and Cluster

$ astrocloud deployment create -d="My Deployment Description" --name="My Deployment Name" --cluster-id="ckwqkz36200140ror6axh8p19"
# Create a Deployment with all required information specified. The CLI will not prompt you for more information

$ astrocloud deployment create -a=50
# Specify 50 AU for the Deployment's workers. The Astro CLI prompts you for required information
```

## Related Commands

- [`astrocloud deployment delete`](cli-reference/astrocloud-deployment-delete.md)
- [`astrocloud deployment list`](cli-reference/astrocloud-deployment-list.md)
