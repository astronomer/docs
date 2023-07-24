---
title: "Manage task and task group dependencies in Airflow"
sidebar_label: "Task dependencies"
id: managing-dependencies
---

<head>
  <meta name="description" content="Learn how to manage dependencies between tasks and TaskGroups in Apache Airflow, including how to set dynamic dependencies." />
  <meta name="og:description" content="Learn how to manage dependencies between tasks and TaskGroups in Apache Airflow, including how to set dynamic dependencies." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import dependencies_example_1 from '!!raw-loader!../code-samples/dags/managing-dependencies/dependencies_example_1.py';
import dependencies_example_2_taskflow from '!!raw-loader!../code-samples/dags/managing-dependencies/dependencies_example_2_taskflow.py';
import dependencies_branch_example_taskflow from '!!raw-loader!../code-samples/dags/managing-dependencies/dependencies_branch_example_taskflow.py';
import dependencies_branch_example_traditional from '!!raw-loader!../code-samples/dags/managing-dependencies/dependencies_branch_example_traditional.py';

[Dependencies](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#relationships) are a powerful and popular Airflow feature. In Airflow, your pipelines are defined as Directed Acyclic Graphs (DAGs). Each task is a node in the graph and dependencies are the directed edges that determine how to move through the graph. Because of this, dependencies are key to following data engineering best practices because they help you define flexible pipelines with atomic tasks.

Throughout this guide, the following terms are used to describe task dependencies:

- **Upstream task**: A task that must reach a specified state before a dependent task can run.
- **Downstream task**: A dependent task that cannot run until an upstream task reaches a specified state.

In this guide you'll learn about the many ways you can implement dependencies in Airflow, including:

- Basic task dependencies.
- Dependency functions.
- Dynamic dependencies.
- Dependencies with task groups.
- Dependencies with the TaskFlow API.
- Trigger rules.

To view a video presentation of these concepts, see [Manage Dependencies Between Airflow Deployments, DAGs, and Tasks](https://www.astronomer.io/events/webinars/manage-dependencies-between-airflow-deployments-dags-tasks/). 

The focus of this guide is dependencies between tasks in the same DAG. If you need to implement dependencies between DAGs, see [Cross-DAG dependencies](cross-dag-dependencies.md).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## Basic dependencies

Basic dependencies between Airflow tasks can be set in the following ways:

- Using bit-shift operators (`<<` and `>>`)
- Using the `set_upstream` and `set_downstream` methods

For example, if you have a DAG with four sequential tasks, the dependencies can be set in four ways:

- Using `set_downstream()`:

    ```python
    t0.set_downstream(t1)
    t1.set_downstream(t2)
    t2.set_downstream(t3)
    ```

- Using `set_upstream()`:

    ```python
    t3.set_upstream(t2)
    t2.set_upstream(t1)
    t1.set_upstream(t0)
    ```

- Using `>>`

    ```python
    t0 >> t1 >> t2 >> t3
    ```

- Using `<<`

    ```python
    t3 << t2 << t1 << t0
    ```

All of these methods are equivalent and result in the DAG shown in the following image:

![Basic Dependencies](/img/guides/managing_dependencies_basic_dependencies.png)

Astronomer recommends using a single method consistently. Using both bit-shift operators and `set_upstream`/`set_downstream` in your DAGs can overly-complicate your code. 

To set a dependency where two downstream tasks are dependent on the same upstream task, use lists or tuples. For example:

```python
# Dependencies with lists
t0 >> t1 >> [t2, t3]

# Dependencies with tuples
t0 >> t1 >> (t2, t3)
```

These statements are equivalent and result in the DAG shown in the following image: 

![List Dependencies](/img/guides/managing-dependencies_list_dependencies.png)

When using bit-shift operators and the `.set_upstream` and `.set_downstream` method, it is not possible to set dependencies between two lists. For example, `[t0, t1] >> [t2, t3]` returns an error. To set dependencies between lists, use the dependency functions described in the next section.

## Dependency functions

Dependency functions are utilities that let you set dependencies between several tasks and lists of tasks. A common reason to use dependency functions over bit-shift operators is for example to create dependencies for tasks that were created in a loop and are stored in a list.

```python
list_of_tasks = []
for i in range(5):
    if i % 3 == 0:
        ta = EmptyOperator(task_id=f"ta_{i}")
        list_of_tasks.append(ta)
    else:
        ta = EmptyOperator(task_id=f"ta_{i}")
        tb = EmptyOperator(task_id=f"tb_{i}")
        tc = EmptyOperator(task_id=f"tc_{i}")
        list_of_tasks.append([ta, tb, tc])

chain(*list_of_tasks)
```

This code creates the following DAG structure:

![List Dependencies](/img/guides/managing-dependencies_chain_dependencies_1.png)

### chain()

To set parallel dependencies between tasks and lists of tasks of the same length, use the [`chain()` function](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html#airflow.models.baseoperator.chain). For example:

```python
# from airflow.models.baseoperator import chain
chain(t0, t1, [t2, t3, t4], [t5, t6, t7], t8)
```

This code creates the following DAG structure:

![Chain Dependencies](/img/guides/managing-dependencies_chain_dependencies.png)

When using the `chain` function, any lists or tuples that are set to depend directly on each other need to be of the same length.  

```python
chain([t0, t1], [t2, t3])  # this code will work
chain([t0, t1], [t2, t3, t4])  # this code will cause an error
chain([t0, t1], t2, [t3, t4, t5])  # this code will work
```

### chain_linear()

To set interconnected dependencies between tasks and lists of tasks, use the `chain_linear()` function. This function is available in Airflow 2.7+, in older versions of Airflow you can set similar dependencies between two lists at a time using the [`cross_downstream()` function](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html#airflow.models.baseoperator.cross_downstream). 

Replacing `chain` with `chain_linear` in the previous example as shown in this code snippet will create a DAG structure where the dependency between lists is set in a pattern so that each element in the downstream list will depend on each element in the upstream list.

```python
# from airflow.models.baseoperator import chain_linear
chain_linear(t0, t1, [t2, t3, t4], [t5, t6, t7], t8)
```

![Chain Linear Dependencies 2](/img/guides/managing-dependencies_chain_linear_dependencies_1.png)

The `chain_linear()` function can take in lists of any length in any order. For example:

```python
chain_linear([t0, t1], [t2, t3, t4])
```

![Chain Linear Dependencies 1](/img/guides/managing-dependencies_chain_linear_dependencies_2.png)

## Loops and dependencies

If you generate tasks in a loop in your DAG, you can define the dependencies within the context of the code used to create the tasks.

In the following example, a set of parallel tasks is generated by looping through a list of endpoints. Each `generate_files` task is downstream of `start` and upstream of `send_email`.

```python
t0 = EmptyOperator(task_id="start")

send_email = EmailOperator(
    task_id="send_email",
    to=email_to,
    subject="Data to S3 DAG",
    html_content="<p>The data to S3 DAG completed successfully. \
    Files can now be found on S3. <p>",
)

for endpoint in endpoints:
    generate_files = PythonOperator(
        task_id="generate_file_{0}".format(endpoint),
        python_callable=upload_to_s3,
        op_kwargs={"endpoint": endpoint, "date": date},
    )

    t0 >> generate_files >> send_email

```

This image shows the resulting DAG:

![Loop Dependencies](/img/guides/managing-dependencies_loop_dep.png)

## Dependencies in dynamic task mapping

Tasks that utilize [dynamic task mapping](dynamic-tasks.md) can be set to be up- and downstream of other tasks as with regular tasks. Keep in mind that when using the default [trigger rule](#trigger-rules) `all_success`, all mapped task instances need to be successful for the downstream task to run. For the purpose of trigger rules, mapped task instances behave like a set of parallel upstream tasks.

```python
start=EmptyOperator(task_id="start")

@task 
def multiply(x,y):
    return x*y

multiply_obj = multiply.partial(x=2).expand(y=[1,2,3])

# end will only run if all mapped task instances of the multiply task are successful
end = EmptyOperator(task_id="end")

start >> multiply_obj >> end

# all of the following ways of setting dependencies are valid
# multiply_obj.set_downstream(end)
# end.set_upstream(multiply_obj)
# chain(start, multiply_obj, end)

```

![Dependencies dynamic tasks](/img/guides/managing-dependencies_dynamic_tasks.png)

## Task group dependencies

[Task groups](task-groups.md) are an Airflow concept allowing for grouping of tasks in the UI and for [dynamic mapping use cases](task-groups.md#generate-task-groups-dynamically-at-runtime). You can get more information on task groups in the respective guide. This section will explain how to set dependencies between task groups.

Dependencies can be set both inside and outside of a task group. For example, in the following DAG code there is a start task, a task group with two dependent tasks, and an end task. All of these task need to happen sequentially. The dependencies between the two tasks in the task group are set within the task group's context (`t1 >> t2`). The dependencies between the task group and the start and end tasks are set within the DAG's context (`t0 >> tg1() >> t3`).

<Tabs
    defaultValue="taskflow"
    groupId= "task-group-dependencies"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
t0 = EmptyOperator(task_id="start")

# Start Task Group definition
@task_group(
    group_id="group1"
)
def tg1():
    t1 = EmptyOperator(task_id="task1")
    t2 = EmptyOperator(task_id="task2")

    t1 >> t2
# End Task Group definition

t3 = EmptyOperator(task_id="end")

# Set Task Group's (tg1) dependencies
t0 >> tg1() >> t3
```

</TabItem>

<TabItem value="traditional">

```python
t0 = EmptyOperator(task_id="start")

# Start Task Group definition
with TaskGroup(group_id="group1") as tg1:
    t1 = EmptyOperator(task_id="task1")
    t2 = EmptyOperator(task_id="task2")

    t1 >> t2
# End Task Group definition
    
t3 = EmptyOperator(task_id="end")

# Set Task Group's (tg1) dependencies
t0 >> tg1 >> t3
```

</TabItem>
</Tabs>

This image shows the resulting DAG:

![Task Group Dependencies](/img/guides/managing-dependencies_tg_dependencies_1.png)

## TaskFlow API dependencies

The [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html), available in Airflow 2.0 and later, lets you turn Python functions into Airflow tasks using the `@task` decorator. 

If your DAG has only Python functions that are all defined with the decorator, invoke Python functions to set dependencies. For example, in the following DAG there are two dependent tasks, `get_a_cat_fact` and `print_the_cat_fact`. To set the dependencies, you invoke the function `print_the_cat_fact(get_a_cat_fact())`:

<CodeBlock language="python">{dependencies_example_2_taskflow}</CodeBlock>

This image shows the resulting DAG:

![TaskFlow Dependencies](/img/guides/dependency_taskflow.png)

If your DAG has a mix of Python function tasks defined with decorators and tasks defined with traditional operators, you can set the dependencies by assigning the decorated task invocation to a variable and then defining the dependencies normally. For example, in the DAG below the `upload_data_to_s3` task is defined by the `@task` decorator and invoked with `upload_data = upload_data_to_s3(s3_bucket, test_s3_key)`. The `upload_data` variable is used in the last line to define dependencies.

```python
@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False
)
def sagemaker_model():

    @task
    def upload_data_to_s3(s3_bucket, test_s3_key):
        """
        Uploads validation data to S3 from /include/data 
        """
        s3_hook = S3Hook(aws_conn_id="aws-sagemaker")

        # Take string, upload to S3 using predefined method
        s3_hook.load_file(
            filename="include/data/test.csv", 
            key=test_s3_key, 
            bucket_name=s3_bucket, 
            replace=True
        )

    upload_data = upload_data_to_s3(s3_bucket, test_s3_key)

    predict = SageMakerTransformOperator(
        task_id="predict",
        config=transform_config,
        aws_conn_id="aws-sagemaker"
    )

    results_to_redshift = S3ToRedshiftOperator(
        task_id="save_results",
        aws_conn_id="aws-sagemaker",
        s3_bucket=s3_bucket,
        s3_key=output_s3_key,
        schema="PUBLIC",
        table="results",
        copy_options=["csv"],
    )

    upload_data >> predict >> results_to_redshift


sagemaker_model()

```

## Trigger rules

When you set dependencies between tasks, the default Airflow behavior is to run a task only when all upstream tasks have succeeded. You can use [trigger rules](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#trigger-rules) to change this default behavior.

The following options are available:

- all_success: (default) The task runs only when all upstream tasks have succeeded.
- all_failed: The task runs only when all upstream tasks are in a failed or upstream\_failed state.
- all_done: The task runs once all upstream tasks are done with their execution.
- all_skipped: The task runs only when all upstream tasks have been skipped. 
- one_failed: The task runs when at least one upstream task has failed. 
- one_success: The task runs when at least one upstream task has succeeded.
- one_done: The task runs when at least one upstream task has either succeeded or failed.
- none_failed: The task runs only when all upstream tasks have succeeded or been skipped.
- none_failed_min_one_success: The task runs only when all upstream tasks have not failed or upstream_failed, and at least one upstream task has succeeded.
- none_skipped: The task runs only when no upstream task is in a skipped state.
- always: The task runs at any time.

### Branching and trigger rules

One common scenario where you might need to implement trigger rules is if your DAG contains conditional logic such as [branching](airflow-branch-operator.md). In these cases, `one_success` might be a more appropriate rule than `all_success`.

In the following example DAG there is a simple branch with a downstream task that needs to run if either of the branches are followed. With the `all_success` rule, the `end` task never runs because all but one of the `branch` tasks is always ignored and therefore doesn't have a success state. If you change the trigger rule to `one_success`, then the `end` task can run so long as one of the branches successfully completes.

<Tabs
    defaultValue="taskflow"
    groupId= "branching-and-trigger-rules"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{dependencies_branch_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{dependencies_branch_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

This image shows the resulting DAG:

![Branch Dependencies](/img/guides/branch_2.png)
