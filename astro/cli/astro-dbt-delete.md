---
sidebar_label: "astro dbt delete"
title: "astro dbt delete"
id: astro-dbt-delete
description: Delete a dbt project from an Astro Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::privatepreview
:::

:::info

This command is only available on Astro.

:::

Delete a dbt project for a Deployment on Astro. This command deletes a dbt project from the Airflow environments where you deployed it.

When you run `astro dbt delete`, you are prompted to select from a list of Deployments that you can access in your Workspace. You can bypass this prompt and specify a Deployment name or ID in the command. To retrieve a Deployment ID, open your Deployment in the Astro UI and copy the value in the **ID** section of the Deployment page. You can also run `astro deployment list` to find a Deployment ID or name.

:::info

To complete this action, [Workspace Owner](user-permissions.md#workspace-roles) permissions are required.

:::

## Usage

```bash
astro dbt delete <your-deployment-id> <options>
```

## Options

| Option              | Description                                                                       | Possible Values           |
| ------------------- | --------------------------------------------------------------------------------- | ------------------------- |
| `-n`, `--deployment-name` | Name of the Deployment to delete your dbt project from | Any valid Deployment ID |
| `--description` | Description of the project to store on the deploy | String |
| `-m`, `--mount-path` | Path describing where the dbt project you want to delete is mounted in Airflow. Default path is `/usr/local/airflow/dbt/<dbt-project-name>` | Any valid path |
| `-p`, `--project-path` | Path to the dbt project that you want to delete. The default is your current directory | Any valid filepath to a dbt project |
| `-w`, `--wait` | Wait for the Deployment to become healthy before ending the delete command. Default is `False` | `True` or `False` |
| `--workspace-id` | The Workspace ID for the Deployment from where you want to delete your dbt project | Any valid Workspace ID |

## Examples

To delete a dbt project from a specific Deployment:

```bash
astro dbt delete clyxf6ivz000008jth73k37r6
```

To delete a project that has the mount path, `/usr/local/airflow/dbt/test-dbt-project` from a specific Deployment.

```bash
astro dbt delete clyxf6ivz000008jth73k37r6 --mount-path="/usr/local/airflow/dbt/test-dbt-project"
```

## Related commands

- [`astro dbt delete`](astro-dbt-delete.md)
- [`astro deployment list`](astro-deployment-list.md)