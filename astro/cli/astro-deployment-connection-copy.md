---
sidebar_label: "astro deployment connection copy"
title: "astro deployment connection copy"
id: astro-deployment-connection-copy
description: Copy an Airflow connection from a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Copy Airflow connections from one Astro Deployment to another. Airflow connections are stored in the target Deployment's metadata database and appear in the Airflow UI.

## Usage

```sh
astro deployment connection copy
```

This command only copies Airflow connections that were configured through the Airflow UI or otherwise stored in the Airflow metadata database.

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), you can generate an API token, then specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI:

```bash
export ASTRO_API_TOKEN=<your-token>
```

See [Organization](organization-api-tokens.md), [Workspace](workspace-api-tokens.md), and [Deployment](deployment-api-tokens.md) API token documentation for more details about ways to use API tokens.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-s`,`--source-id`           |    The ID of the Deployment to copy Airflow connections from.                                             | Any valid Deployment ID |
| `-n`, `--source-name` | The name of the Deployment from which to copy Airflow connections. Use as an alternative to `<source-id>`. | Any valid Deployment name                                            |
| `-t`, `--target-id` | The ID of the Deployment to receive the copied Airflow connections                                     |
| `--target-name` | The name of the Deployment to receive the copied Airflow connections.  Use as an alternative to `<target-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Specify to copy Airflow connections to a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |

## Examples

```bash
# copy connections stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv to a deployment with an ID of cl03oiq7d80402nwn7fsl3dcd
astro deployment connection copy --source-id cl03oiq7d80402nwn7fsl3dmv --target cl03oiq7d80402nwn7fsl3dcd

# copy connections stored in the Deployment "My Deployment" to another Deployment "My Other Deployment"
astro deployment connection copy --source-name="My Deployment" --target-name="My Other Deployment"

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
