---
sidebar_label: "astro deployment pool create"
title: "astro deployment pool create"
id: astro-deployment-pool-create
description: Reference documentation for astro deployment pool create.
hide_table_of_contents: true
---

For a given Deployment on Astro, create pools that are stored in the Airflow metadata database.

## Usage

```sh
astro deployment pool create
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to create pools                                                | Any valid Deployment ID |
| `-n`, `--deployment-name` | The name of the Deployment for which to create pools. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | create pools for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |
| `--name`          | The Airflow pool name. Required         | string                                                         |
| `-v`,`--slots`          | Number of airflow pool slots. Required.           | intieger                                                         |
| `--description`          | The pool description.          | string                                                         |

## Examples

```sh
# create pool called my-pool stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
$ astro deployment pool create --deployment-id cl03oiq7d80402nwn7fsl3dmv --name my-pool --slots 10

# create pool stored in the Deployment "My Deployment"
$ astro deployment pool create --deployment-name="My Deployment" --name my-pool --slots 10
```

## Related Commands

- [`astro deployment pool copy`](cli/astro-deployment-pool-copy.md)
- [`astro deployment pool update`](cli/astro-deployment-pool-update.md)
