---
title: "Custom hooks and operators"
sidebar_label: "Custom hooks and operators"
description: "How to correctly import custom hooks and operators."
id: airflow-importing-custom-hooks-operators
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import custom_operator_example_taskflow from '!!raw-loader!../code-samples/dags/airflow-importing-custom-hooks-operators/custom_operator_example_taskflow.py';
import custom_operator_example_traditional from '!!raw-loader!../code-samples/dags/airflow-importing-custom-hooks-operators/custom_operator_example_traditional.py';

One of the great benefits of Airflow is its vast network of provider packages that provide hooks, operators, and sensors for many common use cases. Another great benefit of Airflow is that it is highly customizable because everything is defined in Python code. If a hook, operator, or sensor you need doesn't exist in the open source, you can easily define your own. 

In this guide, you'll learn how to define your own custom Airflow operators and hooks to use in your DAGs. To explore existing hooks, operators, and sensors, visit the [Astronomer Registry](https://registry.astronomer.io/).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).
- Managing Airflow project structure. See [Managing Airflow code](managing-airflow-code.md).

## Create a custom operator

A custom operator is a Python class which can be imported into your DAG file. Like regular operators, instantiating a custom operator will create an Airflow task.

At a minimum, a custom operator must:

- Inherit from the `BaseOperator` or any other existing operator.
- Define an `.__init__()` method which runs when the DAG is parsed.
- Define an `.execute()` method which runs when a task uses this operator.

The following is an example of a custom operator called `MyOperator`:

```python
# import the operator to inherit from
from airflow.models.baseoperator import BaseOperator


# define the class inheriting from an existing operator class
class MyOperator(BaseOperator):
    """
    Simple example operator that logs one parameter and returns a string saying hi.
    :param my_parameter: (required) parameter taking any input.
    """

    # define the .__init__() method that runs when the DAG is parsed
    def __init__(self, my_parameter, *args, **kwargs):
        # initialize the parent operator
        super().__init__(*args, **kwargs)
        # assign class variables
        self.my_parameter = my_parameter

    # define the .execute() method that runs when a task uses this operator.
    # The Airflow context must always be passed to '.execute()', so make
    # sure to include the 'context' kwarg.
    def execute(self, context):
        # write to Airflow task logs
        self.log.info(self.my_parameter)
        # the return value of '.execute()' will be pushed to XCom by default
        return "hi :)"

```

If your custom operator is modifying functionality of an existing operator, your class can inherit from the operator you are building on instead of the `BaseOperator`. For more detailed instructions see [Creating a custom Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html).

## Create a custom hook

A custom hook is a Python class which can be imported into your DAG file. Like regular hooks, custom hooks can be used to create connections to external tools from within your task code. Custom hooks often contain methods that interact with an external API, which makes them better to use in custom operators than direct API calls.

At a minimum, a custom hook must:

- Inherit from the `BaseHook` or any other existing hook.
- Define an `.__init__()` method which runs when the DAG is parsed. 

Many hooks include a `.get_conn()` method wrapping around a call to the BaseHook method `.get_connection()` to retrieve information from an Airflow connection. It is common to call the `.get_conn()` method within the `.__init__()` method. The following is the minimum recommended code to start with for most custom hooks:

```python
# import the hook to inherit from
from airflow.hooks.base import BaseHook


# define the class inheriting from an existing hook class
class MyHook(BaseHook):
    """
    Interact with <external tool>.
    :param my_conn_id: ID of the connection to <external tool>
    """

    # provide the name of the parameter which receives the connection id
    conn_name_attr = "my_conn_id"
    # provide a default connection id
    default_conn_name = "my_conn_default"
    # provide the connection type
    conn_type = "general"
    # provide the name of the hook
    hook_name = "MyHook"

    # define the .__init__() method that runs when the DAG is parsed
    def __init__(
        self, my_conn_id: str = default_conn_name, *args, **kwargs
    ) -> None:
        # initialize the parent hook
        super().__init__(*args, **kwargs)
        # assign class variables
        self.my_conn_id = my_conn_id
        # (optional) call the '.get_conn()' method upon initialization
        self.get_conn()

    def get_conn(self):
        """Function that initiates a new connection to your external tool."""
        # retrieve the passed connection id
        conn_id = getattr(self, self.conn_name_attr)
        # get the connection object from the Airflow connection
        conn = self.get_connection(conn_id)

        return conn

    # add additional methods to define interactions with your external tool
```

## Import custom hooks and operators

After you've defined a custom hook or operator, you need to make it available to your DAGs. Some legacy Airflow documentation or forums may reference registering your custom operator as an Airflow plugin, but this is not necessary. To import a custom operator or hook to your DAGs, the operator or hook file needs to be in a directory that is present in your `PYTHONPATH`. See the Apache Airflow [module management documentation](https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html) for more info.

When using the [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) you can add your custom operator file to the `include` directory of your Astro project. Consider adding sub-folders to make your `include` directory easier to navigate.

```text
.
├── .astro/
├── dags/                    
│   └── example_dag.py
├── include/                 
│   └── custom_operators/
│       └── my_operator.py
│   └── custom_hooks/
│       └── my_hook.py
├── plugins/
├── tests/
├── .dockerignore
├── .env
├── .gitignore
├── .airflow_settings.yaml
├── Dockerfile
├── packages.txt     
├── README.md
└── requirements.txt    
```

For more details on why Astronomer recommends this project structure, see the [Managing Airflow Code guide](managing-airflow-code.md).

Using the project structure shown above, you can import the `MyOperator` class from the `my_operator.py` file and the `MyHook` class from the `my_hook.py` file in your DAGs with the following import statements:

```
from include.custom_operators.my_operator import MyOperator
from include.custom_hooks.my_hook import MyHook
```

## Example implementation

The following code defines the `MyBasicMathOperator` class. This operator inherits from the BaseOperator and can perform arithmetic when you provide it two numbers and an operation. This code is saved in the `include` folder in a file called `basic_math_operator.py`.

```python
from airflow.models.baseoperator import BaseOperator


class MyBasicMathOperator(BaseOperator):
    """
    Example Operator that does basic arithmetic.
    :param first_number: first number to put into an equation
    :param second_number: second number to put into an equation
    :param operation: mathematical operation to perform
    """

    # provide a list of valid operations
    valid_operations = ("+", "-", "*", "/")
    # define which fields can use Jinja templating
    template_fields = ("first_number", "second_number")

    def __init__(
        self,
        first_number: float,
        second_number: float,
        operation: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.first_number = first_number
        self.second_number = second_number
        self.operation = operation

        # raise an import error if the operation provided is not valid
        if self.operation not in self.valid_operations:
            raise ValueError(
                f"{self.operation} is not a valid operation. Choose one of {self.valid_operations}"
            )

    def execute(self, context):
        self.log.info(
            f"Equation: {self.first_number} {self.operation} {self.second_number}"
        )
        if self.operation == "+":
            res = self.first_number + self.second_number
            self.log.info(f"Result: {res}")
            return res
        if self.operation == "-":
            res = self.first_number - self.second_number
            self.log.info(f"Result: {res}")
            return res
        if self.operation == "*":
            res = self.first_number * self.second_number
            self.log.info(f"Result: {res}")
            return res
        if self.operation == "/":
            try:
                res = self.first_number / self.second_number
            except ZeroDivisionError as err:
                self.log.critical(
                    "If you have set up an equation where you are trying to divide by zero, you have done something WRONG. - Randall Munroe, 2006"
                )
                raise ZeroDivisionError

            self.log.info(f"Result: {res}")
            return res
```

In addition to the custom operator, the example DAG uses a custom hook to connect to the CatFactAPI. This hook abstracts retrieving the API URL from an [Airflow connection](connections.md) and makes several calls to the API in a loop. This code should also be placed in the `include` directory in a file called `cat_fact_hook.py`.

```python
"""This module allows you to connect to the CatFactAPI."""

from airflow.hooks.base import BaseHook
import requests as re


class CatFactHook(BaseHook):
    """
    Interact with the CatFactAPI.

    Performs a connection to the CatFactAPI and retrieves a cat fact client.

    :cat_fact_conn_id: Connection ID to retrieve the CatFactAPI url.
    """

    conn_name_attr = "cat_conn_id"
    default_conn_name = "cat_conn_default"
    conn_type = "http"
    hook_name = "CatFact"

    def __init__(
        self, cat_fact_conn_id: str = default_conn_name, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.cat_fact_conn_id = cat_fact_conn_id
        self.get_conn()

    def get_conn(self):
        """Function that initiates a new connection to the CatFactAPI."""

        # get the connection object from the Airflow connection
        conn = self.get_connection(self.cat_fact_conn_id)

        # return the host URL
        return conn.host

    def log_cat_facts(self, number_of_cat_facts_needed: int = 1):
        """Function that logs between 1 to 10 catfacts depending on its input."""
        if number_of_cat_facts_needed < 1:
            self.log.info(
                "You will need at least one catfact! Setting request number to 1."
            )
            number_of_cat_facts_needed = 1
        if number_of_cat_facts_needed > 10:
            self.log.info(
                f"{number_of_cat_facts_needed} are a bit many. Setting request number to 10."
            )
            number_of_cat_facts_needed = 10

        cat_fact_connection = self.get_conn()

        # log several cat facts using the connection retrieved
        for i in range(number_of_cat_facts_needed):
            cat_fact = re.get(cat_fact_connection).json()
            self.log.info(cat_fact["fact"])
        return f"{i} catfacts written to the logs!"

```

To use this custom hook, you need to create an Airflow connection with the connection ID `cat_fact_conn`, the connection type `HTTP`, and the Host `http://catfact.ninja/fact`.

![Cat fact connection](/img/guides/cat_fact_conn.png)

You can then import the custom operator and custom hook into your DAG. Because the custom operator has defined `first_value` and `second_value` as `template_fields`, you can pass values from other tasks to these parameters using Jinja templating.

<Tabs
    defaultValue="taskflow"
    groupId="example-implementation"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{custom_operator_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{custom_operator_example_traditional}</CodeBlock>

</TabItem>
</Tabs>


