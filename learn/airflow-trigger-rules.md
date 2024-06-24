---
title: "Select the right trigger rule for your task"
sidebar_label: "Trigger rules"
id: airflow-trigger-rules
description: "Learn about available trigger rules and how to use them."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import branch_example_taskflow from '!!raw-loader!../code-samples/dags/airflow-trigger-rules/branch_example_taskflow.py';
import branch_example_traditional from '!!raw-loader!../code-samples/dags/airflow-trigger-rules/branch_example_traditional.py';

Trigger rules are used to determine when a task should run in relation to the previous task. By default, Airflow runs a task when all directly upstream tasks are successful. However, you can change this behavior using the `trigger_rule` parameter in the task definition.

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

## Branching and trigger rules

One common scenario where you might need to implement trigger rules is if your DAG contains conditional logic such as [branching](airflow-branch-operator.md). In these cases, `one_success` or `none_failed` is likely more helpful than `all_success`, because unless all branches are run, at least one upstream task will always be in a `skipped` state.

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

A task with the trigger rule `all_failed` only runs when all upstream tasks are in a failed or upstream_failed state.

![Screenshot of the Airflow UI with a DAG graph showing 2 failed and two upstream failed upstream tasks and one successful downstream task depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_failed_1.png)

As soon as any upstream task is in the state `success`, the downstream task is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 1 successful, 1 upstream failed and 1 running upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_failed_2.png)

Similarly, as soon as any upstream task is in the state `skipped`, the downstream task is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 1 running and 1 skipped, 1 upstream failed upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_failed_3.png)

### Trigger rule `all_done`

The `all_done` trigger rule will make a task wait until all upstream tasks are done with their execution.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 1 running, 1 skipped and one upstream failed upstream tasks and one downstream task in running state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_done_1.png)

As soon as all tasks finish, no matter what their state is, the downstream task will run.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 1 successful, 1 skipped and one upstream failed upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_done_2.png)

### Trigger rule `all_skipped`

A task with the trigger rule `all_skipped` only runs when all upstream tasks have been skipped.

![Screenshot of the Airflow UI with a DAG graph showing 4 skipped upstream tasks and one successful downstream task depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_skipped_1.png)

As soon as any upstream task is in the state `success`, `failed`, or `upstream_failed`, the downstream task with the trigger rule `all_skipped` is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 successful, 3 running and one queued upstream task and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_all_skipped_2.png)

### Trigger rule `one_failed`

The `one_failed` trigger rule will make a task run as soon as at least one of its upstream tasks are in either the `failed` or `upstream_failed` state.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 3 running and 1 queued upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_failed_1.png)

![Screenshot of the Airflow UI with a DAG graph showing 1 upstream failed, 3 running and 1 queued upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_failed_2.png)

If all upstream tasks have completed and none of them are in the `failed` or `upstream_failed` state, the downstream task will be set to the state `skipped`.

![Screenshot of the Airflow UI with a DAG graph showing 2 successful and 2 skipped upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_failed_3.png)

### Trigger rule `one_success`

The `one_success` trigger rule will make a task run as soon as at least one of its upstream tasks are in the `success` state.

![Screenshot of the Airflow UI with a DAG graph showing 1 successful, 3 running and 1 queued upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_success_1.png)

If all upstream tasks have been skipped, the downstream task with the `one_success` trigger rule is set to the state `skipped` as well.

![Screenshot of the Airflow UI with a DAG graph showing 4 skipped upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_success_2.png)

If all upstream tasks have completed and at least one of them is in the `failed` or `upstream_failed` state, the downstream task will be set to the state `upstream_failed`.

![Screenshot of the Airflow UI with a DAG graph showing 2 failed, 1 upstream failed and 1 skipped upstream tasks and one downstream task in upstream_failed state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_success_3.png)

### Trigger rule `one_done`

The `one_done` trigger rule makes a task run as soon as at least one of its upstream tasks is in either the `success` or `failed` state. Upstream tasks with `skipped` or `upstream_failed` states are not considered.

![Screenshot of the Airflow UI with a DAG graph showing 1 upstream failed, 1 skipped and 2 running upstream tasks and one downstream task in queued state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_done_1.png)

Once one upstream task finishes (either in the `success` or `failed` state), the downstream task runs.

![Screenshot of the Airflow UI with a DAG graph showing 1 successful, 1 upstream failed, 1 skipped and 1 running upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_done_2.png)

If all upstream tasks are either in `skipped` or `upstream_failed` states, the downstream task with the `one_done` trigger rule is set to the state `skipped`.

![Screenshot of the Airflow UI with a DAG graph showing 2 upstream failed and 2 skipped tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_one_done_3.png)

### Trigger rule `none_failed`

The `none_failed` trigger rule makes a task run only when all upstream tasks have either succeeded or been skipped.

![Screenshot of the Airflow UI with a DAG graph showing 2 successful and 2 skipped upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_failed_1.png)

As soon as any upstream task is in the state `failed` or `upstream_failed`, the downstream task is set to the state `upstream_failed` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 3 running upstream tasks and one downstream task in upstream_failed state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_failed_2.png)

### Trigger rule `none_failed_min_one_success`

Tasks using the `none_failed_min_one_success` trigger rule run only when three conditions are met:

1. All upstream tasks are finished.
2. No upstream tasks are in the `failed` or `upstream_failed` state.
3. At least one upstream task is in the `success` state.

![Screenshot of the Airflow UI with a DAG graph showing 2 successful and 2 skipped upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_failed_min_one_success_1.png)

If any upstream task is in the `failed` or `upstream_failed` state, the downstream task is set to the state `upstream_failed` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 failed, 1 successful, 1 skipped and 1 upstream failed upstream task and one downstream task in upstream_failed state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_failed_min_one_success_2.png)

If all upstream tasks are in the `skipped` state, the downstream task is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 4 skipped upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_failed_min_one_success_3.png)

### Trigger rule `none_skipped`

Tasks using the `none_skipped` trigger rule run only when no upstream task is in the `skipped` state. Upstream tasks can be in any other state: `success`, `failed`, or `upstream_failed`.

![Screenshot of the Airflow UI with a DAG graph showing 2 successful, 1 failed and 1 upstream failed upstream tasks and one downstream task in success state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_skipped_1.png)

If any upstream task is in the `skipped` state, the downstream task is set to the state `skipped` and does not run.

![Screenshot of the Airflow UI with a DAG graph showing 1 successful, 1 failed, 1 skipped and 1 upstream failed upstream tasks and one downstream task in skipped state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_none_skipped_2.png)

### Trigger rule `always`

A task with the trigger rule `always` runs as soon as the DAG run is started, regardless of the state of its upstream tasks.

![Screenshot of the Airflow UI with a DAG graph showing 4 running upstream tasks and one downstream task in running state depending on all 4 upstream tasks](/img/guides/airflow-trigger-rules_always_1.png)

