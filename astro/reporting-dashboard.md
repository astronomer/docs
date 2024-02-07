---
sidebar_label: 'Reporting dashboard'
title: "Reporting dashboard"
id: reporting-dashboard
description: "View information about your Organization, Deployments, DAGs, and costs."
---

:::warning

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

Astro provides a collection of dashboards that include important metrics about your Organization's use of Astro. These dashboards include:

- Organization explorer
- Deployment detail
- DAG SLA
- Cost Breakdown (Hosted only)
- Operator Use

Dashboards help you quickly identify any problems or opportunities to optimize how your team uses Airflow. For example, you can use the Deployment detail page to identify unexpected DAG behaviors, like unusually high compute use, and then check the **Cost Breakdown** dashboard to identify any associated costs incurred by that behavior.

To view Astro dashboards, click your Workspace name in the upper left corner of the Cloud UI, click **Organization Settings**, then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards). Each dashboard shows the last time that it was updated, in the **Data available through** section.

:::info

Only users with **Organization Billing Admin** [user permissions](user-permissions.md#organization-roles) can access reporting dashboards.

:::

## Organization Explorer

The **Organization Explorer** tab provides at-a-glance summaries about activity across your Organization's Deployments. You can also filter to view summaries for specific Workspaces or Deployments.

This tab allows you compare the activity and performances of Deployments to one another. You can identify Deployments, DAGs, or tasks that have had recent behavior changes or are performing in an unexpected way. For example, you can filter the data shown by time period, Workspace name, or Deployment name, to view data such as the number of successful or failed tasks within Workspaces or Deployments. Hovering your cursor over any of the charts brings up a detailed view of the data, indexed by date.

By examining your data at the Organization level, you can quickly identify Deployments with large numbers of failing tasks by simply looking at the graphs or charts for outliers. Then, you can filter by time period to see if there have been similar events in the past and when.

![Quickly examine summaries about your Organization's DAG activity at the DAG and Workspace level.](/img/docs/dash-organization-overview.png)


## Deployment Detail

The **Deployment Detail** dashboard shows a table of all Deployments in your Organization, indexed by Workspace Name. For each Deployment, the dashboard shows your Deployment configurations as well as use metrics like task run counts, DAG run counts, and operator counts.

Use this dashboard to check that your Deployment has the appropriate resources based on the number of DAGs it runs. You can also use this dashboard to check whether your Astro Runtime version is currently supported or if you need to upgrade it.

![View data about Deployment health and DAG success.](/img/docs/dash-deployment-detail.png)

## DAG SLA

The DAG SLA dashboard allows you to simulate a service level agreement (SLA) for when a DAG should complete and then compare how frequently your DAG runs complete within the SLA. Use this dashboard to check how frequently your Organization meets your SLA obligations, or to create an alert on new SLAs.

![Examine how frequently DAGs meet your SLA.](/img/docs/dash-DAG-SLA.png)

### Set up an SLA

To create an SLA, you must first define an SLA and then select the DAGs you want to compare it to.

1. Choose the **DAG ID** that you want to check DAG run completion times for. If you have a large number of DAGs in your Organization, you can first filter by **Workspace Name** and **Deployment Name** before choosing your DAG ID.
2. Select the time interval over which you want to look at the DAG data.
3. Define the **SLA Time (UTC)**
4. Choose the time interval you want to aggregate the data with by choosing **Day**, **Week**, or **Month** in **Display by**.

The report generates a line graph that shows the **Median End Time** of the DAG, the **Average End Time**, compared to the **SLA** time you defined.

## Cost Breakdown
<HostedBadge/>

In the **Cost Breakdown** tab of your Dashboard, you can find detailed information about how much you spend on Astro over time for each of your Workspaces and Deployments. Use this data alongside your other dashboards to identify the biggest opportunities for cost reduction in your Organization.

![View the cost of your different Astro resources.](/img/docs/dash-cost-breakdown.png)

## Operator use

You can examine how your Deployments and Workspaces use Operators, and the frequency that their tasks succeed and fail. Use this data to identify types of operators that could be replaced with more efficient alternatives, or to find operators that fail more than expected. This dashboard provides data to answer the questions, *What are the top operators used across my organization?* and *Which workspace is using the selected operators the most?*.

You can filter your data, export reports, or set up an email alert, which sends a copy of the data to an email address under certain circumstances.

![Examine how frequently DAGs meet your SLA.](/img/docs/dash-DAG-SLA.png)

## Export data from reporting dashboards

You can set up your reporting Dashboard to email you data reports on a given time interval or as an alert when certain criteria are met. Or, you can export your data in a one-time action.

1. Hover your cursor anywhere in the Dashboard window or over a specific data element, to see the detailed menu view. This menu includes **Filters**, the option to **Maximize element**, or **Expand menu** further.

2. Expand the menu, and then you can choose
    - **Sort** the x-axis data
    - **Alert when...** to define criterial when Astro will send you a data export of the element or dashboard
    - **Export** to download the data in a file format of your choosing, like `.csv`.
    - **Refresh data** to reload the data you're viewing in the Dashboard or element.
