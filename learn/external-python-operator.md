---
title: "Run Snowpark queries with the ExternalPythonOperator"
sidebar_label: "ExternalPythonOperator"
description: "Learn how to run a Snowpark query in a virtual Python environment using the ExternalPythonOperator in Airflow."
id: external-python-operator
---

It is very common in data science and data engineering use cases to need to run a task with different requirements from your Airflow environment. Your task may need a different Python version than Airflow, or require packages that conflict with core Airflow or your other tasks. In these cases, running tasks in an isolated environment can help manage dependency conflicts and enable compatibility with your execution environments.

In this tutorial, you'll learn how to use the [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#externalpythonoperator) to run a task that leverages the [Snowpark API](https://www.snowflake.com/snowpark/) for data transformations. Snowpark allows you to run queries and transformations on your data using different programming languages, making it a flexible addition to traditional Snowflake operators. Snowpark requires Python 3.8, while Airflow will be using Python 3.9. The ExternalPythonOperator will run a task in an existing Python virtual environment, allowing you to choose a different Python version for particular tasks. 

:::note

The general steps presented here could be applied to any other use case for running a task in a reusable Python virtual environment.

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Python virtual environments. See [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).

## Prerequisites

To complete this tutorial, you need:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Snowflake Enterprise account. If you don't already have an account, Snowflake has a [free Snowflake trial](https://signup.snowflake.com/) for 30 days.
- An external secrets manager of your choice (optional). For this tutorial we use [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).   

## Step 1: Set up your data stores

For this example, you will need data in a Snowflake table to query using Snowpark. If you do not already have a suitable table, run the following queries in Snowflake:

1. Create a table.

    ```sql
    CREATE TABLE dog_intelligence (
        BREED varchar(50),
        HEIGHT_LOW_INCHES INT,
        HEIGHT_HIGH_INCHES INT,
        WEIGHT_LOW_LBS INT,
        WEIGHT_HIGH_LBS INT,
        REPS_LOWER INT,
        REPS_UPPER INT
    );
    ```

2. Populate the table.

    ```sql
    INSERT INTO dog_intelligence2
        VALUES
        ('Akita', 26, 28, 80, 120, 1, 4),
        ('Great Dane', 32, 32, 120, 160, 1, 4),
        ('Weimaraner', 25, 27, 70, 85, 16, 25),
        ('Vizsla', 48, 66, 22, 25, 26, 40)
    ;
    ```

## Step 2: Create a connection to Snowflake in your secrets manager (optional)

You will need to pass Snowflake connection information to your virtual environment in order for your DAG to connect to Snowflake. If you are using an external secrets manager, add a new secret called `/airflow/connections/snowflake` with a connection string like the following:

```text
snowflake://USERNAME:PASSWORD@ACCOUNT.REGION.snowflakecomputing.com/?account=ACCOUNT&warehouse=WAREHOUSE&database=DATABASE&region=REGION
```

If you are not using an external secrets manager, you can skip this step.

## Step 3: Configure your Astro project

Now that you have your Snowflake resources configured, you can move on to setting up Airflow.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Add a new file to your project called `snowpark_requirements.txt` and add the following text:

    ```text
    snowflake-snowpark-python[pandas]
    boto3
    ```

    The packages in this file will be installed in your virtual environment. The `snowflake-snowpark-python` package is required to run Snowpark queries. The `boto3` package is used to interact with AWS Parameter Store to retrieve credentials. If you are using a different secrets manager or are managing secrets locally, you can update or remove this line.

3. Update the `Dockerfile` of your Astro project to install `pyenv` and its requirements:

    ```docker
    FROM quay.io/astronomer/astro-runtime:6.0.3

    ##### Docker Customizations below this line #####

    ## The directory where `pyenv` will be installed. You can update the path as needed
    ENV PYENV_ROOT="/home/astro/.pyenv" 
    ENV PATH=${PYENV_ROOT}/bin:${PATH}

    ## If you want to check your dependency conflicts for extra packages that you may require for your ## venv, uncomment the following two lines to install pip-tools
    # RUN pip-compile -h
    # RUN pip-compile snowpark_requirements.txt

    ## Install the required version of pyenv and create the virtual environment
    RUN curl https://pyenv.run | bash  && \
        eval "$(pyenv init -)" && \
        pyenv install 3.8.14 && \
        pyenv virtualenv 3.8.14 snowpark_env && \
        pyenv activate snowpark_env && \
        pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir -r snowpark_requirements.txt
    ```

    These commands install `pyenv` in your Airflow environment and create a Python 3.8 virtual environment called `snowpark_env` with the required packages to run Snowpark that will be used by the ExternalPythonOperator. The `pyenv` environment will be created when you start your Airflow project, and can be used by any number of ExternalPythonOperator tasks. If you use a different virtual environment package (e.g. `venv` or `conda`) you may need to update this step.

4. Add the following to your `packages.txt` file:

    ```text
    git
    make
    build-essential
    libssl-dev
    zlib1g-dev
    libbz2-dev
    libreadline-dev
    libsqlite3-dev
    wget
    curl
    llvm
    libncurses5-dev
    libncursesw5-dev
    xz-utils
    tk-dev
    libpq-dev
    krb5-config
    ```

    This installs all the needed packages to run `pyenv` in your Airflow environment.

5. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 4: Create your DAG

In your Astro project `dags` folder, create a new file called `external-python-pipeline.py`. Paste the following code into the file:

```python
from __future__ import annotations

import logging
import os
import sys
import tempfile
import time
import shutil
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

PYTHON = sys.executable

BASE_DIR = tempfile.gettempdir()

with DAG(
    'py_virtual_env',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 10, 10, tz="UTC"),
    catchup=False,
    tags=['pythonvirtualenv']
) as dag:
    
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    @task.external_python(
        task_id="external_python",
        python='/home/astro/.pyenv/versions/snowpark_env/bin/python'
    )
    def callable_external_python():
        from time import sleep
        import pkg_resources
        from snowflake.snowpark import Session

        import boto3
        import json
        
        # Retrieving connection information from the external secrets manager
        ssm = boto3.client('ssm', region_name='us-east-1')
        parameter = ssm.get_parameter(Name='/airflow/connections/snowflake', WithDecryption=True)
        conn = json.loads(parameter['Parameter']['Value'])
        
        ## Checking for the correct venv packages	
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                for i in installed_packages])
        print(installed_packages_list)

        # Defining parameters for Airflow's Snowpark connection
        connection_parameters = {
            "account": conn['extra']['account'],
            "user": conn['login'],
            "password": conn['password'],
            "role": conn['extra']['role'],
            "warehouse": conn['extra']['warehouse'],
            "database": conn['extra']['database'],
            "schema": conn['schema'],
            "region": conn['extra']['region']
        }
        # Creating a connection session between Snowpark and Airflow
        session = Session.builder.configs(connection_parameters).create()
        # Running a SQL query in Snowpark
        df = session.sql('select avg(reps_upper), avg(reps_lower) from dog_intelligence;')
        print(df)
        print(df.collect())
        # Closing the connection session
        session.close()

    task_print = print_context()
    task_external_python = callable_external_python()

    task_print >> task_external_python
```

This DAG prints the context of your Airflow environment before using the `@task.external_python` decorator to run a Snowpark query in the virtual environment you created in Step 3. 

This example pulls Snowflake connection information from AWS Parameter Store. If you are using a different secrets manager, you will need to update the following lines:

```python
import boto3
import json

ssm = boto3.client('ssm', region_name='us-east-1')
parameter = ssm.get_parameter(Name='/airflow/connections/snowflake', WithDecryption=True)
conn = json.loads(parameter['Parameter']['Value'])
```

To run the DAG without an external secrets manager, simply provide your connection information directly in the `connection_parameters` dictionary (note that this is not best practice as sensitive information will be stored in your DAG file).

Finally, if you chose to use an existing Snowflake table rather than create the one described in Step 1, you may need to update the SQL provided in this line:

```python
df = session.sql('select avg(reps_upper), avg(reps_lower) from dog_intelligence;')
```

## Step 5: Run your DAG to execute your Snowpark query in a virtual environment

Go to the Airflow UI, unpause your `py_virtual_env` DAG, and trigger it to run your Snowpark query in an isolated Python virtual environment. Go to the task logs and you should see the results of your query printed:

LOGS SCREENSHOT HERE

## Other methods for running tasks in isolated environments

Airflow has several other options for running tasks in isolated environments. Which you should choose  depends on your use case and your Airflow infrastructure.

- [The KubernetesPodOperator](https://docs.astronomer.io/learn/kubepod-operator). This operator is ideal for users who are running Airflow on Kubernetes and want more control over the resources and infrastructure used to run the task in addition to package management. Downsides include more complex setup and higher task latency.
- [The PythonVirtualenvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator). This operator works similarly to the ExternalPythonOperator, but it creates and destroys a new virtual environment for each task. This operator is ideal if you don't want to persist your virtual environment. Downsides include higher task latency since the environment must be created each time the task is run.
