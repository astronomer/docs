---
sidebar_label: 'Data Lineage'
title: "Data Lineage on Astro"
id: data-lineage
description: "Track and visualize the movement of your data with data lineage on Astro"
---

## Overview

This guide explains how to navigate the **Lineage** tab in the Cloud UI and configure views that can help you troubleshoot issues with your data pipelines and understand the movement of data across your Organization.

The **Lineage** tab on Astro has three pages:

- **Explore**: A real-time overview of all **jobs** that emit data lineage across your Organization. A job can be an Airflow task or any other process configured to emit lineage data to Astronomer, such as a Spark job.
- **Issues**: A view of potential issues or statistical inconsistencies related to your jobs or datasets
- **Lineage**: A graph view that visualizes data lineage

Generally speaking, you can use these pages to diagnose issues that may otherwise be difficult to identify across environments and tools. For example, if an Airflow task failed because the schema of a database changed, you might go to the **Lineage** page on Astro to determine which job caused that change and which downstream tasks failed because of it.

Views in the **Lineage** page are available to all members of your Organization on Astro. For more information on data lineage and related concepts, see [Lineage Overview](lineage-overview.md).

:::info 

This functionality is early access and under active development. If you have any questions or feedback about this feature, reach out to [Astronomer Support](https://support.astronomer.io/).

:::

## View the Lineage Graph for a Data Pipeline

To view the lineage graph for one of your data pipelines, search for a DAG, task, or dataset with the search bar at the top of the UI. You can also search for jobs from other tools with lineage integrations, including dbt or Spark.

![Example query in the lineage search bar](/img/docs/lineage-search.png)

The search results include the namespace that emitted the matching event. If an Astro Deployment emitted the lineage event, then this namespace will match Deployment's namespace as shown in the **Deployments** page of the Cloud UI. Clicking a search result will open the **Lineage** page and show the lineage graph for the selected job or dataset. You can also access the lineage graph for a recent job run in the **Explore** page under **Most Recent Runs**.

The **Lineage** page shows lineage data only for the most recent run of a given data pipeline. To explore lineage data from previous runs, see [Compare Lineage Graphs from Previous Runs](data-lineage.md#compare-lineage-graphs-from-previous-runs).

:::info

By default, when you directly access the **Lineage** page from the left-hand menu, the page shows the last lineage graph you viewed. If you go directly to the **Lineage** page before having viewed a lineage graph, you will not see lineage graph data. If this happens, try first accessing a job run using the search bar or **Explore** page to populate the **Lineage** page with data.

:::

:::info

If the Lineage graph only shows you a single node, it indicates that the job you selected did not emit any information about input or output datasets. This is likely because the single node represents an Airflow task that isn't using a [supported Airflow operator](data-lineage-support-and-compatibility.md). You will still be able to view the duration of this job over time.

:::

## Navigating the Lineage Graph

In the **Lineage** page, Astronomer renders your data pipeline as a directed graph of **job** and **dataset** nodes:

- A **job** node represents an individual step in your data pipeline, such as an Airflow task or a Spark job.
- A **dataset** node represents a data source that a job interact with, such as a Snowflake database.

Directed vertices connect jobs to datasets and vice versa. A single vertex will never connect two jobs or two datasets together.

In the following example, `insert` is a job that exists as part of the `etl_menu_items` group. A vertex connects `insert` to the `menu_items` dataset to indicate that `insert` interacted with data in this dataset.

![Lineage graph example showing different nodes and vertices](/img/docs/lineage-overview.png)

To navigate larger graphs, click and drag your mouse across the screen. To zoom in on a specific section of a graph, you can either scroll your mouse or click the magnifying glass icons in the information pane on the bottom-left of the screen.

To learn more information about a dataset or job, you can either hover over or click a node. Hovering over a node gives you high level information about the dataset or job at a glance. Specifically, you'll see:

- **Namespace**: The namespace of the Deployment in which the job ran
- **Name**: The DAG ID and task ID of the job, formatted as `<dag-id>.<task-id>`
- **Run information (job only)**: Metadata and status information about the job run
- **Quality checks (dataset only)**: The status of a dataset's data quality checks

Clicking a node populates the information pane with detailed information about the job or dataset. For more information about how to use this view, see [View Metrics for a Specific Job or Dataset](data-lineage.md#view-metrics-for-a-specific-job-or-dataset).

### Access the Graph Legend

Clicking on the key icon in the information pane opens the graph legend. The legend provides a visual guide to help you distinguish between:

- Job nodes and dataset nodes.
- User-selected and unselected nodes.
- Completed, running, failed, and aborted jobs
- Completed, running, failed, and aborted dataset checks

:::info

Dataset and job statuses are based on checks of metadata attached to your data. To see the specifics of why a dataset failed, you can click on the failed dataset node and check the **Quality** tab in the information pane. To check why a job failed, you might need to check the source of the job, such as your DAG or task.

:::

You can also customize how the graph appears in the legend via the **Cluster Mode** and **Edge Drawing Mode** settings.

## View Metrics for a Specific Job or Dataset

Below the lineage graph is the **information pane**: a collection of information and metrics for a single selected node.

The information pane is split into the following tabs:

- **Info**: Shows the code for a job or the schema for a dataset. Also shows the difference between job runs when you create a comparison in the **Compare** tab
- **Inputs/Outputs**: Shows the inputs and outputs for a job or dataset. This information is equivalent to the upstream and downstream nodes in the graph view
- **Quality (Dataset only)**: Shows the data quality checks performed on each element of a dataset. You can drill down further into these checks by expanding a listed dataset element
- **Duration (Job only)**: Shows the duration of upstream job runs, starting with the most upstream job run and descending to the currently selected job run. To view durations for all recent job runs, click the blue arrow next to the name of your most recent job run. After expanding this list, clicking **Maximize** at the bottom of the list will show your job run durations relative to the average duration across all job runs
- **Compare (Job only)**: Shows other job runs of the currently selected job. Select any two job runs and go to the **Info** tab to see how the code changed between the two job runs. Use this tab to compare job runs with different statuses or run times to measure performance between code changes

### Check for Data Quality

Whenever you select a dataset from the lineage graph, the **Quality** tab appears in the information pane. By default, this tab shows a list of columns that correspond to your dataset.

If you have a [Great Expectations](https://docs.greatexpectations.io/docs/) integration, this tab also contains charts that show:

- The number of rows in your dataset over time.
- The amount of megabytes consumed by your dataset over time.
- Successes and failures of data quality checks.

![Quality tab example](/img/docs/quality-tab.png)

These charts display data from up to the past 20 job runs.

Use the **Quality** tab to detect unexpected changes or statistical variance in your dataset that could indicate a problem. The following topics explain each available chart in the tab.

#### Rows

The Rows chart shows the total number of rows in the dataset over time. A drastic change in rows can occur naturally (for example: when a rapid increase of customer orders during the holiday season). However, it can also indicate an error in an upstream job, especially if it is sudden or unexpected.

#### Bytes

The Bytes chart shows the total size of the dataset over time. A sudden increase in dataset size usually means something has changed in the definition of the data. For example, a new column might have been added to your table containing the description of an order, where before it contained only part numbers and quantities.

#### Quality Metrics

The **Quality Metrics** chart shows the pass/fail status of quality assertions in a Great Expectations suite.
To see details on the assertions that have passed or failed, hover over a point on the chart.

#### Distinct Count (Column-level)

The **Distinct Count** chart shows the total number of distinct values for a given column.

A distinct count can sometimes grow unexpectedly, perhaps if a successful campaign creates a set of new `customer_id` values in an order table suddenly. However, it can also suggest an underlying problem if, for example, a `menu_item_id` field shows that thousands of new menu items have been added overnight.

#### Null Count (Column-level)

The **Null Count** chart shows the number of rows in the dataset where a given column contains a null value.

A large number of null values can be normal, such as when most orders on your system do not include a discount. However, an increase in null values on a column representing a ubiquitous piece of data, such as `quantity`, might indicate an issue.

#### Quality Metrics (Column-level)

The **Quality Metrics** chart shows the pass/fail status of quality assertions in a Great Expectations suite for a given column.

To see details on the assertions that have passed or failed, hover over a given point on the chart.

### Compare Lineage Graphs from Previous Runs

The **Compare** tab shows a list of past job runs for a given job. Using the compare tab, you can select pairs of job runs to see what changed in your pipelines between the two runs. The general Compare tab workflow is as follows:

1. Click a job on the graph.
2. Open the **Compare** tab to see a list of all previous job runs for the selected job. The colored bar above a job run represents both the job run’s duration and run state. Job runs with a run state of `COMPLETE` will have a blue bar, and job runs with a run state of `FAILED` will have an orange bar.

    ![Compare tab example](/img/docs/compare.png)

3. Select any two job runs from the list to enter the “Compare view” of your graph. In this view:

    - Jobs and datasets that experienced a code change between the time of your selected job runs are highlighted on the graph.
    - Jobs and datasets that stayed the same between job runs are greyed out.
    - Your selected job is shown with an anchor icon and a blue box.
    - The bottom of the graph shows information about your comparison.

    ![Graph in compare mode](/img/docs/compare-graph.png)

4. Select a job or dataset that experienced a code change.
5. Open the **Info** tab. Instead of showing a single code source, this tab now shows the code source from both of your compared job runs. Use this information to determine what code change might have been responsible for downstream errors.

    ![Info tab when comparing two code sources](/img/docs/compare-code.png)

## View a Summary of Issues across Deployments

The **Issues** page contains metrics that can help you identify irregularities related to the behavior of your data pipelines.

![Lineage issues page](/img/docs/lineage-issues.png)

Specifically, this page tracks following types of issues

- **Job Execution Issues**: A job execution issue occurs when a job emits an error that it did not successfully complete. Note that this metric works only for Deployments using Runtime 5.0.0+.
- **Job Duration Issues**: A job duration issue occurs when a job run's duration differs by more than three standard deviations from the average run time for that specific job.
- **Data Quality Issues**: If you integrate with [Great Expectations](https://www.astronomer.io/guides/airflow-great-expectations/), an open source data quality tool, this metric will track issues generated by expectation quality checks for datasets. Use this tab to detect data quality failures that could indicate an upstream problem.

## View a Summary of Past Runs

By default, the **Lineage** page shows the last lineage graph you accessed. To see high level metrics about all of your job runs and access lineage graphs, open the **Explore** page on the lefthand sidebar. This page is structured similarly to the Airflow UI's calendar view: It contains a list of your most recent runs, as well as a calendar that shows all runs over the last year.

![Lineage summary page](/img/docs/lineage-explore.png)

Airflow tasks will appear as jobs with the name `<dag_id>.<task_id>`. For examplem, the job `example_dag_basic.extract` represents the `extract` task running within the `example_dag_basic` DAG.

This view can help you get a better sense of the scope of your lineage integrations. It can also help you confirm that a recent run was picked up by the lineage backend as expected.
