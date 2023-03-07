from pendulum import datetime
import pandas as pd
from airflow.decorators import dag
from astro.files import File
from astro import sql as aql
from astro.sql.table import Table

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


@dag(start_date=datetime(2021, 12, 1), schedule="@daily", catchup=False)
def example_s3_to_snowflake_etl():
    # Initial load of homes data csv's from S3 into Snowflake
    homes_data1 = aql.load_file(
        task_id="load_homes1",
        input_file=File(path="s3://airflow-kenten/homes1.csv", conn_id=AWS_CONN_ID),
        output_table=Table(name="HOMES1", conn_id=SNOWFLAKE_CONN_ID),
    )
    homes_data2 = aql.load_file(
        task_id="load_homes2",
        input_file=File(path="s3://airflow-kenten/homes2.csv", conn_id=AWS_CONN_ID),
        output_table=Table(name="HOMES2", conn_id=SNOWFLAKE_CONN_ID),
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
    # Delete temporary and unnamed tables
    aql.cleanup()


example_s3_to_snowflake_etl_dag = example_s3_to_snowflake_etl()
