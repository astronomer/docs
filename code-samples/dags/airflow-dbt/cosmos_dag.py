from airflow.decorators import dag
from cosmos.providers.dbt.task_group import DbtTaskGroup
from astro import sql as aql
from astro.sql.table import Table, Metadata
from astro.files import File
from pendulum import datetime
import pandas as pd
import logging

task_logger = logging.getLogger("airflow.task")

CONNECTION_ID = "db_conn"
DB_NAME = "energy_db"
SCHEMA_NAME = "energy_schema"
CSV_FILEPATH = "include/subset_energy_capacity.csv"
DBT_PROJECT_NAME = "my_energy_project"
# the path where the Astro dbt provider will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = "/usr/local/airflow/dbt_venv/bin/dbt"
# The path to your dbt directory
DBT_ROOT_PATH = "/usr/local/airflow/dags/dbt"


@aql.dataframe
def log_data_analysis(df: pd.DataFrame):
    """Analyzes the energy capacity information from the input table in order
    to log a table of % Solar and % renewable energy capacity per year.
    If the latest year in the data was also the year with the highest % of solar
    capacity and/or the year with the highest % of renewables capacity a
    celebratory message is logged as weel."""
    
    # Compatible with Postgres. If you are using database other than Postgres, you might need to adjust the pd.DataFrame column names in this code to be lowercase.

    latest_year = df.YEAR.max()
    year_with_the_highest_solar_pct = df.loc[df["SOLAR_PCT"].idxmax(), "YEAR"]
    year_with_the_highest_renewables_pct = df.loc[df["RENEWABLES_PCT"].idxmax(), "YEAR"]
    df["% Solar"] = round(df["SOLAR_PCT"] * 100, 2)
    df["% Renewable Energy Sources"] = round(df["RENEWABLES_PCT"] * 100, 2)

    task_logger.info(
        df[["YEAR", "% Solar", "% Renewable Energy Sources"]]
        .sort_values(by="YEAR", ascending=True)
        .drop_duplicates()
    )

    if latest_year == year_with_the_highest_solar_pct:
        task_logger.info(
            f"Yay! In {df.COUNTRY.unique()[0]} adoption of solar energy is growing!"
        )
    if latest_year == year_with_the_highest_renewables_pct:
        task_logger.info(
            f"Yay! In {df.COUNTRY.unique()[0]} adoption of renewable energy is growing!"
        )


@dag(
    start_date=datetime(2023, 3, 26),
    schedule=None,
    catchup=False,
)
def my_energy_dag():
    # Astro SDK task that loads information from the local csv into a relational database
    # the table named 'energy' will be created by this task if it does not exist yet
    load_data = aql.load_file(
        input_file=File(CSV_FILEPATH),
        output_table=Table(
            name="energy",
            conn_id=CONNECTION_ID,
            metadata=Metadata(
                database=DB_NAME,
                schema=SCHEMA_NAME,
            ),
        ),
    )

    # use the DbtTaskGroup class to create a task group containing task created
    # from dbt models
    dbt_tg = DbtTaskGroup(
        group_id="transform_data",
        dbt_project_name=DBT_PROJECT_NAME,
        conn_id=CONNECTION_ID,
        dbt_root_path=DBT_ROOT_PATH,
        dbt_args={
            "dbt_executable_path": DBT_EXECUTABLE_PATH,
            "schema": SCHEMA_NAME,
            "vars": '{"country_code": "CH"}',
            # the dataset mostly contains data from EU countries
        },
    )

    (
        load_data
        >> dbt_tg
        >> log_data_analysis(
            Table(
                name="create_pct",
                metadata=Metadata(
                    database=DB_NAME,
                    schema=SCHEMA_NAME,
                ),
                conn_id=CONNECTION_ID,
            )
        )
    )


my_energy_dag()
