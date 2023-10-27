---
title: "Introduction to Airflow DAGs"
sidebar_label: "DAGs"
description: "How to write your first DAG in Apache Airflow"
id: dags
---

<head>
  <meta name="description" content="Learn how to write DAGs and get tips on how to define an Airflow DAG in Python. Learn all about DAG parameters and their settings." />
  <meta name="og:description" content="Learn how to write DAGs and get tips on how to define an Airflow DAG in Python. Learn all about DAG parameters and their settings." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import airflow_decorator_example_traditional_syntax from '!!raw-loader!../code-samples/dags/dags/dags_s3_to_snowflake_example.py';
import example_dag_basic_taskflow from '!!raw-loader!../code-samples/dags/dags/example_dag_basic_taskflow.py';
import example_dag_basic_traditional from '!!raw-loader!../code-samples/dags/dags/example_dag_basic_traditional.py';

In Airflow, data pipelines are defined in Python code as directed acyclic graphs, also known as DAGs. Within a graph, each node represents a task which completes a unit of work, and each edge represents a dependency between tasks.

In this guide, you'll learn DAG basics and about DAG parameters and how to define a DAG in Python.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: DAGs 101](https://academy.astronomer.io/dag-101-1) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## What is a DAG?

In Airflow, a directed acyclic graph (DAG) is a data pipeline defined in Python code. Each DAG represents a collection of tasks you want to run and is organized to show relationships between tasks in the Airflow UI. The mathematical properties of DAGs make them useful for building data pipelines:

- Directed: If multiple tasks exist, then each task must have at least one defined upstream or downstream task.
- Acyclic: Tasks cannot have a dependency to themselves. This avoids infinite loops.
- Graph: All tasks can be visualized in a graph structure, with relationships between tasks defined by nodes and vertices.

Aside from these requirements, DAGs in Airflow can be defined however you need! They can have a single task or thousands of tasks arranged in any number of ways.

An instance of a DAG running on a specific date is called a DAG run. DAG runs can be started by the Airflow scheduler based on the DAG's defined schedule, or they can be started manually.

## Writing a DAG

DAGs in Airflow are defined in a Python script that is placed in an Airflow project's `DAG_FOLDER`. Airflow will execute the code in this folder to load any DAG objects. If you are working with the [Astro CLI](https://docs.astronomer.io/astro/cli/overview), DAG code is placed in the `dags` folder. 

Most DAGs follow this general flow within a Python script:

- Imports: Any needed Python packages are imported at the top of the DAG script. This always includes a `dag` function import (either the `DAG` class or the `dag` decorator). It can also include provider packages or other general Python packages.
- DAG instantiation: A DAG object is created and any DAG-level parameters such as the schedule interval are set.
- Task instantiation: Each task is defined by calling an operator and providing necessary task-level parameters.
- Dependencies: Any dependencies between tasks are set using bitshift operators (`<<` and `>>`), the `set_upstream()` or `set_downstream` functions, or the `chain()` function. Note that if you are using the TaskFlow API, dependencies are inferred based on the task function calls.

The following example DAG loads data from Amazon S3 to Snowflake, runs a Snowflake query, and then sends an email.

<CodeBlock language="python">{airflow_decorator_example_traditional_syntax}</CodeBlock>

In the **Graph** view you can see the example DAG consisting of 3 tasks:

![s3_to_snowflake example DAG](/img/guides/s3_to_snowflake_example.png)

The example DAG makes use of the [Snowflake provider package](https://registry.astronomer.io/providers/snowflake). Providers are Python packages separate from core Airflow that contain hooks, operators, and sensors to integrate Airflow with third party services. The [Astronomer Registry](https://registry.astronomer.io/) is the best place to go to learn about available Airflow providers.

Astronomer recommends creating one Python file for each DAG. Some advanced use cases might require [dynamically generating DAG files](dynamically-generating-dags.md), which can also be accomplished using Python.

### Writing DAGs with the TaskFlow API

Additionally to using operators as shown in the previous example, you can use Airflow [decorators](airflow-decorators.md) to define tasks. One of the most commonly used decorator is the `@task` decorator that allows you to replace the traditional PythonOperator. The purpose of decorators in Airflow is to simplify the DAG authoring experience by eliminating boilerplate code. How you author your DAGs is a matter of preference and style. 

The following DAG consists of 3 tasks and its TaskFlow API version is generated as `example_dag_basic` when you initiate a new project with the Astro CLI. Compare the code between the TaskFlow API syntax and the traditional syntax.

<Tabs
    defaultValue="taskflow"
    groupId= "writing-dags-with-the-taskflow-api"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{example_dag_basic_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{example_dag_basic_traditional}</CodeBlock>

</TabItem>
</Tabs>

Keep in mind: when using decorators, you must call the DAG and task functions in the DAG script for Airflow to register them.

## DAG parameters

In Airflow, you can configure when and how your DAG runs by setting parameters in the DAG object. DAG-level parameters affect how the entire DAG behaves, as opposed to task-level parameters which only affect a single task.

In the previous example, DAG parameters were set within the `@dag()` function call and the `DAG` object:

<Tabs
    defaultValue="taskflow"
    groupId= "dag-parameters"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
@dag(
    "example_dag",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "retries": 2
    },
    tags=["example"]
)
def my_example_dag():

    # add tasks


my_example_dag()

```

</TabItem>

<TabItem value="traditional">

```python
with DAG(
    "example_dag",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "retries": 2
    },
    tags=["example"]
):

    # add tasks

```

</TabItem>
</Tabs>

These parameters define:

- How the DAG is identified: `example_dag` (provided in this case as a positional argument without the `dag_id` parameter name) and `tags`
- When the DAG will run: `schedule`
- What periods the DAG runs for: `start_date` and `catchup`
- How failures are handled for all tasks in the DAG: `retries`

Every DAG requires a `dag_id` and a `schedule`. All other parameters are optional. The following parameters are relevant for most use cases:

- `dag_id`: The name of the DAG. This must be unique for each DAG in the Airflow environment. This parameter is required.
- `schedule`: A timedelta expression defining how often a DAG runs. This parameter is required. If the DAG should only be run on demand, `None` can be provided. Alternatively the schedule interval can be provided as a CRON expression or as a macro like `@daily`.
- `start_date`: The date for which the first DAG run should occur. If a DAG is added after the `start_date`, the scheduler will attempt to backfill all missed DAG runs provided `catchup` (see below) is not set to `False`.
- `end_date`: The date beyond which no further DAG runs will be scheduled. Defaults to `None`.
- `catchup`: Whether the scheduler should backfill all missed DAG runs between the current date and the start date when the DAG is added. Defaults to `True`.
- `default_args`: A dictionary of parameters that will be applied to all tasks in the DAG. These parameters will be passed directly to each operator, so they must be parameters that are part of the [`BaseOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html).
- `max_active_tasks`: The number of task instances allowed to run concurrently.
- `max_active_runs`: The number of active DAG runs allowed to run concurrently.
- `default_view`: The default view of the DAG in the Airflow UI (grid, graph, duration, gantt, or landing_times). 
- `tags`: A list of tags shown in the Airflow UI to help with filtering DAGs.
- `fail_stop`: In Airflow 2.7+ you can set this parameter to `True` to stop DAG execution as soon as one task in this DAG fails. Any tasks that are still running are marked as `failed` and any tasks that have not run yet are marked as `skipped`. Note that you cannot have any [trigger rule](managing-dependencies.md#trigger-rules) other than `all_success` in a DAG with `fail_stop` set to `True`.

For a list of all DAG parameters, see the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/DAG).
