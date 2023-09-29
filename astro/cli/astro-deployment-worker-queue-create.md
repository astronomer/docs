---
sidebar_label: "astro deployment worker-queue create"
title: "astro deployment worker-queue create"
id: astro-deployment-worker-queue-create
description: Reference documentation for astro deployment worker-queue create.
---

Create a [worker queue](configure-worker-queues.md) in a Deployment on Astro. This command is functionally identical to creating a worker queue in the Cloud UI.

## Usage

```sh
astro deployment worker-queue create
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `--concurrency`           |     The maximum number of tasks that each worker can run                          | Any integer from 1 to 64 |
| `-d`,`--deployment-id`           |      The ID of the Deployment where you want to create the worker queue                           | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment where you want to create the worker queue. Use as an alternative to `<deployment-id>` | Any valid Deployment name                                            |
| `--max-count`                  |        The maximum worker count of the worker queue                                                          | Any integer from 0 to 30       |
| `--min-count`                  |        The minimum worker count of the worker queue                                                          | Any integer from 0 to 30       |
| `-n`,`--name`    | The name of the worker queue     |Any string |
| `-t`,`--worker-type`          | The worker type of the worker queue          | Any worker type enabled on the cluster in which the Deployment exists |


## Examples 

```sh
astro deployment worker-queue create --deployment-id cl03oiq7d80402nwn7fsl3dmv
# Creates a new worker queue for a Deployment with ID `cl03oiq7d80402nwn7fsl3dmv`. The Astro CLI prompts you for configuration information.

astro deployment worker-queue create --concurrency 20 --max-count 10 --min-count 2 --name "My worker queue" --worker-type "m5d.8xlarge"
# Creates a new worker queue with specified configurations. The Astro CLI prompts you for Deployment information.
```

## Related commands 

- [`astro deployment worker-queue update`](cli/astro-deployment-worker-queue-update.md)
- [`astro deployment worker-queue delete`](cli/astro-deployment-worker-queue-delete.md)