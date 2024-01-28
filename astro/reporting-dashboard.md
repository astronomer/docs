---
sidebar_label: 'Reporting dashboard'
title: "Reporting dashboard"
id: reporting-dashboard
description: "View information about your Organization, Deployments, DAGs, and costs."
---

:::warning

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

Astro provides [a Dashboard](https://cloud.astronomer.io/dashboards) with a consolidated view of important metrics about your Organization's use of Astro. This includes data about your Deployment performance, DAG statistics, DAG SLA, operator use, and cost breakdown.

## Access reporting Dashboards

You can find the Dashboards in your **Organization settings** menu, by clicking **Dashboards**.

Only users with **Organization Owners** and **Organization Admins** [user permissions](user-permissions.md#organization-roles) can access reporting Dashboards.

## Organization Explorer

The **Organization Explorer** tab provides at-a-glance summaries about activity in your Organization's Deployment and DAGs in your entire Organization, or filtered by Workspace or Deployment name.

This tab allows you to quickly inspect the activity and performance of your Deployments, and compare them to one another which means you can quickly identify any Deployments, DAGs, or tasks that have had recent behavior changes or are performing in an unexpected way. Hovering your cursor over any of the charts brings up a detailed view of the data, indexed by date.

All Dashboards include sharing how recently the data was updated in the **Data available through**.

### Organization explorer filter parameters

You can filter the data shown in the reports by the following:

* **Time period**
* **Workspace name** - Choose which Workspaces' data you want to view. By default, if you don't select any Workspaces, the report shows the aggregated view of all Workspaces.
* **Deployment name** - Choose which Deployments' data you want to view. By default, if you don't select any Deployment, the report shows the aggregated view of all Deployments.
* **Display by** - Select the time interval you want to view over. This view can be as granular as the **Day** or view data aggregated by **Week** or **Month**.

### Organization explorer data

* **Deployments** - The number of Deployments in a Workspace, indexed by time.
* **Task Counts by Success/Failure** - Segmented bar chart showing the counts of successful and failed tasks in the selected Workspace, indexed by time.
* **Active DAG counts** -
* **Task Counts by Workspace** - A line graph of the count of tasks in selected Workspaces over time. If you select more
* **Workspace summary in last 30 Days**
    - Top 10 Workspaces by code push count
    - Top 10 Workspaces by active DAG count
    - Top 10 Workspaces by unique operator count

## Deployment Detail

You can filter down to deployment level to see higher granularity of information.

## DAG SLA

This view allows you to set an SLA time and make sure your DAGs are completing by then.

## Billing details (Hosted Only)

In the **Cost Breakdown** tab of your Dashboard, you can find detailed information regarding your accumulated cost per time period.

## Operator usage