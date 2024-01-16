---
sidebar_label: 'View data lineage'
title: "View data lineage on Astro"
id: data-lineage
description: "Track and visualize the movement of your data with data lineage on Astro"
---

The **Lineage** tab in the Cloud UI can help you troubleshoot issues with your data pipelines and understand the movement of data across your Organization.

From the **Lineage** tab on Astro, you can access the following four pages:

- **Runs**: A real-time overview of all runs that emit data lineage across your Organization. A run can be an Airflow task run or any other process configured to emit lineage metadata to Astronomer, such as a Spark job.
- **Datasets**: A real-time overview of all recent **datasets** that your DAGs have read or written to.
- **Issues**: A view of potential issues or statistical inconsistencies related to your runs or datasets.
- **Lineage**: A graph view that visualizes data lineage.
- **Integrations**: A view of your current data lineage integrations.

:::info

Lineage datasets are different from Airflow's [datasets feature](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html). Airflow datasets are defined explicitly in your DAG code, whereas lineage metadatasets are extracted and generated using lineage metadata. The Cloud UI currently does not show information about Airflow datasets.

:::

You can use these pages to diagnose issues that may be difficult to troubleshoot in other environments. For example, if an Airflow task failed because a database schema changed, you can use the **Lineage** page of the Cloud UI to determine which run caused the change and which downstream tasks failed as a result.

For more information on data lineage and related concepts, see [Data lineage concepts](data-lineage-concepts.md).

:::warning

All members of your Astro Organization can view the **Lineage** tab regardless of their Workspace permissions. The **Lineage** tab could contain plain-text SQL and Python code from any system that emits lineage metadata to Astro. If this is a security concern for your organization, reach out to [Astronomer support](https://support.astronomer.io/).

:::

## Prerequisites

To view lineage metadata for Deployments, you must configure Airflow and your external systems to emit lineage metadata. See [Enable data lineage for external systems](set-up-data-lineage.md).

## View the lineage graph for a data pipeline

You can use the search field at the top of the Cloud UI to view the lineage graph for one of your data pipelines, search for a DAG, task, or dataset. You can also search for runs from other tools with lineage integrations, including dbt or Spark.

![Example query in the lineage search bar](/img/docs/lineage-search.png)

The search results include the namespace that emitted the matching event. When an Astro Deployment emits the lineage event, the namespace matches the Deployment namespace shown in the **Deployments** page of the Cloud UI. Clicking a search result opens the **Lineage** page and shows the lineage graph for the selected job or dataset. You can also access the lineage graph for a recent job run in the **Runs** page below **Most Recent Runs**.

The **Lineage** page shows lineage metadata only for the most recent run of a given data pipeline. To explore lineage metadata from previous runs, see [Compare lineage graphs from previous runs](data-lineage.md#compare-lineage-graphs-from-previous-runs).

:::info

By default, when you access the **Lineage** page from the left menu, the last lineage graph you viewed is displayed. If you go directly to the **Lineage** page without viewing a lineage graph, no lineage graph data is displayed. If this happens, you can access a job run using the search bar or use the **Runs** page to populate the **Lineage** page with data.

:::

:::info

A lineage graph with a single node indicates that the run you selected didn't emit any information about input or output datasets. Typically, this occurs when an Airflow task isn't using a [supported Airflow operator](https://openlineage.io/docs/integrations/about#capability-matrix). You can still view the duration of this run over time.

:::

## Navigating the lineage graph

In the **Lineage** page, Astronomer renders your data pipeline as a directed graph of **run** and **dataset** nodes:

- A **run** node represents an individual step in your data pipeline, such as an Airflow task or a Spark job.
- A **dataset** node represents a data source that a run interacts with, such as a Snowflake database.

Directed vertices connect runs to datasets and datasets to runs. Two runs or two datasets can't be connected by a single vertex.

In the following example, `etl_menus` is a run that exists as part of the `etl_orders` group in the `food_delivery` namespace. A blue vertex connects `etl_menus` to the `public.menus` dataset, and dots moving towards the dataset indicate that `insert` interacted with data in this dataset. The moving dots along the blue line continue into the `etl` group, which contains more runs and datasets. To see exactly where this data will flow in the `etl` group, you can expand the group using the blue arrow to the left of its name.

![Lineage graph example showing different nodes and vertices](/img/docs/lineage-overview.png)

To navigate larger graphs, click and drag your mouse across the screen. To zoom in on a specific section of a graph, you can either scroll your mouse or click the magnifying glass icons in the information pane on the lower-left of the screen.

Click or hover over a node to view the following information about the dataset or run:

- **Namespace**: The namespace of the Deployment containing the run.
- **Name**: The DAG ID and task ID of the run, formatted as `<dag-id>.<task-id>`.
- **Run information (Run only)**: Metadata and status information about the run.
- **Quality Checks (Dataset only)**: The status of a dataset's data quality checks.

Click a node to populate the information pane with detailed information about the run or dataset. For more information about using this view, see [View metrics for a specific run or dataset](data-lineage.md#view-metrics-for-a-specific-run-or-dataset).

## View metrics for a specific run or dataset

On the **Lineage Graph** page for a DAG, the following tabs appear below the lineage graph:

- **Info**: Shows source code, standard facets, and custom facets for a run, or shows the schema for a dataset. Also shows the difference between runs when you are in [**Compare** mode](data-lineage.md#compare-lineage-graphs-from-previous-runs).
- **Inputs/Outputs**: Shows the inputs and outputs for a run or dataset. This information is equivalent to the upstream and downstream nodes in the graph view.
- **Quality (Dataset only)**: Shows the data quality checks performed on each element of a dataset. Expand a listed dataset element to view more information about a specific quality check.
- **Duration (Run only)**: Shows the duration of upstream runs in descending order. To view run durations relative to the average duration across all runs, click the blue arrow next to the name of your most recent run and then click **Maximize** at the bottom of the list.
- **Compare (Run only)**: Shows other runs for the currently selected run. Select any two run runs and go to the **Info** tab to view code changes between the two runs. Use this tab to compare runs with different statuses or run times to measure performance between code changes.

### Check for data quality

When you select a dataset from the lineage graph, the **Quality** tab appears in the information pane. By default, this tab shows a list of columns that correspond to your dataset.

If you're using a [Great Expectations](https://docs.greatexpectations.io/docs/) integration or the `SQLTableCheckOperator` or `SQLColumnCheckOperator` operators, this page contains charts that show successful and failed data quality checks.

Great Expectations and dbt show the number of rows in your dataset and the megabytes consumed by your dataset over time. The dbt test command doesn't currently display quality check results.

![Quality tab example](/img/docs/lineage-quality-tab.png)

These charts display data for up to the past 20 runs.

Use the **Quality** tab to detect unexpected changes or statistical variance in your dataset that could indicate a problem. The following topics explain each available chart in the tab.

#### Rows

The **Rows** chart shows the total number of rows in the dataset over time. A significant change in rows can occur naturally. For example, a rapid increase of customer orders occurs during the holiday season. However, it can also indicate an error in an upstream run, especially if it is sudden or unexpected.

#### Bytes

The **Bytes** chart shows the total size of the dataset over time. A sudden increase in dataset size usually indicates that something has changed in the definition of the data. For example, a new column might have been added to your table containing the description of an order, where before it contained only part numbers and quantities.

#### Quality metrics

The **Quality Counts** chart shows the pass or fail status of quality assertions in a Great Expectations suite.
To see details on the assertions that have passed or failed, hover over a point on the chart.

#### Distinct count (Column-level)

The **Distinct Count** chart shows the total number of distinct values for a given column.

Distinct count can sometimes grow unexpectedly. For example, a successful marketing campaign might suddenly create a set of new `customer_id` values in an order table. However, it can also suggest an underlying problem if, for example, a `menu_item_id` field shows that thousands of new menu items have been added overnight.

#### Null count (Column-level)

The **Null Count** chart shows the number of rows in the dataset where a given column contains a null value.

A large number of null values can be normal, such as when most orders on your system do not include a discount. However, an increase in null values in a column with standard data such as `quantity` might indicate an issue.

#### Quality metrics (Column-level)

The **Quality Metrics** chart shows the pass or fail status of quality assertions in a Great Expectations suite for a given column.

To see details on the assertions that have passed or failed, hover over a given point on the chart.

### Compare lineage graphs from previous runs

**Compare** mode shows a list of past instances for a given run. Using this mode, you can select two different run instances to see what changed in your pipelines between the two run instances.

1. Click a run on the graph.
   
2. Click **Compare**. 

    ![Compare tab example](/img/docs/lineage-compare.png)

    A bar graph appears showing you the time and duration of previous runs with the same run ID. The colored bar for a run indicates the run's duration and state. Successful runs have a green bar while failed runs have a red bar. 

3. Select any two runs to open the comparison view for your graph. In this view:

    - An orange icon identifies runs and datasets that experienced a code change between the time of your selected runs.
    - The run whose instances you're comparing is highlighted in orange and labeled **Comparing Task**.
    - Any part of the data pipeline that is affected by the code change is highlighted with orange vertices. 
    - When you click a run or a dataset which experienced a code change during the comparison period, the code change is highlighted in the bottom table.
  
4. Select a run or dataset that experienced a code change.
   
5. Click the **Info** tab. Instead of showing a single code source, this tab now shows code differences during your comparison period. Use this information to determine what code change might have caused downstream errors.

In the following example, two instances of the run `analytics.delivery_times_7_days` are being compared over time. During this period, the dataset `public.delivery_7_days` experienced a code change. Because this dataset is upstream of the compared run, it's marked with an orange notification and has an orange vertex connecting it to the run.

After clicking the dataset, the metrics window shows the message **CHANGES BETWEEN COMPARED RUNS** and a notification appears on the **Info** tab. After clicking the **Info** tab, the UI shows that the `discount_id` filed was changed from an `INTEGER` to a `VARCHAR` type.

![Info tab when comparing two code sources](/img/docs/lineage-compare-example.png)

## View a summary of issues across Deployments

The **Issues** page contains metrics that can help you identify data pipeline behavior irregularities.

![Lineage issues page](/img/docs/lineage-issues.png)

The **Issues** page identifies the following issues:

- **Job Execution Issues**: A job execution issue occurs when a run emits an error that it did not successfully complete. This metric is only available for Deployments using Runtime 5.0.0 and later.
- **Job Duration Issues**: A job duration issue occurs when a run's duration differs by more than three standard deviations from the average run time for that specific run.
- **Data Quality Issues**: If you integrate with [Great Expectations](https://www.astronomer.io/guides/airflow-great-expectations/), an open source data quality tool, this metric will track issues generated by expectation quality checks for datasets. Use this tab to detect data quality failures that could indicate an upstream problem.

## View a summary of past runs

By default, the **Lineage** page shows the last lineage graph you accessed. To view metrics about all of your runs and access lineage graphs, click **Runs** on the left sidebar. This page is structured similarly to the Airflow UI calendar view. It provides a list of your most recent runs, as well as a calendar that shows all runs for the last year.

![Lineage summary page](/img/docs/lineage-explore.png)

This view can help you get a better sense of the scope of your lineage integrations. It can also help you confirm that a recent run was picked up by the lineage backend as expected.

## View recently accessed datasets

Use the **Datasets** page to view a table of recent datasets that your DAGs have read or written to. This information can help you quickly identify dataset dependencies and data pipeline access requirements.

![Datasets page](/img/docs/lineage-datasets.png)

Each row in the table includes:

- The name of the dataset.
- The namespace of the job run that accessed the dataset.
- The type of job that interacted with the dataset.
- When the dataset was accessed.

Click on the name of a dataset to show its lineage graph.

### Filter datasets by Deployment

To view datasets that a specific Deployment read or wrote to:

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click **Lineage**. Your Organization **Datasets** tab opens and filters to show only datasets that the selected Deployment read or wrote to.

Alternatively, you can filter datasets by Deployment directly from the **Datasets** tab.

1. In the Cloud UI, click **Lineage**, then click **Datasets**.
2. Click **Select namespace**.
3. Select the namespace for your Deployment. You can find a Deployment's namespace by opening the Deployment in the Cloud UI and checking the value in **Namespace**. 