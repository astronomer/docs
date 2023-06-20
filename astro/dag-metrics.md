---
sidebar_label: 'DAGs'
title: 'View metrics for DAGs'
id: dag-metrics
---

<head>
  <meta name="description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
  <meta name="og:description" content="Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
</head>

:::info

DAG metrics are currently available only on [Astro Hosted](astro-overview.md). Support on Astro Hybrid is coming soon.

:::

The **DAGs** page in the Cloud UI lets you view and manage each DAG running on your Workspace. To access the **DAGs** page, you can either click **DAGs** on your sidebar or click **View DAGs** on a Deployment's information page.

## DAGs overview

The **DAGs** page shows the following summary information, all of which you can filter on using the left menu:

- Total DAG runs over the last 14 days, expressed as a bar chart.

    Each bar in the chart represents an individual DAG run. A bar's color represents whether the DAG run was a success or a failure, while its length represents the total duration of the DAG run. If there are more than 14 DAG runs in the last 14 days, then the chart shows only the 14 most recent DAG runs.

- **State**: Indicates whether the DAG is **Active** or **Paused**. If a DAG has a purple lightning symbol next to its name, that DAG is **Active**.
- **Last Run**: The duration of the last DAG run and the ending time of the DAG's most recent DAG run, expressed relative to the current time.
- **Schedule**: The frequency that the DAG runs and the starting time of the next DAG run, expressed relative to the current time.
- **Deployment**:  The Deployment ID of the Deployment for the current DAG Run.
- **Owner(s)**: The Airflow DAG owner attribute. You can change the owner attribute when you write or update your DAG.
- **Tags**: The custom tags that you marked your DAG with. To add custom tags to a DAG, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/add-dag-tags.html).

## View metrics for a DAG

To view more detailed information about a specific DAG, you can either **Open in Airflow** or select the DAG to manage it from the Cloud UI. See [Manage DAGs](manage-dags.md).

## See also 

- [Manage DAGs](manage-dags.md)

