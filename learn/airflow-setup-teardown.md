---
title: "Use Setup/Teardown in Airflow"
sidebar_label: "Setup/Teardown"
description: "Use Setup/Teardown in Airflow."
id: airflow-setup-teardown
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

When using Airflow in production environments, you often need to set up resources and configurations before certain tasks can run and want to tear them down after the tasks completed to save compute costs, even if the tasks failed. For example, you might want to:

- Setup up a Spark cluster to run heavy workloads and tear it down afterwards, even if the transformation failed.
- Setup compute resources to train an ML model and tear them down afterwards, even if the training failed.
- Setup an resources to run [data quality](data-quality.md) checks and tear them down afterwards, even if the checks failed.
- Setup storage in your [custom XCom backend](custom-xcom-backends-tutorial.md) to hold data processed through Airflow tasks and tear it down afterwards, when the XCom data is no longer needed. 

In Airflow 2.7, setup and teardown functionality was added to serve these use cases with convenient decorators and methods. In this guide you will learn all about setup and teardown in Airflow.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators).
- Managing dependencies in Airflow. See [Manage task and task group dependencies in Airflow](managing-dependencies.md).

## Setup/Teardown concept

In Airflow any task can be designated as a setup or a teardown task, irrespective of the operator used or the action performed by the task. It is on you to decide which tasks are setup tasks and which are teardown tasks. 

You can turn any existing tasks into setup and teardown tasks and define relationships between them. If you are using the `@task` decorator you can use either the [.as_setup() and .as_teardown() methods](#setup-and-teardown-methods) or the [`@setup()` and `@teardown()` decorators](#setup-and-teardown-decorators). For traditional operators use the [`.as_setup()` and `.as_teardown()` methods](#setup-and-teardown-methods).

### Regular DAG vs using Setup/Teardown

Setup and teardown tasks can help you write more robust DAGs by making sure resources are setup up in the right moment and torn down even when worker tasks fail. 

The DAG below is not using Airflow setup and teardown functionality. It sets up its resources using the regular `provision_cluster` task, runs three worker tasks using those resources and finally tears down the resources using the `tear_down_cluster` task.

![DAG without Setup/Teardown - all successful](/img/guides/airflow-setup-teardown_nosutd_dag.png)

The way this DAG is set up, a failure in any of the worker tasks will lead to the `tear_down_cluster` task not running. This means that the resources will not be torn down and will continue to incur costs. Additionally, any downstream tasks depending on `tear_down_cluster` will also fail to run unless their [trigger rules](managing-dependencies.md#trigger-rules) have been configured explicitly.

![DAG without Setup/Teardown - upstream failure](/img/guides/airflow-setup-teardown_nosutd_dag_fail.png)

You can turn the `provision_cluster` task into a setup task and the `tear_down_cluster` into a teardown task by using the code examples shown in [Setup and teardown syntax](#setup-and-teardown-syntax). In the graph shown in the **Grid** view the setup task will now be marked with an upwards arrow, while the teardown task is marked with a downwards arrow. Setup and teardown tasks that have been configured to have a relationship will be connected by a dotted line.

![DAG with Setup/Teardown - all successful](/img/guides/airflow-setup-teardown-syntax_dag_successful.png)

Now, even if one of the worker tasks fails, the `tear_down_cluster` task will still run, the resources will be torn down and downstream tasks will run successfully.

![DAG with Setup/Teardown - upstream failure](/img/guides/airflow-setup-teardown_syntax_dag_fail.png)

Additionally, when clearing any of the worker tasks, both its setup and teardown tasks will be cleared and rerun. This is useful when you are recovering from a pipeline issue and need to one or more tasks that use a resource but not all of them. 

For example, in the DAG above `worker_task_2` failed and `worker_task_3` was unable to run due to its upstream task having failed while `worker_task_1` was successful. When clearing the failed task `worker_task_2` by clicking on the **Clear task** button, both the setup task `provision_cluster` and the teardown task `tear_down_cluster` will be cleared and rerun in addition to the `worker_task_3`. This allows for complete recovery without needing to rerun `worker_task_1` or the need for manually rerunning individual tasks.

![DAG with Setup/Teardown - recovery](/img/guides/airflow-setup-teardown_syntax_dag_fail.png)

## .as_setup() and .as_teardown() methods

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

You can define as many setup and teardown tasks in one DAG as you need. In order for Airflow to understand which setup and teardown tasks belong together (e.g. set up and spin down the same resources) you need to [define a relationship between them](#defining-relationships-between-setup-and-teardown-tasks). 

## @setup() and @teardown() decorators

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

After you have defined your setup and teardown tasks you need to [define a relationship between them](#defining-relationships-between-setup-and-teardown-tasks) in order for Airflow to know which setup and teardown tasks perform actions on the same resources.

## Defining Setup/Teardown relationships

After designating tasks as setup or teardown tasks you need to define a relationship between them. There are three ways to do this:

- Use the `setups` argument in the `.as_teardown()` method  
- Directly link the setup and teardown tasks with a traditional dependency, for example by using a bit-shift operator (`>>`)
- When using `@setup` and `@teardown` decorators, Airflow can infer the setup/teardown relationship if you provide the called object of the setup task as an argument to the teardown task

In most cases how to set Setup/Teardown relationship is a matter of personal preference. If you are using `@setup` and `@teardown` decorators you cannot use the `setups` argument.

You can have as many setup and teardown tasks in one relationship as you need. For example, you could have one task that creates a cluster, a second task that modifies the environment within that cluster and a third task that tears down the cluster. In this case you could define the first two tasks as setup tasks and the last one as a teardown task, all belonging to the same resource.

It is also possible to have several sets of setup/teardown tasks within the same DAG that work on different resources and are independent of each other. For example, you could have one set of setup/teardown tasks that spins up a cluster to train your ML model and a second set of setup/teardown tasks in the same DAG that creates and deletes a temporary table in your database.

### `setups` argument

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

![Setup/Teardown method decorator](/img/guides/airflow-setup-teardown-relationships_decorators_1.png)

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

![Setup/Teardown relationships traditional](/img/guides/airflow-setup-teardown-relationships_traditional_1.png)

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

![Setup/Teardown relationships multiple setup](/img/guides/airflow-setup-teardown-multiple_setups_decorators.png)

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

![Setup/Teardown relationships multiple setup](/img/guides/airflow-setup-teardown-multiple_teardowns_decorators.png)

### Direct dependency

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

![Setup/Teardown method decorator](/img/guides/airflow-setup-teardown-relationships_decorators_1.png)

If you have several setup and/or several teardown tasks belonging together, you need to define the dependency between each pair of them when using direct dependencies to define the setup/teardown relationship.

```python
(
    [my_setup_task_obj_1.as_setup(), my_setup_task_obj_2.as_setup()]
    >> worker_task()
    >> [my_teardown_task_obj_1.as_teardown(), my_teardown_task_obj_2.as_teardown()]
)

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

### `@setup` and `@teardown` relationships

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

### Independent sets of setup/teardown tasks

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

![Parallel groups of Setup/Teardown](/img/guides/airflow-setup-teardown-parallel_st.png)

### Setup/Teardown context managers



### Example DAG

Brining it all together here is an example DAG with two sets of setup and teardown tasks.

```python

```



## Teardown and dependencies


## Nesting Setup/Teardown


## Use Setup/Teardown with Task Groups

## Actual example