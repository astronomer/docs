---
title: "Orchestrate Databricks jobs with Airflow"
sidebar_label: "Tutorial"
description: "Orchestrate Databricks jobs with your Airflow DAGs."
id: airflow-databricks
tags: [Integrations, DAGs]
sidebar_custom_props: { icon: 'img/integrations/databricks.png' }
---

import CodeBlock from '@theme/CodeBlock';
import databricks_tutorial_dag from '!!raw-loader!../code-samples/dags/airflow-databricks/databricks_tutorial_dag.py';

[Databricks](https://databricks.com/) is a popular unified data and analytics platform built around [Apache Spark](https://spark.apache.org/) that provides users with fully managed Apache Spark clusters and interactive workspaces.

The open source [Astro Databricks provider](https://github.com/astronomer/astro-provider-databricks) provides full observability and control from Airflow so you can manage your Workflows from one place, which enables you to orchestrate your Databricks notebooks from Airflow and execute them as Databricks Workflows.

You can create a Databricks Workflow from existing Databricks notebooks as a task group in your Airflow DAG with just a few lines of code:

```python
task_group = DatabricksWorkflowTaskGroup(
    group_id="databricks_workflow",
    databricks_conn_id=DATABRICKS_CONN_ID,
    job_clusters=job_cluster_spec,
)

with task_group:
    notebook_1 = DatabricksNotebookOperator(
        task_id="notebook1",
        databricks_conn_id=DATABRICKS_CONN_ID,
        notebook_path=DATABRICKS_NOTEBOOK_PATH_1,
        source="WORKSPACE",
        job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
    )
    notebook_2 = DatabricksNotebookOperator(
        task_id="notebook2",
        databricks_conn_id=DATABRICKS_CONN_ID,
        notebook_path=DATABRICKS_NOTEBOOK_PATH_2,
        source="WORKSPACE",
        job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
    )
    notebook_1 >> notebook_2
```


This tutorial shows how to use the Astro Databricks provider to run two Databricks notebooks as a Databricks Workflow. If you don't use Databricks Workflows, see [Alternative ways to run Databricks with Airflow](#alternative-ways-to-run-databricks-with-airflow).

:::tip Related content

There are multiple resources for learning about this topic. See also:

- Webinar: [How to Orchestrate Databricks Jobs Using Airflow](https://www.astronomer.io/events/webinars/how-to-orchestrate-databricks-jobs-using-airflow/).
- Use case: [ELT with Airflow and Databricks](use-case-airflow-databricks.md) including a ready-to-use [example project repository](https://github.com/astronomer/astro-provider-databricks/blob/main/quickstart/astro-cli.md).

:::

## Why use Airflow with Databricks

Many data teams leverage Databricks' optimized Spark engine to run heavy workloads like machine learning models, data transformations, and data analysis. While Databricks offers some orchestration with Databricks Workflows, they are limited in functionality and do not integrate with the rest of your data stack. Using a tool-agnostic orchestrator like Airflow gives you several advantages, like the ability to:

- Use CI/CD to manage your workflow deployment. Airflow DAGs are Python code, and can be [integrated with a variety of CI/CD tools](https://docs.astronomer.io/astro/ci-cd-templates/template-overview) and [tested](testing-airflow.md).
- Repair single tasks in your Databricks Workflow. If a task fails, you can [re-run it](#repairing-a-databricks-workflow) without having to re-run the entire Workflow, saving valuable compute resources.
- Use [task groups](task-groups.md) within Databricks Workflows, enabling you to collapse and expand parts of larger Databricks Workflows visually.
- Leverage Airflow [cross-DAG dependencies](cross-dag-dependencies.md) to trigger Databricks Workflows from other DAGs in your Airflow environment, allowing for a data-driven architecture.
- Use familiar Airflow code as your interface to orchestrate Databricks notebooks as Workflows.
- [Inject parameters](#parameters) into your Databricks Workflow at the Workflow-level. These parameters can be dynamic and retrieved at runtime from other Airflow tasks.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Databricks. See [Getting started with Databricks](https://www.databricks.com/learn).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- Access to a Databricks workspace. See [Databricks' documentation](https://docs.databricks.com/getting-started/index.html) for instructions. You can use any workspace that has access to the [Databricks Workflows](https://docs.databricks.com/workflows/index.html) feature. You need a user account with permissions to create notebooks and Databricks jobs. You can use any underlying cloud service, and a [14-day free trial](https://www.databricks.com/try-databricks) is available.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-databricks-tutorial && cd astro-databricks-tutorial
    $ astro dev init
    ```

2. Add the [Astro Databricks provider package](https://github.com/astronomer/astro-provider-databricks) to your requirements.txt file.

    ```text
    astro-provider-databricks==0.1.3
    ```

3. Define the following environment variable in your `.env` file. This allows you to serialize Astro Databricks provider objects.

    ```text
    AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES = airflow\.* astro_databricks\.*
    ```

## Step 2: Create Databricks Notebooks

You can orchestrate any Databricks notebooks in a Databricks Workflow using the Astro Databricks provider. If you don't have Databricks notebooks ready, follow these steps to create two notebooks:

1. [Create an empty notebook](https://docs.databricks.com/notebooks/notebooks-manage.html) in your Databricks workspace called `notebook1`. 

2. Copy and paste the following code into the `notebook1` notebook.

    ```python
    print("Hello")
    ```

3. Create a second empty notebook in your Databricks workspace called `notebook2`.

4.  Copy and paste the following code into the `notebook2` notebook.

    ```python
    print("World")
    ```

## Step 3: Configure the Databricks connection

1. Start Airflow by running `astro dev start`.

2. In the Airflow UI, go to **Admin** > **Connections** and click **+**. 

3. Create a new connection named `databricks_conn`. Select the connection type `Databricks` and enter the following information:

    - **Connection ID**: `databricks_conn`.
    - **Connection Type**: `Databricks`.
    - **Host**: Your Databricks host address (format: `https://dbc-1234cb56-d7c8.cloud.databricks.com/`).
    - **Login**: Your Databricks login username (email).
    - **Password**: Your [Databricks personal access token](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens).

## Step 4: Create your DAG

1. In your `dags` folder, create a file called `my_simple_databricks_dag.py`.

2. Copy and paste the following DAG code into the file. Replace`<your-databricks-login-email>` variable with your Databricks login email. If you already had Databricks notebooks and did not create new ones in Step 2, replace the notebook names in the DatabricksNotebookOperator instances.

    <CodeBlock language="python">{databricks_tutorial_dag}</CodeBlock>

    This DAG uses the Astro Databricks provider to create a Databricks Workflow that runs two notebooks. The `databricks_workflow` task group, created using the `DatabricksWorkflowTaskGroup` class, automatically creates a Databricks Workflow that executes the Databricks notebooks you specified in the individual DatabricksNotebookOperators. One of the biggest benefits of this setup is the use of a Databricks job cluster, allowing you to [significantly reduce your Databricks cost](https://www.databricks.com/product/pricing). The task group contains three tasks:

    - The `launch` task, which the task group automatically generates, provisions a Databricks `job_cluster` with the spec defined as `job_cluster_spec` and creates the Databricks job from the tasks within the task group.
    - The `notebook1` task runs the `notebook1` notebook in this cluster as the first part of the Databricks job.
    - The `notebook2` task runs the `notebook2` notebook as the second part of the Databricks job. 

3. Run the DAG manually by clicking the play button and view the DAG in the graph view. Double click the task group in order to expand it and see all tasks.  

    ![Astro Databricks DAG graph view](/img/guides/astro_databricks_provider_dag_graph.png)

4. View the completed Databricks Workflow in the Databricks UI.

    ![Databricks Workflow](/img/guides/databricks_workflow.png)

## How it works

This section explains Astro Databricks provider functionality in more depth. You can learn more about the Astro Databricks provider in the [provider documentation](https://astronomer.github.io/astro-provider-databricks/).

### Parameters

The DatabricksWorkflowTaskGroup provides configuration options via several parameters:

- `job_clusters`: the job clusters for this Workflow to use. You can provide the full `job_cluster_spec` as shown in the tutorial DAG.
- `notebook_params`: a dictionary of parameters to make available to all notebook tasks in a Workflow.
- `notebook_packages`: a list of dictionaries defining Python packages to install in all notebook tasks in a Workflow.
- `extra_job_params`: a dictionary with properties to override the default Databricks Workflow job definitions.

You also have the ability to specifiy parameters at the task level in the DatabricksNotebookOperator:

- `notebook_params`: a dictionary of parameters to make available to the notebook.
- `notebook_packages`: a list of dictionaries defining Python packages to install in the notebook.

Note that you cannot specify the same packages in both the `notebook_packages` parameter of a DatabricksWorkflowTaskGroup and the `notebook_packages` parameter of a task using the DatabricksNotebookOperator in that same task group. Duplicate entries in this parameter cause an error in Databricks.

### Repairing a Databricks Workflow

The Astro Databricks provider includes functionality to repair a failed Databricks Workflow by making a repair request to the [Databricks Jobs API](https://docs.databricks.com/api-explorer/workspace/jobs/repairrun). Databricks expects a single repair request for all tasks that need to be rerun in one cluster, this can be achieved via the Airflow UI by using the operator extra link **Repair All Failed Tasks**. If you would be using Airflow's built in [retry functionality](rerunning-dags.md#automatically-retry-tasks) a separete cluster would be created for each failed task.

![Repair All Failed Tasks OEL](/img/guides/repair_all_failed_databricks_tasks_oel.png)

If you only want to rerun specific tasks within your Workflow, you can use the **Repair a single failed task** operator extra link on an individual task in the Databricks Workflow.

![Repair a single failed task OEL](/img/guides/repair_single_failed_databricks_task_oel.png)

## Alternative ways to run Databricks with Airflow

The Astro Databricks provider is under active development, and support for more Databricks task types is still being added. If you want to orchestrate an action in your Databricks environment that is not yet supported by the Astro Databricks provider such as [updating a Databricks repository](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest/modules/DatabricksReposUpdateOperator), check the [community-managed Databricks provider](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest) for relevant operators. 

Additionally, the community-managed Databricks provider contains hooks (for example the [DatabricksHook](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest/modules/DatabricksHook)) that simplify interaction with Databricks, including writing your own [custom Databricks operators](airflow-importing-custom-hooks-operators.md#create-a-custom-operator).

You can find several example DAGs that use the community-managed Databricks provider on the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest).
