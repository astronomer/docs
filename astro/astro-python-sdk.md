---
title: 'Write DAGs with the Astro Python SDK'
sidebar_label: 'Astro Python SDK'
id: astro-python-sdk
description: Learn how you can use the Astro SDK to build ETL pipelines with Python.
---

The Astro Python SDK is an open source tool for DAG development that is built and maintained by Astronomer. The purpose of the SDK is to remove the complexity associated with writing DAGs and setting Airflow configurations. This enables pipeline authors to focus on writing Python code.

The Astro SDK uses Python [decorators](https://realpython.com/primer-on-python-decorators/) and the TaskFlow API to simplify Python functions for common data orchestration use cases. Specifically, the Astro SDK decorators include eight python functions that make it easier to:

- Extract a file from a remote object store, such as Amazon S3 or Google Cloud Storage (GCS).
- Load that file to a new or existing table in a data warehouse, such as Snowflake.
- Transform the data in that file with SQL written by your team.

For extract, load, and transform (ELT) use cases, these functions significantly reduce the lines of code required. The Astro SDK is more similar to writing a traditional Python script than it is writing a data pipeline in Airflow.

:::info

The Astro Python SDK currently relies on [pickling](https://docs.python.org/3/library/pickle.html), which is a Python serialization method that transforms data into a portable format. A more secure method for the Astro SDK to serialize objects is coming soon.

:::

## Installation

1. Install the Astro Python SDK package by adding the following line to the `requirements.txt` file of your Astro project:

    ```text
    astro-sdk-python
    ```

2. Add the following environment variables to the `.env` file of your Astro project:

    ```text
    AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
    export AIRFLOW__ASTRO_SDK__SQL_SCHEMA=<default-schema>
    ```

    To deploy a pipeline written with the Astro Python SDK to Astro, add these environment variables in your Deployment configuration. See [Environment variables](environment-variables.md).

## Available functions

The Astro SDK includes task decorators for actions that are most commonly required for ETL pipelines:

- `load_file`: Loads a given file into a SQL table.
- `transform`: Applies a SQL select statement to a source table and saves the result to a destination table.
- `drop_table`: Drops a SQL table.
- `run_raw_sql`: Runs any SQL statement without handling its output.
- `append`: Inserts rows from the source SQL table into the destination SQL table, if there are no conflicts.
- `merge`: Inserts rows from the source SQL table into the destination SQL table, if there are no conflicts.
- `export_file`: Exports SQL table rows into a destination file.
- `dataframe`: Exports a specific SQL table into an in-memory pandas DataFrame.
- `cleanup`: Cleans up temporary tables created in your pipeline.

## Example

The following DAG is a complete implementation of an ETL pipeline using the Astro Python SDK. In order, the DAG:

- Loads `.csv` files from Amazon S3 into two tables that contain data about the housing market. Tables are objects that contain all of the necessary functionality to pass database contexts between functions without reconfiguration.
- Combines the two tables of home data using `aql.transform`.
- Turns the combined into a dataframe, melts the values using `aql.dataframe`, and returns the results as a `Table` object.
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

This Astro SDK implementation is different from a standard TaskFlow implementation in the following ways:

- You don't have to manually create temporary tables and pass them through XComs. All operations between different database types are handled automatically by the SDK.
- You don't have to define connections to your databases in each task. Tasks can automatically inherit connection information from `Table` objects.
- You can run common SQL queries using Python alone. The SDK includes Python functions for some of the most common actions in SQL.

## Related documentation

- [Write a DAG with the Astro Python SDK](https://docs.astronomer.io/tutorials/astro-python-sdk): A step-by-step tutorial for setting up Airflow and running an ETL pipeline using the Astro Python SDK.
- [readthedocs.io](https://astro-sdk.readthedocs.io/en/latest/): Complete SDK documentation, including API and operator references.
- [Astro Python SDK README](https://github.com/astronomer/astro-sdk): Includes an overview of the SDK, a quickstart, and supported database types.
- [Astro Python SDK Webinar](https://www.astronomer.io/events/recaps/the-astro-python-sdk/): A recorded demonstration of the SDK led by Astronomer.
