---
sidebar_label: 'Pipeline metrics'
title: 'Pipeline metrics'
id: pipeline-metrics
---

<head>
  <meta name="description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
  <meta name="og:description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
</head>

_Pipelines_ refers to the DAGs that you have deployed to Astro. To access the **Pipelines** page, you can either click the **Pipelines** icon in the UI or click **View DAGs** on a Deployment's information page.

## Pipelines overview

You can view key metrics about recent DAG runs using the **Pipelines** page in the Cloud UI. This page shows DAG runs from the last 14 days across either all Deployments or a specific Deployment in a Workspace. The **Pipelines** page shows the following summary information:

- Total DAG runsin the Pipeline over the last 14 days, expressed as a bar chart.

    Each bar in the chart represents an individual DAG run. A bar's color represents whether the DAG run was a success or a failure, while its length represents the total duration of the DAG run. If there are more than 14 DAG runs in the last 14 days, then the chart shows only the 14 most recent DAG runs.

- **Last Run**: The duration of the last DAG run and the ending time of the DAG's most recent DAG run, expressed relative to the current time.
- **Schedule**: The frequency that the DAG runs and the starting time of the next DAG run, expressed relative to the current time.
- **Runtime**: The Runtime type used for this DAG.
- **Owner(s)**: The Airflow DAG owner attribute. You can change the owner attribute when you write or update your DAG.
- **Tags** You can create custom tags for your Pipelines. These tags can be used to filter and sort your Pipelines. 

:::info DAG visibility

If a DAG run for any given DAG has not run in the last 14 days, then it will not appear in the **DAGs** view.

Additionally, the `astronomer_monitoring_dag` will never appear in this view even if it ran in the last 14 days.

:::

To view more detailed information about a specific Pipeline, you can either **Open in Airflow** or select the Pipeline to open more details. 

## Pipeline details

After you select a particular Pipeline in the **Pipelines** page, you can see detailed information about your DAG runs as well as the Airflow code for the DAG itself. In this view, you can 

- **Pause** or **Unpause** your DAG runs
- Trigger a DAG **Run**
- Open the DAG in Airflow
- Filter your Pipeline data by time, DAG Run Type, or DAG run status
- View your DAG run grid
- Copy your DAG schedule ID
- Edit your code in the IDE

![Detailed information and summary metrics about your DAG Pipelines.](/img/docs/pipeline-details.png)


