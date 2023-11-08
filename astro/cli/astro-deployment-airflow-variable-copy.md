---
sidebar_label: "astro deployment airflow-variable copy"
title: "astro deployment airflow-variable copy"
id: astro-deployment-airflow-variable-copy
description: Copy an Airflow variable from a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Copy Airflow variables from one Astro Deployment to another. Airflow variables are stored in the target Deployment's metadata database and appear in the Airflow UI.  

## Usage

```sh
astro deployment airflow-variable copy
```

This command only copies Airflow variables that were configured through the Airflow UI or Airflow REST API

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), you can generate a Deployment or Workspace API Token and set the following OS-level environment variable in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-s`,`--source-id`           |    The ID of the Deployment to copy Airflow variables from.                                             | Any valid Deployment ID |
| `-n`, `--source-name` | The name of the Deployment from which to copy Airflow variables. Use as an alternative to `<source-id>`. | Any valid Deployment name                                            |
| `-t`, `--target-id` | The ID of the Deployment to receive the copied Airflow variables                                     |
| `--target-name` | The name of the Deployment to receive the copied Airflow variables.  Use as an alternative to `<target-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Specify to copy Airflow variables to a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.          | Any valid Workspace ID                                                         |

## Examples

```bash
# copy airflow variables stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv to a deployment with an ID of cl03oiq7d80402nwn7fsl3dcd
astro deployment airflow-variable copy --source-id cl03oiq7d80402nwn7fsl3dmv --target cl03oiq7d80402nwn7fsl3dcd

# copy airflow variables stored in the Deployment "My Deployment" to another Deployment "My Other Deployment"
astro deployment airflow-variable copy --source-name="My Deployment" --target-name="My Other Deployment"
```

## Related Commands

- [`astro deployment airflow variable create`](cli/astro-deployment-airflow-variable-create.md)
- [`astro deployment airflow variable update`](cli/astro-deployment-airflow-variable-update.md)
