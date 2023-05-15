---
sidebar_label: 'DAGs'
title: 'View metrics for DAGs'
id: dag-metrics
---

<head>
  <meta name="description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
  <meta name="og:description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
</head>

The **DAGs** page in the Cloud UI lets you view and manage each DAG running on your Workspace. To access the **DAGs** page, you can either click **DAGs** on your sidebar or click **View DAGs** on a Deployment's information page.

## DAGs overview

The **DAGs** page shows DAG runs from the last 14 days across either all Deployments or a specific Deployment in a Workspace. The **Pipelines** page shows the following summary information:

- Total DAG runs over the last 14 days, expressed as a bar chart.

    Each bar in the chart represents an individual DAG run. A bar's color represents whether the DAG run was a success or a failure, while its length represents the total duration of the DAG run. If there are more than 14 DAG runs in the last 14 days, then the chart shows only the 14 most recent DAG runs.

- **State**: Indicates whether the DAG is **Active** or **Paused**. If a DAG has a purple lightning symbol next to its name, that DAG is **Active**.
- **Last Run**: The duration of the last DAG run and the ending time of the DAG's most recent DAG run, expressed relative to the current time.
- **Schedule**: The frequency that the DAG runs and the starting time of the next DAG run, expressed relative to the current time.
- **Owner(s)**: The Airflow DAG owner attribute. You can change the owner attribute when you write or update your DAG.
- **Tags**: The custom tags that you marked your DAG with. To add custom tags to a DAG, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/add-dag-tags.html).

:::info DAG visibility

If a DAG run for any given DAG has not run in the last 14 days, then it will not appear in the **DAGs** view.

:::

To view more detailed information about a specific DAG, you can either **Open in Airflow** or select the DAG to open more details. 

