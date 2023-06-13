---
title: "Use DuckDB with Apache Airflow"
sidebar_label: "DuckDB"
id: airflow-duckdb
sidebar_custom_props: { icon: 'img/integrations/duckdb.png' }
---

<head>
  <meta name="description" content="Learn how to use DuckDB with Airflow." />
  <meta name="og:description" content="Learn how to use DuckDB with Airflow." />
</head>

import CodeBlock from '@theme/CodeBlock';
import duckdb_tutorial_dag_1 from '!!raw-loader!../code-samples/dags/airflow-duckdb/duckdb_tutorial_dag_1.py';
import duckdb_tutorial_dag_2 from '!!raw-loader!../code-samples/dags/airflow-duckdb/duckdb_tutorial_dag_2.py';

[DuckDB](https://duckdb.org/) is an open-source in-process SQL OLAP database management system. It allows you to run complex queries on relational datasets using SQL using either local, file-based DuckDB instances, or the cloud service [MotherDuck](https://motherduck.com/).

Airflow can interact with DuckDB in three key ways:

- Use the duckdb Python package directly in [@task decorated tasks](airflow-decorators.md): This method is useful if you want to do ad-hoc analysis in-memory or combine information stored in various DuckDB files.
- Connect to DuckDB via the [DuckDB Airflow provider](https://registry.astronomer.io/providers/airflow-provider-duckdb/versions/0.1.0): The DuckDB Airflow provider is ideal if you connect to the same DuckDB database from many tasks in your Airflow environment and want to standardize this connection in a central place. You can also use the DuckDBHook to create custom operators to modularize your DuckDB interactions from within Airflow.
- Use DuckDB with the [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html). The Astro Python SDK is an open-source package created by Astronomer to make interactions with relational data simple and tool-agnostic. The Astro Python SDK is the ideal tool if you want to easily connect to several database tools without changing any underlying code. Learn more in the [Write a DAG with the Astro Python SDK](astro-python-sdk.md) tutorial.

:::info

If you are already familiar with DuckDB and Airflow, you can clone [Astronomer's DuckDB example repository](https://github.com/astronomer/airflow-duckdb-examples) and run it locally using the Astro CLI to explore different ways of using DuckDB with Airflow.

:::

## Why use Airflow with DuckDB?

DuckDB is a versatile database management system that allows you to store relational data in-memory, in a local file or in the cloud. 

The benefits of using Airflow with DuckDB include:

- Testing complex Airflow pipelines without the need to connect to a remote database.
- Interact with data in various Python formats such as [Pandas](https://pandas.pydata.org/), [Polars](https://www.pola.rs/) and [PyArrow](https://arrow.apache.org/docs/python/index.html).
- Use DuckDB as a database in your Astro SDK pipelines without the need for a remote connection.

## Time to complete

This tutorial takes approximately 15 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of DuckDB. See [the DuckDB documentation](https://duckdb.org/docs/guides/index).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. See [Introduction to Airflow decorators](airflow-decorators.md).
- Airflow connections. See [Manage connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Step 1: Configure your Astro project

To use DuckDB with Airflow, install the [DuckDB Airflow provider](https://github.com/astronomer/airflow-provider-duckdb) in your Astro project. This will also install the newest version of the [DuckDB Python package](https://pypi.org/project/duckdb).

1. Create a new Astro project:

    ```sh
    $ mkdir astro-duckdb-tutorial && cd astro-duckdb-tutorial
    $ astro dev init
    ```

2. Add the DuckDB Airflow provider to your Astro project `requirements.txt` file.

    ```text
    airflow-provider-duckdb==0.1.0
    ```

3. If you are connecting to the DuckDB cloud service, MotherDuck, you need to use the amd64 version of Astro Runtime to prevent package conflicts. Use the following import statement in your Dockerfile. If you are only using DuckDB locally, you do not need to modify your Dockerfile.

    ```Dockerfile
    FROM --platform=linux/amd64 quay.io/astronomer/astro-runtime:8.4.0
    ```

## Step 2: Create a DAG using the duckdb Python package

You can use the [duckdb Python package](https://pypi.org/project/duckdb/) directly in your DAG by utilizing it within your @task decorated tasks. This way of using DuckDB in Airflow does not require you to configure an Airflow connection.

1. Start Airflow by running `astro dev start`.

2. Create a new file in your `dags` folder called `duckdb_tutorial_dag_1.py`.

3. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{duckdb_tutorial_dag_1}</CodeBlock>

    This simple DAG shows how you can pass a Pandas dataframe from an upstream task into a task utilizing the duckdb Python package to create and query a table in DuckDB. You can control the database you connect to by changing the `DUCKDB_CONNECTION_URI` variable:

    - Leave the connection variable empty to use an in-memory database: `duckdb.connect("")`.
    - Specify a local file path to create a local DuckDB database in which your table will persist: `duckdb.connect("include/my_garden_ducks.db")`
    - Specify a MotherDuck connection string without a database to connect to your default MotherDuck database: `duckdb.connect(f"motherduck:?token={YOUR_MOTHERDUCK_TOKEN}")`
    - Specify a MotherDuck connection string with a database to connect to a specific MotherDuck database: `duckdb.connect(f"motherduck:MY_DB?token={YOUR_MOTHERDUCK_TOKEN}")`

4. Run the DAG manually by clicking the play button and view the DAG in the grid view. In the logs of the `create_duckdb_table_from_pandas_df` task you will find a quack for each duck in your garden.

    ![DuckDB tutorial DAG 1 Grid view](/img/tutorials/airflow-duckdb_tutorial_dag_1_grid_view.png)

## Step 3: Create a DuckDB Airflow connection

Next, you will create another DAG that uses the DuckDB Airflow provider. To use the provider, you will need to define an Airflow connection to your DuckDB database.

2. In the Airflow UI, go to **Admin** -> **Connections** and click **+**. 

3. Create a new connection named `my_duckdb_conn` using the following information:

    - **Connection ID**: `my_duckdb_conn`.
    - **Connection Type**: `DuckDB`.
    - **File (leave blank for in-memory database)**: `include/my_garden_ducks.db`.

4. Click **Save**. Note that you cannot currently test a connection to DuckDB from the Airflow UI.

:::info

If you want to use an in-memory DuckDB database you can leave the `File (leave blank for in-memory database)` field empty. If you are connecting to MotherDuck you will need to specify your connection in this field as `motherduck:<your database name>?token=<your token>`.

:::

## Step 4: Create a DAG using the Airflow DuckDB provider

1. Create a new file in your `dags` folder called `duckdb_tutorial_dag_2.py`.

3. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{duckdb_tutorial_dag_2}</CodeBlock>

    This simple DAG will query all information from a table in a DuckDB instance. Make sure the table you are querying exists in the DuckDB instance you specified in your DuckDB connection.

4. Run the DAG manually by clicking the play button.

:::info

You can use the DuckDBHook to create [custom operators](airflow-importing-custom-hooks-operators.md) to modularize your interactions with DuckDB. You can find an example of a custom DuckDB operator for ingesting Excel files [here](https://github.com/astronomer/airflow-duckdb-examples/blob/main/include/custom_operators/duckdb_operator.py).

:::

## Conclusion

Congratulations! You successfully used DuckDB with Airflow. Quack!