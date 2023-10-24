---
title: "The Astro Python SDK for ETL"
sidebar_label: "Astro Python SDK for ETL"
description: "Use the Astro Python SDK to implement ELT use cases in Airflow."
id: "astro-python-sdk-etl"
---

import CodeBlock from '@theme/CodeBlock';
import astro_python_sdk_etl from '!!raw-loader!../code-samples/dags/astro-python-sdk-etl/astro_python_sdk_etl.py';

The [Astro Python SDK](https://github.com/astronomer/astro-sdk/) is an open source tool and Python package for DAG development that is built and maintained by Astronomer. The purpose of the SDK is to remove the complexity of writing DAGs in Apache Airflow, particularly in the context of Extract, Load, Transform (ELT) use cases. This enables pipeline authors to focus more on writing business logic in Python, and less on setting Airflow configurations.

The Astro SDK uses Python [decorators](https://realpython.com/primer-on-python-decorators/) and the TaskFlow API to simplify Python functions for common data orchestration use cases. Specifically, the Astro SDK decorators include eight python functions that make it easier to:

- Extract a file from a remote object store, such as Amazon S3 or Google Cloud Storage (GCS).
- Load that file to a new or existing table in a data warehouse, such as Snowflake.
- Transform the data in that file with SQL written by your team.

These functions make your DAGs easier to write and read with less code. In this guide, you’ll learn about how to install the Python SDK and how to use it in practice. The Astro SDK should feel more similar to writing a traditional Python script than writing a DAG in Airflow.

:::info

This guide is based on the latest version of the Astro SDK. If you're using an earlier version of the Astro SDK, you might need to modify the configuration steps or code. See the [Astro Python SDK Changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#) for a complete list of changes in each version.

:::

:::tip Related Content

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Astro: SDK](https://academy.astronomer.io/astro-runtime-sdk) module.
- Webinar: [Simplified DAG authoring with the Astro SDK](https://www.astronomer.io/events/webinars/simplified-dag-authoring-with-the-astro-sdk/).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of Airflow decorators. See [Introduction to Airflow Decorators guide](airflow-decorators.md).

## Python SDK functions

The Astro Python SDK makes implementing ELT use cases easier by allowing you to seamlessly transition between Python and SQL for each step in your process. Details like creating dataframes, storing intermediate results, passing context and data between tasks, and creating task dependencies are all managed automatically.

More specifically, the Astro Python SDK includes several functions that are helpful when implementing an ETL framework:

- `load_file`: Loads a given file into a SQL table. You can load data from many file types including CSV and JSON. For a list of all supported file types, database types, and storage locations, see the following pages in Astro SDK documentation:

    - [Supported databases](https://astro-sdk-python.readthedocs.io/en/latest/supported_databases.html)
    - [Supported file types](https://astro-sdk-python.readthedocs.io/en/latest/supported_file.html#supported-file-type)
    - [Supported file locations](https://astro-sdk-python.readthedocs.io/en/latest/supported_file.html)

- `transform`: Applies a SQL select statement to a source table and saves the result to a destination table. This function allows you to transform your data with a SQL query. It uses a `SELECT` statement that you define to automatically store your results in a new table. By default, the `output_table` is given a unique name each time the DAG runs, but you can overwrite this behavior by defining a specific `output_table` in your function. You can then pass the results of the `transform` downstream to the next task as if it were a native Python object.
- `dataframe`: Exports a specific SQL table into an in-memory pandas DataFrame. Similar to `transform` for SQL, the `dataframe` function allows you to implement a transformation of your data using Python. You can easily store the results of the `dataframe` function in your database by specifying an `output_table`, which is useful if you want to switch back to SQL in the next step or load your final results to your database.
- `append`: Inserts rows from the source SQL table into the destination SQL table, if there are no conflicts. This function allows you to take resulting data from another function and append it to an existing table in your database. It is particularly useful in ETL scenarios and when dealing with reporting data.
  
For a full list of functions, see the [Astro Python SDK README in GitHub](https://github.com/astronomer/astro-sdk).

## Installation

1. Install the Astro Python SDK package in your Airflow environment. If you're using the Astro CLI, add the following to the `requirements.txt` file of your Astro project:

    ```
    astro-sdk-python
    ```

2. If you're using Airflow 2.4 or earlier, set the following environment variable to use a required custom XCom backend. If you're using the Astro CLI, add this environment variable to the `.env` file of your Astro project
    
    ```text
    AIRFLOW__CORE__XCOM_BACKEND='astro.custom_backend.astro_custom_backend.AstroCustomXcomBackend'
    ```

3. (Optional) Create an [Airflow connection](connections.md) to the database where you want to store the temporary tables created by the Astro SDK. Set the following environment variables to configure your database as an Astro SDK storage backend. If you're using the Astro CLI, add these environment variables to the `.env` file of your Astro project:

    ```text
    AIRFLOW__ASTRO_SDK__XCOM_STORAGE_CONN_ID='<your-database-connection-id>'
    AIRFLOW__ASTRO_SDK__XCOM_STORAGE_URL='<your-storage-folder-name>'
    ```

    For example, to use S3 as your storage backend, you would add the following environment variables:

    ```text
    AIRFLOW__ASTRO_SDK__XCOM_STORAGE_CONN_ID=<your_aws_conn>
    AIRFLOW__ASTRO_SDK__XCOM_STORAGE_URL='s3://<your-bucket>/xcom/'
    ```
    
    If you don't configure an external XCom backend, you will only be able to process small amounts of data with the SDK.

For a guided experience to get started, see the [Astro Python SDK tutorial](astro-python-sdk.md).

## Before and after the Astro Python SDK

To highlight how the Astro Python SDK results in simpler DAG code, we'll show a direct comparison of a DAG written with the SDK to one written with traditional operators. The following DAG is a complete implementation of an ETL pipeline using the Astro Python SDK. In order, the DAG:

- Loads .csv files from Amazon S3 into two tables that contain data about the housing market. Tables are objects that contain all of the necessary functionality to pass database contexts between functions without reconfiguration.
- Combines the two tables of home data using `aql.transform`.
- Turns the combined into a DataFrame, melts the values using `aql.dataframe`, and returns the results as a Table object.
- Creates a new reporting table in Snowflake using `aql.run_raw_sql`.
- Appends the table of transformed home data to a reporting table with `aql.append`.

<CodeBlock language="python">{astro_python_sdk_etl}</CodeBlock>

![Astro Graph](/img/guides/astro_sdk_graph.png)

The following sections break down each step of this DAG and compare the Astro Python SDK implementation to one using traditional operators.

### Load data

The first step in the pipeline is to load the data from S3 to Snowflake. With the Astro Python SDK, the `load_file` and `append` functions take care of loading your raw data from Amazon S3 and appending data to your reporting table. You don't have to write any extra code to get the data into Snowflake.

```python
homes_data1 = aql.load_file(
    task_id="load_homes1",
    input_file=File(path="s3://airflow-kenten/homes1.csv", conn_id=AWS_CONN_ID),
    output_table=Table(name="HOMES1", conn_id=SNOWFLAKE_CONN_ID)
)
homes_data2 = aql.load_file(
    task_id="load_homes2",
    input_file=File(path="s3://airflow-kenten/homes2.csv", conn_id=AWS_CONN_ID),
    output_table=Table(name="HOMES2", conn_id=SNOWFLAKE_CONN_ID)
)
```

Without the SDK, the easiest way to accomplish this is using the traditional `S3ToSnowflakeOperator`.

```python
def classic_etl_dag():
    load_data = S3ToSnowflakeOperator(
        task_id='load_homes_data',
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        s3_keys=[S3_FILE_PATH + '/homes.csv'],
        table=SNOWFLAKE_SAMPLE_TABLE,
        schema=SNOWFLAKE_SCHEMA,
        stage=SNOWFLAKE_STAGE,
        file_format="(type = 'CSV',field_delimiter = ',')",
    )
```

While this operator is straight-forward, it requires knowledge of Snowflake and S3-specific parameters. The Astro Python SDK takes care of all of nuances of different systems for you under the hood.

### Combine data

The next step in the pipeline is to combine data. With the Astro Python SDK `transform` function, you can execute SQL to combine your data from multiple tables. The results are automatically stored in a Snowflake table. 

```python
@aql.transform
def combine_tables(homes1: Table, homes2: Table):
    return """
    SELECT *
    FROM {{homes1}}
    UNION
    SELECT *
    FROM {{homes2}}
    """
```

Without the SDK, you need to write explicit code to complete this step.

```python
@task(task_id='extract_data')
def extract_data():
    # Join data from two tables and save to dataframe to process
    query = ''''
    SELECT *
    FROM HOMES1
    UNION
    SELECT *
    FROM HOMES2
    '''
    # Make connection to Snowflake and execute query
    hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)
    conn = hook.get_conn()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    column_names = list(map(lambda t: t[0], cur.description))
    df = pd.DataFrame(results)
    df.columns = column_names
    return df.to_json()
```

Since there is no way to pass results from the [`SnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator) query to the next task, you have to write a query in a `_DecoratedPythonOperator` function using the [`SnowflakeHook`](https://registry.astronomer.io/providers/snowflake/modules/snowflakehook) and explicitly do the conversion from SQL to a dataframe yourself.

### Transform data

The third step in the pipeline is transforming the data. The transformations required for this pipeline are easier to implement in Python than in SQL. With the Astro Python SDK, you can run a transformation in Python with the `dataframe` function, meaning that you don't need to explicitly convert the results of your previous task to a Pandas DataFrame. You can then write output of your transformation to your aggregated reporting table in Snowflake using the `target_table parameter`, so you don't have to worry about storing the data in XCom.

```python
@aql.dataframe
def transform_data(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    melted_df = df.melt(
        id_vars=["sell", "list"], value_vars=["living", "rooms", "beds", "baths", "age"]
    )
    return melted_df

transformed_data = transform_data(
        df=extracted_data, output_table=Table(name="homes_data_long")
    )
# Append transformed data to reporting table
# Dependency is inferred by passing the previous `transformed_data` task to `source_table` param
record_results = aql.append(
    source_table=transformed_data,
    target_table=Table(name="homes_reporting", conn_id=SNOWFLAKE_CONN_ID),
    columns=["sell", "list", "variable", "value"],
)
```

Implementing this transformation without the SDK is more challenging. 

```python
@task(task_id='transform_data')
def transform_data(xcom: str) -> str:
    # Transform data by melting
    df = pd.read_json(xcom)
    melted_df = df.melt(
        id_vars=["sell", "list"], value_vars=["living", "rooms", "beds", "baths", "age"]
    )
    melted_str = melted_df.to_string()
    # Save results to Amazon S3 so they can be loaded back to Snowflake
    s3_hook = S3Hook(aws_conn_id="s3_conn")
    s3_hook.load_string(melted_str, 'transformed_file_name.csv', bucket_name=S3_BUCKET, replace=True)

load_transformed_data = S3ToSnowflakeOperator(
    task_id='load_transformed_data',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    s3_keys=[S3_FILE_PATH + '/transformed_file_name.csv'],
    table=SNOWFLAKE_RESULTS_TABLE,
    schema=SNOWFLAKE_SCHEMA,
    stage=SNOWFLAKE_STAGE,
    file_format="(type = 'CSV',field_delimiter = ',')",
)
```

Transitioning between Python to complete the transformation and SQL to load the results back to Snowflake requires extra boilerplate code to explicitly make the conversions. You also have to use a S3 as intermediary storage for the results and implement another `S3ToSnowflakeOperator` to load them, because there is no traditional operator to load data from a Pandas dataframe directly to Snowflake.

Overall, your DAG with the Astro Python SDK is shorter, simpler to implement, and easier to read. This allows you to implement even more complicated use cases easily while focusing on the movement of your data.

## Learn more

To learn more about the Astro Python SDK, see:

- [Write a DAG with the Astro Python SDK](https://docs.astronomer.io/learn/astro-python-sdk): A step-by-step tutorial for setting up Airflow and running an ETL pipeline using the Astro Python SDK.
- [readthedocs.io](https://astro-sdk-python.readthedocs.io/en/stable/): Complete SDK documentation, including API and operator references.
- [Astro Python SDK README](https://github.com/astronomer/astro-sdk): Includes an overview of the SDK, a quickstart, and supported database types.
- [Astro Python SDK Webinar](https://www.astronomer.io/events/recaps/the-astro-python-sdk/): A recorded demonstration of the SDK led by the Astronomer team.
