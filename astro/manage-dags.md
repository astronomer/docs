---
sidebar_label: 'Manage DAG runs'
title: "Manage DAG runs from the Cloud UI"
id: manage-dags
---

:::info

Managing DAGs from the Cloud UI is currently available only on [Astro Hosted](astro-overview.md). Support on Astro Hybrid is coming soon.

:::

You can perform some common Airflow UI actions from the Cloud UI, including:

- Marking DAG and task runs as succeeded/failed.
- Retrying DAG and task runs.
- Viewing DAG and task run statuses.

These actions are available on the **DAGs** page, where you can see detailed information about a specific DAG. This page compiles the most commonly used information and actions from the Airflow UI into one place so that you can manage your DAGs without switching between the Airflow UI and Cloud UI.

![DAGs page](/img/docs/DAGs-overview.png)

## Access the DAGs page in the Cloud UI

1. In the Cloud UI, select a Deployment.
2. Click **DAGs**.
3. Click the name of the DAG that you want to manage.

### Available actions

The actions and views on this page are functionally identical to certain actions in the Airflow UI. Use the following table to understand each available Cloud UI action and its equivalent action in the Airflow UI. 

| User action                              | **DAGs** page workflow                                                 | Equivalent Airflow UI workflow                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Trigger a DAG run.                        | Click **Run**.                                                          | Click the **Play** icon on the **DAGs** page.                                                                                   |
| View the DAG run [grid](https://airflow.apache.org/docs/apache-airflow/stable/ui.html#grid-view).                    | None. DAG code appears by default.                                     | Click the DAG name on the **DAGs** page.                                                                                        |
| View the [graph](https://airflow.apache.org/docs/apache-airflow/stable/ui.html#graph-view) for a DAG run.                   | None. DAG code appears by default.                                     | Click the DAG name on the **DAGs** page, then click **Graph**.                                                                                        |
| View [task run logs](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/logging-tasks.html).                       | Click the task run in the DAG run grid, then click **Logs**.                                | Click the DAG name on the **DAGs** page, click the task run in the **Grid** view, then click **Logs**.                          |
| View DAG code.                            | None. DAG code appears by default.                                     | Click the DAG name on the **DAGs** page, then click **Code**.                                                                   |
| [Retry a DAG run](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#re-run-dag).                   | Click the DAG run in the DAG run grid, then click **Retry**.      | Click the DAG name on the **DAGs** page, click the DAG run in the **Grid** view, then click **Clear existing tasks**.      |
| [Retry a task run](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#re-run-tasks).                   | Click the task run in the DAG run grid, click **Retry**, then select additional options for retrying your task(s).   | Click the DAG name on the **DAGs** page, click the task run in the **Grid** view, then click **Clear**.      |
| [Mark a DAG/ task run](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#dag-run-status) as success/ failed. | Click the DAG/task run in the DAG run grid, then click **Mark as...**. | Click the DAG name on the **DAGs** page, click the DAG/task run in the **Grid** view, then click **Mark Success/ Mark Failed**. |


