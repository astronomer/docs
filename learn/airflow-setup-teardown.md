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

You can turn any task in your Airflow DAG into a setup or teardown task by calling the [`.as_setup()` or `.as_teardown()` method](#setup-and-teardown-methods) on the task. If you are using the `@task` decorator you can also create a setup or teardown task by using the [`@setup()` or `@teardown()` decorators](#setup-and-teardown-decorators).

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

## Setup/Teardown syntax

You can turn any existing tasks into setup and teardown tasks and define relationships between them. If you are using the `@task` decorator you can use either the [.as_setup() and .as_teardown() methods](#setup-and-teardown-methods) or the [`@setup()` and `@teardown()` decorators](#setup-and-teardown-decorators). For traditional operators use the [`.as_setup()` and `.as_teardown()` methods](#setup-and-teardown-methods).

### .as_setup() and .teardown() methods

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

### @setup() and @teardown() decorators


### Defining relationships between setup and teardown tasks


### Example DAG




## Teardown and dependencies


## Nesting Setup/Teardown


## Use Setup/Teardown with Task Groups

## Actual example