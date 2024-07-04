---
sidebar_label: "Export metrics"
title: "Export metrics from Astro"
id: export-metrics
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import TeamBadge from '@site/src/components/TeamBadge';
import HostedBadge from '@site/src/components/HostedBadge';

<TeamBadge/>

:::publicpreview
:::

You can export comprehensive metrics about your Astro Deployments directly to any third-party monitoring and alerting system using the universal metrics exporter in Astro. The universal metrics exporter uses the [Prometheus data model](https://prometheus.io/docs/concepts/data_model/) format using the remote-write capability to export metrics about your Astro Deployments to your preferred monitoring tools.

## Metric types

You can export the following types of metrics using the universal metrics exporter: 

- Airflow application level metrics: These are metrics defined by Apache Airflow that are related to the health, success, and performance of the DAGs that are orchestrated and executed by Airflow. You can see the specific list of [application metrics](https://github.com/astronomer/ap-vendor/blob/main/statsd-exporter/include/mappings-gen2.yml) and read their corresponding descriptions in the [Airflow metrics descriptions](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/metrics.html#metric-descriptions). For example, Airflow application metrics include the number of task instance failures, the number of SLA misses, and number of zombie tasks killed.

- Infrastructure level metrics: Metrics about running pods for the different Airflow components. These indicate the usage, health, and performance of the pods based on your workload and pipelines. See the table below for the list of infrastructure metrics that Astro supports.

  | Name                                        | Description           |
  | ------------------------------------------- | --------------------- |
  | `container_cpu_usage_seconds_total`         | CPU usage               |
  | `container_memory_working_set_bytes`        | Memory usage            |
  | `kubelet_stats_ephemeral_storage_pod_usage` | Ephemeral storage usage |
  | `kube_pod_status_*`                         | Kubernetes pod status |
  | `kube_pod_labels`                           | Kubernetes pod label  |

- Metadata labels: Both application and infrastructure metrics have the following metadata labels associated with them.
  - `cloud_provider`
  - `cloud_region`
  - `cluster_organization_id`
  - `container`
  - `namespace`
  - `pod`
  - `deploymentId`
  - `organizationId`
  - `workspaceId`

## Prerequisites

- Supported Auth: Bearer token or license key, username and password, or custom HTTP header(s) of your target data observability server _(Optional)_
- A Prometheus data endpoint
- Network connectivity between your Astro resources and Prometheus endpoint

## Enable metrics export

You can enable metrics export at both the Workspace and Deployment level for Astro Hosted, but only in individual Deployments for Astro Hybrid.

### Workspace metrics

<HostedBadge/>

1. In the Astro UI, select **Environment** on the sidebar menu.
2. Click the **Metrics Export** tab to configure your metrics export.
3. Click **+ Metrics Export** to create a new export connection.
4. Enter the required information for your export.
5. Click **Create metrics export**.
6. (Optional) Allow all Deployments to link to this metrics export configuration. See [Link metrics export](#link-exports).

### Deployment metrics

1. In the Astro UI, select a Deployment, then click the **Environment** tab within the Deployment menu.
2. Click the **Metrics** tab to configure your metrics export.
3. Click **+ Metrics Export** to configure a new export connection.
4. Enter the required information for your export.
5. Click **Create metrics export**.

If you successfully connected your metrics export to your observability service endpoint, after five minutes, your Astro metrics begin to populate in your observability service.

## Share metrics exports across Deployments

<HostedBadge/>

You can configure Astro to link Workspace-level metrics exports to all Deployments in the Workspace by default.

This is useful, for example, when you need to configure a metrics export for development environments that all Deployments in a Workspace should start with. Then, when you create new Deployments, they automatically have a default metrics export configuration to your development resources.

When you're ready to move your Deployments' metrics exports to production configurations, you can either replace the metrics export or [override the configuration](#override-configuration) values with your production resource information.

If you change the setting from **Restricted** to **Linked to all Deployments**, Astro respects any metrics exports fields that you might have configured for existing linked Deployments.

1. Click **Environment** in the main menu and open the **Metrics Export** page.
2. Click the name of the export target that you want to add per-Deployment field overrides to.
3. Click **Export sharing** and toggle the setting to choose either:
   - **Restricted**: Only share individually to Deployments.
   - **Linked to all Deployments**: Link to all current and future Deployments in this Workspace.
4. (Optional) Change the default field values.
5. Click **Update metrics export** to save.

## Override configuration fields

<HostedBadge/>

If you create a metrics export at the Workspace level and link it to a Deployment, you can later edit the endpoint within the Deployment to specify field overrides. When you override a field, you specify values that you want to use for a one Deployment, but not for others. This way, you can configure a metrics export for a single time, but still have the flexibility to customize it at the Deployment level.

For example, you might have created a metrics connection to a dev or internal observability endpoint, and then later you can add field overrides to specify production details you want each Deployment to use.

1. Click **Environment** in the main menu, and click the **Metrics Export** tab.
2. Click the metrics export that you want to add per-Deployment field overrides to.
3. (Optional) Click **Deployment Sharing** and choose if you want to **Restrict** or **Link to all Deployments**. You can also change the default field values. Click **Update metrics export** to save.
4. Click **Edit** to open the metrics export configurations for a specific linked Deployment.
5. Add the override values to the fields you want to edit. You might need to open **More options** to find the full list of available fields.
6. Click **Update metrics export**.
