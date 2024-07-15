from datetime import datetime

import pandas as pd
from airflow.decorators import dag
from astro.files import File
from astro.sql import (
    append,
    dataframe,
    load_file,
    run_raw_sql,
    transform,
)
from astro.sql.table import Table

SNOWFLAKE_CONN_ID = "snowflake_conn"
FILE_PATH = "/usr/local/airflow/include/"


# The first transformation combines data from the two source csv's
@transform
def extract_data(homes1: Table, homes2: Table):
    return """
    SELECT *
    FROM {{homes1}}
    UNION
    SELECT *
    FROM {{homes2}}
    """


# Switch to Python (Pandas) for melting transformation to get data into long format
@dataframe
def transform_data(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    melted_df = df.melt(
        id_vars=["sell", "list"], value_vars=["living", "rooms", "beds", "baths", "age"]
    )

    return melted_df


# Back to SQL to filter data
@transform
def filter_data(homes_long: Table):
    return """
    SELECT *
    FROM {{homes_long}}
    WHERE SELL > 200
    """


@run_raw_sql
def create_table():
    """Create the reporting data which will be the target of the append method"""
    return """
    CREATE TABLE IF NOT EXISTS homes_reporting (
      sell number,
      list number,
      variable varchar,
      value number
    );
    """


@dag(start_date=datetime(2021, 12, 1), schedule="@daily", catchup=False)
def example_snowflake_partial_table_with_append():
    # Initial load of homes data csv's into Snowflake
    homes_data1 = load_file(
        input_file=File(path=FILE_PATH + "homes.csv"),
        output_table=Table(name="HOMES", conn_id=SNOWFLAKE_CONN_ID),
    )

    homes_data2 = load_file(
        task_id="load_homes2",
        input_file=File(path=FILE_PATH + "homes2.csv"),
        output_table=Table(name="HOMES2", conn_id=SNOWFLAKE_CONN_ID),
    )

    # Define task dependencies
    extracted_data = extract_data(
        homes1=homes_data1,
        homes2=homes_data2,
        output_table=Table(name="combined_homes_data"),
    )

    transformed_data = transform_data(
        df=extracted_data, output_table=Table(name="homes_data_long")
    )

    filtered_data = filter_data(
        homes_long=transformed_data,
        output_table=Table(name="expensive_homes_long"),
    )

    create_results_table = create_table(conn_id=SNOWFLAKE_CONN_ID)

    # Append transformed & filtered data to reporting table
    # Dependency is inferred by passing the previous `filtered_data` task to `append_table` param
    record_results = append(
        source_table=filtered_data,
        target_table=Table(name="homes_reporting", conn_id=SNOWFLAKE_CONN_ID),
        columns=["sell", "list", "variable", "value"],
    )
    record_results.set_upstream(create_results_table)


example_snowflake_partial_table_with_append()
