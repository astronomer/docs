---
sidebar_label: "astro deployment airflow-variable update"
title: "astro deployment airflow-variable update"
id: astro-deployment-airflow-variable-update
description: Reference documentation for astro deployment airflow-variable update.
hide_table_of_contents: true
---

For a given Deployment on Astro, update the airflow variables that are stored in the Airflow metadata database.

## Usage

```sh
astro deployment airflow-variable update
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
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to update airflow-variables                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment for which to update airflow variables. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Update airflow variables for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |
| `-k`,`--key`          | The Airflow variable key. Required.          | string                                                         |
| `-v`,`--value`          | The Airflow variable value. Required.           | string                                                         |
| `--description`          | The Airflow variable description.          | string                                                         |

## Examples

```sh
# update airflow-variable called my-airflow-variable stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
$ astro deployment airflow-variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --key my-variable ---value VAR

# update airflow-variables stored in the Deployment "My Deployment"
$ astro deployment airflow-variable update --deployment-name="My Deployment" --key my-variable ---value VAR

## Related Commands

- [`astro deployment airflow-variable create`](cli/astro-deployment-airflow-variable-create.md)
- [`astro deployment airflow-variable list`](cli/astro-deployment-airflow-variable-list.md)
