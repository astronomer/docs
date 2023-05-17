---
sidebar_label: "astro deployment airflow-variable create"
title: "astro deployment airflow-variable create"
id: astro-deployment-airflow-variable-create
description: Reference documentation for astro deployment airflow-variable create.
hide_table_of_contents: true
---

Create Airflow variables on a Deployment. Airflow variables are stored in the Deployment's metadata database and appear in the Airflow UI.  

## Usage

```sh
astro deployment airflow-variable create
```

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

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

```sh
# create airflow variable called my-variable stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
$ astro deployment airflow-variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --key my-variable ---value VAR

# create airflow-variables stored in the Deployment "My Deployment"
$ astro deployment airflow-variable create --deployment-name="My Deployment" --key my-variable --value VAR
```

## Related Commands

- [`astro deployment airflow variable copy`](cli/astro-deployment-airflow-variable-copy.md)
- [`astro deployment airflow variable update`](cli/astro-deployment-airflow-variable-update.md)
