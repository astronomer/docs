---
title: "Select the right trigger rule for your task"
sidebar_label: "Trigger rules"
id: airflow-trigger-rules
description: "Learn about available trigger rules and how to use them."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Trigger rules are used to determine when a task should run in relation to the previous task. By default, Airflow runs a task when all directly upstream tasks are successful. However, you can change this behavior using the `trigger_rule` parameter in the task definition.

## Define a trigger rule

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

## Available trigger rules

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

## Examples

### Trigger rule `all_success`

A task with the trigger rule `all_success` only runs when all upstream tasks have succeeded.

![Screenshot of the Airflow UI with a DAG graph showing 4 successful upstream tasks and one successful downstream task depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_success_1.png)

As soon as any upstream tasks are state of `failed` or `upstream_failed`, the downstream task is set to the state `upstream_failed` and does not run. 

![Screenshot of the Airflow UI with a DAG graph showing 2 successful, 1 running and 1 failed upstream tasks and one downstream task in upstream_failed state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_success_2.png)

Analogously, as soon as any upstream task is in the state `skipped`, the downstream task is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 2 successful, 1 running and 1 skipped upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_success_3.png)

If a task with the trigger rule `all_success` has one upstream task that is skipped and one that is failed, whether the downstream task is set to `skipped` or `upstream_failed` depends on which of the upstream tasks finishes first.

### Trigger rule `all_failed`

### Trigger rule `all_done`