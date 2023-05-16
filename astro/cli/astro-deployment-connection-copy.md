---
sidebar_label: "astro deployment connection copy"
title: "astro deployment connection copy"
id: astro-deployment-connection-copy
description: Reference documentation for astro deployment connection copy.
hide_table_of_contents: true
---

For a given Deployment on Astro, copy its connections stored in the Airflow metadata database to another Deployment on Astro

## Usage

```sh
astro deployment connection copy
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
| `-s`,`--source-id`           |    The ID of the Deployment to copy connections from.                                             | Any valid Deployment ID |
| `-n`, `--source-name` | The name of the Deployment for which to copy connections from. Use as an alternative to `<source-id>`. | Any valid Deployment name                                            |
| `-t`, `--target-id` | The ID of the Deployment to receive the copied connection                                     |
| `--target-name` | The name of the Deployment to receive the copied connection.  Use as an alternative to `<target-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | copy connections for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |

## Examples

```sh
# copy connections stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv to a deployment with an ID of cl03oiq7d80402nwn7fsl3dcd
$ astro deployment connection copy --source-id cl03oiq7d80402nwn7fsl3dmv --target cl03oiq7d80402nwn7fsl3dcd

# copy connections stored in the Deployment "My Deployment" to another Deployment "My Other Deployment"
$ astro deployment connection copy --source-name="My Deployment" --target-name="My Other Deployment"
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
