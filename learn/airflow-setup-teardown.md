---
title: "Use setup and teardown tasks in Airflow"
sidebar_label: "Setup/ teardown tasks"
description: "Learn how to use setup and teardown tasks to manage task resources in Airflow."
id: airflow-setup-teardown
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import setup_teardown_example_methods from '!!raw-loader!../code-samples/dags/airflow-setup-teardown/setup_teardown_example_methods.py';
import setup_teardown_example_decorators from '!!raw-loader!../code-samples/dags/airflow-setup-teardown/setup_teardown_example_decorators.py';

In production Airflow environments, it's best practice to set up resources and configurations before certain tasks can run, then tear the resources down even if the tasks fail. This pattern can reduce resource utilization and save costs.

Starting in Airflow 2.7, you can use a special type of task to create and delete resources. In this guide, you will learn all about _setup_ and _teardown tasks_ in Airflow.

![DAG with setup/teardown - all successful](/img/guides/airflow-setup-teardown_intro_dag.png)

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators).
- Managing dependencies in Airflow. See [Manage task and task group dependencies in Airflow](managing-dependencies.md).

## When to use setup/teardown tasks

This feature allows you to designate any existing Airflow task as a setup or teardown task, with special behavior and added visibility of the setup/teardown relationship in the Airflow UI.

There are many use cases for setup and teardown tasks. For example, you might want to:

- Manage a Spark cluster to run heavy workloads.
- Manage compute resources to train an ML model.
- Manage the resources to run [data quality](data-quality.md) checks.
- Set up storage in your [custom XCom backend](custom-xcom-backends-tutorial.md) to hold data processed through Airflow tasks, then tear the extra storage down afterwards when the XCom data is no longer needed. 

## Setup/teardown concepts

Any task can be designated as a setup or a teardown task. The most typical pattern is to have setup and teardown tasks that are connected in a setup/teardown _grouping_.

Tasks that run after a setup tasks and before the associated teardown tasks are considered to be _in scope_ of a specific setup / teardown grouping. Usually these tasks will use the resources set up by the setup task and which the teardown task will dismantle.

Setup/teardown tasks have different behavior from regular tasks:

- Clearing a task that is in scope of a setup / teardown grouping will also clear and rerun the associated setup and teardown tasks, ensuring that all resources the task needs are created again for the task rerun and torn down after the task has completed.

- A teardown task will run as long as at least one of its associated `setup` tasks have completed successfully and all of its upstream tasks have completed, regardless of whether they were successful or not. If all associated setup tasks fail or are skipped, the teardown task will be failed or skipped respectively.

- A teardown task without any associated setup tasks will always run once all upstream worker tasks have completed running, independently of whether they were successful or not.

- When evaluating whether a DAG run was successful, Airflow will ignore teardown tasks by default. This means if a teardown task fails as the final task of a DAG, the DAG is still marked as having succeeded. In the example shown in the screenshot below, the DAG run state is not impacted by the failure of `tear_down_cluster` and is marked as successful. You can change this behavior by setting `on_failure_fail_dagrun=True` in the teardown task.

    ![Successful DAG with failed teardown](/img/guides/airflow-setup-teardown_teardown_fail_dag_succeed.png)

- When a teardown task is within a [task group](task-groups.md) and a dependency is set on the task group, the teardown task will be ignored when evaluating if a dependency has been met. For example, `run_after_taskgroup`, which dependent on the `work_in_the_cluster` task group, will run even if the teardown task has failed or is still running.

    ![Task group with teardown](/img/guides/airflow-setup-teardown-task_after_taskgroup.png)

- You can have a setup task without an associated teardown task and vice versa. If you define a setup task without a teardown task, everything downstream of the setup task is considered in its scope and will cause the setup task to rerun when cleared.

### Before and after using setup and teardown tasks

Setup and teardown tasks can help you write more robust DAGs by making sure resources are set up in the right moment and torn down even when worker tasks fail. 

The following DAG is not using Airflow setup and teardown functionality. It sets up its resources using a standard task called `provision_cluster`, runs three worker tasks using those resources, and tears down the resources using the `tear_down_cluster` task.

![DAG without Setup/teardown - all successful](/img/guides/airflow-setup-teardown_nosutd_dag.png)

The way this DAG is set up, a failure in any of the worker tasks will lead to the `tear_down_cluster` task not running. This means that the resources will not be torn down and will continue to incur costs. Additionally, any downstream tasks depending on `tear_down_cluster` will also fail to run unless they have [trigger rules](managing-dependencies.md#trigger-rules) to run independent of upstream failures.

![DAG without setup/teardown - upstream failure](/img/guides/airflow-setup-teardown_nosutd_dag_fail.png)

In this example, you can turn the `provision_cluster` task into a setup task and the `tear_down_cluster` into a teardown task by using the code examples shown in [Basic setup/teardown syntax](#basic-setupteardown-syntax). 

After you convert the tasks, the **Grid** view shows your setup tasks with an upwards arrow and teardown tasks with a downwards arrow. After you configure the [setup/teardown relationship](#defining-setupteardown-relationships) between `provision_cluster` and `tear_down_cluster`, they turn into a setup/teardown grouping and are connected by a dotted line. The tasks `worker_task_1`, `worker_task_2` and `worker_task_3` are in the scope of this setup/teardown grouping.

![DAG with setup/teardown - all successful](/img/guides/airflow-setup-teardown-syntax_dag_successful.png)

Now, even if one of the worker tasks fails, like `worker_task_2` in the following screenshot, the `tear_down_cluster` task will still run, the resources will be torn down, and downstream tasks will run successfully.

![DAG with setup/teardown - upstream failure](/img/guides/airflow-setup-teardown_syntax_dag_fail.png)

Additionally, when you clear any of the worker tasks, both the setup and teardown tasks will also be cleared and rerun. This is useful when you are recovering from a pipeline issue and need to rerun one or more tasks that use a resource independent of the other tasks in the scope.

For example, in the previous DAG, consider if `worker_task_2` failed and `worker_task_3` was unable to run due to its upstream task having failed. If you cleared `worker_task_2` by clicking **Clear task**, both the setup task `provision_cluster` and the teardown task `tear_down_cluster` will be cleared and rerun in addition to `worker_task_2` and `worker_task_3`. This lets you completely recover without needing to rerun `worker_task_1` or manually rerun individual tasks.

![DAG with setup/teardown - recovery](/img/guides/airflow-setup-teardown-clear_task.png)

## Setup/teardown implementation

There are two ways to turn tasks into setup/teardown tasks: 

- Using the `.as_setup()` and `.as_teardown()` methods on TaskFlow API tasks or traditional operators.
- Using the `@setup` and `@teardown` decorators on a Python function.

Setup and teardown tasks can be combined into groupings by:

- Providing the setup task object to the `setups` argument in the `.as_teardown()` method of a teardown task object.
- Connecting a setup and a teardown task with a normal task dependency using the bit-shift operator (`>>`) or a dependency function like `chain()`.
- Providing the called object of a task created using the `@setup` decorator as an argument to a task created using the `@teardown` decorator.

Which method you use is a matter of personal preference. However, note that if you are using `@setup` and `@teardown` decorators, you cannot use the `setups` argument.

You can have multiple sets of setup and teardown tasks in a DAG, both in [parallel](#parallel-setupteardown-groupings) and [nested](#nested-setupteardown-groupings).

Worker tasks can be added to the scope of a setup/teardown grouping in two ways:

- By being between the setup and teardown tasks in the DAG dependency relationship.
- By using a context manager with the `.teardown()` method.

Which method you choose to add worker tasks to a setup/teardown scope is a matter of personal preference.

### `.as_setup()` and `.as_teardown()` methods

Any individual tasks can be turned into setup or teardown task on its own.

To turn a task into a setup task, call the `.as_setup()` method on the called task object.  

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

To turn a task into a teardown task, call the `.as_teardown()` method on the called task object. Note that you cannot have a teardown task without at least one upstream worker task.

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

You can define as many setup and teardown tasks in one DAG as you need. In order for Airflow to understand which setup and teardown tasks belong together, you need to [define setup/teardown groupings](#creating-setup-teardown-groupings). 

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

### Creating setup/teardown groupings

There are no limits to how many setup and teardown tasks you can have, nor are there limits to how many worker tasks you include in a grouping.

For example, you could have one task that creates a cluster, a second task that modifies the environment within that cluster, and a third task that tears down the cluster. In this case you could define the first two tasks as setup tasks and the last one as a teardown task, all belonging to the same resource. In a second step you, could add 10 tasks performing actions on that cluster to the scope of the setup / teardown grouping.

There are multiple methods for linking setup and teardown tasks.

<Tabs
    defaultValue="taskflow_setups"
    groupId="defining-setup-teardown-relationships"
    values={[
        {label: 'TaskFlow API setups argument', value: 'taskflow_setups'},
        {label: 'Traditional syntax setups argument', value: 'traditional_setups'},
        {label: 'Direct dependencies', value: 'taskflow_direct'},
        {label: 'Using setup/teardown decorators', value: 'decorators'},
        {label: 'Using a context manager', value: 'context_manager'},
    ]}>
<TabItem value="taskflow_setups">

When using the TaskFlow API's `@task` decorator you can use the `.as_teardown()` method in the `setups` argument to define which setup tasks are being grouped with a teardown task. Note that it is also possible to use [`@setup` and `@teardown` decorators](#setup-and-teardown-decorators) instead and link them using direct dependencies.

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
<TabItem value="traditional_setups">

If you are using traditional Airflow operators, you can use the `.as_teardown()` method in the `setups` argument to define which setup tasks are being grouped with a teardown task.

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
<TabItem value="taskflow_direct">

Instead of using the `setups` argument you can directly link the setup and teardown tasks with a traditional dependency. Whenever you define a direct dependency between a setup and a teardown task Airflow will interpret this as them being grouped together, no matter what actions the tasks actually perform.

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

</TabItem>
<TabItem value="decorators">

With the`@setup` and `@teardown` decorators, you can define the setup/teardown relationship between two tasks either by defining direct dependencies or by providing the object of the setup task as an argument to the teardown task.

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

</TabItem>
<TabItem value="context_manager">

You can also use a task that calls the `.as_teardown()` method to wrap a set of tasks that should be in scope of a setup/teardown grouping. The code snippet below shows three tasks being in scope of the setup/teardown grouping created by `my_cluster_setup_task` and `my_cluster_teardown_task`.

```python
with my_cluster_teardown_task_obj.as_teardown(setups=my_cluster_setup_task_obj):
    worker_task_1() >> [worker_task_2(),  worker_task_3()]
```

![Setup/teardown created using a context manager](/img/guides/airflow-setup-teardown_context_1.png)

Note that a task that was already instantiated outside of the context manager can still be added to the scope, but you have to do this explicitly using the `.add_task()` method on the context manager object.

```python
# task instantiation outside of the context manager
worker_task_1_obj = worker_task_1()

with my_cluster_teardown_task_obj.as_teardown(
    setups=my_cluster_setup_task_obj
) as my_scope:
    # adding the task to the context manager
    my_scope.add_task(worker_task_1_obj)
```

</TabItem>
</Tabs>

#### Using multiple setup/teardown tasks in one grouping

To define several setup tasks for one teardown task, you can pass a list of setup tasks to the `setups` argument. You do not need to call `.as_setup()` on any of the setup tasks.

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

To define several teardown tasks for one setup task, you have to provide the setup task object to the `setups` argument of the `.as_teardown()` method of each teardown task.

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

If you have a DAG with several setup and teardown tasks belonging together, you need to define explicit dependencies between each setup and each teardown to define the setup/teardown relationship.

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

#### Parallel setup/teardown groupings

You can have several independent sets of setup and teardown tasks in the same DAG. For example, you might have a grouping of tasks that sets up and tears down a cluster and another grouping that sets up and tears down a temporary database.

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

#### Nested setup/teardown groupings

You can nest setup and teardown tasks to have an outer and inner scope. This is useful if you have basic resources, such as a cluster that you want to set up once and then tear down after all the work is done, but you also have resources running on that cluster that you want to set up and tear down for individual groups of tasks.

The example below shows the dependency code for a simple structure with an outer and inner setup/teardown grouping:

- `outer_setup` and `outer_teardown` are the outer setup and teardown tasks.
- `inner_setup` and `inner_teardown` are the inner setup and teardown tasks and both are in scope of the outer setup/teardown grouping.
- `inner_worker_1` and `inner_worker_2` are worker tasks that are in scope of the inner setup/teardown grouping. All tasks in scope of the inner setup/teardown grouping will also be in scope of the outer setup/teardown grouping.
- `outer_worker_1`, `outer_worker_2`, `outer_worker_3` are worker tasks that are in scope of the outer setup/teardown grouping.

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

Clearing a task will clear all setups and teardowns the task is in scope of, in addition to all downstream tasks. For example:

- Clearing any of the outer worker tasks (`outer_worker_1`, `outer_worker_2`, `outer_worker_3`) will also clear `outer_setup`, `outer_teardown`.
- Clearing any of the inner worker tasks (`inner_worker_1`, `inner_worker_2`) will clear `inner_setup`, `inner_teardown`, `outer_setup`, and `outer_teardown`. Additionally `outer_worker_1` and `outer_worker_2` will be cleared because they are downstream of the inner worker tasks. `outer_worker_3` will not be cleared because it runs parallel to the inner worker tasks.

### Narrowing the scope of a setup task

If you have a setup task with no associated downstream task, you can narrow the scope of the setup task by using an empty task as its teardown. For example, if `my_worker_task_3_obj` does not need the resources created by `my_setup_task` and should not cause a rerun of the setup task when cleared, you can add an empty teardown task in the dependency chain:

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
- The `fetch_data`, `write_to_csv` and `get_average_age_obj` tasks are in the scope of the setup/teardown grouping. Any failure in these tasks would still need the resource "CSV file" to be deleted afterwards (to make it more real, consider the CSV file to be an expensive cluster). To recover from a failure when rerunning any of these tasks, you always need the CSV file to be created again, which automatically happens by rerunning the `create_csv` task when any of the tasks in scope are cleared.

This DAG comes with a convenience parameter to test setup/teardown functionality. Toggle `fetch_bad_data` in the **Trigger DAG** view to cause bad data to get into the pipeline and the `get_average_age_obj` to fail. You will see that `delete_csv` will still run and delete the CSV file.

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