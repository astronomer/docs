---
sidebar_label: 'Export Task Logs'
title: 'Export Task Logs to ElasticSearch'
id: export-task-logs
description: Configure how Astronomer exports task logs to your ElasticSearch instance.
---

## Overview

Because Software Deployments run on Kubernetes Pods that are ephemeral by nature, Airflow task logs must be stored in a logging backend to ensure they can continue to be accessed even after your Pods terminate. By default, Astronomer uses [Fluentd](https://www.fluentd.org/) to collect task logs and export them to an ElasticSearch instance.

To have more control over how your system reads your Airflow task logs, you can configure how Astronomer collects Deployment task logs and exports them to ElasticSearch.

Astronomer supports two different methods for exporting task logs to ElasticSearch:

- Export task logs using a Fluentd Daemonset pod on each Kubernetes node in your cluster.
- Export task logs using container sidecars for Deployment components.

## Export Task Logs Using a Fluentd DaemonSet

By default, Astronomer Software uses a Fluentd Daemonset to aggregate task logs. In the default implementation:

1. Deployments write task logs to stdout.
2. Kubernetes takes the output from stdout and writes it to the Deployment’s node.
3. A Fluentd pod reads logs from the node and forwards them to ElasticSearch.

This approach works best for organizations that:

- Run longer tasks using CeleryExecutor.
- Run Astronomer Software in a dedicated cluster.
- Can run privileged containers in a cluster with a clusterrole.

This approach is not suited for organizations that run many small tasks using the KubernetesExecutor. Because task logs exist only for the lifetime of the pod, your pods running small tasks might spin down before Fluentd can collect their task logs.

## Exporting Logs Using Container Sidecars

You can use a logging sidecar container to collect and export logs. In this implementation:

1. Each container running an Airflow component for a Deployment receives its own [Vector](https://vector.dev/) sidecar.
2. Task logs are written to a shared directory .
3. The Vector sidecar reads logs from the shared directory and writes them to ElasticSearch .

This approach is best suited for organizations that:

- Run Astronomer Software in a multi-tenant cluster, where security is a concern.
- Use the KubernetesExecutor to run many short-lived tasks, which requires improved reliability.

The downside to this implementation is that the Vector sidecars each utilize 100m cpu and 384Mi memory. Therefore, more compute and memory resources are used for exporting logs with sidecars than when using a Fluentd Daemonset.

### Configure Logging Sidecars

To enable sidecar logging, please follow the steps below:

1. Locate your Astronomer Software `config.yaml`. To retrieve it programatically, run the following:

    ```bash
    # platform-release-name is usually "astronomer"
    helm get values <your-platform-release-name> astronomer/astronomer -n astronomer
    ```

2. And the below to your `config.yaml:`

    ```yaml
    global:
      fluentdEnabled: false
      loggingSidecar:
        enabled: true
        name: sidecar-log-consumer
        # needed to prevent zombie deployment worker pods when using KubernetesExecutor
        terminationEndpoint: http://localhost:8000/quitquitquit
    ```

3. Push the configuration change as described in [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config)


:::info

To revert to Astronomer's default behavior of exporting task logs using a Fluentd Daemonset, remove this configuration from your `config.yaml` file.

:::
