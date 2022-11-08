---
title: "Test Airflow DAGs"
sidebar_label: "Test DAGs"
id: testing-airflow
---

<head>
  <meta name="description" content="Learn about testing Airflow DAGs and gain insight into various types of tests — validation testing, unit testing, and data and pipeline integrity testing." />
  <meta name="og:description" content="Learn about testing Airflow DAGs and gain insight into various types of tests — validation testing, unit testing, and data and pipeline integrity testing." />
</head>


Effectively testing DAGs requires an understanding of their structure and their relationship to other code and data in your environment. In this guide, you'll learn about DAG validation testing, unit testing, and data and pipeline integrity testing.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Python testing basics. See [Getting Started with Testing in Python](https://realpython.com/python-testing/).
- CI/CD for Python scripts. See [Continuous Integration with Python: An Introduction](https://realpython.com/python-continuous-integration/).

## Test runners

There are multiple test runners available for Python, including `unittest`, `pytest`, and `nose2`. Airflow doesn't require a specific test runner. This guide uses `pytest`.

## DAG validation testing

DAG validation tests are designed to ensure that your DAG objects are defined correctly, acyclic, and free of import errors. These are things that you would likely catch if you were starting with local development of your DAGs. But in cases where you may not have access to a local Airflow environment, or you want an extra layer of security, these tests can ensure that simple coding errors don't get deployed and slow development. 

DAG validation tests apply to all DAGs in your Airflow environment, so you only need to create one test suite.

To test whether your DAG can be loaded and doesn't contain syntax errors, you run the following command:

```bash
python your-dag-file.py
```

To test for import errors, run a command similar to the following example:

```python
from airflow.models import DagBag

def test_no_import_errors():
    dag_bag = DagBag()
    assert len(dag_bag.import_errors) == 0, "No Import Failures"
```

You can also use DAG validation tests to test for properties that you want to be consistent across all DAGs. For example, if all of your DAGs must include two retries for each task, run a command similar to the following example to enforce this requirement:

```python
def test_retries_present():
    dag_bag = DagBag()
    for dag in dag_bag.dags:
        retries = dag_bag.dags[dag].default_args.get('retries', [])
        error_msg = 'Retries not set to 2 for DAG {id}'.format(id=dag)
        assert retries == 2, error_msg
```

To see an example of running these tests as part of a CI/CD workflow, see the [airflow-testing-guide](https://github.com/astronomer/airflow-testing-guide)repository.

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
        self.dag = DAG('test_dag', default_args={'owner': 'airflow', 'start_date': DEFAULT_DATE})
        self.even = 10
        self.odd = 11

    def test_even(self):
        """Tests that the EvenNumberCheckOperator returns True for 10."""
        task = EvenNumberCheckOperator(my_operator_param=self.even, task_id='even', dag=self.dag)
        ti = TaskInstance(task=task, execution_date=datetime.now())
        result = task.execute(ti.get_template_context())
        assert result is True

    def test_odd(self):
        """Tests that the EvenNumberCheckOperator returns False for 11."""
        task = EvenNumberCheckOperator(my_operator_param=self.odd, task_id='odd', dag=self.dag)
        ti = TaskInstance(task=task, execution_date=datetime.now())
        result = task.execute(ti.get_template_context())
        assert result is False
```

If your DAGs contain `PythonOperators` that execute your own Python functions, it is recommended that you write unit tests for those functions as well. 

The most common way to implement unit tests in production is to automate them as part of your CI/CD process. Your CI tool executes the tests and stops the deployment process when errors occur.

### Mocking

Mocking is the imitation of an external system, dataset, or other object. For example, you might use mocking with an Airflow unit test if you are testing a connection, but don't have access to the metadata database. Mocking could also be used when you need to test an operator that executes an external service through an API endpoint, but you don't want to wait for that service to run a simple test. 

Many [Airflow tests](https://github.com/apache/airflow/tree/master/tests) use mocking. The blog [Testing and debugging Apache Airflow](https://godatadriven.com/blog/testing-and-debugging-apache-airflow/) discusses Airflow mocking and it might help you get started.

## Data integrity testing

Data integrity tests prevent data quality issues from breaking your pipelines or negatively impacting downstream systems. These tests can also ensure your DAG tasks produce the expected output when processing a given piece of data. Data integrity tests are different from code-related tests because data is not static like a DAG. 

One straightforward way to implement data integrity tests is to build them directly into your DAGs. This allows you to make use of Airflow dependencies to manage any errant data in whatever way makes sense for your organization.

There are many ways you can integrate data checks into your DAG. One method is using [Great Expectations](https://greatexpectations.io/) which is an open source Python framework for data validations. The [Great Expectations provider package](https://registry.astronomer.io/providers/great-expectations) lets you quickly integrate Great Expectations tasks into your DAGs. In the following example DAG, an Azure Data Factory pipeline generates data and then Great Expectations validates the data before sending an email.

```python
from datetime import datetime, timedelta

from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

from airflow import DAG
from airflow.providers.microsoft.azure.hooks.azure_data_factory import AzureDataFactoryHook
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook

# Get yesterday's date, in the correct format
yesterday_date = "{{ yesterday_ds_nodash }}"

# Define Great Expectations file paths
data_dir = "/usr/local/airflow/include/data/"
data_file_path = "/usr/local/airflow/include/data/"
ge_root_dir = "/usr/local/airflow/include/great_expectations"


def run_adf_pipeline(pipeline_name, date):
    """Runs an Azure Data Factory pipeline using the AzureDataFactoryHook and passes in a date parameter"""

    # Create a dictionary with date parameter
    params = {}
    params["date"] = date

    # Make connection to ADF, and run pipeline with parameter
    hook = AzureDataFactoryHook("azure_data_factory_conn")
    hook.run_pipeline(pipeline_name, parameters=params)


def get_azure_blob_files(blobname, output_filename):
    """Downloads file from Azure blob storage"""
    azure = WasbHook(wasb_conn_id="azure_blob")
    azure.get_file(output_filename, container_name="covid-data", blob_name=blobname)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "adf_great_expectations",
    start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_adf_pipeline,
        op_kwargs={"pipeline_name": "pipeline1", "date": yesterday_date},
    )

    download_data = PythonOperator(
        task_id="download_data",
        python_callable=get_azure_blob_files,
        op_kwargs={
            "blobname": "or/" + yesterday_date + ".csv",
            "output_filename": data_file_path + "or_" + yesterday_date + ".csv",
        },
    )

    ge_check = GreatExpectationsOperator(
        task_id="ge_checkpoint",
        expectation_suite_name="azure.demo",
        batch_kwargs={"path": data_file_path + "or_" + yesterday_date + ".csv", "datasource": "data__dir"},
        data_context_root_dir=ge_root_dir,
    )

    send_email = EmailOperator(
        task_id="send_email",
        to="noreply@astronomer.io",
        subject="Covid to S3 DAG",
        html_content="<p>The great expectations checks passed successfully. <p>",
    )

    run_pipeline >> download_data >> ge_check >> send_email
```

If the Great Expectations validation fails, all downstream tasks are skipped. Implementing checkpoints like this allows you to conditionally branch your pipeline to deal with data that doesn't meet your criteria, or skip all downstream tasks so problematic data won't be loaded into your data warehouse or fed to a model. For more information on conditional DAG design, see [Trigger Rules](https://airflow.apache.org/docs/apache-airflow/2.0.0/concepts.html#trigger-rules) and [Branching in Airflow](airflow-branch-operator.md).

Data integrity testing works better at scale if you design your DAGs to load or process data incrementally. To learn more about incremental loading, see [DAG Writing Best Practices in Apache Airflow](dag-best-practices.md). Processing smaller, incremental chunks of data in each DAG Run ensures that any data quality issues have a limited effect.
