---
title: "Introduction to Airflow decorators"
sidebar_label: "Task decorators"
description: "An overview of Airflow decorators and how they can improve the DAG authoring experience."
id: airflow-decorators
---

import CodeBlock from '@theme/CodeBlock';
import airflow_decorator_example_traditional_syntax from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorator_example_traditional_syntax.py';
import airflow_decorator_example from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorator_example.py';
import airflow_decorators_traditional_mixing from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorators_traditional_mixing.py';
import airflow_decorators_sdk_example from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorators_sdk_example.py';

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Since Airflow 2.0, decorators have been available for some functions as an alternative DAG authoring experience to traditional operators. In Python, [decorators](https://realpython.com/primer-on-python-decorators/) are functions that take another function as an argument and extend the behavior of that function. In the context of Airflow, decorators provide a simpler, cleaner way to define your tasks and DAG. 

In this guide, you'll learn about the benefits of decorators, the decorators available in Airflow, and decorators provided in the Astronomer open source Astro Python SDK library. You'll also review examples and learn when you should use decorators and how you can combine them with traditional operators in a DAG.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## When to use decorators

The purpose of decorators in Airflow is to simplify the DAG authoring experience by eliminating the boilerplate code required by traditional operators. The result can be cleaner DAG files that are more concise and easier to read. Currently, decorators can be used for Python and SQL functions.

In general, whether to use decorators is a matter of developer preference and style. Generally, a decorator and the corresponding traditional operator will have the same functionality. One exception to this is the Astro Python SDK library of decorators (more on these below), which do not have equivalent traditional operators. You can also easily mix decorators and traditional operators within your DAG if your use case requires that.

## How to use Airflow decorators

Airflow decorators were introduced as part of the TaskFlow API, which also handles passing data between tasks using XCom and inferring task dependencies automatically. To learn more about the TaskFlow API, check out this [Astronomer webinar](https://www.astronomer.io/events/webinars/taskflow-api-airflow-2.0) or this Apache Airflow [TaskFlow API tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html#tutorial-on-the-taskflow-api). 

Using decorators to define your Python functions as tasks is easy. Let's take a before and after example. Under the **Traditional syntax** tab below, there is a basic ETL DAG with tasks to get data from an API, process the data, and store it. Click on the **Decorators** tab to see the same DAG written using Airflow decorators.

<Tabs
    defaultValue="traditional"
    groupId= "decorator-example"
    values={[
        {label: 'Traditional syntax', value: 'traditional'},
        {label: 'TaskFlow API', value: 'taskflow'},
    ]}>

<TabItem value="traditional">

<CodeBlock language="python">{airflow_decorator_example_traditional_syntax}</CodeBlock>

</TabItem>

<TabItem value="taskflow">

<CodeBlock language="python">{airflow_decorator_example}</CodeBlock>

</TabItem>
</Tabs>

The decorated version of the DAG eliminates the need to explicitly instantiate the PythonOperator, has much less code and is easier to read. Notice that it also doesn't require using `ti.xcom_pull` and `ti.xcom_push` to pass data between tasks. This is all handled by the TaskFlow API when you define your task dependencies with `store_data(process_data(extract_bitcoin_price()))`. 

Here are some other things to keep in mind when using decorators:

- For any decorated object in your DAG file, you must call them so that Airflow can register the task or DAG (e.g. `dag = taskflow()`).
- When you define a task, the `task_id` will default to the name of the function you decorated. If you want to change that, you can simply pass a `task_id` to the decorator as you did in the `extract` task above. Similarly, other task level parameters such as retries or pools can be defined within the decorator (see the example with `retries` above).
- You can decorate a function that is imported from another file with something like the following:

    ```python
    from include.my_file import my_function

    @task
    def taskflow_func():
        my_function()
    ```
    
    This is recommended in cases where you have lengthy Python functions since it will make your DAG file easier to read. 

### Mixing decorators with traditional operators

If you have a DAG that uses `PythonOperator` and other operators that don't have decorators, you can easily combine decorated functions and traditional operators in the same DAG. For example, you can add an `EmailOperator` to the previous example by updating your code to the following:

<CodeBlock language="python">{airflow_decorators_traditional_mixing}</CodeBlock>

Note that when adding traditional operators, dependencies are still defined using bitshift operators.

## Astro Python SDK decorators

The [Astro Python SDK](https://github.com/astronomer/astro-sdk) provides decorators and modules that allow data engineers to think in terms of data transformations rather than Airflow concepts when writing DAGs. The goal is to allow DAG writers to focus on defining *execution* logic without having to worry about orchestration logic.

The library contains SQL and dataframe decorators that greatly simplify your DAG code and allow you to directly define tasks without boilerplate operator code. It also allows you to transition seamlessly between SQL and Python for transformations without having to explicitly pass data between tasks or convert the results of queries to dataframes and vice versa. For a full description of functionality, check out the [Astro Python SDK documentation](https://astro-sdk-python.readthedocs.io/en/stable/).

To use the Astro Python SDK, you need to install the `astro-sdk-python` package in your Airflow environment and enable pickling (`AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True`). For more instructions, check out the [Use the Astro Python SDK tutorial](https://docs.astronomer.io/learn/astro-python-sdk).

To show the Astro Python SDK in action, we'll use a simple ETL example. We have homes data in two different CSVs that we need to aggregate, clean, transform, and append to a reporting table. Some of these tasks are better suited to SQL, and some to Python, but we can easily combine both using `astro-sdk-python` functions. The DAG looks like this:

<CodeBlock language="python">{airflow_decorators_sdk_example}</CodeBlock>

![Astro ETL](/img/guides/astro_etl_graph.png)

The general steps in the DAG are:

1. Combine data from your two source tables. You use a `transform()` function since you are running a SQL statement on tables that already exist in our database. You define the source tables with the `Table()` parameter when you call the function (`center_1=Table('ADOPTION_CENTER_1', conn_id="snowflake", schema='SANDBOX_KENTEND')`).
2. Run another `transform()` function to clean the data; you don't report on guinea pig adoptions in this example, so you'll remove them from the dataset. Each `transform` function will store results in a table in your database. You can specify an `output_table` to store the results in a specific table, or you can let the SDK create a table in a default temporary schema for you by not defining any output.
3. Transform the data by pivoting using Python. Pivoting is notoriously difficult in Snowflake, so you seamlessly switch to Pandas. In this task you specify an `output_table` that you want the results stored in.
4. Append the results to an existing reporting table using the `append` function. Because you pass the results of the previous function (`aggregated_data`) to the `append_data` parameter, the SDK infers a dependency between the tasks. You don't need to explicitly define the dependency yourself.

By defining your task dependencies when calling the functions (for example, `cleaned_data = clean_data(combined_data)`), the Astro Python SDK takes care of passing all context and metadata between the tasks. The result is a DAG where you accomplished some tricky transformations without having to write a lot of Airflow code or transition between SQL and Python.

## List of available Airflow decorators

There are a limited number of decorators available to use with Airflow, although more will be added in the future. This list provides a reference of what is currently available so you don't have to dig through source code:

- [Astro Python SDK decorators](https://github.com/astronomer/astro-sdk)
- DAG decorator (`@dag()`)
- Task decorator (`@task()`), which creates a Python task
- Python Virtual Env decorator (`@task.virtualenv()`), which runs your Python task in a virtual environment
- Docker decorator (`@task.docker()`), which creates a `DockerOperator` task
- TaskGroup decorator (`@task_group()`), which creates a TaskGroup
- [Short circuit decorator](airflow-branch-operator.md#taskshortcircuit-and-shortcircuitoperator) (`@task.short_circuit()`), which evaluates a condition and skips downstream tasks if the condition is False
- [Branch decorator](airflow-branch-operator.md#taskbranch-and-branchpythonoperator) (`@task.branch()`), which creates a branch in your DAG based on an evaluated condition
- Kubernetes pod decorator (`@task.kubernetes()`), which runs a KubernetesPodOperator task
- [Sensor decorator](what-is-a-sensor.md#sensor-decorator) (`@task.sensor()`), which turns a Python funtion into a sensor. This sensor was introduced in Airflow 2.5.

As of Airflow 2.2, you can also [create your own custom task decorator](https://airflow.apache.org/docs/apache-airflow/stable/howto/create-custom-decorator.html).
