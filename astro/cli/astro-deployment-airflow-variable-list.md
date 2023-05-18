---
sidebar_label: "astro deployment airflow-variable list"
title: "astro deployment airflow variable list"
id: astro-deployment-airflow-variable-list
description: Reference documentation for astro deployment airflow-variable list.
hide_table_of_contents: true
---

List the Airflow variables stored in a Deployment's metadata database. 

## Usage

```sh
astro deployment airflow-variable list
```

This command only lists Airflow variables that were configured through the Airflow UI or otherwise stored in the Airflow metadata database. 

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment to list Airflow variables for.                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment to list Airflow variables for. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | List Airflow variables for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.           | Any valid Workspace ID                                                         |

## Examples

```bash
# List airflow variables stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment airflow-variable list --deployment-id cl03oiq7d80402nwn7fsl3dmv

# List airflow variables stored in the Deployment "My Deployment"
astro deployment airflow-variable list --deployment-name="My Deployment"
```

## Related Commands

- [`astro deployment airflow-variable create`](cli/astro-deployment-airflow-variable-create.md)
- [`astro deployment airflow-variable update`](cli/astro-deployment-airflow-variable-update.md)
