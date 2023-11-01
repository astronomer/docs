---
sidebar_label: "astro deployment connection list"
title: "astro deployment connection list"
id: astro-deployment-connection-list
description: List Airflow connections in a Deployment.
hide_table_of_contents: true
---

List the Airflow connections stored in a Deployment's metadata database. 

## Usage

```sh
astro deployment connection list
```

This command only lists Airflow connections that were configured through the Airflow UI or otherwise stored in the Airflow metadata database. 

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to list connections                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment for which to list connections. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | List connections for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```bash
# List connections stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment connection list --deployment-id cl03oiq7d80402nwn7fsl3dmv

# List connections stored in the Deployment "My Deployment"
astro deployment connection list --deployment-name="My Deployment"
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
