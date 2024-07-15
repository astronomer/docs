---
title: "Apache Airflow® trigger rules"
sidebar_label: "Trigger rules"
id: airflow-trigger-rules
description: "Learn about available trigger rules and how to use them."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import branch_example_taskflow from '!!raw-loader!../code-samples/dags/airflow-trigger-rules/branch_example_taskflow.py';
import branch_example_traditional from '!!raw-loader!../code-samples/dags/airflow-trigger-rules/branch_example_traditional.py';

Trigger rules are used to determine when a task should run in relation to the previous task. By default, Apache Airflow® runs a task when all directly upstream tasks are successful. However, you can change this behavior using the `trigger_rule` parameter in the task definition.

:::info

Trigger rules define whether a task runs based on its direct upstream dependencies. To learn how to set task dependencies, see the [Manage task and task group dependencies in Airflow](managing-dependencies.md) guide.

:::

## Define a trigger rule

You can override the default trigger rule by setting the `trigger_rule` parameter in the task definition.

<Tabs
    defaultValue="taskflow"
    groupId= "branching-and-trigger-rules"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python {8}
# from airflow.decorators import task
# from airflow.models.baseoperator import chain

@task 
def upstream_task():
    return "Hello..."

@task(trigger_rule="all_success")
def downstream_task():
    return " World!"

chain(upstream_task(), downstream_task())
```

</TabItem>

<TabItem value="traditional">

```python {6}
# from airflow.operators.empty import EmptyOperator

upstream_task = EmptyOperator(task_id="upstream_task")
downstream_task = EmptyOperator(
    task_id="downstream_task",
    trigger_rule="all_success"
)
chain(upstream_task, downstream_task)
```

</TabItem>
</Tabs>

## Available trigger rules in Apache Airflow®

The following trigger rules are available:

- `all_success`: (default) The task runs only when all upstream tasks have succeeded.
- `all_failed`: The task runs only when all upstream tasks are in a failed or upstream\_failed state.
- `all_done`: The task runs once all upstream tasks are done with their execution.
- `all_skipped`: The task runs only when all upstream tasks have been skipped. 
- `one_failed`: The task runs when at least one upstream task has failed. 
- `one_success`: The task runs when at least one upstream task has succeeded.
- `one_done`: The task runs when at least one upstream task has either succeeded or failed.
- `none_failed`: The task runs only when all upstream tasks have succeeded or been skipped.
- `none_failed_min_one_success`: The task runs only when all upstream tasks have not failed or upstream_failed, and at least one upstream task has succeeded.
- `none_skipped`: The task runs only when no upstream task is in a skipped state.
- `always`: The task runs at any time.

:::info 

There are several advanced Airflow features that influence trigger rules. You can define a DAG in which any task failure stops the DAG execution by setting the [DAG parameter](airflow-dag-parameters.md) `fail_stop` to `True`. This will set all tasks that are still running to `failed` and mark any tasks that have not run yet as `skipped`. Note that you cannot have any trigger rule other than `all_success` in a DAG with `fail_stop` set to `True`.

[Setup and Teardown tasks](airflow-setup-teardown.md) are a special type of task to create and delete resources that also influence trigger rules.

:::

## Branching and trigger rules

One common scenario where you might need to implement trigger rules is if your DAG contains conditional logic such as [branching](airflow-branch-operator.md). In these cases, `one_success` or `none_failed` are likely more helpful than `all_success`, because unless all branches are run, at least one upstream task will always be in a `skipped` state.

In the following example DAG there is a simple branch with a downstream task that needs to run if either of the branches are followed. With the `all_success` rule, the `end` task never runs because all but one of the `branch` tasks is always ignored and therefore doesn't have a success state. If you change the trigger rule to `one_success`, then the `end` task can run so long as one of the branches successfully completes.

<Tabs
    defaultValue="taskflow"
    groupId= "branching-and-trigger-rules"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{branch_example_taskflow}</CodeBlock>

This image shows the resulting DAG:

![Branch Dependencies](/img/guides/managing-dependencies_branch_decorator.png)

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{branch_example_traditional}</CodeBlock>

This image shows the resulting DAG:

![Branch Dependencies](/img/guides/managing-dependencies_branch_traditional.png)

</TabItem>
</Tabs>