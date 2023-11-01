---
sidebar_label: "astro deployment pool list"
title: "astro deployment pool list"
id: astro-deployment-pool-list
description: List Airflow pools in a Deployment. 
hide_table_of_contents: true
---

List the Airflow pools stored in a Deployment's metadata database. 

## Usage

```sh
astro deployment pool list
```

This command only lists Airflow pools that were configured through the Airflow UI or otherwise stored in the Airflow metadata database. 

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment to list Airflow pools for.                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment to list Airflow pools for. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | List Airflow pools for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.           | Any valid Workspace ID                                                         |

## Examples

```bash
# List pools stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment pool list --deployment-id cl03oiq7d80402nwn7fsl3dmv

# List pools stored in the Deployment "My Deployment"
astro deployment pool list --deployment-name="My Deployment"

## Related Commands

- [`astro deployment pool create`](cli/astro-deployment-pool-create.md)
- [`astro deployment pool update`](cli/astro-deployment-pool-update.md)
