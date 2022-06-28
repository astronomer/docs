---
sidebar_label: 'Export task logs'
title: 'Export task logs to ElasticSearch'
id: export-task-logs
description: Configure how Astronomer exports task logs to your ElasticSearch instance.
---

## Overview

Airflow task logs are stored in a logging backend to ensure you can access them after your Pods terminate. By default, Astronomer uses [Fluentd](https://www.fluentd.org/) to collect task logs and export them to an ElasticSearch instance.

You can configure how Astronomer collects Deployment task logs and exports them to ElasticSearch. The following are the supported methods for exporting task logs to ElasticSearch:

- Using a Fluentd Daemonset pod on each Kubernetes node in your cluster.
- Using container sidecars for Deployment components.

## Export task logs Using a Fluentd DaemonSet

By default, Astronomer Software uses a Fluentd DaemonSet to aggregate task logs. The is the workflow for the default implementation:

- Deployments write task logs to stdout.
- Kubernetes takes the output from stdout and writes it to the Deployment’s node.
- A Fluentd pod reads logs from the node and forwards them to ElasticSearch.

This implementation is recommended for organizations that:

- Run longer tasks using Celery executor.
- Run Astronomer Software in a dedicated cluster.
- Run privileged containers in a cluster with a ClusterRole.

This approach is not suited for organizations that run many small tasks using the Kubernetes executor. Because task logs exist only for the lifetime of the pod, your pods running small tasks might complete before Fluentd can collect their task logs.

## Export logs using container sidecars

You can use a logging sidecar container to collect and export logs. In this implementation:

- Each container running an Airflow component for a Deployment receives its own [Vector](https://vector.dev/) sidecar.
- Task logs are written to a shared directory.
- The Vector sidecar reads logs from the shared directory and writes them to ElasticSearch.

This implementation is recommended for organizations that:

- Run Astronomer Software in a multi-tenant cluster, where security is a concern.
- Use the KubernetesExecutor to run many short-lived tasks, which requires improved reliability.

:::caution

With this implementation, the Vector sidecars each utilize 100m cpu and 384Mi memory. More compute and memory resources are used for exporting logs with sidecars than when using a Fluentd Daemonset.

:::

### Configure logging sidecars

1. Retrieve your `config.yaml` file. See [Apply a config change](apply-platform-config.md)
2. Add the following entry to your `config.yaml` file:

    ```yaml
    global:
      fluentdEnabled: false
      loggingSidecar:
        enabled: true
        name: sidecar-log-consumer
        # needed to prevent zombie deployment worker pods when using KubernetesExecutor
        terminationEndpoint: http://localhost:8000/quitquitquit
    ```
3. Push the configuration change. See [Apply a config change](apply-platform-config.md)


:::info

To revert to the default behavior and export task logs using a Fluentd Daemonset, remove this configuration from your `config.yaml` file.

:::
