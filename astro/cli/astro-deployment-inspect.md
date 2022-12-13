---
sidebar_label: "astro deployment inspect"
title: "astro deployment inspect"
id: astro-deployment-inspect
description: Reference documentation for astro deployment inspect.
hide_table_of_contents: true
---

Inspect an Astro Deployment. This command returns a YAML or JSON representation of a Deployment's current configuration and state as shown in the Cloud UI. When the `--key` flag is used, it returns only the values specified with the flag.

## Usage

```sh
astro deployment inspect
```

When using the `--key` flag, specify the complete path of the key you want to return the value for, excluding `deployment`. For example, to return the `cluster_id` for a specific Deployment, you would run:

```sh
astro deployment inspect <deployment-name> --key configuration.cluster_id
```

See [Example output](#example-output) for all possible values to return. 

## Example output

The following output is an example of what you receive when you run `astro deployment inspect <deployment-id>` with no other flags specified. It includes all possible values that you can return using the `--key` flag.

```yaml
deployment:
    astronomer_variables:
        - is_secret: false
          key: AWS_DEFAULT_REGION
          updated_at: "2022-09-26T13:58:54.427Z"
          value: us-east-1
        - is_secret: true
          key: AWS_ACCESS_KEY_ID
          updated_at: "2022-09-26T13:57:36.564Z"
          value: ""
        - is_secret: true
          key: AWS_SECRET_ACCESS_KEY
          updated_at: "2022-09-26T13:57:36.564Z"
          value: ""
    configuration:
        name: Prod
        description: ""
        runtime_version: 6.0.2
        scheduler_au: 20
        scheduler_count: 2
        cluster_name: Prod Cluster
        workspace_name: Data Engineering
    worker_queues:
        - name: heavy-compute
          is_default: false
          max_worker_count: 10
          min_worker_count: 0
          worker_concurrency: 16
          worker_type: m5.xlarge
        - name: default
          is_default: true
          max_worker_count: 10
          min_worker_count: 1
          worker_concurrency: 16
          worker_type: m5.xlarge
    alert_emails:
        - me@myorganization.com
        - me2@myorganization.com
# not needed or used when creating/updating a deployment
    metadata:
        deployment_id: cl6l2mhvq280081b01cg9g9nzw
        workspace_id: cl0v1p6lc728255byzyfs7lw21
        cluster_id: cl66604ph00tx0s2tb3v313qu
        release_name: primitive-twinkling-4105
        airflow_version: 2.4.1
        status: HEALTHY
        created_at: 2022-08-08T18:12:18.566Z
        updated_at: 2022-11-03T15:26:57.316Z
        deployment_url: cloud.astronomer.io/<deployment url>
        webserver_url: <org>.astronomer.run/<deployment url>
```

## Options

| Option                    | Description                                                                                                             | Possible Values          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `-n`, `--deployment-name` | Name of the Deployment to inspect. Use as an alternative to `<deployment-id>`.                                                                                     | Any valid Deployment name |
| `<deployment-id>`   | The ID of the Deployment to inspect.                                                | Any valid Deployment ID   |
| `--workspace-id`          | Specify a Workspace to run this command for a Deployment that is outside of your current Workspace.                                               | Any valid Workspace ID   |
| `-k`, `--key`             | Return only a specific configuration key for a Deployment. For example `--key configuration.cluster_id` to get a Deployment's cluster ID.       | Any valid Deployment configuration key   |
| `-o`, `--output`          | Output format can be one of: YAML or JSON. By default, inspecting a Deployment returns  a file in YAML format. | `yaml` or `json`             |

## Examples

```sh
# Shows a list of Deployments to inspect and prompts you to choose one
$ astro deployment inspect

# Shows a specific Deployment's configuration
$ astro deployment inspect <deployment-id>

# Shows a specific Deployment's health status
$ astro deployment inspect <deployment-id> --key information.status

# store a Deployment's configuration in a deployment file
$ astro deployment inspect <deployment-id> > deployment.yaml
```

:::note
For more inforamtion on Deploymen files read [Manage Deployments as Code](manage-deployments-as-code.md)
:::

## Related Commands

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment create`](cli/astro-deployment-create.md)
