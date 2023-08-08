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
import custom_task_group_example from '!!raw-loader!../code-samples/dags/task-groups/custom_task_group_example.py';

Airflow [task groups](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) are a tool to organize tasks into groups within your DAGs. Using task groups allows you to:

- Organize complicated DAGs, visually grouping tasks that belong together in the Airflow UI **Grid View** and **Graph View**.
- Apply `default_args` to sets of tasks, instead of at the [DAG level](dags.md#dag-parameters).
- [Dynamically map](dynamic-tasks.md) over groups of tasks, enabling complex dynamic patterns.
- Turn task patterns into modules that can be reused across DAGs or Airflow instances.

In this guide, you'll learn how to create and use task groups in your DAGs. You can find many example DAGs using task groups in [this repository](https://github.com/astronomer/webinar-task-groups).

![Task group intro gif](/img/guides/task-groups_intro_task_group_gif.gif)

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).

## When to use task groups

There are many use cases for task groups in Airflow DAGs and often they are used to visually organize complicated DAGs. For example, you might use task groups to organize tasks:

- In big ELT/ETL DAGs, where you could have a task group per table being modified, or per schema and leverage passing of different sets of `default_args` to each task group.
- In MLOps DAGs, where you could have a task group per model being trained. 
- In situations where several teams work on parts of the same DAG and you want to visually separate the tasks that belong to each team. In this case you might also want to consider separating the DAG into multiple DAGs and using [Datasets](airflow-datasets.md) to connect them.
- When you are using the same patterns of tasks in multiple DAGs and want to create a reusable module.

Additionally when you have an input of unknown length, for example an unknown number of files in a directory, you can use task groups to [dynamically map](#generate-task-groups-dynamically-at-runtime) over the input and create a task group performing sets of actions for each file. This is the only way to dynamically map sequential tasks in Airflow.

## Define task groups

There are two ways to define task groups in your DAGs:

- Using the `TaskGroup` class to create a task group context
- Using the `@task_group` decorator on a Python function

In most cases, it is a matter of personal preference which method you use. The only exception is when you want to [dynamically map](dynamic-tasks.md) over a task group; this is only possible using `@task_group`. See [Airflow decorators](airflow-decorators.md) for more information on decorators and the TaskFlow API.

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

In the **Graph View** of the Airflow UI, task groups are shown in cornflower blue by default. You can expand and collapse them by clicking anywhere on the task group. Expanded task groups will have blue circles when a dependency was defined up- or downstream the whole task group.

![Task groups simple example](/img/guides/task-groups_simple_example.gif)

In the **Grid View** of the Airflow UI, task groups have a note showing how many tasks they contain. Click on the note, for example `+ 2 tasks`, to expand the task group and on `- 2 tasks` to collapse it again. In this view you can also collapse and expand all task groups using the buttons on top of the task list or individual task groups by clicking on their downwards error as shown in the gif below.

![Task groups simple example](/img/guides/task-groups_grid_view.gif)

As of Airflow 2.7, task groups can be cleared and marked as successful/failed from the **Grid View** in the same way as individual tasks.

![Task groups mark success/failed](/img/guides/task-groups_mark_success_failed.gif)

## Task group parameters

When creating a task group there are a few parameters you can define, such as changing the UI color or adding a tooltip to your task group. The two most important parameters are the `group_id` which determines the name of your task group, as well as the `default_args` which will be passed to all tasks in the task group.

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
    ui_color="#7352BA",  # Background color in graph view
    ui_fgcolor="#FFFFFF",  # Font color for in graph view
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
    ui_color="#7352BA",  # Background color in graph view
    ui_fgcolor="#FFFFFF",  # Font color for in graph view
    prefix_group_id=True,
    # parent_group=None,
    # dag=None,
    # add_suffix_on_collision=True, # resolves group_id collisions by adding a suffix
) as tg2:
    t1 = EmptyOperator(task_id="t1")
```

</TabItem>
</Tabs>

## `task_id` in task groups

When your task is within a task group, your callable `task_id` will be `group_id.task_id`. This ensures the task_id is unique across the DAG. It is important that you use this format when calling specific tasks when working with [XComs](airflow-passing-data-between-tasks.md) or [branching](airflow-branch-operator.md). You can disable this behavior by setting the [task group parameter](#task-group-parameters) `prefix_group_id=False`.

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

When using the `@task_group` decorator of the TaskFlow API you can pass data through the task group as with regular `@task` decorators:

<CodeBlock language="python">{task_group_example}</CodeBlock>

The resulting DAG looks similar to this image:

![Decorated task group](/img/guides/task-groups_passing_data_dag.png)

There are a few things to consider when passing information into and out of task groups:

- If downstream tasks require the output of tasks that are in the task group decorator, then the task group function must return a result. In the previous example, a dictionary with two values was returned, one from each of the tasks in the task group, that are then passed to the downstream `load()` task.
- If your task group function returns an output that another task takes as an input, Airflow can infer the task group and task dependency with the TaskFlow API. If your task group function does not return any output that is used as a task input, you must use the bit-shift operators (`<<` or `>>`) to define downstream dependencies to the task group.

## Generate task groups dynamically at runtime

As of Airflow 2.5, you can use [dynamic task mapping](dynamic-tasks.md) with the `@task_group` decorator to dynamically map over task groups. The following DAG shows how you can dynamically map over a task group with different inputs for a given parameter.

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

![Task group Dependencies](/img/guides/task-groups_looped.png)

This example also shows how to add an additional task to `group1` based on your `group_id`, demonstrating that even though you're creating task groups in a loop to take advantage of patterns, you can still introduce variations to the pattern while avoiding code redundancies introduced by building each task group definition manually.

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

If you use the same patterns of tasks in several DAGs or Airflow instances, it may be useful to create a custom task group class module. To do so, you need to inherit from the `TaskGroup` class and then define your tasks within that custom class. The task definitions will be the same as if you were defining them in a DAG file, with the only added requirement that you'll need to use `self` to assign the task to the task group.

```python
from airflow.utils.task_group import TaskGroup
from airflow.decorators import task


class MyCustomMathTaskGroup(TaskGroup):
    """A task group summing two numbers."""

    # defining defaults of input arguments num1 and num2
    def __init__(self, group_id, num1=0, num2=0, **kwargs):
        """Instantiate a MyCustomMathTaskGroup."""
        super().__init__(group_id=group_id, ui_color="#32CD32", **kwargs)

        # assing the task to the task group by using `self`
        @task(task_group=self)
        def task_1(num1, num2):
            """Adds two numbers."""
            return num1 + num2

        @task(task_group=self)
        def task_2(num):
            """Multiplies a number by 23."""
            return num * 23

        # define dependencies
        task_2(task_1(num1, num2))
```

In the DAG you import your custom TaskGroup class and instantiate it with the values for your custom arguments:

<CodeBlock language="python">{custom_task_group_example}</CodeBlock>

The resulting DAG shows the custom templated task group which can now be reused in other DAGs with different inputs for `num1` and `num2`.

![Custom task group](/img/guides/task-groups_custom_tg.png)