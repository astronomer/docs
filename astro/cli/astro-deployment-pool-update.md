---
sidebar_label: "astro deployment pool update"
title: "astro deployment pool update"
id: astro-deployment-pool-update
description: Update a Deployment's Airflow pool. 
hide_table_of_contents: true
---

Update the value for a Deployment's Airflow pool. 

## Usage

```sh
astro deployment airflow-pool update
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment pools in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the pools, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment where you want to create Airflow pools.                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment where you want to create Airflow pools. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Create Airflow pools in a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |
| `--name`          | The Airflow pool name. Required.        | Any string                                                         |
| `-v`,`--slots`          | Number of airflow pool slots. Required.           | Any integer                                                         |
| `--description`          | The pool description.          | Any string                                                         |

## Examples

```bash
# update pool called my-pool stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment pool update --deployment-id cl03oiq7d80402nwn7fsl3dmv --name my-pool --slots 10

# update pools stored in the Deployment "My Deployment"
astro deployment pool update --deployment-name="My Deployment" --name my-pool --slots 10

## Related Commands

- [`astro deployment pool create`](cli/astro-deployment-pool-create.md)
- [`astro deployment pool list`](cli/astro-deployment-pool-list.md)
