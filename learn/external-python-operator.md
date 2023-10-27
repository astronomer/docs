---
title: "Run Snowpark queries with the ExternalPythonOperator in Apache Airflow"
sidebar_label: "Use the ExternalPythonOperator"
description: "Learn how to run a Snowpark query in a virtual Python environment using the ExternalPythonOperator in Airflow."
id: external-python-operator
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import external_python_operator from '!!raw-loader!../code-samples/dags/external-python-operator/external_python_operator.py';
import external_python_operator_traditional from '!!raw-loader!../code-samples/dags/external-python-operator/external_python_operator_traditional.py';

It is very common to run a task with different dependencies than your Airflow environment. Your task might need a different Python version than core Airflow, or it has packages that conflict with your other tasks. In these cases, running tasks in an isolated environment can help manage dependency conflicts and enable compatibility with your execution environments.

In this tutorial, you'll learn how to use the [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#externalpythonoperator) to run a task that leverages the [Snowpark API](https://www.snowflake.com/snowpark/) for data transformations. Snowpark allows you to run queries and transformations on your data using different programming languages, making it a flexible addition to traditional Snowflake operators. 

Snowpark requires Python 3.8, while the [Astro Runtime](https://docs.astronomer.io/astro/runtime-image-architecture) uses Python 3.9. The ExternalPythonOperator can run your Snowpark query in a Python 3.8 virtual environment, allowing you to use a different Python version for your task than in the Airflow environment. You can use these same general steps for any use case for running a task in a reusable Python virtual environment.

:::tip Other ways to learn:

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: The ExternalPythonOperator](https://academy.astronomer.io/astro-runtime-the-externalpythonoperator) module.
- Webinar: [Running Airflow Tasks in Isolated Environments](https://www.astronomer.io/events/webinars/running-airflow-tasks-in-isolated-environments/).

:::

## Time to complete

This tutorial takes approximately one hour to complete.

## Assumed knowledge

To get the most out of this tutorial, you should be familiar with:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Python virtual environments. See [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A Snowflake Enterprise account. If you don't already have an account, Snowflake has a [free Snowflake trial](https://trial.snowflake.com/?owner=SPN-PID-365384) for 30 days. 

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

## Step 2: Configure your Astro project

Now that you have your Snowflake resources configured, you can set up Airflow.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Add a new file to the root folder of your project called `snowpark-requirements.txt` and add the following text:

    ```text
    snowflake-snowpark-python[pandas]
    apache-airflow
    psycopg2-binary
    apache-airflow-providers-snowflake
    ```

    The packages in this file will be installed in your virtual environment. Your Airflow task requires the `snowflake-snowpark-python` package to run Snowpark queries in the virtual environment.  The virtual environment uses the other packages to access the Snowflake connection you defined in Airflow. If you are using a different method of connecting to Snowflake, such as a secrets manager or managing secrets locally, you can update or remove these lines.

3. Add the following to your `packages.txt` file:

    ```text
    build-essential
    ```

4. Update the `Dockerfile` of your Astro project to install `pyenv` and its requirements using Astronomer's Docker BuildKit frontend for Airflow:

    ```docker
    # syntax=quay.io/astronomer/airflow-extensions:v1

    FROM quay.io/astronomer/astro-runtime:7.2.0-base

    PYENV 3.8 snowpark snowpark-requirements.txt
    ```

    These commands install `pyenv` in your Airflow environment and create a Python 3.8 virtual environment called `snowpark` with the required packages to run Snowpark. The `pyenv` environment is initialized when you start your Airflow project and can be used by any ExternalPythonOperator tasks. 
    
    Creating a `pyenv` environment in your Airflow project requires installing multiple operating system level packages and a series of Docker commands. The open source [Astro BuildKit](https://github.com/astronomer/astro-provider-venv) simplifies this process and allows you to create a Python virtual environment with only two lines of code.

    :::note

    To modify this example for other use cases, you can update `3.8` in the Dockerfile to a different version of Python. Note that there are some limitations when using a Python version greater than the version used by Airflow. For more details, see the [project Readme](https://github.com/astronomer/astro-provider-venv#caveats).

    :::

5. Ensure [Docker BuildKit](https://docs.docker.com/build/buildkit/) is enabled. To enable BuildKit by default, you can update the parameter in Docker Desktop or modify your `/etc/docker/daemon.json` file with the following:

    ```json
    {
        "features": {
            "buildkit" : true
        }
    }
    ```

6. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

  :::info

  The build of this project's Dockerfile can take up to 20 minutes due to the `pyenv` and Python 3.8 installation. If you are an Astronomer customer and will be deploying this project to Astro, you can use a `dag-only` deploy after the initial deployment to avoid rebuilding the Dockerfile when making changes to DAGs in the project.

  :::

## Step 3: Create a connection to Snowflake

1. In the Airflow UI, go to **Admin** > **Connections** and click **+**.

2. Create a new connection named `snowflake_default` and choose the `Snowflake` connection type. Enter the following information:

    - [Schema](https://docs.snowflake.com/en/sql-reference/sql/create-schema.html): Your Snowflake schema.
    - Login: Your Snowflake login username.
    - Password: Your Snowflake password.
    - Account: Your Snowflake account in the format `xy12345`.
    - [Database](https://docs.snowflake.com/en/sql-reference/sql/create-database.html): Your Snowflake database.
    - Region: Your Snowflake region, for example `us-east-1`.

    The following example shows an Airflow Connection configuration in the Airflow UI.

    ![Snowflake connection](/img/guides/snowflake_tutorial_connection.png)

## Step 4: Create your DAG

In your Astro project `dags` folder, create a new file called `external-python-pipeline.py`. Choose between the TaskFlow API (recommended) and traditional syntax for your DAG and paste the code into your file:

<Tabs
    defaultValue="taskflow"
    groupId="step-4-create-your-dag"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

<CodeBlock language="python">{external_python_operator}</CodeBlock>

This DAG prints the context of your Airflow environment before using the `@task.external_python` decorator to run a Snowpark query in the virtual environment you created in [Step 2](#step-2-configure-your-astro-project).

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{external_python_operator_traditional}</CodeBlock>

This DAG prints the context of your Airflow environment before using the ExternalPythonOperator to run a Snowpark query in the virtual environment you created in [Step 2](#step-2-configure-your-astro-project).

</TabItem>

</Tabs>


## Step 5: Run your DAG to execute your Snowpark query in a virtual environment

Go to the Airflow UI, unpause your `py_virtual_env` DAG, and trigger it to run your Snowpark query in an isolated Python virtual environment. Open your tasks logs to see the results of your query printed:

```text
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - <snowflake.snowpark.dataframe.DataFrame object at 0x7fb86f142a90>
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - [ [34m2023-04-07 17:10:50,271 [0m] {[34mcursor.py:[0m738} INFO [0m - query: [select avg(reps_upper), avg(reps_lower) from dog_intelligence;][0m
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - [ [34m2023-04-07 17:10:50,814 [0m] { [34mcursor.py:[0m751} INFO[0m - query execution done[0m
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - [[34m2023-04-07 17:10:50,815[0m] {[34mcursor.py:[0m890} INFO[0m - Number of results in first chunk: 1[0m
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - [Row(AVG(REPS_UPPER)=Decimal('41.507353'), AVG(REPS_LOWER)=Decimal('25.588235'))]
[2023-04-07, 17:10:50 UTC] {process_utils.py:187} INFO - [[34m2023-04-07 17:10:50,827[0m] {[34msession.py:[0m373} INFO[0m - Closing session: 114491144789286[0m
```

## Other methods for running tasks in isolated environments

Airflow has several other options for running tasks in isolated environments:

- [The KubernetesPodOperator](https://docs.astronomer.io/learn/kubepod-operator). This operator is ideal for users who are running Airflow on Kubernetes and want more control over the resources and infrastructure used to run the task in addition to package management. Downsides include more complex setup and higher task latency.
- [The PythonVirtualenvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator). This operator works similarly to the ExternalPythonOperator, but it creates and destroys a new virtual environment for each task. This operator is ideal if you don't want to persist your virtual environment. Downsides include higher task latency since the environment must be created each time the task is run.
- [The ExternalBranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.ExternalBranchPythonOperator) (available in Airflow 2.7+). This operator is an extension of the ExternalPythonOperator and allows you to run a [branching](airflow-branch-operator.md) task in a virtual environment.
