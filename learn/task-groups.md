---
title: "Airflow task groups"
sidebar_label: "Task groups"
description: "Use task groups to build modular Airflow workflows."
id: task-groups
---

Use [task groups](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html#taskgroups) to organize tasks in the Airflow UI DAG graph view.

In this guide, you'll learn how to create task groups and review some example DAGs that demonstrate their scalability.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Create task groups

To use task groups, run the following import statement:

```python 
from airflow.utils.task_group import TaskGroup
```

For your first example, you'll instantiate a Task Group using a `with` statement and provide a `group_id`. Inside your Task Group, you'll define your two tasks, `t1` and `t2`, and their respective dependencies. 

You can use dependency operators (`<<` and `>>`) in task groups in the same way that you can with individual tasks. Dependencies applied to a Task Group are applied across its tasks. In the following code, you'll add additional dependencies to `t0` and `t3` to the Task Group, which automatically applies the same dependencies across `t1` and `t2`:  

```python
t0 = DummyOperator(task_id='start')

# Start Task Group definition
with TaskGroup(group_id='group1') as tg1:
    t1 = DummyOperator(task_id='task1')
    t2 = DummyOperator(task_id='task2')

    t1 >> t2
# End Task Group definition
    
t3 = DummyOperator(task_id='end')

# Set Task Group's (tg1) dependencies
t0 >> tg1 >> t3

```

In the Airflow UI, blue highlighting is used to identify tasks and task groups. When you click and expand `group1`, blue circles identify the Task Group dependencies. The task immediately to the right of the first blue circle (`t1`) gets the group's upstream dependencies and the task immediately to the left (`t2`) of the last blue circle gets the group's downstream dependencies. The Task Group dependencies are shown in the following animation: 

![UI Task Group](https://assets2.astronomer.io/main/guides/task-groups/task_groups_ui.gif)

When your task is within a Task Group, your callable `task_id` is the `task_id` prefixed with the `group_id`. For example, `group_id.task_id`. This ensures the task_id is unique across the DAG. It is important that you use this format when calling specific tasks with XCOM passing or branching operator decisions.

## Use the Task Group decorator

Another way of defining task groups in your DAGs is by using the Task Group decorator. The Task Group decorator is available in Airflow 2.1 and later. The Task Group decorator functions like other [Airflow decorators](airflow-decorators.md) and allows you to define your Task Group with the TaskFlow API. Using Task Group decorators doesn't change the functionality of task groups, but they can make your code formatting more consistent if you're already using them in your DAGs.

To use the decorator, add `@task_group` before a Python function which calls the functions of tasks that should go in the Task Group. For example:

```python
@task_group(group_id="tasks")
def my_independent_tasks():
    task_a()
    task_b()
    task_c()
```

This function creates a Task Group with three independent tasks that are defined elsewhere in the DAG.

You can also create a Task Group of dependent tasks. For example:

```python
@task_group(group_id="tasks")
def my_dependent_tasks():
    return task_a(task_b(task_c()))
```

The following DAG shows a full example implementation of the Task Group decorator, including passing data between tasks before and after the Task Group:

```python
import json
from airflow.decorators import dag, task, task_group

import pendulum

@dag(schedule_interval=None, start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False)

def task_group_example():

    @task(task_id='extract', retries=2)
    def extract_data():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task()
    def transform_sum(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def transform_avg(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
            avg_order_value = total_order_value / len(order_data_dict)

        return {"avg_order_value": avg_order_value}

    @task_group
    def transform_values(order_data_dict):
        return {'avg': transform_avg(order_data_dict), 'total': transform_sum(order_data_dict)}

    @task()
    def load(order_values: dict):
        print(f"Total order value is: {order_values['total']['total_order_value']:.2f} and average order value is: {order_values['avg']['avg_order_value']:.2f}")

    load(transform_values(extract_data()))

    
task_group_example = task_group_example()
```

The resulting DAG looks similar to this image:

![Decorated Task Group](/img/guides/decorated_task_group.png)

There are a few things to consider when using the Task Group decorator:

- If downstream tasks require the output of tasks that are in the Task Group decorator, then the Task Group function must return a result. In the previous example, a dictionary with two values was returned, one from each of the tasks in the Task Group, that are then passed to the downstream `load()` task.
- If your Task Group function returns an output, you can call the function from your DAG with the TaskFlow API. If your Task Group function does not return any output, you must use the bitshift operators (`<<` or `>>`) to define dependencies to the Task Group.

## Dynamically generate task groups

Task groups can be dynamically generated to make use of patterns within your code. In an ETL DAG, you might have similar downstream tasks that can be processed independently, such as when you call different API endpoints for data that needs to be processed and stored in the same way. For this use case, you can dynamically generate task groups by API endpoint. You can expand generated task groups in the Airflow UI to see specific tasks. 

In the following code, iteration is used to create multiple task groups. While the tasks and dependencies remain the same across task groups, you can change which parameters are passed in to each Task Group based on the `group_id`:

```python
for g_id in range(1,3):
    with TaskGroup(group_id=f'group{g_id}') as tg1:
        t1 = DummyOperator(task_id='task1')
        t2 = DummyOperator(task_id='task2')

        t1 >> t2
```

The following image shows the expanded view of the task groups in the Airflow UI:

![Dynamic Task Group](/img/guides/dynamic_task_groups.png)

## Order task groups

By default, using a loop to generate your task groups will put them in parallel. If your task groups are dependent on elements of another Task Group, you'll want to run them sequentially. For example, when loading tables with foreign keys, your primary table records need to exist before you can load your foreign table.

In the following example, your third dynamically generated Task Group has a foreign key constraint on both your first and second dynamically generated task groups, so you'll want to process it last. To do this, you'll create an empty list and append your Task Group objects as they are generated. Using this list, you can reference the task groups and define their dependencies to each other:

```python
groups = []
for g_id in range(1,4):
    tg_id = f'group{g_id}'
    with TaskGroup(group_id=tg_id) as tg1:
        t1 = DummyOperator(task_id='task1')
        t2 = DummyOperator(task_id='task2')

        t1 >> t2

        if tg_id == 'group1':
            t3 = DummyOperator(task_id='task3')
            t1 >> t3
                
        groups.append(tg1)

[groups[0] , groups[1]] >> groups[2]
```

The following image shows how these task groups appear in the Airflow UI:

![Task Group Dependencies](/img/guides/task_group_dependencies.png)

### Task group conditioning

In the previous example, you added an additional task to `group1` based on your `group_id`. This demonstrated that even though you're dynamically creating task groups to take advantage of patterns, you can still introduce variations to the pattern while avoiding code redundancies introduced by building each Task Group definition manually.

## Nest task groups

For additional complexity, you can nest task groups. Building on our previous ETL example, when calling API endpoints you may need to process new records for each endpoint before you can process updates to them.

In the following code, your top-level task groups represent your new and updated record processing, while the nested task groups represent your API endpoint processing:

```python
groups = []
for g_id in range(1,3):
    with TaskGroup(group_id=f'group{g_id}') as tg1:
        t1 = DummyOperator(task_id='task1')
        t2 = DummyOperator(task_id='task2')

        sub_groups = []
        for s_id in range(1,3):
            with TaskGroup(group_id=f'sub_group{s_id}') as tg2:
                st1 = DummyOperator(task_id='task1')
                st2 = DummyOperator(task_id='task2')

                st1 >> st2
                sub_groups.append(tg2)

        t1 >> sub_groups >> t2
        groups.append(tg1)

groups[0] >> groups[1]
```

The following image shows the expanded view of the nested task groups in the Airflow UI:

![Nested task groups](/img/guides/nested_task_groups.png)

