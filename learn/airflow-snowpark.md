---
title: "Orchestrate Machine Learning in Snowpark with Apache Airflow"
sidebar_label: "Snowpark"
description: "Learn how to integrate Snowpark and Airflow."
id: airflow-weaviate
sidebar_custom_props: { icon: 'img/integrations/snowflake.png' }
---

import CodeBlock from '@theme/CodeBlock';
import airflow_with_snowpark_tutorial from '!!raw-loader!../code-samples/dags/airflow-snowpark/airflow_with_snowpark_tutorial.py';

[Snowpark](https://www.snowflake.com/en/data-cloud/snowpark/) is a framework containing runtimes and libraries to run non-SQL code in [Snowflake](https://www.snowflake.com/en/). 

In this tutorial you'll learn how to: 

- Create a [custom XCom backend](custom-xcom-backends-tutorial.md) in Snowflake.
- Create and use a model registry in Snowflake.
- Use Airflow decorators to run code in Snowpark, both in a pre-built and custom virtual environment.

:::caution

The provider used in this tutorial is currently in beta and subject to change. Classes from this provider might be subject to change and will be included in the Snowflake provider in a future release.After this release, this tutorial will be updated. The source code of the operators shown is currently available on . The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-snowpark-tutorial). 

:::

## Why use Airflow with Snowpark?

Snowpark allows you to run non-SQL code in Snowflake and comes with a comprehensive machine learning library optimized for Snowflake. 

Integrating Snowpark with Airflow offers the benefit of:

- Running machine learning models directly in Snowflake, without having to move data out of your Snowflake database.
- Express data transformations in Snowflake in Python instead of SQL.
- Store and version your machine learning models in Snowflake.
- Running Airflow tasks using different Python versions and packages side-by-side with Snowpark tasks requiring Python 3.8 in the same DAG while maintaining separate Python environments.

Additionally this tutorial shows how to use Snowflake as a custom XCom backend, this is especially useful for organizations with strict compliance requirements who want to keep all their data in Snowflake but still leverage [Airflow XCom](airflow-passing-data-between-tasks.md) to pass data between tasks.

## Time to complete

This tutorial takes approximately 45 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Snowflake and Snowpark. See [Introduction to Snowflake](https://docs.snowflake.com/en/user-guide-intro.html) and [Snowflake API documentation](https://docs.snowflake.com/en/developer-guide/snowpark/index).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Snowflake account. A [30-day free trial](https://signup.snowflake.com/) is available. You will need to have at least one database and one schema created to store the data and models used in this tutorial.

If you want to run this tutorial using the Snowflake XCom backend you will need to either:

- Use a Snowflake account with `ACCOUNTADMIN` privileges. In this case the Snowflake XCom backend can be created and cleaned up by the [setup/ teardown](airflow-setup-teardown.md) tasks (`create_snowflake_objects` and `cleanup_xcom_table`) at the beginning and end of the tutorial DAG. The free trial account does have the required privileges.
- Ask your Snowflake administrator to create the following for you:
    - A database called `SNOWPARK_XCOM_DB`.
    - A schema called `SNOWPARK_XCOM_SCHEMA`.
    - A table called `XCOM_TABLE`.
    - A stage called `XCOM_STAGE`.

Similarly, the tutorial DAG includes a toggle to use a [Snowpark-optimized warehouse](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized) for model training. While the tutorial DAG uses a small dataset where model training can be accomplished using the standard Snowflake warehouse, Astronomer recommends to use a Snowpark warehouse for model training in production. If you want to use a Snowpark warehouse for model training you will need to either:

- Use a Snowflake account with `ACCOUNTADMIN` privileges. In this case the Snowpark-optimized warehouse can be created by the [setup](airflow-setup-teardown.md) task (`create_snowflake_objects`) at the beginning of the tutorial DAG. The free trial account does have the required privileges.
- Ask your Snowflake administrator to create a Snowpark-optimized warehouse (`SNOWPARK_WH`) for you.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Download the `whl` file for the Astro Snowpark provider beta version from the [Astronomer Github repository](https://github.com/astronomer/learn-tutorials-data/blob/main/wheel_files/astro_provider_snowflake-0.0.0-py3-none-any.whl) and save it in your Astro project's `include` directory.

3. Create a new file in your Astro project's root directory called `requirements-snowpark.txt`. This file contains all Python packages that you will install in your reuseable Snowpark environment.

    ```text
    psycopg2-binary
    snowflake_snowpark_python[pandas]==1.5.1
    virtualenv
    /tmp/astro_provider_snowflake-0.0.0-py3-none-any.whl
    ```

3. Change the content of the `Dockerfile` of your Astro project to the following, importing the wheel file and creating a virtual environment using the [Astro venv buildkit](https://github.com/astronomer/astro-provider-venv), in which the requirements added in the previous step will be installed.

    ```dockerfile
    # syntax=quay.io/astronomer/airflow-extensions:latest

    FROM quay.io/astronomer/astro-runtime:9.1.0-python-3.9-base

    # Copy the wheel file to the image
    COPY include/astro_provider_snowflake-0.0.0-py3-none-any.whl /tmp

    # Create the virtual environment
    PYENV 3.8 snowpark requirements-snowpark.txt

    # Install packages into the virtual environment
    COPY requirements-snowpark.txt /tmp
    RUN python3.8 -m pip install -r /tmp/requirements-snowpark.txt
    ```

4. Add the following package to your `packages.txt` file:

    ```text
    build-essential
    ```

5. Add the following packages to your `requirements.txt` file to install the Astro Snowflake provider from the `whl` file:

    ```text
    apache-airflow-providers-snowflake==4.1.0
    snowflake-snowpark-python[pandas]==1.5.1
    snowflake-ml-python==1.0.7
    matplotlib==3.7.3
    /tmp/astro_provider_snowflake-0.0.0-py3-none-any.whl
    ```

:::caution

The Astro Snowpark provider is currently in beta. Classes from this provider might be subject to change and will be included in the Snowflake provider in a future release. After this release Steps 1.2 to 1.5 will be updated in this tutorial.

:::

6. To create an [Airflow connection](connections.md) to Snowflake and [allow serialization of Astro Python SDK objects](https://astro-sdk-python.readthedocs.io/en/stable/guides/xcom_backend.html#airflow-s-xcom-backend), add the following to your `.env` file. Make sure to enter your own Snowflake credentials.

    ```text
    AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES=airflow\.* astro\.* 
    AIRFLOW_CONN_SNOWFLAKE_DEFAULT='{
        "conn_type": "snowflake",
        "login": "<username>",
        "password": "<password>",
        "schema": "<schema>",
        "extra":
            {
                "account": "<account>",
                "warehouse": "<warehouse>",
                "database": "<database>",
                "region": "<region>",
                "role": "<role>",
                "authenticator": "snowflake",
                "session_parameters": null,
                "application": "AIRFLOW"
            }
    }'
    ```

7. Optional. If you want to use a Snowflake custom XCom backend add the following variables to your `.env` as well. Make sure to replace the values with the name of your own database, schema, table and stage if you are not using the suggested values.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND='astronomer.providers.snowflake.xcom_backends.snowflake.SnowflakeXComBackend'
    AIRFLOW__CORE__XCOM_SNOWFLAKE_TABLE='SNOWPARK_XCOM_DB.SNOWPARK_XCOM_SCHEMA.XCOM_TABLE'
    AIRFLOW__CORE__XCOM_SNOWFLAKE_STAGE='SNOWPARK_XCOM_DB.SNOWPARK_XCOM_SCHEMA.XCOM_STAGE'
    ```

## Step 2: Add your data

The DAG in this tutorial runs a classification model on synthetic data to predict with afternoon beverage a skier will choose based on attributes like ski color, ski resort and amount of new snow. The data is being generated using [this script](https://github.com/astronomer/airflow-snowpark-tutorial/blob/main/include/data/create_ski_dataset.py). 

1. Create a new directory in your Astro project's `include` directory called `data`.

2. Download the dataset from [Astronomer's GitHub](https://github.com/astronomer/learn-tutorials-data/blob/main/ski_dataset.csv) and save it in `include/data`.

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `airflow_with_snowpark_tutorial.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{airflow_with_snowpark_tutorial}</CodeBlock>

    This DAG consists of seven tasks comprising a simple ML orchestration pipeline.
