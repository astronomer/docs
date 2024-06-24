---
sidebar_label: 'Universal Metrics Export'
title: 'Export metrics from Astro'
id: metrics-export
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import TeamBadge from '@site/src/components/TeamBadge';

<TeamBadge/>

:::publicpreview
:::

You can export comprehensive metrics about your Astro Deployments from Astro directly to any third-party monitoring and alerting systems. The universal metrics exporter uses the[OpenTelemetry (OTel)](https://opentelemetry.io/docs/) protocol to ensure that measurements about your Astro Deployments can be exported and used across any OTel compatible tool.

This functionality allows you to move operational data about your Astro Deployments to your prefferred monitoring tools, like Prometheus.

## Metric types

- Application level metrics: Metrics defined by Airflow, or custom metrics you write, about the health, success, and performance of data pipelines orchestrated and executed by Airflow.

- Infrastructure level metrics: Metrics about running pods for the different Airflow components. These indicate of the use, health, and performance of the pods based on your workload and pipelines.

## Prerequisites

-



