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

Dashboards help you quickly identify any problems or opportunities to optimize how your team uses Airflow. For example, you can use the Deployment detail page to identify unexpected DAG behaviors, like unusually high compute usage, and then check the Billing details dashboard to identify any associated costs incurred by that behavior.

To view Astro dashboards, click your Workspace name in the upper left corner of the Cloud UI, click **Organization Settings**, then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards).

:::info

Only users with **Organization Billing Admin** [user permissions](user-permissions.md#organization-roles) can access reporting dashboards.

:::

## Organization Explorer

The **Organization Explorer** tab provides at-a-glance summaries about activity across your Organization's Deployments. You can also filter to view summaries for specific Workspaces or Deployments.

This tab allows you compare the activity and performances of Deployments to one another. You can identify Deployments, DAGs, or tasks that have had recent behavior changes or are performing in an unexpected way. Hovering your cursor over any of the charts brings up a detailed view of the data, indexed by date.

All Dashboards include sharing how recently the data was updated in the **Data available through**.

### Organization explorer filter parameters

You can filter the data shown in the reports by the following:

- **Time period** - Choose the date range that you want to view data for.
- **Workspace name** - Choose which Workspaces' data you want to view. By default, if you don't select any Workspaces, the report shows the aggregated view of all Workspaces.
- **Deployment name** - Choose which Deployments' data you want to view. By default, if you don't select any Deployment, the report shows the aggregated view of all Deployments.
- **Display by** - Select the time interval you want the data organized by. The dashboard can show you data in  **Day**, **Week**, or **Month** intervals.

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

The **Deployment Detail** report shows a table of all Deployments in your Organization, indexed by Workspace Name. For each Deployment, the dashboard shows your Deployment configurations as awell as usage metrics including task run counts, DAG run counts, and operator counts.

Use this dashboard to check that your Deployment has the appropriate resources based on the number of DAGs it runs. You can also use this dashboard to check whether your Astro Runtime version is in support or needs to be upgraded.

## DAG SLA

The DAG SLA dashboard allows you to simulate a service level agreement (SLA) for when a DAG should complete and then compare your DAG runs against the SLA. Use this dashboard to ensure that your Organization meets your SLA obligations, or to create and alert on new SLAs.

To use this dashboard, you must first define an SLA and the DAGs which should be compared against the SLA.

1. Choose the **DAG ID** that you want to check DAG run completion times for. If you have a large number of DAGs in your Organization, you can first filter by **Workspace Name** and **Deployment Name** before choosing your DAG ID.
2. Select the time interval over which you want to look at the DAG data.
3. Define the **SLA Time (UTC)**
4. Choose the time interval you want to aggregate the data with by choosing **Day**, **Week**, or **Month** in **Display by**.

The report generates a line graph that shows the **Median End Time** of the DAG, the **Average End Time**, compared to the **SLA** time you defined.

## Billing Details (Hosted Only)

In the **Cost Breakdown** tab of your Dashboard, you can find detailed information about how much you spend on Astro over time for each of your Workspaces and Deployments. Use this data alongside your other dashboards to identify the biggest opportunities for cost reduction in your Organization.

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

You can examine how your Deployments and Workspaces use Operators, and the frequency that their tasks succeed and fail. Use this data to identify types of operators that could be replaced with more efficient alternatives, or to find operators that fail more than expected. 

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
