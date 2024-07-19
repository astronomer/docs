---
sidebar_label: "astro deployment airflow-variable update"
title: "astro deployment airflow-variable update"
id: astro-deployment-airflow-variable-update
description: Update an existing Deployment Apache Airflow® variable.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

Update the value for a Deployment's [Apache Airflow®](https://airflow.apache.org/) variable.

## Usage

```sh
astro deployment airflow-variable update
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
| `-d`,`--deployment-id`           |    The ID of the Deployment where you want to update an Airflow variable.                                           | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment where you want to update Airflow variables. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Update Airflow variables for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |
| `-k`,`--key`          | The Airflow variable key. Required.          | string                                                         |
| `-v`,`--value`          | The Airflow variable value. Required.           | string                                                         |
| `--description`          | The Airflow variable description.          | string                                                         |

## Examples

```bash
# update Apache Airflow®-variable called my-airflow-variable stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment airflow-variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --key my-variable ---value VAR

# update airflow-variables stored in the Deployment "My Deployment"
astro deployment airflow-variable update --deployment-name="My Deployment" --key my-variable ---value VAR

## Related Commands

- [`astro deployment airflow-variable create`](cli/astro-deployment-airflow-variable-create.md)
- [`astro deployment airflow-variable list`](cli/astro-deployment-airflow-variable-list.md)
