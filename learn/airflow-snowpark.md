---
title: "Orchestrate Snowpark Machine Learning Workflows with Apache Airflow"
sidebar_label: "Snowpark Tutorial"
description: "Learn how to integrate Snowpark and Airflow."
id: airflow-snowpark
sidebar_custom_props: { icon: 'img/integrations/snowflake.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import airflow_with_snowpark_tutorial from '!!raw-loader!../code-samples/dags/airflow-snowpark/airflow_with_snowpark_tutorial.py';

[Snowpark](https://www.snowflake.com/en/data-cloud/snowpark/) is a framework containing runtimes and libraries to run non-SQL code in [Snowflake](https://www.snowflake.com/en/). Snowpark comes with a [comprehensive machine learning library](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index) optimized for Snowflake. 

In this tutorial, you'll learn how to: 

- Create a [custom XCom backend](custom-xcom-backends-tutorial.md) in Snowflake.
- Create and use a model registry in Snowflake.
- Use Airflow decorators to run code in Snowpark, both in a pre-built and custom virtual environment.
- Run a [Logistic Regression model](https://mlu-explain.github.io/logistic-regression/) on a synthetic dataset describing skiers to predict their afternoon beverage choice.

:::caution

The provider used in this tutorial is currently in beta and its contents as well as the decorators used are subject to change. After the official release, this tutorial will be updated.

:::

![A plot showing a confusion matrix and ROC curve with a high AUC for hot_chocolate, a medium AUC for snow_mocha and tea and low predictive power for wine and coffee.](/img/tutorials/airflow-snowpark_plot_metrics.png)

## Why use Airflow with Snowpark?

Snowpark allows you to use Python to perform transformations and machine learning operations on data stored in Snowflake.

Integrating Snowpark with Airflow offers the benefits of:

- Running machine learning models directly in Snowflake, without having to move data out of your Snowflake database.
- Express data transformations in Snowflake in Python instead of SQL.
- Store and version your machine learning models in a model registry inside Snowflake.
- Use Snowpark's compute resources instead of the resources of your Airflow cluster for machine learning.

Additionally, this tutorial shows how to use Snowflake as a custom XCom backend. This is especially useful for organizations with strict compliance requirements who want to keep all their data in Snowflake but still leverage [Airflow XCom](airflow-passing-data-between-tasks.md) to pass data between tasks.

## Time to complete

This tutorial takes approximately 45 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Snowflake and Snowpark. See [Introduction to Snowflake](https://docs.snowflake.com/en/user-guide-intro.html) and the [Snowpark API documentation](https://docs.snowflake.com/en/developer-guide/snowpark/index).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).
- Setup/ teardown tasks in Airflow. See [Use setup and teardown tasks in Airflow](airflow-setup-teardown.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Snowflake account. A [30-day free trial](https://signup.snowflake.com/) is available. You will need to have at least one database and one schema created to store the data and models used in this tutorial.

- Optional. This tutorial includes instructions on how to use the Snowflake [custom XCom backend](custom-xcom-backends-tutorial.md) included in the provider. If you want to this custom XCom backend you will need to either:
    - Use a Snowflake account with `ACCOUNTADMIN` privileges. In this case the Snowflake custom XCom backend is created and cleaned up by the [setup/ teardown](airflow-setup-teardown.md) tasks (`create_snowflake_objects` and `cleanup_xcom_table`) at the beginning and end of the tutorial DAG. The free trial account does have the required privileges.
    - Ask your Snowflake administrator to create the following for you:
        - A database called `SNOWPARK_XCOM_DB`.
        - A schema called `SNOWPARK_XCOM_SCHEMA`.
        - A table called `XCOM_TABLE`.
        - A stage called `XCOM_STAGE`.

:::info

The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-snowpark-tutorial). 

:::

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Download the `whl` file for the Astro Snowflake provider beta version from the [Astronomer Github repository](https://github.com/astronomer/learn-tutorials-data/blob/main/wheel_files/astro_provider_snowflake-0.0.0-py3-none-any.whl) and save it in your Astro project's `include` directory.

3. Create a new file in your Astro project's root directory called `requirements-snowpark.txt`. This file contains all Python packages that you will install in your reuseable Snowpark environment.

    ```text
    psycopg2-binary
    snowflake_snowpark_python[pandas]==1.5.1
    virtualenv
    /tmp/astro_provider_snowflake-0.0.0-py3-none-any.whl
    ```

4. Change the content of the `Dockerfile` of your Astro project to the following, importing the `whl` file and creating a virtual environment using the [Astro venv buildkit](https://github.com/astronomer/astro-provider-venv), in which the requirements added in the previous step will be installed.

    ```dockerfile
    # syntax=quay.io/astronomer/airflow-extensions:latest

    FROM quay.io/astronomer/astro-runtime:9.1.0-python-3.9-base

    # Copy the whl file to the image
    COPY include/astro_provider_snowflake-0.0.0-py3-none-any.whl /tmp

    # Create the virtual environment
    PYENV 3.8 snowpark requirements-snowpark.txt

    # Install packages into the virtual environment
    COPY requirements-snowpark.txt /tmp
    RUN python3.8 -m pip install -r /tmp/requirements-snowpark.txt
    ```

5. Add the following package to your `packages.txt` file:

    ```text
    build-essential
    ```

6. Add the following packages to your `requirements.txt` file. The Astro Snowflake provider is installed from the `whl` file.

    ```text
    apache-airflow-providers-snowflake==4.1.0
    snowflake-snowpark-python[pandas]==1.5.1
    snowflake-ml-python==1.0.7
    matplotlib==3.7.3
    /tmp/astro_provider_snowflake-0.0.0-py3-none-any.whl
    ```

:::caution

The Astro Snowflake provider is currently in beta. Classes from this provider might be subject to change and will be included in the [Snowflake provider](https://registry.astronomer.io/providers/apache-airflow-providers-snowflake/versions/latest) in a future release. 

:::

7. To create an [Airflow connection](connections.md) to Snowflake and [allow serialization of Astro Python SDK objects](https://astro-sdk-python.readthedocs.io/en/stable/guides/xcom_backend.html#airflow-s-xcom-backend), add the following to your `.env` file. Make sure to enter your own Snowflake credentials as well as the name of an existing database and schema.

    ```text
    AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES=airflow\.* astro\.*
    AIRFLOW__CORE__XCOM_SNOWFLAKE_CONN_NAME='snowflake_default'
    AIRFLOW_CONN_SNOWFLAKE_DEFAULT='{
        "conn_type": "snowflake",
        "login": "<username>",
        "password": "<password>",
        "schema": "MY_SKI_DATA_SCHEMA",
        "extra":
            {
                "account": "<account>",
                "warehouse": "<warehouse>",
                "database": "MY_SKI_DATA_DATABASE",
                "region": "<region>",
                "role": "<role>",
                "authenticator": "snowflake",
                "session_parameters": null,
                "application": "AIRFLOW"
            }
        }'
    ```

8. Optional. If you want to use a Snowflake custom XCom backend, add the following additional variables to your `.env`. Replace the values with the name of your own database, schema, table, and stage if you are not using the suggested values.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND='astronomer.providers.snowflake.xcom_backends.snowflake.SnowflakeXComBackend'
    AIRFLOW__CORE__XCOM_SNOWFLAKE_TABLE='SNOWPARK_XCOM_DB.SNOWPARK_XCOM_SCHEMA.XCOM_TABLE'
    AIRFLOW__CORE__XCOM_SNOWFLAKE_STAGE='SNOWPARK_XCOM_DB.SNOWPARK_XCOM_SCHEMA.XCOM_STAGE'
    ```

## Step 2: Add your data

The DAG in this tutorial runs a classification model on synthetic data to predict which afternoon beverage a skier will choose based on attributes like ski color, ski resort, and amount of new snow. The data is generated using [this script](https://github.com/astronomer/airflow-snowpark-tutorial/blob/main/include/data/create_ski_dataset.py). 

1. Create a new directory in your Astro project's `include` directory called `data`.

2. Download the dataset from [Astronomer's GitHub](https://github.com/astronomer/learn-tutorials-data/blob/main/ski_dataset.csv) and save it in `include/data`.

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `airflow_with_snowpark_tutorial.py`.

2. Copy the following code into the file. Make sure to provide your Snowflake database and schema names to `MY_SNOWFLAKE_DATABASE` and `MY_SNOWFLAKE_SCHEMA`. 

    <CodeBlock language="python">{airflow_with_snowpark_tutorial}</CodeBlock>

    This DAG consists of eight tasks in a simple ML orchestration pipeline.

    - Optional. `create_snowflake_objects`: Creates the Snowflake objects required for the Snowflake custom XCom backend. This task uses the `@task.snowflake_python` decorator to run code within Snowpark, automatically instantiating a Snowpark session called `snowpark_session` from the connection ID provided to the `snowflake_conn_id` parameter. This task is a [setup task](airflow-setup-teardown.md) and will only be shown in the DAG graph if you set `SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND` to `True`. See also Step 3.3.

    - `load_file`: Loads the data from the `ski_dataset.csv` file into the Snowflake table `MY_SNOWFLAKE_TABLE` using the [load_file operator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/load_file.html) from the Astro Python SDK. 

    - `create_model_registry`: Creates a model registry in Snowpark using the [Snowpark ML package](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index). Since the task is defined using the `@task.snowflake_python` decorator, the snowpark session is automatically instantiated from provided connection ID.

    - `transform_table_step_one`: Transforms the data in the Snowflake table using Snowpark syntax to filter to only include rows of skiers that ordered the beverages we are interested in. Computation of this task runs within Snowpark. The resulting table is written to [XCom](airflow-passing-data-between-tasks.md) as a pandas DataFrame. 

    - `transform_table_step_two`: Transforms the pandas dataframe created by the upstream task to filter only for serious skiers (those who skied at least one hour that day).
    This task uses the `@task.snowpark_ext_python` decorator, running the code in the Snowpark virtual environment created in Step 1. Which virtual environment to run a task in is determined by the binary provided to the `python` parameter of the decorator. The `@task.snowpark_ext_python` decorator works analogously to the [@task.external_python decorator](external-python-operator.md) with the difference being that the code is executed within Snowpark's compute.

    - `train_beverage_classifier`: Trains a [Snowpark Logistic Regression model](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/modeling/snowflake.ml.modeling.linear_model.LogisticRegression) on the dataset, saves the model to the model registry and creates predictions from a test dataset. This task uses the `@task.snowpark_virtualenv` decorator to run the code in a newly created virtual environment within Snowpark's compute. The packages to be installed within the virtual environment are specified to the `requirements` parameter of the decorator. The model predictions are saved to XCom as a pandas DataFrame.

    - `plot_metrics`: Creates a plot of the model performance metrics and saves it to the `include` directory. This task runs in the Airflow environment using the `@task` decorator.

    - Optional. `cleanup_xcom_table`: Cleans up the Snowflake custom XCom backend by dropping the `XCOM_TABLE` and `XCOM_STAGE`. This task is a [teardown task](airflow-setup-teardown.md) and will only be shown in the DAG graph if you set `SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND` to `True`. See also Step 3.3.

3. Optional. This DAG has two optional features you can enable.

    - If you want to use [setup/ teardown tasks](airflow-setup-teardown.md) to create and clean up a Snowflake custom XCom backend for this DAG, set `SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND` to `True`. This will add the `create_snowflake_objects` and `cleanup_xcom_table` tasks to your DAG and create a setup/ teardown workflow.  Note that your Snowflake account needs to have `ACCOUNTADMIN` privileges to perform the operations in the `create_snowflake_objects` task.

    - If you want to use a [**Snowpark-optimized warehouse**](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized) for model training set the `USE_SNOWPARK_WH` variable to `True` and provide your warehouse names to `MY_SNOWPARK_WAREHOUSE` and `MY_SNOWFLAKE_REGULAR_WAREHOUSE`. The `MY_SNOWPARK_WAREHOUSE` warehouse will be created by the `create_snowflake_objects` task if it is enabled, otherwise you will need to create the warehouse manually before running the DAG.

:::info

While this tutorial DAG uses a small dataset where model training can be accomplished using the standard Snowflake warehouse, Astronomer recommends to use a Snowpark warehouse for model training in production.

:::

## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start up Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `airflow_with_snowpark_tutorial` DAG by clicking the play button.

<Tabs
    defaultValue="standard"
    groupId="step-4-run-your-dag"
    values={[
        {label: 'Basic DAG', value: 'standard'},
        {label: 'DAG with setup/ teardown enabled', value: 'setup-teardown'},
    ]}>
<TabItem value="standard">

![Screenshot of the Airflow UI showing the `airflow_with_snowpark_tutorial` DAG having completed successfully in the Grid view with the Graph tab selected.](/img/tutorials/airflow-snowpark_dag_graph_basic.png)

</TabItem>
<TabItem value="setup-teardown">

![Screenshot of the Airflow UI showing the `airflow_with_snowpark_tutorial` DAG having completed successfully in the Grid view with the Graph tab selected. This screenshot shows the version of the DAG where SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND is set to true, creating an additional setup/ teardown workflow.](/img/tutorials/airflow-snowpark_dag_graph.png)

</TabItem>
</Tabs>

3. In the Snowflake UI, view the model registry to see the model that was created by the DAG. In a production context, you could pull a specific model from the registry to run predictions on new data.

    ![Screenshot of the Snowflake UI showing the model registry containing one model.](/img/tutorials/airflow-snowpark_model_registry.png)

4. Navigate to your `include` directory to view the `metrics.png` image that contains the model performance metrics shown at the start of this tutorial.

## Conclusion

Congratulations! You trained a classification model in Snowpark using Airflow. This pipeline is meant as a simple example showcasing the three main options to run code in Snowpark using Airflow decorators:

- `@task.snowpark_python` runs your code in a standard Snowpark environment. Use this decorator if you need to run code in Snowpark that does not require any additional packages, which are not preinstalled in a standard Snowpark environment. The corresponding traditional operator is the SnowparkPythonOperator.
- `@task.snowpark_ext_python` runs your code in a pre-existing virtual environment within Snowpark. Use this decorator when you want to reuse virtual environments in different tasks in the same Airflow instances, or your virtual environment takes a long time to be built. The corresponding traditional operator is the SnowparkExternalPythonOperator.
- `@task.snowpark_virtualenv` runs your code in a virtual environment within Snowpark that is created at runtime for that specific task. Use this decorator when you want to tailor a virtual environment to a task and don't need to reuse it. The corresponding traditional operator is the SnowparkVirtualenvOperator.