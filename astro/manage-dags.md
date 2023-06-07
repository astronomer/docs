---
sidebar_label: 'Manage DAG runs from the Cloud UI'
title: "Manage DAGs"
id: manage-dags
---

:::info

Managing DAGs from the Cloud UI is currently available only on [Astro Hosted](astro-overview.md). Support on Astro Hybrid is coming soon.

:::
When you select a specific DAG in the **DAGs** page, you can see detailed information about your DAG runs and complete a number of tasks that are normally available from the Airflow UI. This page compiles the most commonly used information and actions from the Airflow UI into one place.

![DAGs page](/img/docs/DAGs-overview.png)

To access the DAG management page:

1. In the Cloud UI, select a Deployment.
2. Click **DAGs**.
3. Click the name of the DAG that you want to manage.

The actions and views on this page are functionally identical to certain actions in the Airflow UI. Use the following table to understand each available Cloud UI action and its equivalent action in the Airflow UI. 

| User action                              | **DAGs** page workflow                                                 | Equivalent Airflow UI workflow                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Trigger a DAG run                        | Click **Run**                                                          | Click the **Play** icon on the **DAGs** page.                                                                                   |
| View the DAG run grid                    | None. DAG code appears by default.                                     | Click the DAG name on the **DAGs** page.                                                                                        |
| Retry a DAG/ task run.                   | Click the DAG run in the DAG run grid, then click **Retry**.      | Click the DAG name on the **DAGs** page, click the DAG run in the **Grid** view, then click **Clear existing tasks**.      |
| Retry a task run.                   | Click the task run in the DAG run grid, click **Retry**, then select additional options for retrying your task(s).   | Click the DAG name on the **DAGs** page, click the task run in the **Grid** view, then click **Clear**.      |
| Mark a DAG/ task run as success/ failed. | Click the DAG/task run in the DAG run grid, then click **Mark as...**. | Click the DAG name on the **DAGs** page, click the DAG/task run in the **Grid** view, then click **Mark Success/ Mark Failed**. |
| View DAG code                            | None. DAG code appears by default.                                     | Click the DAG name on the **DAGs** page, then click **Code**.                                                                   |
| View task run logs                       | Click the task run in the DAG run grid.                                | Click the DAG name on the **DAGs** page, click the task run in the **Grid** view, then click **Logs**.                          |
