---
sidebar_label: "astro dbt deploy"
title: "astro dbt deploy"
id: astro-dbt-deploy
description: Deploy a dbt project to an Astro Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::privatepreview
:::

:::info

This command is only available on Astro.

:::

This command allows you to deploy your dbt code to Astro, instead of writing your data transformation processes in Python.

This command bundles all files in your dbt project and pushes them to Astro. Before completing the process, it tests your DAGs in your Astro project for errors. If this test fails, the deploy to Astro will also fail.

When you run `astro dbt deploy`, the CLI prompts you to select from a list of all Deployments that you can access across Workspaces. To bypass this prompt, you can also specify a Deployment ID in the command. To retrieve a Deployment ID, open your Deployment in the Astro UI and copy the value in the **ID** section of the Deployment page. You can also run `astro deployment list` to find a Deployment ID or name.

## Usage

```bash
astro dbt deploy <your-deployment-id> <options>
```

## Options

| Option              | Description                                                                       | Possible Values           |
| ------------------- | --------------------------------------------------------------------------------- | ------------------------- |
| `-n`, `--deployment-name` | Name of the Deployment to deploy your dbt project to | Any valid Deployment ID |
| `--description` | Description of the project to store on the deploy | String |
| `-m`, `--mount-path` | Path describing where to mount the dbt project in Airflow, so that it is accessible to your DAGs. Default path is `/usr/local/airflow/dbt/<dbt-project-name>` | Any valid path except  `/usr/local/airflow/dags`, which is used for DAG deploys |
| `-p`, `--project-path` | Path to the dbt project that you want to deploy. The default is your current directory | Any valid filepath to a dbt project |
| `-w`, `--wait` | Wait for the Deployment to become healthy before ending the deploy command. Default is `False` | `True` or `False` |
| `--workspace-id` | The Workspace ID for the Deployment where you want to deploy your dbt project | Any valid Workspace ID |

## Examples

To deploy directly to a specific Deployment:

```bash
astro dbt deploy <add-example-id>
```

to deploy a project to a specific deployment on the mount path, `example-path`.

```bash
astro dbt deploy <add-example-id> --mount-path="<need-example-path>"
```

## Related commands

- [`astro dbt delete`](astro-dbt-delete.md)
- [`astro deployment list`](astro-deployment-list.md)