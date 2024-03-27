---
sidebar_label: "astro deployment pool update"
title: "astro deployment pool update"
id: astro-deployment-pool-update
description: Update a Deployment's Airflow pool.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

Update the value for a Deployment's Airflow pool.

## Usage

```sh
astro deployment airflow-pool update
```

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
```

## Related Commands

- [`astro deployment pool create`](cli/astro-deployment-pool-create.md)
- [`astro deployment pool list`](cli/astro-deployment-pool-list.md)
