---
sidebar_label: 'DAGs'
title: 'View DAG metrics in Astro'
id: dag-metrics
description: "Learn how to monitor Pipeline performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting."
---

The **DAGs** page in the Cloud UI lets you view and manage each DAG running on your Workspace. You can view high level metrics about each DAG in a summary table, or select specific DAGs to view DAG code and the status of DAG runs. Use the **DAGs** page to check the performance of DAGs and debug issues in your DAG code based on your DAG run statuses.

To access the **DAGs** page, either click **DAGs** on the left sidebar or click **View DAGs** on a Deployment's information page.

![The DAGs page in the Cloud UI, showing summary information for two DAGs](/img/docs/dag-metrics.png)

## DAGs overview

The **DAGs** page shows the following summary information about the DAGs for all Deployments in your Workspace. You can filter through these DAGs using the left menu:

- Total DAG runs over the last 14 days, expressed as a bar chart.

    Each bar in the chart represents an individual DAG run. A bar's color represents whether the DAG run was a success or a failure, while its length represents the total duration of the DAG run. If there are more than 14 DAG runs in the last 14 days, then the chart shows only the 14 most recent DAG runs.

- **State**: Indicates whether the DAG is **Active** or **Paused**. If a DAG has a purple lightning symbol next to its name, that DAG is **Active**.
- **Last Run**: The duration of the last DAG run and the ending time of the DAG's most recent DAG run, expressed relative to the current time.
- **Schedule**: The frequency that the DAG runs and the starting time of the next DAG run, expressed relative to the current time.
- **Deployment**:  The Deployment ID of the Deployment for the current DAG Run.
- **Owner(s)**: The Airflow DAG owner attribute. You can change the owner attribute when you write or update your DAG.
- **Tags**: The custom tags that you marked your DAG with. To add custom tags to a DAG, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/add-dag-tags.html).

## View detailed metrics for a DAG

To view more detailed information about a specific DAG in the Cloud UI, select the DAG from the **DAGs** page. This view contains the same metrics from the **DAGs** page, plus detailed views of the DAG run chart, graph, and code. See [Manage DAGs](manage-dags.md) to learn how to manually mark and trigger DAG runs from this view.

![The detailed information page for a DAG, accessible from the DAGs view in the Cloud UI](/img/docs/dag-detail-metrics.png)

## See also 

- [Manage DAGs](manage-dags.md)

