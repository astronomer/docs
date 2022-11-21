---
title: "The Astro Python SDK for ETL"
sidebar_label: "Astro Python SDK for ETL"
description: "Use the Astro Python SDK to implement ELT use cases in Airflow."
id: "astro-python-sdk-etl"
---

The [Astro Python SDK](https://github.com/astro-projects/astro) is an open source tool and Python package for DAG development that is built and maintained by Astronomer. The purpose of the SDK is to remove the complexity of writing DAGs in Apache Airflow, particularly in the context of Extract, Load, Transform (ELT) use cases. This enables pipeline authors to focus more on writing business logic in Python, and less on setting Airflow configurations.

The Astro SDK uses Python [decorators](https://realpython.com/primer-on-python-decorators/) and the TaskFlow API to simplify Python functions for common data orchestration use cases. Specifically, the Astro SDK decorators include eight python functions that make it easier to:

- Extract a file from a remote object store, such as Amazon S3 or Google Cloud Storage (GCS).
- Load that file to a new or existing table in a data warehouse, such as Snowflake.
- Transform the data in that file with SQL written by your team.

These functions make your DAGs easier to write and read with less code. In this guide, you’ll learn about how to install the Python SDK and how to use it in practice. The Astro SDK should feel more similar to writing a traditional Python script than writing a DAG in Airflow.

:::tip

To get the most out of this guide, you should have an understanding of Airflow decorators. See [Introduction to Airflow Decorators guide](airflow-decorators.md).

:::

## Python SDK functions

The Astro Python SDK makes implementing ELT use cases easier by allowing you to seamlessly transition between Python and SQL for each step in your process. Details like creating dataframes, storing intermediate results, passing context and data between tasks, and creating task dependencies are all managed automatically.

More specifically, the Astro Python SDK includes several functions that are helpful when implementing an ETL framework:

- `load_file`: Loads a given file into a SQL table. The file should be in CSV, JSON, or parquet files stored in Amazon S3 or GCS.
- `transform`: Applies a SQL select statement to a source table and saves the result to a destination table. This function allows you to transform your data with a SQL query. It uses a `SELECT` statement that you define to automatically store your results in a new table. By default, the `output_table` is given a unique name each time the DAG runs, but you can overwrite this behavior by defining a specific `output_table` in your function. You can then pass the results of the `transform` downstream to the next task as if it were a native Python object.
- `dataframe`: Exports a specific SQL table into an in-memory pandas DataFrame. Similar to `transform` for SQL, the `dataframe` function allows you to implement a transformation of your data using Python. You can easily store the results of the `dataframe` function in your database by specifying an `output_table`, which is useful if you want to switch back to SQL in the next step or load your final results to your database.
- `append`: Inserts rows from the source SQL table into the destination SQL table, if there are no conflicts. This function allows you to take resulting data from another function and append it to an existing table in your database. It is particularly useful in ETL scenarios and when dealing with reporting data.
  
For a full list of functions, see the [Astro Python SDK README in GitHub](https://github.com/astronomer/astro-sdk).

## Installation

Using the Astro Python SDK requires configuring a few things in your Airflow project.

1. Install the Astro Python SDK package in your Airflow environment. If you're using the Astro CLI, add the following to the `requirements.txt` file of your Astro project:

    ```
    astro-sdk-python
    ```
    
2. Add the following environment variables. If you're using the Astro CLI locally, add these to the `.env` file of your Astro project:

    ```text
    export AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
    export AIRFLOW__ASTRO_SDK__SQL_SCHEMA=<snowflake_schema>
    ```

    The `AIRFLOW__ASTRO_SDK__SQL_SCHEMA` variable should be the schema you want to store all intermediary tables in. To deploy a pipeline written with the Astro Python SDK to Astro, add these environment variables to your Deployment. See [Environment variables](https://docs.astronomer.io/astro/environment-variables).

For a guided experience to get started, see the [Astro Python SDK tutorial](astro-python-sdk.md).

## Example

The following DAG is a complete implementation of an ETL pipeline using the Astro Python SDK. In order, the DAG:

- Loads .csv files from Amazon S3 into two tables that contain data about the housing market. Tables are objects that contain all of the necessary functionality to pass database contexts between functions without reconfiguration.
- Combines the two tables of home data using `aql.transform`.
- Turns the combined into a DataFrame, melts the values using `aql.dataframe`, and returns the results as a Table object.
- Creates a new reporting table in Snowflake using `aql.run_raw_sql`.
- Appends the table of transformed home data to a reporting table with `aql.append`.

```python
import os
from datetime import datetime
import pandas as pd
from airflow.decorators import dag
from astro.files import File
from astro import sql as aql
from astro.sql.table import Metadata, Table
SNOWFLAKE_CONN_ID = "snowflake_conn"
AWS_CONN_ID = "aws_conn"
# The first transformation combines data from the two source tables
@aql.transform
def combine_tables(homes1: Table, homes2: Table):
    return """
    SELECT *
    FROM {{homes1}}
    UNION
    SELECT *
    FROM {{homes2}}
    """
# Switch to Python (Pandas) for melting transformation to get data into long format
@aql.dataframe
def transform_data(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    melted_df = df.melt(
        id_vars=["sell", "list"], value_vars=["living", "rooms", "beds", "baths", "age"]
    )
    return melted_df
# Run a raw SQL statement to create the reporting table if it doesn't already exist
@aql.run_raw_sql
def create_reporting_table():
    """Create the reporting data which will be the target of the append method"""
    return """
    CREATE TABLE IF NOT EXISTS homes_reporting (
      sell number,
      list number,
      variable varchar,
      value number
    );
    """
@dag(start_date=datetime(2021, 12, 1), schedule_interval="@daily", catchup=False)
def example_s3_to_snowflake_etl():
    # Initial load of homes data csv's from S3 into Snowflake
    homes_data1 = load_file(
        task_id="load_homes1",
        input_file=File(path="s3://airflow-kenten/homes1.csv", conn_id=AWS_CONN_ID),
        output_table=Table(name="HOMES1", conn_id=SNOWFLAKE_CONN_ID)
    )
    homes_data2 = load_file(
        task_id="load_homes2",
        input_file=File(path="s3://airflow-kenten/homes2.csv", conn_id=AWS_CONN_ID),
        output_table=Table(name="HOMES2", conn_id=SNOWFLAKE_CONN_ID)
    )
    # Define task dependencies
    extracted_data = combine_tables(
        homes1=homes_data1,
        homes2=homes_data2,
        output_table=Table(name="combined_homes_data"),
    )
    transformed_data = transform_data(
        df=extracted_data, output_table=Table(name="homes_data_long")
    )
    create_reporting_table = create_reporting_table(conn_id=SNOWFLAKE_CONN_ID)
    # Append transformed data to reporting table
    # Dependency is inferred by passing the previous `transformed_data` task to `source_table` param
    record_results = aql.append(
        source_table=transformed_data,
        target_table=Table(name="homes_reporting", conn_id=SNOWFLAKE_CONN_ID),
        columns=["sell", "list", "variable", "value"],
    )
    record_results.set_upstream(create_results_table)
example_s3_to_snowflake_etl_dag = example_s3_to_snowflake_etl()
```

![Astro Graph](/img/guides/astro_sdk_graph.png)

This Astro SDK implementation is different from a standard TaskFlow implementation in the following ways:

- The `load_file` and `append` functions take care of loading your raw data from Amazon S3 and appending data to your reporting table. You don't have to write any extra code to get the data into Snowflake. A `load_file` task exists for each file instead of one task for all files in Amazon S3, which supports atomicity.
- Using the `transform` function, you can execute SQL to combine your data from multiple tables. The results are automatically stored in a Snowflake table. You don't have to use the `SnowflakeHook` in Airflow or write any of the code to execute the query.
- You can run a transformation in Python with the `dataframe` function, meaning that you don't need to explicitly convert the results of your previous task to a Pandas DataFrame. You can then write output of your transformation to your aggregated reporting table in Snowflake using the `target_table parameter`, so you don't have to worry about storing the data in XCom.
- You don't have to redefine your Airflow connections in any tasks that are downstream of your original definitions, including `load_file` and `create_reporting_table`. Any downstream task that inherits from a task with a defined connection can use the same connection without additional configuration.
- You can run common SQL queries using Python alone. The SDK includes Python functions for some of the most common actions in SQL.

Overall, your DAG with the Astro Python SDK is shorter, simpler to implement, and easier to read. This allows you to implement even more complicated use cases easily while focusing on the movement of your data.

### The DAG before the Astro Python SDK

To showcase the difference in performing this exact same use case without the help of the Astro Python SDK, here is what your DAG would look like:

```python
from datetime import datetime
import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
S3_BUCKET = 'bucket_name'
S3_FILE_PATH = '</path/to/file/'
SNOWFLAKE_CONN_ID = 'snowflake'
SNOWFLAKE_SCHEMA = 'schema_name'
SNOWFLAKE_STAGE = 'stage_name'
SNOWFLAKE_WAREHOUSE = 'warehouse_name'
SNOWFLAKE_DATABASE = 'database_name'
SNOWFLAKE_ROLE = 'role_name'
SNOWFLAKE_SAMPLE_TABLE = 'sample_table'
SNOWFLAKE_RESULTS_TABLE = 'result_table'
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
@dag(start_date=datetime(2021, 12, 1), schedule_interval='@daily', catchup=False)
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
    create_reporting_table = SnowflakeOperator(
        task_id="create_reporting_table",
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        sql='''
        CREATE TABLE IF NOT EXISTS homes_reporting (
            sell number, 
            list number, 
            variable varchar,
            value number
            );'''
    )
    load_transformed_data = S3ToSnowflakeOperator(
        task_id='load_transformed_data',
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        s3_keys=[S3_FILE_PATH + '/transformed_file_name.csv'],
        table=SNOWFLAKE_RESULTS_TABLE,
        schema=SNOWFLAKE_SCHEMA,
        stage=SNOWFLAKE_STAGE,
        file_format="(type = 'CSV',field_delimiter = ',')",
    )
    extracted_data = extract_data()
    transformed_data = transform_data(extracted_data)
    load_subscription_data >> extracted_data >> transformed_data >> load_transformed_data
    create_reporting_table >> load_transformed_data
classic_etl_dag = classic_etl_dag()
```

![Classic Graph](/img/guides/classic_graph.png)

Although you achieved your ETL goal with the DAG, the following limitations made this implementation more complicated:

- Since there is no way to pass results from the [`SnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator) query to the next task, you had to write a query in a `_DecoratedPythonOperator` function using the [`SnowflakeHook`](https://registry.astronomer.io/providers/snowflake/modules/snowflakehook) and explicitly do the conversion from SQL to a dataframe yourself.
- Some of the transformations are better suited to SQL, and others are better suited to Python, but transitioning between the two requires extra boilerplate code to explicitly make the conversions.
- While the TaskFlow API makes it easier to pass data between tasks, it stores the resulting dataframes as XComs by default. This means that you need to worry about the size of your data. You could implement a custom XCom backend, but that would require additional configuration.
- Loading data back to Snowflake after the transformation is complete requires writing extra code to store an intermediate CSV in Amazon S3.

## Learn more

To learn more about the Astro Python SDK, see:

- [Write a DAG with the Astro Python SDK](https://docs.astronomer.io/learn/astro-python-sdk): A step-by-step tutorial for setting up Airflow and running an ETL pipeline using the Astro Python SDK.
- [readthedocs.io](https://astro-sdk.readthedocs.io/en/latest/): Complete SDK documentation, including API and operator references.
- [Astro Python SDK README](https://github.com/astronomer/astro-sdk): Includes an overview of the SDK, a quickstart, and supported database types.
- [Astro Python SDK Webinar](https://www.astronomer.io/events/recaps/the-astro-python-sdk/): A recorded demonstration of the SDK led by the Astronomer team.
