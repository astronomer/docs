---
sidebar_label: "astro deployment pool create"
title: "astro deployment pool create"
id: astro-deployment-pool-create
description: Create Apache Airflow® pools in a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

Create [Apache Airflow®](https://airflow.apache.org/) pools in a Deployment. Airflow pools are stored in the Deployment's metadata database and appear in the Airflow UI.

## Usage

```sh
astro deployment pool create
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
| `-v`,`--slots`          | Number of Airflow pool slots. Required.           | Any integer                                                         |
| `--description`          | The pool description.          | Any string                                                         |

## Examples

```bash
# create pool called my-pool stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment pool create --deployment-id cl03oiq7d80402nwn7fsl3dmv --name my-pool --slots 10

# create pool stored in the Deployment "My Deployment"
astro deployment pool create --deployment-name="My Deployment" --name my-pool --slots 10
```

## Related Commands

- [`astro deployment pool copy`](cli/astro-deployment-pool-copy.md)
- [`astro deployment pool update`](cli/astro-deployment-pool-update.md)
