---
title: "Test Airflow DAGs"
sidebar_label: "Test DAGs"
id: testing-airflow
---

<head>
  <meta name="description" content="Learn about testing Airflow DAGs and gain insight into various types of tests — validation testing, unit testing, and data and pipeline integrity testing." />
  <meta name="og:description" content="Learn about testing Airflow DAGs and gain insight into various types of tests — validation testing, unit testing, and data and pipeline integrity testing." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Effectively testing DAGs requires an understanding of their structure and their relationship to other code and data in your environment. In this guide, you'll learn about various types of DAG validation testing, unit testing, and where to find further information on data quality checks.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Webinar: [How to easily test your Airflow DAGs with the new dag.test() function](https://www.astronomer.io/events/webinars/how-to-easily-test-your-airflow-dags-with-the-new-dag-test-function/).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Python testing basics. See [Getting Started with Testing in Python](https://realpython.com/python-testing/).
- At least one Python test runner. This guide mostly uses [`pytest`](https://docs.pytest.org/en/stable/index.html), but you can use others including [`nose2`](https://docs.nose2.io/en/latest/getting_started.html) and [`unittest`](https://docs.python.org/3/library/unittest.html).
- CI/CD for Python scripts. See [Continuous Integration with Python: An Introduction](https://realpython.com/python-continuous-integration/).
- Basic Airflow and [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) concepts. See [Get started with Airflow](get-started-with-airflow.md).

## Write DAG validation tests

DAG validation tests ensure that your DAGs fulfill a list of criteria. Using validation tests can help you:

- Develop DAGs without access to a local Airflow environment.
- Ensure that custom DAG requirements are systematically checked and fulfilled.
- Test DAGs automatically in a CI/CD pipeline.
- Enable power users to test DAGs from the CLI.

At a minimum, you should run DAG validation tests to check for [import errors](#prevent-import-errors). Additional tests can check things like custom logic, ensuring that `catchup` is set to False for every DAG in your Airflow instance, or making sure only `tags` from a defined list are used in the DAGs.

DAG validation tests apply to all DAGs in your Airflow environment, so you only need to create one test suite.

### Common DAG validation tests

This section covers the most common types of DAG validation tests with full code examples.

#### Check for import errors

The most common DAG validation test is to check for import errors. Checking for import errors through a validation test is faster than starting your Airflow environment and checking for errors in the Airflow UI. In the following test, `get_import_errors` checks the `.import_errors` attribute of the current [`DagBag`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dagbag/index.html#).

```python
import os
import pytest
from airflow.models import DagBag


def get_import_errors():
    """
    Generate a tuple for import errors in the dag bag
    """

    dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    # prepend "(None,None)" to ensure that a test object is always created even if it's a no op.
    return [(None, None)] + [
        (strip_path_prefix(k), v.strip()) for k, v in dag_bag.import_errors.items()
    ]


@pytest.mark.parametrize(
    "rel_path,rv", get_import_errors(), ids=[x[0] for x in get_import_errors()]
)
def test_file_imports(rel_path, rv):
    """Test for import errors on a file"""
    if rel_path and rv:
        raise Exception(f"{rel_path} failed to import with message \n {rv}")
```

#### Check for custom code requirements

Airflow DAGs support many types of custom plugins and code. It is common for data engineering teams to define best practices and custom rules around how their DAGs should be written and create DAG validation tests to ensure those standards are met.

The code snippet below includes a test which checks that all DAGs have their `tags` parameter set to one or more of the `APPROVED_TAGS`.

```python
import os
import pytest
from airflow.models import DagBag


def get_dags():
    """
    Generate a tuple of dag_id, <DAG objects> in the DagBag
    """

    dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


APPROVED_TAGS = {"customer_success", "op_analytics", "product"}


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    """
    test if a DAG is tagged and if those TAGs are in the approved list
    """
    assert dag.tags, f"{dag_id} in {fileloc} has no tags"
    if APPROVED_TAGS:
        assert not set(dag.tags) - APPROVED_TAGS
```

:::tip

You can view the attributes and methods available for the `dag` model in the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/DAG).

:::

You can also set requirements at the task level by accessing the `tasks` attribute within the `dag` model, which contains a list of all task objects of a DAG. The test below checks that all DAGs contain at least one task and all tasks use `trigger_rule="all_success"`.

```python
@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    """
    test if all DAGs contain a task and all tasks use the trigger_rule all_success
    """
    assert dag.tasks, f"{dag_id} in {fileloc} has no tasks"
    for task in dag.tasks:
        t_rule = task.trigger_rule
        assert (
            t_rule == "all_success"
        ), f"{task} in {dag_id} has the trigger rule {t_rule}"
```

## Implement DAG validation tests

Airflow offers different ways to run DAG validation tests using any Python test runner. This section gives an overview of the most common implementation methods. If you are new to testing Airflow DAGs, you can quickly get started by using Astro CLI commands.



### Airflow CLI 

The Airflow CLI offers two commands related to local testing:

- [`airflow dags test`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#test): Given a DAG ID and execution date, this command writes the results of a single DAG run to the metadata database. This command is useful for testing full DAGs by creating manual DAG runs from the command line.
- [`airflow tasks test`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#test_repeat1): This command tests one specific task instance without checking for dependencies or recording the outcome in the metadata database.

With the Astro CLI, you can run all Airflow CLI commands using [`astro dev run`](https://docs.astronomer.io/astro/cli/astro-dev-run). For example, to run `airflow dags test` on the DAG `my_dag` for the execution date of `2023-01-29` run:

```sh
astro dev run dags test my_dag '2023-01-29'
```

### The Astro CLI

The Astro CLI includes many commands to help simplify many of these common testing procedures. For more details, please visit the dedicated page: [Test your Astro project locally](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally).

### Test DAGs in a CI/CD pipeline

You can use CI/CD tools to test and deploy your Airflow code. For more information on how to do so, please visit our dedicated page: [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd).

## Add test data or files for local testing

Use the `include` folder of your Astro project to store files for testing locally, such as test data or a dbt project file. The files in your `include` folder are included in your deploys to Astro, but they are not parsed by Airflow. Therefore, you don't need to specify them in `.airflowignore` to prevent parsing. 

If you're running Airflow locally, apply your changes by refreshing the Airflow UI.

## Debug interactively with dag.test()

Airflow 2.5.0 introduced the `dag.test()` method which allows you to run all tasks in a DAG within a single serialized Python process without running the Airflow scheduler. The `dag.test()` method allows for faster iteration and use of IDE debugging tools when developing DAGs.

This functionality replaces the deprecated DebugExecutor. Learn more in the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html).

### Prerequisites

Ensure that your testing environment has:

- [Airflow 2.5.0](https://airflow.apache.org/docs/apache-airflow/stable/start.html) or later. You can check your version by running `airflow version`.
- All provider packages that your DAG uses.
- An initialized [Airflow metadata database](airflow-database.md), if your DAG uses elements of the metadata database like XCom. The Airflow metadata database is created when Airflow is first run in an environment. You can check that it exists with `airflow db check` and initialize a new database with `airflow db migrate` (`airflow db init` in Airflow versions pre-2.7).

You may wish to install these requirements and test your DAGs in a [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid dependency conflicts in your local environment.

### Setup

To use `dag.test()`, you only need to add a few lines of code to the end of your DAG file. If you are using a traditional DAG context, call `dag.test()` after your DAG declaration. If you are using the `@dag` decorator, assign your DAG function to a new object and call the method on that object. 

<Tabs
    defaultValue="traditional"
    groupId="debug-interactively-with-dagtest"
    values={[
        {label: 'Traditional DAG context', value: 'traditional'},
        {label: '@dag decorator', value: 'decorator'},
    ]}>
<TabItem value="traditional">

```python {14-15}
from airflow import DAG
from pendulum import datetime
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="simple_classic_dag",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:  # assigning the context to an object is mandatory for using dag.test()

    t1 = EmptyOperator(task_id="t1")

if __name__ == "__main__":
    dag.test()
```

</TabItem>

<TabItem value="decorator">

```python {18-19}
from airflow.decorators import dag
from pendulum import datetime
from airflow.operators.empty import EmptyOperator


@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
)
def my_dag():

    t1 = EmptyOperator(task_id="t1")


dag_object = my_dag()

if __name__ == "__main__":
    dag_object.test()
```

</TabItem>

</Tabs>

You can run the `.test()` method with popular debugging tools such as:

- [VSCode](https://code.visualstudio.com/docs/editor/debugging).
- [PyCharm](https://www.jetbrains.com/help/pycharm/debugging-your-first-python-application.html).
- Tools like [The Python Debugger](https://docs.python.org/3/library/pdb.html) and the built-in [`breakpoint()`](https://docs.python.org/3/library/functions.html#breakpoint) function. These allow you to run `dag.test()` from the command line by running `python <path-to-dag-file>`.

### Use `dag.test()` with the Astro CLI

If you use the Astro CLI exclusively and do not have the `airflow` package installed locally, you can still debug using `dag.test()` by running `astro dev start`, entering the scheduler container with `astro dev bash -s`, and executing `python <path-to-dag-file>` from within the Docker container. Unlike using the base `airflow` package, this testing method requires starting up a complete Airflow environment. 

### Use variables and connections in dag.test()

To debug your DAGs in a more realistic environment, you can pass the following Airflow environment configurations to `dag.test()`:

- `execution_date` passed as a `pendulum.datetime` object.
- [Airflow connections](connections.md) passed as a `.yaml` file.
- Airflow variables passed as a `.yaml` file.
- DAG configuration passed as a dictionary.

This is useful for testing your DAG for different dates or with different connections and configurations. The following code snippet shows the syntax for passing various parameters to `dag.test()`:

```python
from pendulum import datetime 

if __name__ == "__main__":
    conn_path = "connections.yaml"
    variables_path = "variables.yaml"
    my_conf_var = 23

    dag.test(
        execution_date=datetime(2023, 1, 29),
        conn_file_path=conn_path,
        variable_file_path=variables_path,
        run_conf={"my_conf_var": my_conf_var},
    )
```

The `connections.yaml` file should list connections with their properties as shown in the following example:

```yaml
my_aws_conn:
  conn_type: amazon
  login: <your-AWS-key>
  password: <your-AWS-secret>
  conn_id: my_aws_conn
```

Variables in a `variables.yaml` need to be listed with their `key` and `value`:

```yaml
my_variable:
  key: my_variable
  value: 42
```

## Unit testing

[Unit testing](https://en.wikipedia.org/wiki/Unit_testing) is a software testing method where small chunks of source code are tested individually to ensure they function correctly. The objective is to isolate testable logic inside of small, well-named functions. For example:

```python
def test_function_returns_5():
    assert my_function(input) == 5
```

In the context of Airflow, you can write unit tests for any part of your DAG, but they are most frequently applied to hooks and operators. All Airflow hooks, operators, and provider packages must pass unit testing before code can be merged into the project. For an example of unit testing, see [AWS `S3Hook`](https://registry.astronomer.io/providers/amazon/modules/s3hook) and the associated [unit tests](https://github.com/apache/airflow/blob/main/tests/providers/amazon/aws/hooks/test_s3.py). 

If you are using custom hooks or operators, Astronomer recommends using unit tests to check the logic and functionality. In the following example, a custom operator checks if a number is even:

```python
from airflow.models import BaseOperator


class EvenNumberCheckOperator(BaseOperator):
    def __init__(self, my_operator_param, *args, **kwargs):
        self.operator_param = my_operator_param
        super().__init__(*args, **kwargs)

    def execute(self, context):
        if self.operator_param % 2:
            return True
        else:
            return False

```

You then write a `test_evencheckoperator.py` file with unit tests similar to the following example:

```python
import unittest
from datetime import datetime
from airflow import DAG
from airflow.models import TaskInstance

DEFAULT_DATE = datetime(2021, 1, 1)


class EvenNumberCheckOperator(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dag = DAG(
            "test_dag", default_args={"owner": "airflow", "start_date": DEFAULT_DATE}
        )
        self.even = 10
        self.odd = 11

    def test_even(self):
        """Tests that the EvenNumberCheckOperator returns True for 10."""
        task = EvenNumberCheckOperator(
            my_operator_param=self.even, task_id="even", dag=self.dag
        )
        ti = TaskInstance(task=task, execution_date=datetime.now())
        result = task.execute(ti.get_template_context())
        assert result is True

    def test_odd(self):
        """Tests that the EvenNumberCheckOperator returns False for 11."""
        task = EvenNumberCheckOperator(
            my_operator_param=self.odd, task_id="odd", dag=self.dag
        )
        ti = TaskInstance(task=task, execution_date=datetime.now())
        result = task.execute(ti.get_template_context())
        assert result is False

```

If your DAGs contain `PythonOperators` that execute your own Python functions, it is recommended that you write unit tests for those functions as well. 

The most common way to implement unit tests in production is to automate them as part of your CI/CD process. Your CI tool executes the tests and stops the deployment process when errors occur.

### Mocking

Mocking is the imitation of an external system, dataset, or other object. For example, you might use mocking with an Airflow unit test if you are testing a connection, but don't have access to the metadata database. Mocking could also be used when you need to test an operator that executes an external service through an API endpoint, but you don't want to wait for that service to run a simple test. 

Many [Airflow tests](https://github.com/apache/airflow/tree/master/tests) use mocking. The blog [Testing and debugging Apache Airflow](https://godatadriven.com/blog/testing-and-debugging-apache-airflow/) discusses Airflow mocking and it might help you get started.

## Data quality checks

Testing your DAG ensures that your code fulfills your requirements. But even if your code is perfect, data quality issues can break or negatively affect your pipelines. Airflow, being at the center of the modern data engineering stack, is the ideal tool for checking data quality.

Data quality checks differ from code-related testing because the data is not static like your DAG code. It is best practice to incorporate data quality checks into your DAGs and use [Airflow dependencies](managing-dependencies.md) and [branching](airflow-branch-operator.md) to handle what should happen in the event of a data quality issue, from halting the pipeline to [sending notifications](error-notifications-in-airflow.md) to data quality stakeholders.

There are many ways you can integrate data quality checks into your DAG:

- [SQL check operators](airflow-sql-data-quality.md): Airflow-native operators that run highly customizable data quality checks on a wide variety of relational databases.
- [Great Expectations](airflow-great-expectations.md): A data quality testing suite with an [Airflow provider](https://registry.astronomer.io/providers/great-expectations) offering the ability to define data quality checks in JSON to run on relational databases, Spark and pandas DataFrames.
- [Soda Core](https://docs.astronomer.io/learn/soda-data-quality): A framework to check data quality using YAML configuration to define data quality checks to run on relational databases and Spark dataframes.

Data quality checks work better at scale if you design your DAGs to load or process data incrementally. To learn more about incremental loading, see [DAG Writing Best Practices in Apache Airflow](dag-best-practices.md). Processing smaller, incremental chunks of data in each DAG Run ensures that any data quality issues have a limited effect.

Learn more about how to approach data quality within Airflow: 

- [Data quality and Airflow guide](data-quality.md)
- [How to Keep Data Quality in Check with Airflow](https://www.astronomer.io/blog/how-to-keep-data-quality-in-check-with-airflow/)
- [Get Improved Data Quality Checks in Airflow with the Updated Great Expectations Operator](https://www.astronomer.io/blog/improved-data-quality-checks-in-airflow-with-great-expectations-operator/)
