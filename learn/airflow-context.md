---
title: "Access the Apache Airflow context"
sidebar_label: "Context"
description: "Access the Airflow context in your tasks."
id: airflow-context
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import context_and_xcom from '!!raw-loader!../code-samples/dags/airflow-context/context_and_xcom.py';

The Airflow context is a dictionary containing information about a running DAG and its Airflow environment that can be accessed from a task. One of the most common values to retrieve from the Airflow context is the [`ti` / `task_instance` keyword](#ti--task_instance), which allows you to access attributes and methods of the [`taskinstance` object](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/taskinstance/index.html).

Other common reasons to access the Airflow context are:

- You want to use [DAG-level parameters](airflow-params.md) in your Airflow tasks.
- You want to use the DAG run's [logical date](scheduling-in-airflow.md#scheduling-concepts) in an Airflow task, for example as part of a file name.
- You want to explicitly push and pull values to [XCom](airflow-passing-data-between-tasks.md#xcom) with a custom key.
- You want to make an action in your task conditional on the setting of a specific [Airflow configuration](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html).

Use this document to learn about the data stored in the Airflow context and how to access it.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Access the Airflow context

The Airflow context is available in all Airflow tasks. You can access information from the context using the following methods:

- Pass the `**context` argument to the function used in a [`@task` decorated task](airflow-decorators.md) or [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/PythonOperator).
- Use [Jinja templating](templating.md) in traditional Airflow operators.
- Access the context `kwarg` in the `.execute` method of any traditional or custom operator.

You cannot access the Airflow context dictionary outside of an Airflow task.

### Retrieve the Airflow context using the `@task` decorator or PythonOperator

To access the Airflow context in a `@task` decorated task or PythonOperator task, you need to add a `**context` argument to your task function. This will make the context available as a dictionary in your task.

The following code snippets show how to print out the full context dictionary from a task:

<Tabs
    defaultValue="taskflow"
    groupId= "task-decorator-PythonOperator"
    values={[
        {label: 'TaskFlow', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
from pprint import pprint

@task
def print_context(**context)
    pprint(context)
```

</TabItem>

<TabItem value="traditional">

```python
from pprint import pprint

def print_context_func(**context):
    pprint(context)

print_context = PythonOperator(
    task_id="print_context",
    python_callable=print_context_func,
)
```

</TabItem>

</Tabs>

### Retrieve the Airflow context using Jinja templating

Many elements of the Airflow context can be accessed by using [Jinja templating](templating.md). You can get the list of all parameters that allow templates for any operator by printing out its `.template_fields` attribute.

For example, you can access a DAG run's logical date in the format `YYYY-MM-DD` by using the template `{{ ds }}` in the `bash_command` parameter of the BashOperator.

```python
print_logical_date = BashOperator(
    task_id="print_logical_date",
    bash_command="echo {{ ds }}",
)
```

It is also common to use Jinja templating to access [XCom](airflow-passing-data-between-tasks.md#xcom) values in the parameter of a traditional task. In the code snippet below, the first task `return_greeting` will push the string "Hello" to XCom, and the second task `greet_friend` will use a Jinja template to pull that value from the `ti` (task instance) object of the Airflow context and print `Hello friend! :)` into the logs.

```python
@task 
def return_greeting():
    return "Hello"

greet_friend = BashOperator(
    task_id="greet_friend",
    bash_command="echo '{{ ti.xcom_pull(task_ids='return_greeting') }} friend! :)'",
)

return_greeting() >> greet_friend
```

Find an up to date list of all available templates in the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html). Learn more about using XComs to pass data between Airflow tasks in [Pass data between tasks](airflow-passing-data-between-tasks.md).

### Retrieve the Airflow context using custom operators

In a traditional operator, the Airflow context is always passed to the `.execute` method using the `context` keyword argument. If you write a [custom operator](airflow-importing-custom-hooks-operators.md), you have to include a `context` kwarg in the `execute` method as shown in the following custom operator example.

```python
class PrintDAGIDOperator(BaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        print(context["dag"].dag_id)
```

## Common Airflow context values

This section gives an overview of the most commonly used keys in the Airflow context dictionary. To see an up-to-date list of all keys and their types, view the [Airflow source code](https://github.com/apache/airflow/blob/main/airflow/utils/context.pyi). 

### ti / task_instance

The `ti` or `task_instance` key contains the [TaskInstance object](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/taskinstance/index.html). The most commonly used attributes are `.xcom_pull` and `.xcom_push`, which allow you to push and pull [XComs](airflow-passing-data-between-tasks.md).

The following DAG shows an example of using `context["ti"].xcom_push(...)` and `context["ti"].xcom_pull(...)` to explicitly pass data between tasks.

<CodeBlock language="python">{context_and_xcom}</CodeBlock>

The `downstream_task` will print the following information to the logs:

```text
[2023-06-16, 13:14:11 UTC] {logging_mixin.py:149} INFO - Returned Num:  19
[2023-06-16, 13:14:11 UTC] {logging_mixin.py:149} INFO - Passed Num:  19
[2023-06-16, 13:14:11 UTC] {logging_mixin.py:149} INFO - Explicit Num:  23
```

### Scheduling keys

One of the most common reasons to access the Airflow context in your tasks is to retrieve information about the scheduling of their DAG. A common pattern is to use the timestamp of the logical date in names of files written from a DAG to create a unique file for each DAG run.

The task below creates a new text file in the `include` folder for each DAG run with the timestamp in the filename in the format `YYYY-MM-DDTHH:MM:SS+00:00`. Refer to [Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) for an up to date list of time related keys in the context, and [Jinja templating](templating.md) for more information on how to pass these values to templateable parameters of traditional operators.

```python
@task
def write_file_with_ts(**context):
    ts = context["ts"]
    with open(f"include/{ts}_hello.txt", "a") as f:
        f.write("Hello, World!")
```

### conf

The `conf` key contains an [AirflowConfigParser object](https://github.com/apache/airflow/blob/main/airflow/configuration.py#L149) that contains information about your Airflow configuration. To see your full Airflow configuration in dictionary format, use the following code:

```python 
from pprint import pprint

@task
def print_config(**context)
    pprint(context["conf"].as_dict())
```

The Airflow configuration includes information about the settings for your Airflow environment. By accessing these settings programmatically, you can make your pipeline conditional on the setting of a specific Airflow configuration. For example, you can have a task check which [executor](airflow-executors-explained.md) your environment is using by accessing the [executor configuration setting](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#executor). The task can then [branch](airflow-branch-operator.md) depending on the result:

```python
@task.branch
def branch_based_on_executor(**context):
    executor = context["conf"].get(section="core", key="EXECUTOR")
    if executor == "LocalExecutor":
        return "t1"
    else:
        return "t2"
```

### dag

The `dag` key contains the DAG object. There are many attributes and methods available for the DAG object. One example is the `.get_run_dates` method from which you can fetch a list of all timestamps on which the DAG will run within a certain time period. This is especially useful for DAGs with [complex schedules](scheduling-in-airflow.md).

```python 
@task
def get_dagrun_dates(**context):
    run_dates = context["dag"].get_run_dates(
        start_date=datetime(2023, 10, 1), end_date=datetime(2023, 10, 10)
    )
    print(run_dates)
```

You can find a list of all attributes and methods of the DAG object in the [Airflow documentation of the DAG object](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#airflow.models.dag.DAG).

### dag_run

The `dag_run` key contains the [DAG run object](https://github.com/apache/airflow/blob/main/airflow/models/dagrun.py). Two commonly used elements of the DAG run object are the `.active_runs_of_dags` method, which gives you the number of currently active runs of a specific DAG, and the `.external_trigger` attribute, which returns `True` if a DAG run was triggered outside of its normal schedule.

```python
@task
def print_dagrun_info(**context):
    print(context["dag_run"].active_runs_of_dags())
    print(context["dag_run"].external_trigger)
```

You can find a list of all attributes and methods of the DAG run object in the [Airflow source code](https://github.com/apache/airflow/blob/main/airflow/models/dagrun.py).

### params

The `params` key contains a dictionary of all DAG- and task-level params that were passed to a specific task instance. Individual params can be accessed using their respective key.

```python
@task
def print_param(**context):
    print(context["params"]["my_favorite_param"])
```

Learn more about params in the [Airflow params guide](airflow-params.md).

### var

The `var` key contains all Airflow variables of your Airflow instance. [Airflow variables](airflow-variables.md) are key-value pairs that are commonly used to store instance-level information that rarely changes.

```python
@task
def get_var_from_context(**context):
    print(context["var"]["value"].get("my_regular_var"))
    print(context["var"]["json"].get("my_json_var")["num2"])
```