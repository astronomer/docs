---
sidebar_label: "astro deployment airflow-variable create"
title: "astro deployment airflow-variable create"
id: astro-deployment-airflow-variable-create
description: Create an Airflow variable in a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Create Airflow variables on a Deployment. Airflow variables are stored in the Deployment's metadata database and appear in the Airflow UI.

## Usage

```bash
astro deployment airflow-variable create
```

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), you can generate a Deployment or Workspace API Token, then specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI:

```bash
export ASTRO_API_TOKEN=<your-token>
```

See [Deployment API Tokens](deployment-api-tokens.md) and [Workspace API Tokens](workspace-api-tokens.md) for more details about ways to use tokens.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment where you want to create Airflow variables.                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment where you want to create Airflow variables. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Create Airflow variables in a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |
| `-k`,`--key`          | The Airflow variable key. Required.          | string                                                         |
| `-v`,`--value`          | The Airflow variable value. Required.           | string                                                         |
| `--description`          | The Airflow variable description.          | string                                                         |

## Examples

```bash
# create airflow variable called my-variable stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment airflow-variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --key my-variable ---value VAR

# create airflow-variables stored in the Deployment "My Deployment"
astro deployment airflow-variable create --deployment-name="My Deployment" --key my-variable --value VAR
```

## Related Commands

- [`astro deployment airflow variable copy`](cli/astro-deployment-airflow-variable-copy.md)
- [`astro deployment airflow variable update`](cli/astro-deployment-airflow-variable-update.md)
