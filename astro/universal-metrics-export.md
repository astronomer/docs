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

You can export comprehensive metrics about your Astro Deployments directly to any third-party monitoring and alerting system using the universal metrics exporter in Astro. This incorporates metrics about your Astro resource use and performance into your existing obsevability tooling, which gives you access to the data you need to right size Celery workers, Kubernetes executors, and scheduler pods as well as keep you informed about Airflow uptime and task execution status. The universal metrics exporter uses the [Prometheus data model](https://prometheus.io/docs/concepts/data_model/) format using the remote-write capability to export metrics about your Astro Deployments to your preferred monitoring tools.

This universal metrics export also provides an alternative to other Astro observability tools, such as viewing [Deployment metrics](deployment-metrics.md) and [exporting metrics and logs to Datadog](export-datadog.md), which are limited to [Datadog's supported Airflow metrics](https://docs.datadoghq.com/integrations/airflow/?tab=host#data-collected).

With the metrics export, you can configure metrics export at the per-Deployment level. Or, you can define a default metrics exports for your entire Workspace, so that you can create a default process that all Deployments are created with and then later customize at the per-Deployment level.

## Metric types

There are two types of metrics that you can export using the universal metrics exporter:

- Airflow application level metrics
- Infrastructure level metrics

Both application and infrastructure metrics have metadata labels associated with them. The following list shows the default standard set of labels that Astro attaches to each metric, however, each metric can also include metric-specific labels as well:

- `cloud_provider`
- `cloud_region`
- `cluster_organization_id`
- `container`
- `namespace`
- `pod`
- `deploymentId`
- `organizationId`
- `workspaceId`

Use these metadata labels to indentify each individual metric with its corresponding environment in Astro.

### Airflow application metrics

Airflow application metrics are defined by Apache Airflow and are related to the health, success, and performance of the DAGs that are orchestrated and executed by Airflow.

For example, Airflow application metrics include:

- The number of task instance failures in your Deployment
- The number of SLA misses in your Deployment
- The number of zombie tasks killed
- The historical count of scheduler hearbeats

To see the complete list of Airflow application metrics that Astro supports, see [the Astro StatsD repository](https://github.com/astronomer/ap-vendor/blob/main/statsd-exporter/include/mappings-gen2.yml). To learn more, read the [descriptions of each metric Airflow metrics descriptions in Airflow documentation.
](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/metrics.html#metric-descriptions).

### Infrastructure level metrics

Infrastructure level metrics can help you understand information about the individual nodes and pods that run each Airflow component. These metrics indicate the usage, health, and performance of the pods based on your workload and use case. See the table below for the list of infrastructure metrics that Astro supports.

| Name                                          | Description                             |
| --------------------------------------------- | --------------------------------------- |
| `container_cpu_usage_seconds_total`           | CPU usage                               |
| `container_memory_working_set_bytes`          | Memory usage                            |
| `kubelet_stats_ephemeral_storage_pod_usage`   | Ephemeral storage usage                 |
| `kube_pod_status_*`                           | Kubernetes pod status                   |
| `kube_pod_labels`                             | Kubernetes pod label                    |
| `kube_pod_container_status_terminated_reason` | Kubernetes container termination reason |

## Prerequisites

- Supported Auth: Bearer token or license key, username and password, or custom HTTP header(s) of your target data observability server _(Optional)_
- A Prometheus data endpoint
- Network connectivity between your Astro resources and Prometheus endpoint

### Set up your Prometheus endpoint

The following list includes the setup instructions of different commonly used prometheus endpoints. Use these resources to set up your observability tools to receive metrics exports from Astro.

- [Chronosphere](https://docs.chronosphere.io/ingest/collector/configure/prometheus-backend)
- [Coralogix](https://coralogix.com/docs/prometheus/)
- [Cribl](https://docs.cribl.io/stream/4.2/sources-prometheus-remote-write/)
- [Elastic](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-metricset-prometheus-remote_write.html)
- [Grafana Cloud](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/configure-infrastructure-manually/prometheus/)
- [Logz.io](http://Logz.iohttps://docs.logz.io/docs/shipping/other/prometheus-remote-write/)
- [New Relic](https://docs.newrelic.com/docs/infrastructure/prometheus-integrations/install-configure-remote-write/set-your-prometheus-remote-write-integration/)
- [Sysdig](https://docs.sysdig.com/en/docs/installation/sysdig-monitor/install-prometheus-remote-write/#configure-remote-write-in-prometheus-server)

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
