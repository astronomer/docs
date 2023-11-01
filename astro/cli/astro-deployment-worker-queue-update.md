---
sidebar_label: "astro deployment worker-queue update"
title: "astro deployment worker-queue update"
id: astro-deployment-worker-queue-update
description: Update a Deployment worker queue.
---

Update the settings for an existing [worker queue](configure-worker-queues.md) in a Deployment on Astro. This is functionally identical to updating the settings of a worker queue in the Cloud UI.

## Usage

```sh
astro deployment worker-queue update
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `--concurrency`           |     The maximum number of tasks that each worker can run                          | Any integer from 1 to 64 |
| `-d`,`--deployment-id`           |      The ID of the Deployment whose worker queue you want to update                           | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment whose worker queue you want to update. Use as an alternative to `<deployment-id>` | Any valid Deployment name                                            |
| `-f` `--force` | Skip prompting the user to confirm the update | `` |
| `--max-count`                  |        The maximum worker count of the worker queue                                                          | Any integer from 0 to 30       |
| `--min-count`                  |        The minimum worker count of the worker queue                                                          | Any integer from 0 to 30       |
| `-n`,`--name`    | The name of the worker queue     |Any string |
| `-t`,`--worker-type`          | The worker type of the worker queue          | Any worker type enabled on the cluster in which the Deployment exists |

## Examples

```sh
astro deployment worker-queue update --deployment-id cl03oiq7d80402nwn7fsl3dmv --name="Updated name"
# Update a worker queue's name in a specified Deployment.

astro deployment worker-queue update --concurrency 20 --max-count 10 --min-count 2 --name "My worker queue" --worker-type "m5d.8xlarge"
# Update a new worker queue in a Deployment. The CLI prompts you to specify a Deployment and worker queue to update
```

## Related commands 

- [`astro deployment worker-queue create`](cli/astro-deployment-worker-queue-create.md)
- [`astro deployment worker-queue delete`](cli/astro-deployment-worker-queue-delete.md)