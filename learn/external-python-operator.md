---
title: "Run Snowpark queries with the ExternalPythonOperator in Apache Airflow"
sidebar_label: "Use the ExternalPythonOperator"
description: "Learn how to run a Snowpark query in a virtual Python environment using the ExternalPythonOperator in Airflow."
id: external-python-operator
---

import CodeBlock from '@theme/CodeBlock';
import external_python_operator from '!!raw-loader!../code-samples/dags/external-python-operator/external_python_operator.py';

It is very common to run a task with different dependencies than your Airflow environment. Your task might need a different Python version than core Airflow, or it has packages that conflict with your other tasks. In these cases, running tasks in an isolated environment can help manage dependency conflicts and enable compatibility with your execution environments.

In this tutorial, you'll learn how to use the [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#externalpythonoperator) to run a task that leverages the [Snowpark API](https://www.snowflake.com/snowpark/) for data transformations. Snowpark allows you to run queries and transformations on your data using different programming languages, making it a flexible addition to traditional Snowflake operators. 

Snowpark requires Python 3.8, while [Astro runtime](https://docs.astronomer.io/astro/runtime-image-architecture) uses Python 3.9. The ExternalPythonOperator will run your Snowpark query in a Python 3.8 virtual environment, allowing you to use a different python version than Airflow. You can use these same general steps for any use case for running a task in a reusable Python virtual environment.

## Time to complete

This tutorial takes approximately one hour to complete.

## Assumed knowledge

To get the most out of this tutorial, you should be familiar with:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Python virtual environments. See [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A Snowflake Enterprise account. If you don't already have an account, Snowflake has a [free Snowflake trial](https://signup.snowflake.com/) for 30 days.
- An external secrets manager of your choice (optional). This tutorial uses [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).   

## Step 1: Set up your data stores

For this example, you will need data in a Snowflake table to query using Snowpark. To create a table, run the following queries in Snowflake:

1. Create a table:

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

2. Populate the table:

    ```sql
    INSERT INTO dog_intelligence
        VALUES
        ('Akita', 26, 28, 80, 120, 1, 4),
        ('Great Dane', 32, 32, 120, 160, 1, 4),
        ('Weimaraner', 25, 27, 70, 85, 16, 25),
        ('Vizsla', 48, 66, 22, 25, 26, 40)
    ;
    ```

## Step 2: Create a connection to Snowflake in your secrets manager (optional)

Your Python virtual environment needs access to Snowflake through a connection. If you are using an external secrets manager, add a new secret called `/airflow/connections/snowflake` with the connection information with the following JSON:

```text
{
    "conn_type": "snowflake",
    "login": "your-login",
    "password": "your-password",
    "schema": "your-schema",
    "extra": {
        "account": "<your-account>",
        "database": "<your-database>",
        "region": "<your-region>",
        "warehouse": "<your-warehouse>",
        "role": "<your-role>"
    }
}
```

If you are not using an external secrets manager, you can skip this step.

## Step 3: Configure your Astro project

Now that you have your Snowflake resources configured, you can set up Airflow.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Add a new file to the root folder of your project called `snowpark_requirements.txt` and add the following text:

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

    These commands install `pyenv` in your Airflow environment and create a Python 3.8 virtual environment called `snowpark_env` with the required packages to run Snowpark. The `pyenv` environment is initialized when you start your Airflow project and can be used by any ExternalPythonOperator tasks. If you use a different virtual environment package (such as `venv` or `conda`), you might need to update this configuration.

4. (Optional) If you set up a Snowflake connection with a secrets manager as described in [Step 2](#step-2-create-a-connection-to-snowflake-in-your-secrets-manager-optional), add a new file to the root folder of your project called `secrets-manager.env` and add environment variables that can be used to connect to your secrets manager. For example, if you use AWS parameter store, you might add the following:

    ```text
    AWS_ACCESS_KEY_ID=<your-access-key-id>
    AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    ```

    Add the `secrets-manager.env` file to your project's `.gitignore` file so sensitive credentials aren't tracked in git, and update the last two lines of your Dockerfile to the following:

    ```docker
    pip install --no-cache-dir -r snowpark_requirements.txt && \
    source secrets-manager.env
    ```

    If you are not using an external secrets manager, you can skip this step.

  :::info

  There are many ways to connect your virtual environment to your secrets manager, including passing a profile with a shared credential file or having your environment assume a role that has access to your secrets manager. The access key and secret method described here is the most straight forward when working with a local project, but might not work for production in some organizations.

  ::: 

5. Add the following to your `packages.txt` file:

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

6. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

  :::info

  The build of this project's Dockerfile can take up to 20 minutes due to the `pyenv` and Python 3.8 installation. If you are an Astronomer customer and will be deploying this project to Astro, you can use a `dag-only` deploy after the initial deployment to avoid rebuilding the Dockerfile when making changes to DAGs in the project.

  :::

## Step 4: Create your DAG

In your Astro project `dags` folder, create a new file called `external-python-pipeline.py`. Paste the following code into the file:

<CodeBlock language="python">{external_python_operator}</CodeBlock>

This DAG prints the context of your Airflow environment before using the `@task.external_python` decorator to run a Snowpark query in the virtual environment you created in [Step 3](#step-3-configure-your-astro-project). The ExternalPythonOperator task also prints a list of packages installed in the virtual environment, which can be helpful for debugging.

This example pulls Snowflake connection information from AWS Parameter Store. If you are using a different secrets manager, you will need to update the following lines:

```python
import boto3
import json

ssm = boto3.client('ssm', region_name='us-east-1')
parameter = ssm.get_parameter(Name='/airflow/connections/snowflake', WithDecryption=True)
conn = json.loads(parameter['Parameter']['Value'])
```

To run the DAG without an external secrets manager, simply provide your connection information directly in the `connection_parameters` dictionary (note that this is not best practice as sensitive information will be stored in your DAG file).

## Step 5: Run your DAG to execute your Snowpark query in a virtual environment

Go to the Airflow UI, unpause your `py_virtual_env` DAG and trigger it to run your Snowpark query in an isolated Python virtual environment. Open your tasks logs to see the list of installed packages and the results of your query printed:

```text
[2022-11-17, 18:55:56 UTC] {process_utils.py:179} INFO - Executing cmd: /home/astro/.pyenv/versions/snowpark_env/bin/python /tmp/tmd_3cp_1al/script.py /tmp/tmd_3cp_1al/script.in /tmp/tmd_3cp_1al/script.out /tmp/tmd_3cp_1al/string_args.txt
[2022-11-17, 18:55:56 UTC] {process_utils.py:183} INFO - Output:
[2022-11-17, 18:56:02 UTC] {process_utils.py:187} INFO - ['asn1crypto==1.5.1', 'boto3==1.26.10', 'botocore==1.29.10', 'certifi==2022.9.24', 'cffi==1.15.1', 'charset-normalizer==2.1.1', 'cloudpickle==2.0.0', 'cryptography==38.0.3', 'filelock==3.8.0', 'idna==3.4', 'jmespath==1.0.1', 'numpy==1.23.4', 'oscrypto==1.3.0', 'pandas==1.5.1', 'pip==22.3.1', 'pyarrow==8.0.0', 'pycparser==2.21', 'pycryptodomex==3.15.0', 'pyjwt==2.6.0', 'pyopenssl==22.1.0', 'python-dateutil==2.8.2', 'pytz==2022.6', 'requests==2.28.1', 's3transfer==0.6.0', 'setuptools==56.0.0', 'six==1.16.0', 'snowflake-connector-python==2.8.1', 'snowflake-snowpark-python==1.0.0', 'typing-extensions==4.4.0', 'urllib3==1.26.12', 'wheel==0.38.4']
[2022-11-17, 18:56:02 UTC] {process_utils.py:187} INFO - <snowflake.snowpark.dataframe.DataFrame object at 0x7f69710e1d60>
[2022-11-17, 18:56:02 UTC] {process_utils.py:187} INFO - [Row(AVG(REPS_UPPER)=Decimal('41.507353'), AVG(REPS_LOWER)=Decimal('25.588235'))]
[2022-11-17, 18:56:02 UTC] {python.py:177} INFO - Done. Returned value was: None
[2022-11-17, 18:56:02 UTC] {taskinstance.py:1401} INFO - Marking task as SUCCESS. dag_id=py_virtual_env, task_id=external_python, execution_date=20221117T185554, start_date=20221117T185555, end_date=20221117T185602
```

## Other methods for running tasks in isolated environments

Airflow has several other options for running tasks in isolated environments:

- [The KubernetesPodOperator](https://docs.astronomer.io/learn/kubepod-operator). This operator is ideal for users who are running Airflow on Kubernetes and want more control over the resources and infrastructure used to run the task in addition to package management. Downsides include more complex setup and higher task latency.
- [The PythonVirtualenvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator). This operator works similarly to the ExternalPythonOperator, but it creates and destroys a new virtual environment for each task. This operator is ideal if you don't want to persist your virtual environment. Downsides include higher task latency since the environment must be created each time the task is run.
