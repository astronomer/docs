---
sidebar_label: 'Reporting dashboard'
title: "Reporting dashboard"
id: reporting-dashboard
description: "View information about your Organization, Deployments, DAGs, and costs."
---

:::warning

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

Astro provides [a Dashboard](https://cloud.astronomer.io/dashboards) with a consolidated view of important metrics about your Organization's use of Astro. This includes the following Dashboards:

- Organization explorer
- Deployment detail
- DAG SLA
- Billing details (Hosted only)
- Operator Use

These Dashboards show in depth view about your Organization's DAG performance, Operator use, Deployment details, and cost breakdown. This data allows you to quickly identify any problems or opportunities to optimize the Deployments in your Workspace. For example, you can use the Deployment detail page to identify any unexpected DAG behaviors, like more compute use than expected, and then examine the Billing details page to identify any associated costs that behavior might incur.

You can find the reporting Dashboards in your **Organization settings** menu, by clicking **Dashboards**.

:::info

Only users with **Organization Owners** and **Organization Admins** [user permissions](user-permissions.md#organization-roles) can access reporting Dashboards.

:::

## Organization Explorer

The **Organization Explorer** tab provides at-a-glance summaries about activity in your Organization's Deployment and DAGs in your entire Organization, or filtered by Workspace or Deployment name.

This tab allows you to quickly inspect the activity and performance of your Deployments, and compare them to one another. This means you can quickly identify any Deployments, DAGs, or tasks that have had recent behavior changes or are performing in an unexpected way. Hovering your cursor over any of the charts brings up a detailed view of the data, indexed by date.

All Dashboards include sharing how recently the data was updated in the **Data available through**.

### Organization explorer filter parameters

You can filter the data shown in the reports by the following:

* **Time period**
* **Workspace name** - Choose which Workspaces' data you want to view. By default, if you don't select any Workspaces, the report shows the aggregated view of all Workspaces.
* **Deployment name** - Choose which Deployments' data you want to view. By default, if you don't select any Deployment, the report shows the aggregated view of all Deployments.
* **Display by** - Select the time interval you want to view over. This view can be as granular as the **Day** or view data aggregated by **Week** or **Month**.

### Organization explorer data

In the Dashboard, you can take a detailed view of the following different reporting elements. Each has its own section where you can filter the data within the element, export reports, or set up an email alert.

* **Deployments** - The number of Deployments in a Workspace, indexed by time.
* **Task Counts by Success/Failure** - Segmented bar chart showing the counts of successful and failed tasks in the selected Workspace, indexed by time.
* **Active DAG counts** -
* **Task Counts by Workspace** - A line graph of the count of tasks in selected Workspaces over time. If you select more
* **Workspace summary in last 30 Days**
    - Top 10 Workspaces by code push count
    - Top 10 Workspaces by active DAG count
    - Top 10 Workspaces by unique operator count

## Deployment Detail

The **Deployment Detail** report shows a table of all your non-deleted Deployments in your Organization, indexed by Workspace Name. You can filter this table by **Workspace Name** or **Deployment Name** Additionally, the task counts, DAG counts, and unique operator counts are shown for the latest completed month.

This report view also highlights if you have any Deployments that use a version of the Astro Runtime that are either unsupported or are expected to reach end of maintenance in the next six months.

## DAG SLA

If you have a service level agreement (SLA) where your DAGs need to complete by a certain consistent time, you can use this view to compare DAG completion times with an SLA time. This view can help you report the frequency your Organization meets their SLA obligations.

1. Choose the **DAG ID** that you want to check DAG run completion times for. If you have a large number of DAGs in your Organization, you can first filter by **Workspace Name** and **Deployment Name** before choosing your DAG ID.
2. Select the time interval over which you want to look at the DAG data.
3. Define the **SLA Time (UTC)**
4. Choose the time interval you want to aggregate the data with by choosing **Day**, **Week**, or **Month** in **Display by**.

The report generates a line graph that shows the **Median End Time** of the DAG, the **Average End Time**, and the **SLA** time you defined.

## Billing Details (Hosted Only)

In the **Cost Breakdown** tab of your Dashboard, you can find detailed information regarding your accumulated cost per time period, depending on the Workspace Name and Deployment.

### Cost breakdown data filters

You can filter the data shown in the reports by the following:

* **Date**
* **Workspace Name**: Choose which Workspaces' details you want to examine in detail.
* **Deployment Name**: Choose which Deployments' details you want to examine in detail.

### Cost breakdown data details

- **Total spend** - The total cost per time period.
- **Deployment spend**- The cost per time period related to your Deployment scheduler configuration.
- **Compute spend** - The cost per time period related to your Worker runtime.
- **Workspaces** - The Number of Workspaces in your Organization.
- **Deployments** - The Number of Deployments in your Organization
- **Workspace Spend** - A segmented bar chart that shows the **Deployment** and **Compute** spend amount, organized by Workspace.
- **Spend for all Workspaces** - A segmented bar chart that shows the aggregated cost over time, with each segment representing the cost of a specific Workspace.
- **Spend by Workspace Deployments** - <!--needs feedback from data team-->
- **Detailed Spend for Deployments** - This detailed table describes the accumulated cost in terms of **Billable metrics**, which are the same metrics used in your invoices.

## Operator usage

You can examine how your Deployments and Workspaces use Operators, and the frequency that their tasks succeed and fail.

### Operator usage data filters

You can filter the data shown in the reports by the following:

* **Date**
* **Filter operators by string**: Use a string as a search query for the Operator you want to examine.
* **Operator**: Select the Operator from a menu of options or search for one.
* **Workspace Name**: Choose which Workspaces' details you want to examine in detail.
* **Deployment Name**: Choose which Deployments' details you want to examine in detail.

### Operator usage data details

In the Dashboard, you can take a detailed view of the following different reporting elements. Each has its own section where you can filter the data within the element, export reports, or set up an email alert.

* **Operators by Task/Distinct DAG Count** - This view shows you the top operators used in your Organization, ordered by the count of tasks and distinct DAGs. You can use expand each row to examine the **Workspace Name** and **Deployment Name** specifically. This data answers the question, *What are the top operators used across my organization?*
* **Workspace Operator Usage by Task/Distinct DAG Count** - This view shows you the most used Workspaces based on total Task Count and Distinct DAGs. You can then expand each row to find the most frequently used Operators in each Deployment in that Workspace. This data answers the question, *Which workspace is using the selected operators the most?*
* **Task Usage By Period, Failed/Successful** - An aggregate view of the number of tasks that failed or succeeded in the selected Workspace and Deployment over the defined time period.
* **Task Usage By Period, Workspace** - An aggregate view of the number of tasks by Workspace over the defined time period.

## Export data from reporting Dashboards

You can set up your reporting Dashboard to email you data reports on a given time interval or as an alert when certain criteria are met. Or, you can export your data in a one-time action.

1. Hover your cursor anywhere in the Dashboard window or over a specific data element, to see the detailed menu view. This menu includes **Filters**, the option to **Maximize element**, or **Expand menu** further.

2. Expand the menu, and then you can choose
    - **Sort** the x-axis data
    - **Alert when...** to define criterial when Astro will send you a data export of the element or dashboard
    - **Export** to download the data in a file format of your choosing, like `.csv`.
    - **Refresh data** to reload the data you're viewing in the Dashboard or element.
