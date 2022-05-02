---
sidebar_label: 'Data Lineage'
title: "Data Linage on Astro"
id: data-lineage-astro
description: "Track and visualize the movement of your data with data lineage on Astro"
---

## Overview

Data lineage is a critical part of data orchestration tooling. This guide explains how to navigate the **Lineage** tab in the Cloud UI and configure views that can help you both troubleshoot issues with your data pipelines as well as understand the movement of data across your Organization.

The Lineage tab on Astro has three pages:

- **Explore**: A real-time overview of all jobs that emit data lineage across your Organization. This includes a heatmap of jobs that have run within the last year as well as a more detailed list of recent job runs.
- **Issues**: A view of potential issues or statistical inconsistencies related to your jobs or datasets. On this page, you can see metadata for job duration, job failures, and data quality checks.
- **Lineage**: A graph view that visualizes data movements across DAGs, tasks, and Deployments. The graph primarily shows relationships between datasets and jobs.

Generally speaking, these views map your organization's data ecosystem and can help you diagnose issues that may otherwise be difficult to identify across environments and tools. For example, if an Airflow task failed because the schema of a database changed, you might go to the **Lineage** tab on Astro to determine which job caused that change and which downstream tasks failed because of it.

Views in the **Lineage** tab are available to all members of your Organization on Astro.

## Explore

[Info about Explore]

## Issues

The **Issues** page contains metadata that can help you identify irregularities related to the behavior of your data pipelines. Specifically, this page has information on:

- Job execution
- Job duration
- Data quality

![Lineage summary page](/img/docs/lineage-summary.png)

To see an issue in the context of a lineage graph, click the name of the related dataset or job in the table.

### Job execution

[Info about job execution]

### Job duration

[Info about job duration]

### Data quality

If you integrate with [Great Expectations](https://www.astronomer.io/guides/airflow-great-expectations/), an open source data quality tool, the **Quality** tab of the **Issues** page in the Cloud UI will show metadata on data quality checks for both your jobs and datasets. Use this tab to detect data quality failures that could indicate an upstream problem.

![Quality tab example](/img/docs/quality-tab.png)

#### Data quality for datasets

This view has the following:

- A **Bytes** chart that shows the total size of the dataset over time. A sudden increase in dataset size usually means something has changed in the definition of the data. For example, a new column might have been added to your table containing the description of a restaurant order, where before it contained only the order number.
- A **Quality Metrics** chart that shows the pass/fail status of quality assertions, as defined in Great Expectations. To see details on the assertions that have failed, hover over a point on the chart.
- A **Distinct Count** chart that shows the total number of distinct values for a given column. If distinct count changes significantly, it might indicate an upstream data problem.
- A **Null** chart shows the number of rows in the dataset where a given column contains a null value.

A large number of null values can be normal, such as when most orders on your system do not include a discount. However, an increase in null values on a column representing a ubiquitous piece of data, such as `quantity`, might indicate an issue.

#### Data quality for jobs

[Info about job duration]

#### Compare Lineage Between Runs Using the Compare Tab

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

## Lineage

In the **Lineage** page of the Cloud UI, there is a graph that visualizes your organization's data ecosystem as a set of nodes. In this view, a node can be either:

- A **job** that represents an individual task in your data pipeline, such as an Airflow task or Spark job.
- A **dataset** that represents a data source that your tasks interact with, such as a Snowflake database.

Directed vertices connect jobs to datasets and vice versa. A single vertex will never connect two jobs or two datasets to each other.

In the Lineage page, you can:

- View metadata for any job in your Organization, including inputs and outputs.
- Look at the SQL code that ran for any given task in your Organization.
- Confirm which datasets have been read from or written to, and by which tasks.
- See the downstream effects and upstream dependencies between tasks.

### View Job Metadata

To learn more information about a dataset or job, you can either hover over or click on its node. Hovering over a node gives you high level information about the node at a glance. Specifically, you'll see:

- **Namespace**: The namespace of the Deployment in which the job ran.
- **Name**: The DAG ID and task ID of the job, formatted as `<dag-id>.<task-id>`.
- **Run information**: Metadata and status information about the job run. This applies to jobs only.
- **Quality checks**: The status of a dataset's data quality checks. This applies to datasets only.

In the following example, `insert` is a job that exists as part of the `etl_menu_items` group. A vertex connects the `insert` job to the `menu_items` dataset to indicate that `insert` interacted with this dataset.

![Lineage graph example showing different nodes and vertices](/img/docs/lineage-overview.png)

Clicking a node populates the information pane with detailed information about the node. For more information about how to use this view, see [Using the Information Pane](lineage.md#using-the-information-page).

### Manage groupings

To reduce the complexity of the graph, nodes are automatically organized into groups based on an assumed shared context between jobs and datasets. A group is represented by a transparent grey box surrounding a subset of nodes. You can change how your graph is grouped by using the **Graph Cluster Mode** settings in the **Graph Legend**:

- The ***Job Groups*** cluster mode creates groups based on relations between different jobs. This mode prioritizes visualizing the sequence, inputs, and outputs within jobs.
- The ***Dataset Groups*** cluster mode creates groups based on relations between different databases. This mode prioritizes showing which datasets share a common source or infrastructure.

Note that changing to a different graph cluster mode will change where certain nodes appear on the graph. All nodes and the vertices between them, however, remain structurally the same regardless of your cluster mode.

## Using the Information Pane

Below the lineage graph is the **information pane**: a collection of information and metrics for a single selected node. When you click on a node in the graph, the information pane populates all of that nodes information.

The information pane is split into the following tabs:

- **Info**: Shows the code for a job or the schema for a dataset. Also shows the difference between job runs when you create a comparison in the **Compare** tab.
- **Inputs/Outputs**: Shows the inputs and outputs for a job or dataset. This information is equivalent to the upstream and downstream nodes in the graph view.
- **Quality (Dataset only)**: Shows the data quality checks performed on each element of a dataset. You can drill down further into these checks by expanding a listed dataset element.
- **Duration (Job only)**: Shows the duration of upstream job runs, starting with the most upstream job run and descending to the currently selected job run.
- **Compare (Job only)**: Shows other job runs of the currently selected job. Select any two job runs and go to the **Info** tab to see how the code changed between the two job runs. Use this tab to compare job runs with different statuses or run times to measure performance between code changes.

## View Graphs from Past Runs

By default, the lineage graph shows the information based on your Deployment's most recent job runs. To see the lineage graph for a previous job run and high level metrics about all of your job runs, open the **Explore** page on the lefthand sidebar. This page is structured similarly to the Airflow UI's calendar view: It contains a list of your most recent runs, as well as a calendar that shows all runs over the last year.

![Lineage summary page](/img/docs/lineage-explore.png)

This view can help you get a better sense of the scope of your lineage integrations. It can also help you confirm that a recent run was picked up by the lineage backend as expected.

To view the lineage graph from a previous date, click that date in the calendar and click on any of the tasks that appear in the **Runs on [Date]** table. This will bring up the lineage graph for the selected date and focus on the specific task that you clicked.