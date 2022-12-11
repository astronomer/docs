---
title: "Airflow task groups"
sidebar_label: "Task groups"
id: task-groups
---

<head>
  <meta name="description" content="Follow Astronomer’s step-by-step guide to use task groups for organizing tasks within the graph view of the Airflow user interface." />
  <meta name="og:description" content="Follow Astronomer’s step-by-step guide to to use task groups for organizing tasks within the graph view of the Airflow user interface." />
</head>

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

The following DAG shows a full example implementation of the task groupp decorator, including passing data between tasks before and after the task group:

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

![Decorated task group](/img/guides/decorated_task_group.png)

There are a few things to consider when using the task group decorator:

- If downstream tasks require the output of tasks that are in the task group decorator, then the task group function must return a result. In the previous example, a dictionary with two values was returned, one from each of the tasks in the task group, that are then passed to the downstream `load()` task.
- If your task group function returns an output, you can call the function from your DAG with the TaskFlow API. If your task group function does not return any output, you must use the bitshift operators (`<<` or `>>`) to define dependencies to the task group.

## Generate task groups dynamically at runtime

In Airflow 2.5 the possibility to use [dynamic task mapping](dynamic-tasks.md) syntax with the `@task_group` decorator was added. An implementation is shown in the DAG below.

```python
from airflow import DAG
from airflow.decorators import task_group, task
from pendulum import datetime

with DAG(
    dag_id="task_group_mapping_example",
    start_date=datetime(2022, 12, 1),
    schedule=None,
    catchup=False,
):

    # creating a task group using the decorator with the dynamic input my_num
    @task_group(
        group_id="group1"
    )
    def tg1(my_num):

        @task
        def print_num(num):
            return num
        
        @task
        def add_42(num):
            return num + 42
        
        print_num(my_num) >> add_42(my_num)

    # a downstream task to print out resulting XComs
    @task
    def pull_xcom(**context):

        pulled_xcom = context["ti"].xcom_pull(
            # reference a task in a task group with task_group_id.task_id
            task_ids=['group1.add_42'], 
            # only pull xcom from specific mapped task group instances (2.5 feature)
            map_indexes=[2, 3], 
            key="return_value"
        )

        # will print out a list of results from map index 2 and 3 of the add_42 task 
        print(pulled_xcom)

    # creating 6 mapped task group instances of the task group group1 (2.5 feature)
    tg1_object = tg1.expand(my_num=[19, 23, 42, 8, 7, 108])

    # setting dependencies
    tg1_object >> pull_xcom()
```

This DAG dynamically maps over the task group `group1` with different inputs for the `my_num` parameter. 6 mapped task group instances are created, one for each input. Within each mapped task group instance two tasks will run using that instances' value for `my_num` as an input. The `pull_xcom()` task downstream of the dynamically mapped task group shows how to access a specific [XCom](airflow-passing-data-between-tasks.md) value from a list of mapped task group instances (`map_indexes`). 

It is also possible to dynamically map a task group over several input parameters. Analogous to dynamically mapped tasks there are 3 methods to map over multiple parameters. 

- **Cross-product**: Mapping over two or more keyword arguments results in a mapped task group instance for each possible combination of inputs. This type of mapping uses the `expand()` function. 
- **Zip**: Mapping over a set of positional arguments created with Python's built-in `zip()` function or with the `.zip()` method of an XComArg results in one mapped task for every set of positional arguments. Each set of positional arguments is passed to the same keyword argument of the operator. This type of mapping uses the `expand()` function.
- **Sets of keyword arguments**: Mapping over two or more sets of one or more keyword arguments results in a mapped task group instance for every defined set. These keyword arguments must be valid parameters of the TaskGroup class ([source code](https://github.com/apache/airflow/blob/main/airflow/utils/task_group.py)). This type of mapping uses the `expand_kwargs()` function and is less relevant for task group mapping than for dynamic task mapping. You cannot use `expand_kwargs()` to map over arguments passed to the task group function.

Learn more in the [section on mapping over multiple parameters](dynamic-tasks.md#mapping-over-multiple-parameters) of the Create dynamic Airflow tasks guide.

The code examples below shows how to dynamically map over a task group with multiple input parameters. The task group `group2` will be mapped 6 times, once for each possible combination to the inputs to `num_1` and `num_2`, a cross-product.

```python
@task_group(
    group_id="group2",
)
def tg2(num_1, num_2):

    @task
    def multiply(num_1, num_2):
        return num_1 * num_2
    
    multiply(num_1, num_2)

# creating 2x3=6 mapped task instances of the task group group2 (2.5 feature)
tg2_object = tg2.expand(num_1=[1, 2], num_2=[3, 4, 5])
```

Like tasks, task groups can also be mapped over zipped inputs. The code below shows the task group `group3` being mapped over zipped XComArgs. The `numbers` parameter of the task group receives a ZipXComArg object containing a list of three 2-tuples: `[(1, 3), (2, 4), (3, 5)]`. One mapped task group instance is created for each tuple.

```python
@task
def num_list_1():
    return [1, 2, 3]

@task
def num_list_2():
    return [3, 4, 5]

@task_group(
    group_id="group3",
)
def tg3(numbers):

    @task
    def multiply(numbers):
        return numbers[0] * numbers[1]
    
    multiply(numbers)

# creating 3 mapped task instances of the task group group3 (2.5 feature)
tg3_object = tg3.expand(
    numbers=num_list_1().zip(num_list_2())
)
```

## Generate task groups within a loop

Task groups can be generated in loops to make use of patterns within your code. This is useful when the number of task groups you want to generate is static, for example if you need one task group running the same tasks on data retrieved from different APIs in an ETL DAG and the list of APIs is static.
In the Airflow UI task groups generated within a loop are indistinguisheable from task groups that were defined outside of a loop. 

In the following code, iteration is used to create multiple task groups. While the tasks and dependencies remain the same across task groups, you can change which parameters are passed in to each task group based on the `group_id`:

```python
for g_id in range(1,3):
    with TaskGroup(group_id=f'group{g_id}') as tg1:
        t1 = EmptyOperator(task_id='task1')
        t2 = EmptyOperator(task_id='task2')

        t1 >> t2
```

The following image shows the expanded view of the task groups in the Airflow UI:

![Looped task group](/img/guides/looped_task_groups.png)

## Order task groups

By default, using a loop to generate your task groups will put them in parallel. If your task groups are dependent on elements of another task group, you'll want to run them sequentially. For example, when loading tables with foreign keys, your primary table records need to exist before you can load your foreign table.

In the following example, the third task group generated in the loop has a foreign key constraint on both previously generated task groups (first and second iteration of the loop), so you'll want to process it last. To do this, you'll create an empty list and append your task Group objects as they are generated. Using this list, you can reference the task groups and define their dependencies to each other:

```python
groups = []
for g_id in range(1,4):
    tg_id = f'group{g_id}'
    with TaskGroup(group_id=tg_id) as tg1:
        t1 = EmptyOperator(task_id='task1')
        t2 = EmptyOperator(task_id='task2')

        t1 >> t2

        if tg_id == 'group1':
            t3 = EmptyOperator(task_id='task3')
            t1 >> t3
                
        groups.append(tg1)

[groups[0] , groups[1]] >> groups[2]
```

The following image shows how these task groups appear in the Airflow UI:

![task group Dependencies](/img/guides/task_group_dependencies.png)

### Task group conditioning

In the previous example, you added an additional task to `group1` based on your `group_id`. This demonstrated that even though you're creating task groups in a loop to take advantage of patterns, you can still introduce variations to the pattern while avoiding code redundancies introduced by building each task group definition manually.

## Nest task groups

For additional complexity, you can nest task groups. Building on our previous ETL example, when calling API endpoints you may need to process new records for each endpoint before you can process updates to them.

In the following code, your top-level task groups represent your new and updated record processing, while the nested task groups represent your API endpoint processing:

```python
groups = []
for g_id in range(1,3):
    with TaskGroup(group_id=f'group{g_id}') as tg1:
        t1 = EmptyOperator(task_id='task1')
        t2 = EmptyOperator(task_id='task2')

        sub_groups = []
        for s_id in range(1,3):
            with TaskGroup(group_id=f'sub_group{s_id}') as tg2:
                st1 = EmptyOperator(task_id='task1')
                st2 = EmptyOperator(task_id='task2')

                st1 >> st2
                sub_groups.append(tg2)

        t1 >> sub_groups >> t2
        groups.append(tg1)

groups[0] >> groups[1]
```

The following image shows the expanded view of the nested task groups in the Airflow UI:

![Nested task groups](/img/guides/nested_task_groups.png)

