---
sidebar_label: "astrocloud deployment update"
title: "astrocloud deployment update"
id: astrocloud-deployment-update
description: Reference documentation for astrocloud deployment update.
---

## Description

Update the configuration for a Deployment on Astro. This command is functionally identical to modifying a Deployment in the Cloud UI via the **Edit Configuration** button.

## Usage

```sh
astrocloud deployment update <deployment-id> <flags>
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `<deployment-id>` (_Required_) | The Deployment to update                                                               | Any valid Deployment ID                                                        |
| `-d`,`--description`           | The description for the Deployment                                                     | Any string. Multiple-word descriptions should be specified in quotations (`"`) |
| `-l`,`--name`                  | The Deployment's name                                                                  | Any string. Multiple-word descriptions should be specified in quotations       |
| `-s`,`--scheduler-au`          | The number of AU to allocate towards the Deployment's Scheduler(s). The default is`5`. | Integer between `0` and `30`                                                   |
| `-a`,`--worker-au`             | The number of AU to allocate towards the Deployment's worker(s). The default is `10`.  | Integer between `0` and `175`                                                  |
| `-r`,`--scheduler-replicas`    | The number of Scheduler replicas for the Deployment. The default is `1`.               | Integer between `0` and `4`                                                    |
| `-f`,`--force`          | Force a Deployment update                             | ``                                                                             |
| `-w`,`--workspace-id`          | Specify a Workspace to update a Deployment outside of your current Workspace           | Any valid Workspace ID                                                         |

## Examples

```sh
# Update a Deployment's name and description
$ astrocloud deployment update cl03oiq7d80402nwn7fsl3dmv -d="My Deployment Description" --name="My Deployment Name"

# Force update a Deployment
$ astrocloud deployment update cl03oiq7d80402nwn7fsl3dmv -d="My Deployment Description" --force
```

## Related Commands

- [`astrocloud deployment delete`](cli-reference/astrocloud-deployment-delete.md)
- [`astrocloud deployment list`](cli-reference/astrocloud-deployment-list.md)
