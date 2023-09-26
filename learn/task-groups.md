---
title: "Airflow task groups"
sidebar_label: "Task groups"
id: task-groups
---

<head>
  <meta name="description" content="Follow Astronomer’s step-by-step guide to use task groups for organizing tasks within the grid view of the Airflow user interface." />
  <meta name="og:description" content="Follow Astronomer’s step-by-step guide to to use task groups for organizing tasks within the grid view of the Airflow user interface." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import task_group_example from '!!raw-loader!../code-samples/dags/task-groups/task_group_example.py';
import task_group_mapping_example from '!!raw-loader!../code-samples/dags/task-groups/task_group_mapping_example.py';
import custom_task_group_example from '!!raw-loader!../code-samples/dags/task-groups/custom_task_group_example.py';
import custom_task_group_example_dag from '!!raw-loader!../code-samples/dags/task-groups/custom_task_group_example_dag.py';

Airflow [task groups](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) are a tool to organize tasks into groups within your DAGs. Using task groups allows you to:

- Organize complicated DAGs, visually grouping tasks that belong together in the Airflow UI **Grid View**.
- Apply `default_args` to sets of tasks, instead of at the DAG level using [DAG parameters](dags.md#dag-parameters).
- [Dynamically map](dynamic-tasks.md) over groups of tasks, enabling complex dynamic patterns.
- Turn task patterns into modules that can be reused across DAGs or Airflow instances.

In this guide, you'll learn how to create and use task groups in your DAGs. You can find many example DAGs using task groups on the [Astronomer GitHub](https://github.com/astronomer/webinar-task-groups).

![Task group intro gif](/img/guides/task-groups_intro_task_group_gif.gif)

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).

## When to use task groups

Task groups are most often used to visually organize complicated DAGs. For example, you might use task groups:

- In big ELT/ETL DAGs, where you have a task group per table or schema.
- In MLOps DAGs, where you have a task group per model being trained. 
- In DAGs owned by several teams, where you have task groups to visually separate the tasks that belong to each team. Although in this case, it might be better to separate the DAG into multiple DAGs and use [Datasets](airflow-datasets.md) to connect them.
- When you are using the same patterns of tasks in multiple DAGs and want to create a reusable module.
- When you have an input of unknown length, for example an unknown number of files in a directory. You can use task groups to [dynamically map](#generate-task-groups-dynamically-at-runtime) over the input and create a task group performing sets of actions for each file. This is the only way to dynamically map sequential tasks in Airflow.

## Define task groups

There are two ways to define task groups in your DAGs:

- Use the `TaskGroup` class to create a task group context.
- Use the `@task_group` decorator on a Python function.

In most cases, it is a matter of personal preference which method you use. The only exception is when you want to [dynamically map](dynamic-tasks.md) over a task group; this is possible only when using `@task_group`. 

The following code shows how to instantiate a simple task group containing two sequential tasks. You can use dependency operators (`<<` and `>>`) both within and between task groups in the same way that you can with individual tasks.

<Tabs
    defaultValue="decorator"
    groupId="define-task-groups"
    values={[
        {label: '@task_group', value: 'decorator'},
        {label: 'TaskGroup', value: 'context'},
    ]}>

<TabItem value="decorator">

```python
# from airflow.decorators import task_group

t0 = EmptyOperator(task_id='start')

# Start task group definition
@task_group(group_id='my_task_group')
def tg1():
    t1 = EmptyOperator(task_id='task_1')
    t2 = EmptyOperator(task_id='task_2')

    t1 >> t2
# End task group definition

t3 = EmptyOperator(task_id='end')

# Set task group's (tg1) dependencies
t0 >> tg1() >> t3
```

</TabItem>
<TabItem value="context">

```python
# from airflow.utils.task_group import TaskGroup

t0 = EmptyOperator(task_id='start')

# Start task group definition
with TaskGroup(group_id='my_task_group') as tg1:
    t1 = EmptyOperator(task_id='task_1')
    t2 = EmptyOperator(task_id='task_2')

    t1 >> t2
# End task group definition
    
t3 = EmptyOperator(task_id='end')

# Set task group's (tg1) dependencies
t0 >> tg1 >> t3
```

</TabItem>
</Tabs>

In the **Grid View** of the Airflow UI, task groups have a note showing how many tasks they contain. There are three ways to expand or collapse task groups:

- Click on the note (for example **+2 tasks**).
- Click the buttons on top of the task list.
- Click the arrow next to names of task groups in the task list.

See the following GIF for examples of each of these options:

![Task groups simple example](/img/guides/task-groups_grid_view.gif)

In Airflow 2.7, task groups can be cleared and marked as success/failed just like individual tasks.

![Task groups mark success/failed](/img/guides/task-groups_mark_success_failed.gif)

## Task group parameters

You can use parameters to customize individual task groups. The two most important parameters are the `group_id` which determines the name of your task group, as well as the `default_args` which will be passed to all tasks in the task group. The following examples show task groups with some commonly configured parameters:

<Tabs
    defaultValue="decorator"
    groupId="define-task-groups"
    values={[
        {label: '@task_group', value: 'decorator'},
        {label: 'TaskGroup', value: 'context'},
    ]}>

<TabItem value="decorator">

```python
@task_group(
    group_id="task_group_1",
    default_args={"conn_id": "postgres_default"},
    tooltip="This task group is very important!",
    prefix_group_id=True,
    # parent_group=None,
    # dag=None,
)
def tg1():
    t1 = EmptyOperator(task_id="t1")

tg1()
```

</TabItem>
<TabItem value="context">

```python
with TaskGroup(
    group_id="task_group_2",
    default_args={"conn_id": "postgres_default"},
    tooltip="This task group is also very important!",
    prefix_group_id=True,
    # parent_group=None,
    # dag=None,
    # add_suffix_on_collision=True, # resolves group_id collisions by adding a suffix
) as tg2:
    t1 = EmptyOperator(task_id="t1")
```

</TabItem>
</Tabs>

In older Airflow versions using the old **Graph** view you can change the background and font color of the task group with the `ui_color` and `ui_fgcolor` parameters.

## `task_id` in task groups

When your task is within a task group, your callable `task_id` will be `group_id.task_id`. This ensures the `task_id` is unique across the DAG. It is important that you use this format when referring to specific tasks when working with [XComs](airflow-passing-data-between-tasks.md) or [branching](airflow-branch-operator.md). You can disable this behavior by setting the [task group parameter](#task-group-parameters) `prefix_group_id=False`.

For example, the `task_1` task in the following DAG has a `task_id` of `my_outer_task_group.my_inner_task_group.task_1`.

<Tabs
    defaultValue="decorator"
    groupId="task_id-in-task-groups"
    values={[
        {label: '@task_group', value: 'decorator'},
        {label: 'TaskGroup', value: 'context'},
    ]}>

<TabItem value="decorator">

```python
@task_group(group_id="my_outer_task_group")
def my_outer_task_group():
    @task_group(group_id="my_inner_task_group")
    def my_inner_task_group():
        EmptyOperator(task_id="task_1")

    my_inner_task_group()

my_outer_task_group()
```

</TabItem>
<TabItem value="context">

```python
with TaskGroup(group_id="my_outer_task_group") as tg1:
    with TaskGroup(group_id="my_inner_task_group") as tg2:
        EmptyOperator(task_id="task_1")
```
</TabItem>
</Tabs>

## Passing data through task groups

When you use the `@task_group` decorator, you can pass data through the task group just like with regular `@task` decorators:

<CodeBlock language="python">{task_group_example}</CodeBlock>

The resulting DAG looks is shown in the following image:

![Decorated task group](/img/guides/task-groups_passing_data_dag.png)

There are a few things to consider when passing information into and out of task groups:

- If downstream tasks require the output of tasks that are in the task group decorator, then the task group function must return a result. In the previous example, a dictionary with two values was returned, one from each of the tasks in the task group, that are then passed to the downstream `load()` task.
- If your task group function returns an output that another task takes as an input, Airflow can infer the task group and task dependency with the TaskFlow API. If your task group function's output isn't used as a task input, you must use the bit-shift operators (`<<` or `>>`) to define downstream dependencies to the task group.

## Generate task groups dynamically at runtime

As of Airflow 2.5, you can use [dynamic task mapping](dynamic-tasks.md) with the `@task_group` decorator to dynamically map over task groups. The following DAG shows how you can dynamically map over a task group with different inputs for a given parameter.

<CodeBlock language="python">{task_group_mapping_example}</CodeBlock>

This DAG dynamically maps over the task group `group1` with different inputs for the `my_num` parameter. 6 mapped task group instances are created, one for each input. Within each mapped task group instance two tasks will run using that instances' value for `my_num` as an input. The `pull_xcom()` task downstream of the dynamically mapped task group shows how to access a specific [XCom](airflow-passing-data-between-tasks.md) value from a list of mapped task group instances (`map_indexes`).

For more information on dynamic task mapping, including how to map over multiple parameters, see [Dynamic Tasks](dynamic-tasks.md).

## Order task groups

By default, using a loop to generate your task groups will put them in parallel. If your task groups are dependent on elements of another task group, you'll want to run them sequentially. For example, when loading tables with foreign keys, your primary table records need to exist before you can load your foreign table.

In the following example, the third task group generated in the loop has a foreign key constraint on both previously generated task groups (first and second iteration of the loop), so you'll want to process it last. To do this, you'll create an empty list and append your task group objects as they are generated. Using this list, you can reference the task groups and define their dependencies to each other:

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

![Task group Dependencies](/img/guides/task-groups_looped.png)

This example also shows how to add an additional task to `group1` based on your `group_id`, Even when you're creating task groups in a loop to take advantage of patterns, you can still introduce variations to the pattern while avoiding code redundancies.

## Nest task groups

For additional complexity, you can nest task groups by defining a task group indented within another task group. There is no limit to how many levels of nesting you can have.

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

![Nested task groups](/img/guides/task-groups_nested_tg.png)

## Custom task group classes

If you use the same patterns of tasks in several DAGs or Airflow instances, it may be useful to create a custom task group class module. To do so, you need to inherit from the `TaskGroup` class and then define your tasks within that custom class. You also need to use `self` to assign the task to the task group. Other than that, the task definitions will be the same as if you were defining them in a DAG file. 

<CodeBlock language="python">{custom_task_group_example}</CodeBlock>

In the DAG, you import your custom TaskGroup class and instantiate it with the values for your custom arguments:

<CodeBlock language="python">{custom_task_group_example_dag}</CodeBlock>

The resulting image shows the custom templated task group which can now be reused in other DAGs with different inputs for `num1` and `num2`.

![Custom task group](/img/guides/task-groups_custom_tg.png)