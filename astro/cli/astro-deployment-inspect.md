---
sidebar_label: "astro deployment inspect"
title: "astro deployment inspect"
id: astro-deployment-inspect
description: Reference documentation for astro deployment inspect.
hide_table_of_contents: true
---

Inspect an Astro Deployment. This command returns a yaml or json representation of a Deployment's current configuration and state. See the example below for a full list values that can be returned. You can return a specfic value using the `--key` flag. Give the "path" to the value you want to return as an argument to the `--key` flag. For example `astro deployment inspect <deployment-id> --key configuration.cluster_id` will return a Deployment's Cluster ID.

## Usage

```sh
astro deployment inspect <deployment-id>
```

## Deployment YAML Example

```yaml
deployment:
    alert_emails: []
    astronomer_variables:
        - is_secret: true
          key: AWS_ACCESS_KEY_ID
          updated_at: "2022-09-26T13:57:36.564Z"
          value: ""
        - is_secret: true
          key: AWS_SECRET_ACCESS_KEY
          updated_at: "2022-09-26T13:57:36.564Z"
          value: ""
        - is_secret: false
          key: AWS_DEFAULT_REGION
          updated_at: "2022-09-26T13:58:54.427Z"
          value: us-east-1
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

| Option           | Description                                                               | Possible Values        |
| ---------------- | ------------------------------------------------------------------------- | ---------------------- |
| `-n`, `--deployment-name`     |  Name of the deployment to inspect.           | An Valid Deployment Name                  |
| `--workspace-id` | Specify a Workspace to list Deployments outside of your current Workspace | Any valid Workspace ID |
| `-k`, `--key` | A specific key for the deployment. For example `--key configuration.cluster_id` to get a deployment's cluster id. | Any valid Workspace ID |
| `-o`, `--output` | Output format can be one of: yaml or json. By default the inspected deployment will be in YAML format. (default "yaml") | yaml or json |

## Examples

```sh
# Shows a list of Deployments to inspect
$ astro deployment inspect

# Shows a particular Deployment's configuration
$ astro deployment inspect <deployment-id>

# Shows a particular deployments health status
$ astro deployment inspect <deployment-id> -k information.status
$ HEALTHY
```

## Related Commands

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment create`](cli/astro-deployment-create.md)
