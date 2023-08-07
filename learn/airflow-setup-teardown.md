---
title: "Use Setup/Teardown in Airflow"
sidebar_label: "Setup/Teardown"
description: "Use Setup/Teardown in Airflow."
id: airflow-setup-teardown
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import setup_teardown_example_methods from '!!raw-loader!../code-samples/dags/airflow-setup-teardown/setup_teardown_example_methods.py';
import setup_teardown_example_decorators from '!!raw-loader!../code-samples/dags/airflow-setup-teardown/setup_teardown_example_decorators.py';

When using Airflow in production environments, you often need to set up resources and configurations before certain tasks can run and want to tear these resources down after the tasks completed to save compute costs, even if the tasks failed.

In Airflow 2.7, setup and teardown functionality was added to offer intuitive tools to create and delete resources as part of a DAG. In this guide you will learn all about setup and teardown tasks in Airflow. For an introduction to dependencies and trigger rules, see [Manage task and task group dependencies in Airflow](managing-dependencies.md).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators).
- Managing dependencies in Airflow. See [Manage task and task group dependencies in Airflow](managing-dependencies.md).

## Why to use setup/teardown tasks

Setup and teardown tasks allow you to designate any existing Airflow task as a task that is setting up or tearing down resources with special behavior attached and added visibility of the setup/teardown relationship in the Airflow UI.

There are many use cases for setup and teardown tasks. For example, you might want to:

- Setup up a Spark cluster to run heavy workloads and tear it down afterwards, even if the transformation failed.
- Setup compute resources to train an ML model and tear them down afterwards, even if the training failed.
- Setup the resources to run [data quality](data-quality.md) checks and tear them down afterwards, even if the checks failed.
- Setup storage in your [custom XCom backend](custom-xcom-backends-tutorial.md) to hold data processed through Airflow tasks and tear the extra storage down afterwards, when the XCom data is no longer needed. 

## Setup/teardown behaviors

In Airflow any task can be designated as a setup or a teardown task, irrespective of the operator used or the action performed by the task. You can freely decide which tasks are setup tasks and which are teardown tasks. 

You can turn any existing tasks into setup and teardown tasks and define relationships between them to create setup/teardown groupings, i.e. define which setup and teardown tasks should be connected.

Tasks that run after a (set of) setup task(s) and before the associated teardown task(s) are considered to be in _scope_ of this specific setup / teardown grouping. Usually these tasks will use the resources set up by the setup task which the teardown task will dismantle.

If you are using the `@task` decorator you can use either the [.as_setup() and .as_teardown() methods](#setup-and-teardown-methods) or the [`@setup()` and `@teardown()` decorators](#setup-and-teardown-decorators). For traditional operators use the [`.as_setup()` and `.as_teardown()` methods](#setup-and-teardown-methods).

When using setup/teardown tasks, you can expect the following behaviors:

- Each teardown tasks has its trigger rule configured to run if all of its upstream tasks have completed running, independently of whether they were successful or not and at least one of its associated `setup` tasks have completed successfully (e.g. there is at least one resource that needs to be torn down). If all associated setup tasks fail or are skipped, the teardown task will be failed or skipped respectively.

- A teardown task without any associated setup tasks will always run once all upstream worker tasks have completed running, independently of whether they were successful or not.

- When evaluating whether a DAG run was successful or not Airflow will ignore teardown tasks by default. This means if a teardown tasks that is a leaf task or final task in a DAG has failed, the DAG is still marked as having succeeded. In the example shown in the screenshot below, the success of the DAG run solely depends on whether `worker_task_3` completes successfully. You can change this behavior by setting `on_failure_fail_dagrun=True` in the teardown task.

    ![Successful DAG with failed teardown](/img/guides/airflow-setup-teardown_teardown_fail_dag_succeed.png)

- When a teardown task is located within a [task group](task-groups.md) and a dependency is set on this task group, the teardown task will be ignored, meaning the task `run_after_taskgroup` which is set to depend on the whole `work_in_the_cluster` task group will run even if the teardown task has failed or is still running.

    ```python
    work_in_the_cluster() >> run_after_taskgroup()
    ```

    ![Task group with teardown](/img/guides/airflow-setup-teardown-task_after_taskgroup.png)

- You can have a setup task without an associated teardown task and vice versa. If you define a setup task without a teardown task everything downstream of the setup task is considered in its scope and will cause the setup task to rerun when cleared. 

### Regular DAG vs using setup/teardown

Setup and teardown tasks can help you write more robust DAGs by making sure resources are set up in the right moment and torn down even when worker tasks fail. 

The DAG below is not using Airflow setup and teardown functionality. It sets up its resources using the regular `provision_cluster` task, runs three worker tasks using those resources and finally tears down the resources using the `tear_down_cluster` task.

![DAG without Setup/teardown - all successful](/img/guides/airflow-setup-teardown_nosutd_dag.png)

The way this DAG is set up, a failure in any of the worker tasks will lead to the `tear_down_cluster` task not running. This means that the resources will not be torn down and will continue to incur costs. Additionally, any downstream tasks depending on `tear_down_cluster` will also fail to run unless their [trigger rules](managing-dependencies.md#trigger-rules) have been configured explicitly to run independent of upstream failures.

![DAG without setup/teardown - upstream failure](/img/guides/airflow-setup-teardown_nosutd_dag_fail.png)

You can turn the `provision_cluster` task into a setup task and the `tear_down_cluster` into a teardown task by using the code examples shown in [Basic setup/teardown syntax](#basic-setupteardown-syntax). 

In the graph shown in the **Grid** view the setup task will now be marked with an upwards arrow, while the teardown task is marked with a downwards arrow. Once the [setup/teardown relationship](#defining-setupteardown-relationships) between `provision_cluster` and `tear_down_cluster` has been configured they turn into a setup/teardown grouping and are connected by a dotted line. The tasks `worker_task_1`, `worker_task_2` and `worker_task_3` are in the scope of this setup/teardown grouping.

![DAG with setup/teardown - all successful](/img/guides/airflow-setup-teardown-syntax_dag_successful.png)

Now, even if one of the worker tasks fails, like `worker_task_2` in the following screenshot, the `tear_down_cluster` task will still run, the resources will be torn down and downstream tasks will run successfully.

![DAG with setup/teardown - upstream failure](/img/guides/airflow-setup-teardown_syntax_dag_fail.png)

Additionally, when clearing any of the worker tasks, both its setup and teardown tasks will be cleared and rerun. This is useful when you are recovering from a pipeline issue and need to rerun one or more tasks that use a resource but not all of the tasks in the scope of a specific setup/teardown grouping. 

For example, in the DAG above `worker_task_2` failed and `worker_task_3` was unable to run due to its upstream task having failed while `worker_task_1` was successful. When clearing the failed task `worker_task_2` by clicking on the **Clear task** button, both the setup task `provision_cluster` and the teardown task `tear_down_cluster` will be cleared and rerun in addition to `worker_task_2` and `worker_task_3`. This allows for complete recovery without needing to rerun `worker_task_1` or creating the need to manually rerun individual tasks.

![DAG with setup/teardown - recovery](/img/guides/airflow-setup-teardown-clear_task.png)

## Setup/teardown implementation

There are two ways to turn tasks into setup/teardown tasks: 

- using the `.as_setup()` and `.as_teardown()` methods on TaskFlow API tasks or traditional operators.
- using the `@setup` and `@teardown` decorators instead of `@task` on a Python function.

### `.as_setup()` and `.as_teardown()` methods

Any individual tasks can be turned into setup or teardown task on its own.

To turn a task into a setup task call the `.as_setup()` method on the called task object.  

<Tabs
    defaultValue="taskflow"
    groupId="as_setup-and-teardown-methods"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task 
def my_setup_task():
    return "Setting up resources!"

my_setup_task().as_setup()

# it is also possible to call `.as_setup()` on the task object
# my_setup_task_obj = my_setup_task()
# my_setup_task_obj.as_setup()
```

![Setup task decorator](/img/guides/airflow-setup-teardown_setup_task_decorator.png)

</TabItem>
<TabItem value="traditional">

```python
def my_setup_task_func():
    return "Setting up resources!"


my_setup_task_obj = PythonOperator(
    task_id="my_setup_task",
    python_callable=my_setup_task_func,
)

my_setup_task_obj.as_setup()
```

![Setup task traditional operator](/img/guides/airflow-setup-teardown_setup_task_traditional.png)

</TabItem>
</Tabs>

To turn a task into a teardown task call the `.as_teardown()` method on the called task object. Note that you cannot have a teardown task without at least one upstream worker task.

<Tabs
    defaultValue="taskflow"
    groupId="as_setup-and-teardown-methods"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task
def worker_task():
    return "Doing some work!"

@task
def my_teardown_task():
    return "Tearing down resources!"

worker_task() >> my_teardown_task().as_teardown()

# it is also possible to call `.as_teardown()` on the task object
# my_teardown_task_obj = my_teardown_task()
# worker_task() >> my_teardown_task_obj.as_teardown()
```

![Teardown task decorator](/img/guides/airflow-setup-teardown_teardown_decorators.png)

</TabItem>
<TabItem value="traditional">

```python
def worker_task_func():
    return "Doing some work!"

worker_task_obj = PythonOperator(
    task_id="worker_task",
    python_callable=worker_task_func,
)

def my_teardown_task_func():
    return "Setting up resources!"

my_teardown_task_obj = PythonOperator(
    task_id="my_teardown_task",
    python_callable=my_teardown_task_func,
)

worker_task_obj >> my_teardown_task_obj.as_teardown()
```

![Teardown task traditional](/img/guides/airflow-setup-teardown_teardown_traditional.png)

</TabItem>
</Tabs>

You can define as many setup and teardown tasks in one DAG as you need. In order for Airflow to understand which setup and teardown tasks belong together (e.g. set up and spin down the same resources) you need to [define setup/teardown groupings](#defining-setupteardown-groupings). 

### `@setup` and `@teardown` decorators

When working with the TaskFlow API you can also use the `@setup()` and `@teardown()` decorators to turn any Python function into a setup or teardown task.

```python
from airflow.decorators import setup

@setup 
def my_setup_task():
    return "Setting up resources!"

my_setup_task()
```

![Setup task decorator](/img/guides/airflow-setup-teardown_setup_task_decorator.png)

As with the `.as_teardown()` method you cannot have a `@teardown` task without at least one upstream worker task. The worker task can use the `@task` decorator or be defined with a traditional operator.

```python
from airflow.decorators import task, teardown

@task 
def worker_task():
    return "Doing some work!"

@teardown
def my_teardown_task():
    return "Tearing down resources!"

worker_task() >> my_teardown_task()
```

![Teardown task decorator](/img/guides/airflow-setup-teardown_teardown_decorators.png)

After you have defined your setup and teardown tasks you need to [define their groupings](#defining-setupteardown-groupings) in order for Airflow to know which setup and teardown tasks perform actions on the same resources.

### Defining setup/teardown groupings

After designating tasks as setup or teardown tasks you need to define a relationship between them to create setup/teardown groupings. There are three ways to do this:

- Use the `setups` argument in the `.as_teardown()` method.
- Directly link the setup and teardown tasks with a traditional dependency, for example by using a bit-shift operator (`>>`).
- When using `@setup` and `@teardown` decorators, Airflow can infer the setup/teardown relationship if you provide the called object of the setup task as an argument to the teardown task.

In most cases how to set setup/teardown relationship is a matter of personal preference. If you are using `@setup` and `@teardown` decorators you cannot use the `setups` argument.

Worker tasks can be added to the scope of a setup/teardown grouping in two ways:

- By being between the setup and teardown tasks in the DAG dependency structure.
- By using a [context manager](#setupteardown-context-managers) with the `.teardown()` method.

Which method you choose to add worker tasks to a setup/teardown scope is a matter of personal preference.

You can have as many setup and teardown tasks in one relationship as you need, wrapping as many worker tasks as necessary. 

For example, you could have one task that creates a cluster, a second task that modifies the environment within that cluster and a third task that tears down the cluster. In this case you could define the first two tasks as setup tasks and the last one as a teardown task, all belonging to the same resource. In a second step you could add 10 tasks performing actions on that cluster to the scope of this setup / teardown grouping. 

It is also possible to have [several parallel groupings of setup/teardown tasks](#parallel-setupteardown-groupings) within the same DAG that work on different resources and are independent of each other. For example, you could have one set of setup/teardown tasks that spins up a cluster to train your ML model and a second set of setup/teardown tasks in the same DAG that creates and deletes a temporary table in your database.

You can also [nest setup/teardown groupings](#nested-setupteardown-groupings). 

You can tell Airflow that a task is a teardown task for a specific setup task by passing the setup task object to the `setups` argument of the `.as_teardown()` method. Note that if you do this, you do not need to call the `.as_setup()` method on the setup task anymore.

<Tabs
    defaultValue="taskflow"
    groupId="defining-setup-teardown-relationships"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task
def my_setup_task():
    return "Setting up resources!"

@task
def worker_task():
    return "Doing some work!"

@task
def my_teardown_task():
    return "Tearing down resources!"

my_setup_task_obj = my_setup_task()

(
    my_setup_task_obj#.as_setup() does not need to be called anymore
    >> worker_task()
    >> my_teardown_task().as_teardown(setups=my_setup_task_obj)
)
```

![Setup/teardown method decorator](/img/guides/airflow-setup-teardown-relationships_decorators_1.png)

</TabItem>
<TabItem value="traditional">

```python
def my_setup_task_func():
    return "Setting up resources!"

def worker_task_func():
    return "Doing some work!"

def my_teardown_task_func():
    return "Tearing down resources!"

my_setup_task_obj = PythonOperator(
    task_id="my_setup_task",
    python_callable=my_setup_task_func,
)

worker_task_obj = PythonOperator(
    task_id="worker_task",
    python_callable=worker_task_func,
)

my_teardown_task_obj = PythonOperator(
    task_id="my_teardown_task",
    python_callable=my_teardown_task_func,
)

(
    my_setup_task_obj#.as_setup() does not need to be called anymore
    >> worker_task_obj
    >> my_teardown_task_obj.as_teardown(setups=my_setup_task_obj)
)
```

![Setup/teardown relationships traditional](/img/guides/airflow-setup-teardown-relationships_traditional_1.png)

</TabItem>
</Tabs>

To define several setup tasks for one teardown task you can pass a list of setup tasks to the `setups` argument. You do not need to call `.as_setup()` on any of the setup tasks.

```python
(
    [my_setup_task_obj_1, my_setup_task_obj_2, my_setup_task_obj_3]
    >> worker_task()
    >> my_teardown_task().as_teardown(
        setups=[my_setup_task_obj_1, my_setup_task_obj_2, my_setup_task_obj_3]
    )
)
```

![Setup/teardown relationships multiple setup](/img/guides/airflow-setup-teardown-multiple_setups_decorators.png)

To define several teardown tasks for one setup task you have to provide the setup task object to the `setups` argument of the `.as_teardown()` method of each teardown task.

```python
(
    my_setup_task_obj
    >> worker_task()
    >> [
        my_teardown_task_obj_1.as_teardown(setups=my_setup_task_obj),
        my_teardown_task_obj_2.as_teardown(setups=my_setup_task_obj),
        my_teardown_task_obj_3.as_teardown(setups=my_setup_task_obj),
    ]
)
```

![Setup/teardown relationships multiple setup](/img/guides/airflow-setup-teardown-multiple_teardowns_decorators.png)

Instead of using the `setups` argument you can directly link the setup and teardown tasks with a traditional dependency. Whenever you define a direct dependency between a setup and a teardown task Airflow will interpret this as them belonging together, no matter what actions the tasks actually perform.

The following code snippet uses a direct dependency to define `my_setup_task` as the setup task belonging to `my_teardown_task`.

```python
(
    my_setup_task_obj.as_setup()
    >> worker_task()
    >> my_teardown_task_obj.as_teardown()
)

my_setup_task_obj >> my_teardown_task_obj
```

This code creates an identical DAG using the `setups` argument.

```python
(
    my_setup_task_obj#.as_setup() is not necessary
    >> worker_task()
    >> my_teardown_task_obj.as_teardown(setups=my_setup_task_obj)
)
```

![Setup/teardown method decorator](/img/guides/airflow-setup-teardown-relationships_decorators_1.png)

If you have several setup and/or several teardown tasks belonging together, you need to define the dependency between each setup and each teardown when using direct dependencies to define the setup/teardown relationship.

```python
(
    [my_setup_task_obj_1.as_setup(), my_setup_task_obj_2.as_setup()]
    >> worker_task()
    >> [my_teardown_task_obj_1.as_teardown(), my_teardown_task_obj_2.as_teardown()]
)

# defining the dependency between each setup and each teardown task
my_setup_task_obj_1 >> my_teardown_task_obj_1
my_setup_task_obj_1 >> my_teardown_task_obj_2
my_setup_task_obj_2 >> my_teardown_task_obj_1
my_setup_task_obj_2 >> my_teardown_task_obj_2
```

This code creates an identical DAG using the `setups` argument.

```python
(
    [my_setup_task_obj_1, my_setup_task_obj_2]
    >> worker_task()
    >> [
        my_teardown_task_obj_1.as_teardown(
            setups=[my_setup_task_obj_1, my_setup_task_obj_2]
        ),
        my_teardown_task_obj_2.as_teardown(
            setups=[my_setup_task_obj_1, my_setup_task_obj_2]
        ),
    ]
)
```

![Multiple setups/teardowns](/img/guides/airflow-setup-teardown-multiple_setups_and_teardowns.png)

When using the `@setup` and `@teardown` decorators you can define the setup/teardown relationship between two tasks either by defining [a direct dependency](#direct-dependency) or by providing the object of the called setup task as an argument to the teardown task.

The latter pattern is often used to pass information like a resource id from the setup task to the teardown task.

```python
from airflow.decorators import task, setup, teardown

@setup
def my_setup_task():
    print("Setting up resources!")
    my_cluster_id = "cluster-2319"
    return my_cluster_id

@task
def worker_task():
    return "Doing some work!"

@teardown
def my_teardown_task(my_cluster_id):
    return f"Tearing down {my_cluster_id}!"

my_setup_task_obj = my_setup_task()
my_setup_task_obj >> worker_task() >> my_teardown_task(my_setup_task_obj)
```

![Setup/Teardown method decorator](/img/guides/airflow-setup-teardown-relationships_decorators_1.png)

It is also possible to use a task with a called `.as_teardown()` method as a context manager to wrap a set of tasks that should be in scope of a setup/teardown grouping. The code snippet below shows three tasks being in scope of the setup/teardown pair created by `my_cluster_setup_task` and `my_cluster_teardown_task`.

```python
with my_cluster_teardown_task_obj.as_teardown(setups=my_cluster_setup_task_obj):
    worker_task_1() >> [worker_task_2(),  worker_task_3()]
```

![Setup/teardown created using a context manager](/img/guides/airflow-setup-teardown_context_1.png)

Note that if a task was already instantiated outside of the context manager it can still be added to the scope, but you have to do this explicitly using the `.add_task()` method on the context manager object.

```python
# task instantiation outside of the context manager
worker_task_1_obj = worker_task_1()

with my_cluster_teardown_task_obj.as_teardown(
    setups=my_cluster_setup_task_obj
) as my_scope:
    # adding the task to the context manager
    my_scope.add_task(worker_task_1_obj)
```

### Parallel setup/teardown groupings

You can have several independent sets of setup and teardown tasks in the same DAG which can be connected using any of the relationship management methods described previously. For example you might have a pair of tasks that sets up and tears down a cluster and another pair that sets up and tears down a temporary database.

<Tabs
    defaultValue="decorators"
    groupId="independent-sets-of-setup-teardown-tasks"
    values={[
        {label: '@setup/@teardown', value: 'decorators'},
        {label: '.as_teardown()', value: 'methods'},
    ]}>
<TabItem value="decorators">

```python
from airflow.decorators import task, setup, teardown

@setup
def my_cluster_setup_task():
    print("Setting up resources!")
    my_cluster_id = "cluster-2319"
    return my_cluster_id

@task
def my_cluster_worker_task():
    return "Doing some work!"

@teardown
def my_cluster_teardown_task(my_cluster_id):
    return f"Tearing down {my_cluster_id}!"

@setup
def my_database_setup_task():
    print("Setting up my database!")
    my_database_name = "DWH"
    return my_database_name

@task
def my_database_worker_task():
    return "Doing some work!"

@teardown
def my_database_teardown_task(my_database_name):
    return f"Tearing down {my_database_name}!"

my_setup_task_obj = my_cluster_setup_task()
(
    my_setup_task_obj
    >> my_cluster_worker_task()
    >> my_cluster_teardown_task(my_setup_task_obj)
)

my_database_setup_obj = my_database_setup_task()
(
    my_database_setup_obj
    >> my_database_worker_task()
    >> my_database_teardown_task(my_database_setup_obj)
)
```

</TabItem>
<TabItem value="methods">

```python
@task
def my_cluster_setup_task():
    print("Setting up resources!")
    my_cluster_id = "cluster-2319"
    return my_cluster_id

@task
def my_cluster_worker_task():
    return "Doing some work!"

@task
def my_cluster_teardown_task(my_cluster_id):
    return f"Tearing down {my_cluster_id}!"

@task
def my_database_setup_task():
    print("Setting up my database!")
    my_database_name = "DWH"
    return my_database_name

@task
def my_database_worker_task():
    return "Doing some work!"

@task
def my_database_teardown_task(my_database_name):
    return f"Tearing down {my_database_name}!"

my_setup_task_obj = my_cluster_setup_task()
(
    my_setup_task_obj
    >> my_cluster_worker_task()
    >> my_cluster_teardown_task(my_setup_task_obj).as_teardown(
        setups=my_setup_task_obj
    )
)

my_database_setup_obj = my_database_setup_task()
(
    my_database_setup_obj
    >> my_database_worker_task()
    >> my_database_teardown_task(my_database_setup_obj).as_teardown(
        setups=my_database_setup_obj
    )
)
```

</TabItem>
</Tabs>

![Parallel groups of Setup/teardown](/img/guides/airflow-setup-teardown-parallel_st.png)

### Nested setup/teardown groupings

You can nest setup and teardown tasks to have an outer and inner scope. This is useful if you have basic resources, such as a cluster that you want to set up once and then tear down after all the work is done, but you also have resources running on that cluster that you want to set up and tear down for individual groups of tasks.

The example below shows the dependency code for a simple structure with an outer and inner setup/teardown pair:

- `outer_setup` and `outer_teardown` are the outer setup and teardown tasks
- `inner_setup` and `inner_teardown` are the inner setup and teardown tasks and both are in scope of the outer setup/teardown pair
- `inner_worker_1` and `inner_worker_2` are worker tasks that are in scope of the inner setup/teardown pair. All tasks in scope of the inner setup/teardown pair will also be in scope of the outer setup/teardown pair.
- `outer_worker_1`, `outer_worker_2`, `outer_worker_3` are worker tasks that are in scope of the outer setup/teardown pair

```python
outer_setup_obj = outer_setup()
inner_setup_obj = inner_setup()
outer_teardown_obj = outer_teardown()

(
    outer_setup_obj
    >> inner_setup_obj
    >> [inner_worker_1(), inner_worker_2()]
    >> inner_teardown().as_teardown(setups=inner_setup_obj)
    >> [outer_worker_1(), outer_worker_2()]
    >> outer_teardown_obj.as_teardown(setups=outer_setup_obj)
)

outer_setup_obj >> outer_worker_3() >> outer_teardown_obj
```

![Setup/teardown nesting](/img/guides/airflow-setup-teardown_nesting.png)

Clearing a task will clear all setups and teardowns of all scopes a task is in, additionally to all downstream tasks. For example:

- clearing any of the outer worker tasks (`outer_worker_1`, `outer_worker_2`, `outer_worker_3`) will clear `outer_setup`, `outer_teardown` in addition to the worker task itself
- clearing any of the inner worker tasks (`inner_worker_1`, `inner_worker_2`) will clear `inner_setup`, `inner_teardown`, `outer_setup`, `outer_teardown` as the setup and teardown tasks of the two scopes that these tasks are in. Additionally `outer_worker_1` and `outer_worker_2` will be cleared because they are downstream of the inner worker tasks. `outer_worker_3` will not be cleared because it runs parallel to the inner worker tasks.

### Narrowing the scope of a setup task

If you have a setup task with no associated downstream task you can narrow the scope of the setup task by using an empty task as its teardown. For example, if `my_worker_task_3_obj` does not need the resources created by `my_setup_task` and should not cause a rerun of the setup task when cleared, you can add an empty teardown task in the dependency chain:

```python
my_setup_task >> [my_worker_task_1_obj >> my_worker_task_2_obj] >> my_worker_task_3_obj

[my_worker_task_1_obj >> my_worker_task_2_obj] >> EmptyOperator(
    task_id="empty_task"
).as_teardown(setups=my_setup_task)
```

## Example DAG

The DAG shown in this example mimics a setup/teardown pattern that you can run locally: 

- The `create_csv` file will create a CSV file in a directory specified as a [DAG param](airflow-params.md). This task has been turned into a setup task.
- The `delete_csv` task is the associated teardown task, deleting the resource of the CSV file.
- The `fetch_data`, `write_to_csv` and `get_average_age_obj` tasks are in the scope of the setup/teardown pair. Any failure in these tasks would still need the resource "CSV file" to be deleted afterwards (we will pretend the CSV file is an expensive cluster). To recover from a failure, when rerunning any of these tasks, we always need the CSV file to be created again, which automatically happens by rerunning the `create_csv` task when any of the tasks in scope are cleared.

This DAG comes with a convenience parameter to test setup/teardown functionality. Toggle `fetch_bad_data` in the **Trigger DAG** view to cause bad data to get into the pipeline and the `get_average_age_obj` to fail, you will see that `delete_csv` will still run and delete the CSV file.

<Tabs
    defaultValue="decorators"
    groupId="independent-sets-of-setup-teardown-tasks"
    values={[
        {label: '@setup/@teardown', value: 'decorators'},
        {label: '.as_teardown()', value: 'methods'},
    ]}>
<TabItem value="decorators">

<CodeBlock language="python">{setup_teardown_example_methods}</CodeBlock>

</TabItem>
<TabItem value="methods">

<CodeBlock language="python">{setup_teardown_example_decorators}</CodeBlock>

</TabItem>
</Tabs>