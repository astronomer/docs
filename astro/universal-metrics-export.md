---
sidebar_label: 'Universal Metrics Export'
title: 'Export metrics from Astro'
id: metrics-export
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import TeamBadge from '@site/src/components/TeamBadge';
import HostedBadge from '@site/src/components/HostedBadge';

<TeamBadge/>

:::publicpreview
:::

You can export comprehensive metrics about your Astro Deployments from Astro directly to any third-party monitoring and alerting systems. The universal metrics exporter uses the[OpenTelemetry (OTel)](https://opentelemetry.io/docs/) protocol to ensure that measurements about your Astro Deployments can be exported and used across any OTel compatible tool.

This functionality allows you to move operational data about your Astro Deployments to your prefferred monitoring tools, like Prometheus.

## Metric types

- Application level metrics: Metrics defined by Airflow, or custom metrics you write, about the health, success, and performance of data pipelines orchestrated and executed by Airflow.

- Infrastructure level metrics: Metrics about running pods for the different Airflow components. These indicate of the use, health, and performance of the pods based on your workload and pipelines.

## Prerequisites

- A data observability Prometheus server
- Bearer token or license key of your target Prometheus server.

## Enable metrics export

You can enable metrics export at either the Deployment and Workspace level for Astro Hosted.

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

<!-- HOW TO CONFIRM SUCCESSFUL EXPORT?-->

## Share metrics exports across Deployments

After you configure metrics export at the Workspace level, you can link it to multiple Deployments. Linking an export target is useful for standardizing observability pipelines and streamlining monitoring.

For the most flexibility, you can set a default server to export development environment metrics to, and then later override the configuration per-Deployment based on your needs.

1. Click **Environment** in the main menu and open the **Metrics Export** page.
2. Click the name of the export target that you want to add per-Deployment field overrides to.
3. Click **Export sharing** and toggle the setting to choose either:
    - **Restricted**: Only share individually to Deployments.
    - **Linked to all Deployments**: Link to all current and future Deployments in this Workspace.
4. (Optional) Change the default field values.
5. Click **Update metrics export** to save.