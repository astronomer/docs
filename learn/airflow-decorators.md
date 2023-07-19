---
title: "Introduction to the TaskFlow API and Airflow decorators"
sidebar_label: "TaskFlow API & decorators"
description: "An overview of Airflow decorators and how they can improve the DAG authoring experience."
id: airflow-decorators
---

import CodeBlock from '@theme/CodeBlock';
import airflow_decorator_example_traditional_syntax from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorator_example_traditional_syntax.py';
import airflow_decorator_example from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorator_example.py';
import airflow_decorators_traditional_mixing from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorators_traditional_mixing.py';
import airflow_decorators_sdk_example from '!!raw-loader!../code-samples/dags/airflow-decorators/airflow_decorators_sdk_example.py';

The _TaskFlow API_ is a functional API for using decorators to define DAGs and tasks, which simplifies the process for passing data between tasks and defining dependencies. You can use TaskFlow decorator functions (for example, `@task`) to pass data between tasks by providing the output of one task as an argument to another task. Decorators are a simpler, cleaner way to define your tasks and DAGs and can be used in combination with traditional operators.

In this guide, you'll learn about the benefits of decorators and the decorators available in Airflow. You'll also review an example DAG and learn when you should use decorators and how you can combine them with traditional operators in a DAG.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## What is a decorator?

In Python, [decorators](https://realpython.com/primer-on-python-decorators/) are functions that take another function as an argument and extend the behavior of that function. For example, the `@multiply_by_100_decorator` takes any function as the `decorated_function` argument and returns the result of that function multiplied by 100. 


```python
# definition of the decorator function
def multiply_by_100_decorator(decorated_function):
    def wrapper(num1, num2):
        result = decorated_function(num1, num2) * 100
        return result

    return wrapper


# definition of the `add` function decorated with the `multiply_by_100_decorator`
@multiply_by_100_decorator
def add(num1, num2):
    return num1 + num2


# definition of the `subtract` function decorated with the `multiply_by_100_decorator`
@multiply_by_100_decorator
def subtract(num1, num2):
    return num1 - num2


# calling the decorated functions
print(add(1, 9))  # prints 1000
print(subtract(4, 2))  # prints 200
```

In the context of Airflow, decorators contain more functionality than this simple example, but the basic idea is the same: the Airflow decorator function extends the behavior of a normal Python function to turn it into an Airflow task, task group or DAG.

## When to use the TaskFlow API

The purpose of the TaskFlow API in Airflow is to simplify the DAG authoring experience by eliminating the boilerplate code required by traditional operators. The result can be cleaner DAG files that are more concise and easier to read.

In general, whether you use the TAskFlow API is a matter of your own preference and style. In most cases, a TaskFlow decorator and the corresponding traditional operator will have the same functionality. You can also [mix decorators and traditional operators](#mixing-decorators-with-traditional-operators) within a single DAG.

## How to use the TaskFlow API

The TaskFlow API allows you to write your Python tasks with decorators. It handles passing data between tasks using XCom and infers task dependencies automatically.

Using decorators to define your Python functions as tasks is easy. Let's take a before and after example. Under the **Traditional syntax** tab below, there is a basic ETL DAG with tasks to get data from an API, process the data, and store it. Click on the **Decorators** tab to see the same DAG written using Airflow decorators.

<Tabs
    defaultValue="traditional"
    groupId= "how-to-use-airflow-decorators"
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

The decorated version of the DAG eliminates the need to explicitly instantiate the PythonOperator, has much less code and is easier to read. Notice that it also doesn't require using `ti.xcom_pull` and `ti.xcom_push` to [pass data between tasks](airflow-passing-data-between-tasks.md). This is all handled by the TaskFlow API when you define your task dependencies with `store_data(process_data(extract_bitcoin_price()))`.

Here are some other things to keep in mind when using decorators:

- You must call all decorated functions in your DAG file so that Airflow can register the task or DAG. For example, `taskflow()` is called at the end of the previous example to call the DAG function. 
- When you define a task, the `task_id` defaults to the name of the function you decorated. If you want to change this behavior, you can pass a `task_id` to the decorator as shown in the `extract` task example. Similarly, other [BaseOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html#airflow.models.baseoperator.BaseOperator) task-level parameters, such as retries or pools, can be defined within the decorator:

    ```python
    @task(
        task_id="say_hello_world"
        retries=3,
        pool="my_pool",
    )
    def taskflow_func():
        retun "Hello World"

    taskflow_func()  # this creates a task with the task_id `say_hello_world`
    ```

- Override task-level parameters when you call the task by using the `.override()` method. The `()` at the end of the line calls the task with the overridden parameters applied.

    ```python
    # this creates a task with the task_id `greeting`
    taskflow_func.override(retries=5, pool="my_other_pool", task_id="greeting")()
    ```

- If you call the same task multiple times and do not override the `task_id`, Airflow creates multiple unique task IDs by appending a number to the end of the original task ID (for example, `say_hello`, `say_hello__1`, `say_hello__2`, etc). You can see the result of this in the following example:

    ```python
    # task definition
    @task
    def say_hello(dog):
        return f"Hello {dog}!"

    ### calling the task 4 times, creating 4 tasks in the DAG
    # this task will have the id `say_hello` and print "Hello Avery!"
    say_hello("Avery")
    # this task will have the id `greet_dog` and print "Hello Piglet!"
    say_hello.override(task_id="greet_dog")("Piglet")
    # this task will have the id `say_hello__1` and print "Hello Peanut!"
    say_hello("Peanut")
    # this task will have the id `say_hello__2` and print "Hello Butter!"
    say_hello("Butter")
    ```

- You can decorate a function that is imported from another file as shown in the following code snippet:

    ```python
    from include.my_file import my_function

    @task
    def taskflow_func():
        my_function()
    ```
    
    This is recommended in cases where you have lengthy Python functions since it will make your DAG file easier to read.

- You can assign the output of a called decorated task to a Python object to be passed as an argument into another decorated task. This is helpful when the output of one decorated task is needed in several downstream functions, as it makes the DAG more legible. 

    ```python
    @task 
    def get_fruit_options():
        return ["peach", "raspberry", "pineapple"]
    
    @task
    def eat_a_fruit(list):
        index = random.randint(0, len(list) - 1)
        print(f"I'm eating a {list[index]}!")

    @task 
    def gift_a_fruit(list):
        index = random.randint(0, len(list) - 1)
        print(f"I'm giving you a {list[index]}!")
    
    # you can assign the output of a decorated task to a Python object
    my_fruits = get_fruit_options()
    eat_a_fruit(my_fruits)
    gift_a_fruit(my_fruits)
    ```

View more examples on how to use Airflow task decorators in the [Astronomer webinars](https://www.astronomer.io/events/webinars/writing-functional-dags-with-decorators/) and the Apache Airflow [TaskFlow API tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html).

## Mixing TaskFlow decorators with traditional operators

If you have a DAG that uses `PythonOperator` and other operators that don't have decorators, you can easily combine decorated functions and traditional operators in the same DAG. For example, you can add an `EmailOperator` to the previous example by updating your code to the following:

<CodeBlock language="python">{airflow_decorators_traditional_mixing}</CodeBlock>

Note that when adding traditional operators, dependencies are still defined using bit-shift operators.

You can pass information between decorated tasks and traditional operators using [XCom](airflow-passing-data-between-tasks.md). See the following tabs for examples.

### TaskFlow to TaskFlow

If both tasks are defined using the TaskFlow API, you can pass information directly between them by providing the called task function as a positional argument to the downstream task. Airflow will infer the dependency between the two tasks.

```python
@task
def get_23_TF():
    return 23

@task
def plus_10_TF(x):
    return x + 10

plus_10_TF(get_23_TF())  # plus_10_TF will return 33
# or `plus_10_TF(x=get_23_TF())` if you want to use kwargs
```

### TaskFlow to traditional operator

You can access the returned value of a traditional operator using the `.output` attribute of the task object and pass it to a downstream task defined using Airflow decorators. Airflow will infer the dependency between the two tasks.

```python
def get_23_traditional():
    return 23

@task
def plus_10_TF(x):
    return x + 10

get_23_task = PythonOperator(
    task_id="get_23_task",
    python_callable=get_23_traditional
)

plus_10_TF(get_23_task.output)  # plus_10_TF will return 33
# or `plus_10_TF(x=get_23_task.output)` if you want to use kwargs
```

### Traditional operator to TaskFlow

When using the result from an upstream TaskFlow task in a traditional task you can provide the called decorated task directly to a parameter in the traditional operator. Airflow will infer the dependency between the two tasks.

```python
@task
def get_23_TF():
    return 23

def plus_10_traditional(x):
    return x + 10

plus_10_task = PythonOperator(
    task_id="plus_10_task",
    python_callable=plus_10_traditional,
    op_args=[get_23_TF()]  # note that op_args expects a list as an input
)

# plus_10_task will return 33
```

### Traditional operator to traditional operator

For the sake of completeness the below example shows how to use the output of one traditional operator in another traditional operator by accessing the `.output` attribute of the upstream task. The dependency has to be defined explicitly using bit-shift operators.

```python
def get_23_traditional():
    return 23

def plus_10_traditional(x):
    return x + 10

get_23_task = PythonOperator(
    task_id="get_23_task",
    python_callable=get_23_traditional
)

plus_10_task = PythonOperator(
    task_id="plus_10_task",
    python_callable=plus_10_traditional,
    op_args=[get_23_task.output]
)

# plus_10_task will return 33

# when only using traditional operators, define dependencies explicitly
get_23_task >> plus_10_task
```

:::info

If you want to access any XCom that is not the returned value from an operator, you can use the `xcom_pull` method inside a function, see [how to access ti / task_instance in the Airflow context](airflow-context.md#ti--task_instance) for an example. Traditional operators can also pull from XCom using [Jinja templates](templating.md) in templateable parameters.

:::

## Astro Python SDK decorators

The [Astro Python SDK](https://github.com/astronomer/astro-sdk) provides decorators and modules that let you write data pipelines in terms of data transformations rather than Airflow concepts. You can focus on defining *execution* logic in SQL and Python without having to worry about orchestration logic or the specifics of underlying databases. 

The code snippet below shows how to use the `@aql.transform` and `@aql.dataframe` decorators to create transformation tasks. 

```python
# the @aql.transform decorator allows you to run a SQL query on any number of tables
# and write the results to a new table
@aql.transform
def join_orders_customers(filtered_orders_table: Table, customers_table: Table):
    return """SELECT c.customer_id, customer_name, order_id, purchase_date, amount, type
    FROM {{filtered_orders_table}} f JOIN {{customers_table}} c
    ON f.customer_id = c.customer_id"""


# the @aql.dataframe decorator allows you to use pandas and other Python libraries
# to transform relational data and write the results to a new table
@aql.dataframe
def transform_dataframe(df: pd.DataFrame):
    purchase_dates = df.loc[:, "purchase_date"]
    print("purchase dates:", purchase_dates)
    return pd.DataFrame(purchase_dates)

# the decorated functions can be used as tasks in a DAG, writing ELT/ETL logic in 
# a functional style
join_orders_customers(filter_orders(orders_data), customers_table)
```

The Astro Python SDK offers much more functionality that greatly simplifies DAG authoring, for example a decorator to load files from object storage directly into a relational table while inferring its schema. To learn more about the Astro Python SDK, check out: 

- [Write a DAG with the Astro Python SDK tutorial](https://docs.astronomer.io/learn/astro-python-sdk)
- [The Astro Python SDK for ETL guide](https://docs.astronomer.io/learn/astro-python-sdk-etl)
- [Astro Python SDK documentation](https://astro-sdk-python.readthedocs.io/en/stable/)

## Available Airflow decorators

There are several decorators available to use with Airflow. This list provides a reference of currently available decorators:

- DAG decorator (`@dag()`), which creates a DAG
- TaskGroup decorator (`@task_group()`), which creates a [TaskGroup](task-groups.md)
- Task decorator (`@task()`), which creates a Python task
- Python Virtual Env decorator (`@task.virtualenv()`), which runs your Python task in a [virtual environment](https://www.astronomer.io/events/webinars/running-airflow-tasks-in-isolated-environments/)
- Docker decorator (`@task.docker()`), which creates a [DockerOperator](https://registry.astronomer.io/providers/apache-airflow-providers-docker/versions/latest/modules/DockerOperator) task
- [Short circuit decorator](airflow-branch-operator.md#taskshortcircuit-and-shortcircuitoperator) (`@task.short_circuit()`), which evaluates a condition and skips downstream tasks if the condition is False
- [Branch decorator](airflow-branch-operator.md#taskbranch-and-branchpythonoperator) (`@task.branch()`), which creates a branch in your DAG based on an evaluated condition
- Kubernetes pod decorator (`@task.kubernetes()`), which runs a [KubernetesPodOperator](kubepod-operator.md) task
- [Sensor decorator](what-is-a-sensor.md#sensor-decorator) (`@task.sensor()`), which turns a Python function into a sensor. This sensor was introduced in Airflow 2.5.
- [Astro Python SDK decorators](https://github.com/astronomer/astro-sdk), which simplify writing ETL/ELT DAGs

You can also [create your own custom task decorator](https://airflow.apache.org/docs/apache-airflow/stable/howto/create-custom-decorator.html).
