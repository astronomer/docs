---
sidebar_label: 'Datadog'
title: 'Export metrics and logs to Datadog'
id: export-datadog
description: "Configure your Deployment to forward observability data to your Datadog instance."
---

By forwarding Astro data to Datadog, you can integrate Astro into your existing observability practices by analyzing information about your Deployments' performance with Datadog cloud monitoring tools. Currently, you can send the following data to Datadog:

- Airflow task logs.
- Supported Datadog [Airflow metrics](https://docs.datadoghq.com/integrations/airflow/?tab=host#data-collected).

Complete the following setup to authenticate your Deployments to Datadog and forward your observability data to your Datadog instance.

## Export task logs to Datadog

You can forward Airflow task logs from a Deployment to [Datadog](https://www.datadoghq.com/) using a Datadog API key. This allows you to view and manage task logs across all Deployments from a centralized observability plane.

### Prerequisites

- Your Deployment must run Astro Runtime 9 (AWS) or 9.1 (Azure and GCP) or later. See [Upgrade Astro Runtime](upgrade-runtime.md).

### Setup

1. Create a new Datadog API key or copy an existing API key. See [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/).
2. Set the following [environment variable](environment-variables.md) on your Deployment:

    - **Key 1**: `DATADOG_API_KEY`
    - **Value 1**: Your Datadog API key.

    - **Key 2**: `ASTRO_DATADOG_TASK_LOGS_ENABLED`
    - **Value 2**: `true`

    Select the **Secret?** checkbox for `DATADOG_API_KEY`. This ensures that your Datadog API key is saved securely and is not available to Workspace users in plain text.

  :::info

  By default, the Astro Datadog integration also sends a Deployment's [Airflow metrics](deployment-metrics.md#export-airflow-metrics-to-datadog) to Datadog. To send only task logs to Datadog, add the following environment variable:

    - **Key**: `ASTRO_DATADOG_METRICS_DISABLED`
    - **Value**: `true`

  :::

3. (Optional) Set the following [environment variable](environment-variables.md) on your Deployment to send your logs to a specific [Datadog site](https://docs.datadoghq.com/getting_started/site/):

    - **Key**: `DATADOG_SITE`
    - **Value**: Your Datadog **Site Parameter**. For example, `datadoghq.com`.
   
4. (Optional) For Astro Runtime 9.2.0 and greater, set the following [environment variable](environment-variables.md) on your Deployment to [add specific tags to your logs](https://docs.datadoghq.com/getting_started/tagging/):

    - **Key**: `ASTRO_DATADOG_TASK_LOGS_TAGS`
    - **Value**: `<tag-key-1>:<tag-value-1>,<tag-key-2>:<tag-value-2>`

  By default, Astro uses the tags `source=astronomer` and `service=astronomer-task-logs`.


## Export Airflow metrics to Datadog

Export over 40 Airflow metrics related to the state and performance of your Astro Deployment to [Datadog](https://www.datadoghq.com/) by adding a Datadog API key to your Deployment. These metrics include most information that is available in the Cloud UI, as well as additional metrics that Datadog automatically collects, including number of queued tasks, DAG processing time, and more. For a complete list of supported metrics, see [Data Collected](https://docs.datadoghq.com/integrations/airflow/?tab=host#data-collected) in the Datadog documentation.

:::info

Astro does not export any [service checks](https://docs.datadoghq.com/integrations/airflow/?tab=host#service-checks) to Datadog. Information about the general health of your Deployment is available only as part of the Cloud UI's [Deployment health](#deployment-health) metric.

:::

1. Create a new Datadog API key or copy an existing API key. See [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/).
2. In the Cloud UI, select a Workspace and then select an Astro Deployment for which you want to export metrics.
3. Create a new [environment variable](environment-variables.md#set-environment-variables-in-the-cloud-ui) in your Deployment with the Datadog API key from step 1:
   
   - **Key:** `DATADOG_API_KEY`
   - **Value:** `<Your-Datadog-API-key>`.
  
   Select the **Secret?** checkbox. This ensures that your Datadog API key is saved securely and is not available to Workspace users in plain text.

4. (Optional) Add the following environment variable if your organization doesn't use the default Datadog site `datadoghq.com`:
   
   - **Key:** `DATADOG_SITE`
   - **Value:** `<Your-Datadog-Site>`
  
5. (Optional) Add the following environment variables to create [custom Datadog tags](https://docs.datadoghq.com/getting_started/tagging/) associated with your Deployment:

   - **Key 1**: `AIRFLOW__METRICS__STATSD_DATADOG_ENABLED`
   - **Value 1**: `True`

  
    - **Key 2**: `AIRFLOW__METRICS__STATSD_DATADOG_TAGS`
   - **Value 2**: `<tag-key-1>:<tag-value-1>,<tag-key-2>:<tag-value-2>`
   
6. Click **Save variable**.

After you complete this setup, Astro automatically launches a sidecar container in your Deployment that runs [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent). This container works with your Deployment's existing infrastructure to export Airflow metrics to the Datadog instance associated with your API key.

### View metrics in Datadog

1. In the Datadog UI, go to **Metrics** > **Summary**.
2. Search for metrics starting with `airflow` and open any Airflow metric.
3. In the **Tags** table, check the values for the `namespace` tag key. The namespaces of the Deployments you configured to export logs should appear as tag values.

To check the health of a Deployment's DogStatsD container, open the `datadog.dogstatsd.running` metric in the Datadog UI. If the Deployment's namespace appears under the metric's `host` tag key, its DogStatsD container is healthy and exporting metrics to Datadog.