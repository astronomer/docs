"""
## Check data quality using SQL check operators

This DAG creates a toy table about birds in SQLite to run data quality checks on using the 
SQLColumnCheckOperator, SQLTableCheckOperator, and SQLCheckOperator.
"""

from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import (
    SQLColumnCheckOperator,
    SQLTableCheckOperator,
    SQLCheckOperator,
)
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from pendulum import datetime

_CONN_ID = "sqlite_conn"
_TABLE_NAME = "birds"


@dag(
    start_date=datetime(2023, 7, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["/usr/local/airflow/include/"],
)
def sql_data_quality():
    create_table = SqliteOperator(
        task_id="create_table",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
            bird_name VARCHAR,
            observation_year INT,
            bird_happiness INT
        );
        """,
    )

    populate_data = SqliteOperator(
        task_id="populate_data",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
            INSERT INTO {_TABLE_NAME} (bird_name, observation_year, bird_happiness) VALUES
                ('King vulture (Sarcoramphus papa)', 2022, 9),
                ('Victoria Crowned Pigeon (Goura victoria)', 2021, 10),
                ('Orange-bellied parrot (Neophema chrysogaster)', 2021, 9),
                ('Orange-bellied parrot (Neophema chrysogaster)', 2020, 8),
                (NULL, 2019, 8),
                ('Indochinese green magpie (Cissa hypoleuca)', 2018, 10);
        """,
    )

    column_checks = SQLColumnCheckOperator(
        task_id="column_checks",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        partition_clause="bird_name IS NOT NULL",
        column_mapping={
            "bird_name": {
                "null_check": {"equal_to": 0},
                "distinct_check": {"geq_to": 2},
            },
            "observation_year": {"max": {"less_than": 2023}},
            "bird_happiness": {"min": {"greater_than": 0}, "max": {"leq_to": 10}},
        },
    )

    table_checks = SQLTableCheckOperator(
        task_id="table_checks",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        checks={
            "row_count_check": {"check_statement": "COUNT(*) >= 3"},
            "average_happiness_check": {
                "check_statement": "AVG(bird_happiness) >= 9",
                "partition_clause": "observation_year >= 2021",
            },
        },
    )

    custom_check = SQLCheckOperator(
        task_id="custom_check",
        conn_id=_CONN_ID,
        sql="custom_check.sql",
        params={"table_name": _TABLE_NAME},
    )

    create_table >> populate_data >> [column_checks, table_checks, custom_check]


sql_data_quality()
