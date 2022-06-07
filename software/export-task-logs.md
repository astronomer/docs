---
sidebar_label: 'Export Task Logs'
title: 'Export Task Logs to ElasticSearch'
id: export-task-logs
description: Configure how Astronomer exports task logs to your ElasticSearch instance.
---

## Overview

Airflow task logs are stored in a logging backend to ensure you can access them after your Pods terminate. By default, Astronomer uses [Fluentd](https://www.fluentd.org/) to collect task logs and export them to an ElasticSearch instance.

You can configure how Astronomer collects Deployment task logs and exports them to ElasticSearch. The following are the supported methods for exporting task logs to ElasticSearch:

- Using a Fluentd Daemonset pod on each Kubernetes node in your cluster.
- Using container sidecars for Deployment components.

## Export Task Logs Using a Fluentd DaemonSet

By default, Astronomer Software uses a Fluentd Daemonset to aggregate task logs. The is the workflow for the default implementation:

- Deployments write task logs to stdout.
- Kubernetes takes the output from stdout and writes it to the Deployment’s node.
- A Fluentd pod reads logs from the node and forwards them to ElasticSearch.

This implementation is recommended for organizations that:

- Run longer tasks using CeleryExecutor.
- Run Astronomer Software in a dedicated cluster.
- Run privileged containers in a cluster with a ClusterRole.

This approach is not suited for organizations that run many small tasks using the KubernetesExecutor. Because task logs exist only for the lifetime of the pod, your pods running small tasks might complete before Fluentd can collect their task logs.

## Export Logs Using Container Sidecars

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

### Configure Logging Sidecars

1. Locate your Astronomer Software `config.yaml`. To retrieve it programatically, run the following:

    ```bash
    # platform-release-name is usually "astronomer"
    helm get values <your-platform-release-name> astronomer/astronomer -n astronomer
    ```

2. Add the following entry to your `config.yaml:`

    ```yaml
    global:
      fluentdEnabled: false
      loggingSidecar:
        enabled: true
        name: sidecar-log-consumer
        # needed to prevent zombie deployment worker pods when using KubernetesExecutor
        terminationEndpoint: http://localhost:8000/quitquitquit
    ```

3. Push the configuration change. See [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config)


:::info

To revert to the default behavior and export task logs using a Fluentd Daemonset, remove this configuration from your `config.yaml` file.

:::
