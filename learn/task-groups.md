---
title: "Airflow task groups"
sidebar_label: "Task groups"
id: task-groups
---

<head>
  <meta name="description" content="Follow Astronomer’s step-by-step guide to use task groups for organizing tasks within the graph view of the Airflow user interface." />
  <meta name="og:description" content="Follow Astronomer’s step-by-step guide to to use task groups for organizing tasks within the graph view of the Airflow user interface." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import task_group_example from '!!raw-loader!../code-samples/dags/task-groups/task_group_example.py';
import task_group_mapping_example from '!!raw-loader!../code-samples/dags/task-groups/task_group_mapping_example.py';

Airflow [task groups](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) are a tool to organize tasks into groups within your DAGs. Using task groups allows you to:

- Organize complicated DAGs, visually grouping tasks that belong together in the Airflow UI **Grid View** and **Graph View**.
- Apply `default_args` to sets of tasks, instead of at the [DAG level](dags.md#dag-parameters).
- [Dynamically map](dynamic-tasks.md) over task patterns creating dynamically mapped complex sets of tasks.
- Turn task patterns into modules that can be reused across DAGs and even Airflow instances.

In this guide, you'll learn how to create and use task groups in your DAGs.

![Task group intro gif](/img/guides/task-groups_intro_task_group_gif.gif)

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).

## When to use task groups

There are many use cases for task groups in Airflow DAGs and often they are used to visually organize complicated DAGs. For example, you might use task groups to organize tasks:

- In big ELT/ETL DAGs, where you could have a task group per table being modified, or per schema and leverage passing of different sets of `default_args` to each task group.
- In MLOps DAGs, where you could have a task group per model being trained. 
- In Situations where several teams work on parts of the same DAG and you want to visually separate the tasks that belong to each team. In this case you might also want to consider separating the DAG into multiple DAGs and using [Datasets](airflow-datasets.md) to connect them.
- When you are using the same patterns of tasks in multiple DAGs and want to create a reusable module.

Additionally when you have an input of unknown length, for example an unknown number of files in a directory, you can use task groups to [dynamically map](dynamic-tasks#mapping-over-task-groups) over the input and create a task group performing sets of actions for each file. This is the only way to dynamically map sequential tasks in Airflow.

## Create task groups

To use task groups, run the following import statement:

```python 
from airflow.utils.task_group import TaskGroup
```

For your first example, you'll instantiate a task group using a `with` statement and provide a `group_id`. Inside your task group, you'll define your two tasks, `t1` and `t2`, and their respective dependencies. 

You can use dependency operators (`<<` and `>>`) in task groups in the same way that you can with individual tasks. Dependencies applied to a task group are applied across its tasks. In the following code, you'll add additional dependencies to `t0` and `t3` to the task group, which automatically applies the same dependencies across `t1` and `t2`:  

```python
t0 = EmptyOperator(task_id='start')

# Start task group definition
with TaskGroup(group_id='group1') as tg1:
    t1 = EmptyOperator(task_id='task1')
    t2 = EmptyOperator(task_id='task2')

    t1 >> t2
# End task group definition
    
t3 = EmptyOperator(task_id='end')

# Set task group's (tg1) dependencies
t0 >> tg1 >> t3

```

In the Airflow UI, blue highlighting is used to identify tasks and task groups. When you click and expand `group1`, blue circles identify the task group dependencies. The task immediately to the right of the first blue circle (`t1`) gets the group's upstream dependencies and the task immediately to the left (`t2`) of the last blue circle gets the group's downstream dependencies. The task group dependencies are shown in the following animation: 

![UI task group](https://assets2.astronomer.io/main/guides/task-groups/task_groups_ui.gif)

When your task is within a task group, your callable `task_id` is the `task_id` prefixed with the `group_id`. For example, `group_id.task_id`. This ensures the task_id is unique across the DAG. It is important that you use this format when calling specific tasks with XCOM passing or branching operator decisions.

## Use the task group decorator

Another way of defining task groups in your DAGs is by using the task group decorator. The task group decorator is available in Airflow 2.1 and later. The task group decorator functions like other [Airflow decorators](airflow-decorators.md) and allows you to define your task group with the TaskFlow API. Using task group decorators doesn't change the functionality of task groups, but they can make your code formatting more consistent if you're already using them in your DAGs.

To use the decorator, add `@task_group` before a Python function which calls the functions of tasks that should go in the task group. For example:

```python
@task_group(group_id="tasks")
def my_independent_tasks():
    task_a()
    task_b()
    task_c()
```

This function creates a task group with three independent tasks that are defined elsewhere in the DAG.

You can also create a task group of dependent tasks. For example:

```python
@task_group(group_id="tasks")
def my_dependent_tasks():
    return task_a(task_b(task_c()))
```

The following DAG shows a full example implementation of the task group decorator, including passing data between tasks before and after the task group:

<CodeBlock language="python">{task_group_example}</CodeBlock>

The resulting DAG looks similar to this image:

![Decorated task group](/img/guides/decorated_task_group.png)

There are a few things to consider when using the task group decorator:

- If downstream tasks require the output of tasks that are in the task group decorator, then the task group function must return a result. In the previous example, a dictionary with two values was returned, one from each of the tasks in the task group, that are then passed to the downstream `load()` task.
- If your task group function returns an output, you can call the function from your DAG with the TaskFlow API. If your task group function does not return any output, you must use the bitshift operators (`<<` or `>>`) to define dependencies to the task group.

## Generate task groups dynamically at runtime

As of Airflow 2.5, you can use [dynamic task mapping](dynamic-tasks.md) with the `@task_group` decorator to dynamically map over task groups. The following DAG shows how you can dynamically maps over a task group with different inputs for a given parameter.

<CodeBlock language="python">{task_group_mapping_example}</CodeBlock>

This DAG dynamically maps over the task group `group1` with different inputs for the `my_num` parameter. 6 mapped task group instances are created, one for each input. Within each mapped task group instance two tasks will run using that instances' value for `my_num` as an input. The `pull_xcom()` task downstream of the dynamically mapped task group shows how to access a specific [XCom](airflow-passing-data-between-tasks.md) value from a list of mapped task group instances (`map_indexes`).

For more information on dynamic task mapping, including how to map over multiple parameters, see [Dynamic Tasks](dynamic-tasks.md).

## Order task groups

By default, using a loop to generate your task groups will put them in parallel. If your task groups are dependent on elements of another task group, you'll want to run them sequentially. For example, when loading tables with foreign keys, your primary table records need to exist before you can load your foreign table.

In the following example, the third task group generated in the loop has a foreign key constraint on both previously generated task groups (first and second iteration of the loop), so you'll want to process it last. To do this, you'll create an empty list and append your task Group objects as they are generated. Using this list, you can reference the task groups and define their dependencies to each other:

<Tabs
    defaultValue="taskflow"
    groupId="order-task-groups"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
groups = []
for g_id in range(1,4):
    tg_id = f"group{g_id}"

    @task_group(group_id=tg_id)
    def tg1():
        t1 = EmptyOperator(task_id="task1")
        t2 = EmptyOperator(task_id="task2")

        t1 >> t2

        if tg_id == "group1":
            t3 = EmptyOperator(task_id="task3")
            t1 >> t3
                
    groups.append(tg1())

[groups[0] , groups[1]] >> groups[2]
```

</TabItem>

<TabItem value="traditional">

```python
groups = []
for g_id in range(1,4):
    tg_id = f"group{g_id}"
    with TaskGroup(group_id=tg_id) as tg1:
        t1 = EmptyOperator(task_id="task1")
        t2 = EmptyOperator(task_id="task2")

        t1 >> t2

        if tg_id == "group1":
            t3 = EmptyOperator(task_id="task3")
            t1 >> t3
                
        groups.append(tg1)

[groups[0] , groups[1]] >> groups[2]
```

</TabItem>
</Tabs>

The following image shows how these task groups appear in the Airflow UI:

![task group Dependencies](/img/guides/task_group_dependencies.png)

### Task group conditioning

In the previous example, you added an additional task to `group1` based on your `group_id`. This demonstrated that even though you're creating task groups in a loop to take advantage of patterns, you can still introduce variations to the pattern while avoiding code redundancies introduced by building each task group definition manually.

## Nest task groups

For additional complexity, you can nest task groups. Building on our previous ETL example, when calling API endpoints you may need to process new records for each endpoint before you can process updates to them.

In the following code, your top-level task groups represent your new and updated record processing, while the nested task groups represent your API endpoint processing:

<Tabs
    defaultValue="taskflow"
    groupId="nest-task-groups"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
groups = []
for g_id in range(1,3):
    @task_group(group_id=f"group{g_id}")
    def tg1():
        t1 = EmptyOperator(task_id="task1")
        t2 = EmptyOperator(task_id="task2")

        sub_groups = []
        for s_id in range(1,3):
            @task_group(group_id=f"sub_group{s_id}")
            def tg2():
                st1 = EmptyOperator(task_id="task1")
                st2 = EmptyOperator(task_id="task2")

                st1 >> st2
            sub_groups.append(tg2())

        t1 >> sub_groups >> t2
    groups.append(tg1())

groups[0] >> groups[1]
```

</TabItem>

<TabItem value="traditional">

```python
groups = []
for g_id in range(1,3):
    with TaskGroup(group_id=f"group{g_id}") as tg1:
        t1 = EmptyOperator(task_id="task1")
        t2 = EmptyOperator(task_id="task2")

        sub_groups = []
        for s_id in range(1,3):
            with TaskGroup(group_id=f"sub_group{s_id}") as tg2:
                st1 = EmptyOperator(task_id="task1")
                st2 = EmptyOperator(task_id="task2")

                st1 >> st2
                sub_groups.append(tg2)

        t1 >> sub_groups >> t2
        groups.append(tg1)

groups[0] >> groups[1]
```

</TabItem>
</Tabs>

The following image shows the expanded view of the nested task groups in the Airflow UI:

![Nested task groups](/img/guides/nested_task_groups.png)

