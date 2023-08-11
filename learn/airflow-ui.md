---
title: "An introduction to the Airflow UI"
sidebar_label: "The Airflow UI"
description: "An overview of the Airflow UI"
id: airflow-ui
---

<head>
  <meta name="description" content="Explore the Airflow UI, which helps you monitor and troubleshoot your data pipelines. Learn about some of its key features and visualizations." />
  <meta name="og:description" content="Explore the Airflow UI, which helps you monitor and troubleshoot your data pipelines. Learn about some of its key features and visualizations." />
</head>

A notable feature of Apache Airflow is the [user interface (UI)](https://airflow.apache.org/docs/apache-airflow/stable/ui.html), which provides insights into your DAGs and DAG runs. The UI is a useful tool for understanding, monitoring, and troubleshooting your pipelines.

This guide is an overview of some of the most useful features and visualizations in the Airflow UI. Each section of this guide corresponds to one of the tabs at the top of the Airflow UI. If you're not already using Airflow and want to get it up and running to follow along, see [Install the Astro CLI](https://docs.astronomer.io/astro/cli/get-started) to quickly run Airflow locally.

This guide focuses on the Airflow 2 UI. If you're using an older version of the UI, see [Upgrading from 1.10 to 2](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/index.html).

All images in this guide were taken from an [Astronomer Runtime](https://docs.astronomer.io/astro/runtime-release-notes) Airflow image. Other than some modified colors and an additional `Astronomer` tab, the UI is the same as that of OSS Airflow.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).

## DAGs

The **DAGs** view is the landing page when you sign in to Airflow. It shows a list of all your DAGs, the status of recent DAG runs and tasks, the time of the last DAG run, and basic metadata about the DAG like the owner and the schedule. To see the status of the DAGs update in real time, toggle **Auto-refresh**.

![DAGs View](/img/guides/airflow-ui_DAGs_overview.png)

In the DAGs view you can:

- Pause/unpause a DAG with the toggle to the left of the DAG name.
- Filter the list of DAGs to show active, paused, or all DAGs.
- Filter the list of DAGs to show currently running DAGs or DAGs that failed their last DAG run.
- Trigger or delete a DAG with the buttons in the Actions section.
- Navigate quickly to other DAG-specific pages from the Links section.

To see more information about a specific DAG, click its name or use one of the links.

## Grid view

The **Grid** view is the main DAG view and gives you detailed insights into a specific DAG, including its DAG runs and task instances. When running the DAG, toggle **Auto-refresh** to see the status of the tasks update in real time.

On the left side the **Grid** view shows a grid representation of the DAG's previous runs, including their duration and the outcome of all individual task instances. Each column represents a DAG run and each square represents a task instance in that DAG run. Task instances are color-coded according to their status. A small play icon on a DAG run indicates that a run was triggered manually, and a small dataset icon shows that a run was triggered via a [dataset update](https://astronomer.io/guides/airflow-datasets). If no icon is shown, the DAG ran according to its schedule.

![Grid view left side](/img/guides/airflow-ui_grid_left_side.png)

On the right side you can see further details about the item (DAG, DAG run or task instance) that is currently selected. 

![Grid view right side](/img/guides/airflow-ui_grid_right_side.png)

There are 4 tabs available within the **Grid** view:

- **Details**: Shows more details about the DAG, DAG run or task instance.
- **Graph**: Shows a graph representation of the DAG, with tasks as nodes and dependencies as edges.
- **Gantt**: Shows the duration of each task instance in a DAG run as a Gantt chart.
- **Code**: Shows the DAG code.

### Details

The **Details** tab displays information about the DAG, individual DAG runs and in-depth information about each task instance. In the **Details** tab you will for example find the total historic runs of a DAG, the data interval start of a DAG run or the duration of a task instance. 

In order to access the details of a specific DAG run or task instance, you need first need to select it in the grid, as shown in the following gif:

![Grid view details](/img/guides/airflow-ui_grid_details.gif)

When you select a task instance in the **Grid** view, four additional options appear underneath the tabs:

![Grid view task instance](/img/guides/airflow-ui_grid_ti_options.png)

- **More Details:**  Shows the fully rendered task - an exact summary of what the task does (attributes, values, templates, etc.).
- **Rendered Template:** Shows the task's metadata after it has been templated.
- **XCom:** Shows XComs created by that particular `TaskInstance`.
- **List Instances, all runs:** Shows a historical view of task instances and statuses for that particular task.

### Graph

In Airflow version 2.6 and later, the **Grid** view includes an integrated graph visualization of the tasks and dependencies in your DAG. If you select a task or task group instance in the **Grid** column, the graph highlights and zooms to the selected task. You can also navigate complex DAGs using **Filter Tasks** and the minimap. This view is useful to explore the DAG structure and task dependencies.

![Grid graph](/img/guides/airflow-ui_grid_graph.gif)

### Gantt

The **Gantt** tab shows the duration of each task instance in a DAG run as a Gantt chart. This view is often used to quickly identify which tasks cause a DAG to run long and which tasks were running in parallel.

![Grid gantt](/img/guides/airflow-ui_grid_gantt.png)

### Code

Under the **Code** tab you can access the code that generates the DAG you are viewing. While your code should live in source control, the **Code** tab provides a quick insight into what is going on in the DAG. DAG code can't be edited in the UI.

![Grid code](/img/guides/airflow-ui_grid_code.png)

This tab shows code only from the file that generated the DAG. It does not show any code that may be imported in the DAG, such as custom hooks or operators or code in your `/include` directory.

### Logs

To access the [logs](logging.md#log-locations) of a specific task instance, click on the **Logs** tab which appears in the **Grid** view, as soon as you select a task instance.

![Grid logs](/img/guides/airflow-ui_grid_logs.gif)

### Actions

When a DAG run, task instance or [task group](task-groups.md) instance is selected in the **Grid** view several action buttons appear.

![Grid actions](/img/guides/airflow-ui_grid_actions.png)

- **Clear** / **Clear task** : This button will clear the selected DAG run, task group instance or task instance and run it again. This is useful if you want to re-run a task or DAG run that has failed or during local development. After clicking **Clear task** you will be offered a detailed interface controlling which task instances should be cleared and rerun. See [Manually rerun tasks or DAGs](rerunning-dags.md#manually-rerun-tasks-or-dags).
- **Mark state as...**: This button allows you to mark the selected DAG run, task group instance or task instance as successful or failed without actually running it. This option is often used when the root cause of a task failure was fixed manually in the target data tool and the pipeline should continue after that task without rerunning it. Many data teams leverage [Task Instance Notes and DAG Run Notes](rerunning-dags#add-notes-to-cleared-tasks-and-dags) in order to document the reason for marking a task instance as failed or successful.
- **Clear Task Filter**: This button allows you to filter the tasks shown in the **Grid** view based on task dependencies. For example, by selecting **Filter downstream** only the tasks downstream of your selected task will show. 

![Grid filter](/img/guides/airflow-ui_grid_filter.gif)

### Keyboard shortcuts

In Airflow 2.7 keyboard shortcuts where added to the **Grid** view. You can see all available shortcuts by pressing `shift` + `/` while in the **Grid** view.

![Grid view shortcuts](/img/guides/airflow-ui_shortcuts.png)

## Additional DAG views

The following are the additional DAG views that are available, but not discussed in this guide:

- **Calendar** view: Shows the state of DAG runs overlaid on a calendar. States are represented by color. If there were multiple DAG runs on the same day with different states, the color is a gradient between green (success) and red (failure).

![Calendar View](/img/guides/2_4_CalendarView.png)

- **Task Duration:** Shows a line graph of the duration of each task over time.
- **Task Tries:** Shows a line graph of the number of tries for each task in a DAG run over time.
- **Landing Times:** Shows a line graph of the time of day each task started over time.
- **Details:** Shows details of the DAG configuration and DagModel debug information.
- **Audit Log:** Shows selected events for all DAG runs.

## Cluster activity tab

The cluster activity tab was added in Airflow 2.7 and shows aggregated metrics for the entire Airflow cluster. There are live metrics available such as currently occupied slots in different [pools](airflow-pools.md), unpaused DAGs and scheduler health.
The historical metrics shown include states of past DAG runs, task instances and how DAGs runs were triggered.

![Cluster activity](/img/guides/airflow-ui_cluster_activity.png)

## Datasets tab

The **Dataset** tab was introduced in Airflow 2.4 in support of the new [dataset driven scheduling](airflow-datasets.md) feature. The **Dataset** tab links to a page showing all datasets that have been produced in the Airflow environment, as well as all dependencies between datasets and DAGs in a graph.

![Datasets](/img/guides/2_5_Datasets.png)

Click a dataset to open the history of all updates to the dataset that were recorded in the Airflow environment.

![Dataset History](/img/guides/2_5_DatasetsDetails.png)

## Security tab

The **Security** tab links to multiple pages, including **List Users** and **List Roles**, that you can use to review and manage Airflow role-based access control (RBAC). For more information on working with RBAC, see [Security](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html).

![Security](/img/guides/2_4_SecurityTab.png)

If you are running Airflow on Astronomer, the Astronomer RBAC will extend into Airflow and take precedence. There is no need for you to use Airflow RBAC in addition to Astronomer RBAC. Astronomer RBAC can be managed from the Astronomer UI, so the **Security** tab might be less relevant for Astronomer users.

## Browse tab

The **Browse** tab links to multiple pages that provide additional insight into and control over your DAG runs and task instances for all DAGs in one place.

![Browse](/img/guides/2_4_BrowseTab.png)

The DAG runs and task instances pages are the easiest way to view and manipulate these objects in aggregate. If you need to re-run tasks in multiple DAG runs, you can do so from this page by selecting all relevant tasks and clearing their status.

![Task Instance](/img/guides/2_4_ListTaskInstance.png)

The DAG Dependencies view shows a graphical representation of any [cross-DAG](cross-dag-dependencies.md) and dataset dependencies in your Airflow environment.

![DAG Dependencies](/img/guides/2_4_DAGDependencies.png)

Other views on the **Browse** tab include:

- **Jobs:** Shows a list of all jobs that have been completed. This includes executed tasks as well as scheduler jobs.
- **Audit Logs:** Shows a list of events that have occurred in your Airflow environment that can be used for auditing purposes.
- **Task Reschedules:** Shows a list of all tasks that have been rescheduled.
- **Triggers:** Shows any triggers that occurred in this Airflow environment. To learn more about triggers and related concepts added in Airflow 2.2, you can check out the guide on [Deferrable Operators](deferrable-operators.md).
- **SLA Misses:** Shows any task instances that have missed their SLAs.

## Admin tab

The **Admin** tab links to pages for content related to Airflow administration that are not specific to any particular DAG. Many of these pages can be used to both view and modify your Airflow environment.

![Admin](/img/guides/2_4_AdminTab.png)

For example, the **Connections** page shows all Airflow connections stored in your environment. Click `+` to add a new connection. For more information, see [Managing your Connections in Apache Airflow](connections.md).

![Connections](/img/guides/2_4_Connections.png)

Similarly, the XComs page shows a list of all XComs stored in the metadata database and allows you to easily delete them.

![XComs](/img/guides/2_4_XComs.png)

Other pages on the **Admin** tab include:

- **Variables:** View and manage [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html).
- **Configurations:** View the contents of your `airflow.cfg` file. Note that this can be disabled by your Airflow admin for security reasons.
- **Plugins:** View any [Airflow plugins](https://airflow.apache.org/docs/apache-airflow/stable/plugins.html) defined in your environment.
- **Providers:** View all [Airflow providers](https://airflow.apache.org/docs/apache-airflow-providers/) included in your Airflow environment with their version number.
- **Pools:** View and manage [Airflow pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html).

## Docs

The Docs tab provides links to external Airflow resources including:

- [Airflow documentation](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/)
- [The Airflow website](https://airflow.apache.org/)
- [The Airflow GitHub repo](https://github.com/apache/airflow)
- The REST API Swagger and the Redoc documentation

![Docs](/img/guides/2_4_DocsTab.png)

## Conclusion

This guide provided a basic overview of some of the most commonly used features of the Airflow UI. 

The Airflow community is consistently working on improvements to the UI to provide a better user experience and additional functionality. Make sure you upgrade your Airflow environment frequently to ensure you are taking advantage of Airflow UI updates as they are released.

## Legacy: Graph view

The old **Graph** view was replaced by the integrated **Graph** tab in the **Grid** view in Airflow 2.7. It shows a visualization of the tasks and dependencies in your DAG and their current status for a specific DAG run. 

![Graph View](/img/guides/2_4_GraphView.png)

Click a specific task in the graph to access additional views and actions for the task instance. In Airflow 2.7+ you will find these options after clicking on a task instance in the **Grid** view.

![Graph Actions](/img/guides/2_4_GraphView_TaskInstance.png)