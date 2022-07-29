---
sidebar_label: "astro deployment create"
title: "astro deployment create"
id: astro-deployment-create
description: Reference documentation for astro deployment create.
---

Create a Deployment on Astro. This command is functionally identical to using the Cloud UI to [create a Deployment](create-deployment.md).

## Usage

```sh
astro deployment create
```

## Options

| Option                      | Description                                                                        | Possible Values                                                          |
| --------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `-c`, `--cluster-id`        | The cluster in which you want to create a Deployment                                                                      | The name of any cluster that you can create Deployments in               |
| `-d`,`--description`        | The description for the Deployment                                    | Any string. Multiple-word descriptions should be specified in quotations (`"`) |
| `-n`,`--name`        | The Deployment's name                                                       | Any string. Multiple-word descriptions should be specified in quotations |
| `-v`,`--runtime-version`    | The Astro Runtime version for the Deployment                                                   | Any supported version of Astro Runtime. Major, minor, and patch versions must be specified.                                                |
| `-s`,`--scheduler-au`       | The number of AU to allocate towards the Deployment's Scheduler(s). The default is`5`.     | Integer between `0` and `30`                                             |
| `-a`,`--worker-au`          | The number of AU to allocate towards the Deployment's worker(s). The default is `10`.      | Integer between `0` and `175`                                            |
| `-r`,`--scheduler-replicas` | The number of scheduler replicas for the Deployment. The default is `1`. | Integer between `0` and `4`                                              |
| `--workspace-id` | The Workspace in which to create a Deployment. If not specified, your current Workspace is assumed. | Any valid Workspace ID                                            |

## Examples

```sh
$ astro deployment create
# CLI prompts you for a Deployment name and Cluster

$ astro deployment create -d="My Deployment Description" --name="My Deployment Name" --cluster-id="ckwqkz36200140ror6axh8p19"
# Create a Deployment with all required information specified. The CLI will not prompt you for more information

$ astro deployment create -a=50
# Specify 50 AU for the Deployment's workers. The Astro CLI prompts you for required information
```

## Related Commands

- [`astro deployment delete`](cli/astro-deployment-delete.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
