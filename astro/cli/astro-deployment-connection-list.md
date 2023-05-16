---
sidebar_label: "astro deployment connection list"
title: "astro deployment connection list"
id: astro-deployment-connection-list
description: Reference documentation for astro deployment connection list.
hide_table_of_contents: true
---

For a given Deployment on Astro, list its connections stored in the Airflow metadata database.

## Usage

```sh
astro deployment connection list
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
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to list connections                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment for which to list Conections. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | List connections for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# List connections stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
$ astro deployment connection list --deployment-id cl03oiq7d80402nwn7fsl3dmv

# List connections stored in the Deployment "My Deployment"
$ astro deployment connection list --deployment-name="My Deployment"
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
