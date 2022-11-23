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
astro deployment inspect <deployment-name> --key information.status
```

See [Example output](#example-output) for all possible values to return. 

## Example output

The following output is an example of what you receive when you run `astro deployment inspect <deployment-id>` with no other flags specified. It includes all possible values that you can return using the `--key` flag.

```yaml
deployment:
    alert_emails: []
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
        cluster_id: cl66604ph00tx0s2tb3v313qu
        description: ""
        name: Prod
        runtime_version: 6.0.2
        scheduler_au: 20
        scheduler_replicas: 2
    information:
        airflow_version: 2.4.1
        cluster_id: cl66604ph00tx0s2tb3v313qu
        created_at: 2022-08-08T18:12:18.566Z
        deployment_id: cl6l2mhvq280081b01cg9g9nzw
        deployment_url: cloud.astronomer.io/<deployment url>
        release_name: primitive-twinkling-4105
        status: HEALTHY
        updated_at: 2022-11-03T15:26:57.316Z
        webserver_url: <org>.astronomer.run/<deployment url>
        workspace_id: cl1ntvrrk411461gxsvvitduiy
    worker_queues:
        - id: cl8oigdwh135879hfw37mu9qrev
          is_default: false
          max_worker_count: 10
          min_worker_count: 0
          name: heavy-compute
          node_pool_id: cl8c3xz901505872c1d498z2zt9
          worker_concurrency: 16
        - id: cl6l2mhvq280121b01r5mkcj05
          is_default: true
          max_worker_count: 10
          min_worker_count: 1
          name: default
          node_pool_id: cl66604pi447851h2tpkvtlkrt
          worker_concurrency: 16
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
```

## Related Commands

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment create`](cli/astro-deployment-create.md)
