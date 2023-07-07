from airflow.decorators import dag
from pendulum import datetime
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import (
    SQLColumnCheckOperator,
    SQLTableCheckOperator,
    SQLCheckOperator,
)

DB_CONN = "snowflake_default"
DB = "database_name"
SCHEMA = "schema_name"
TABLE = "example_table"


@dag(
    start_date=datetime(2023, 7, 1),
    schedule="@daily",
    catchup=False,
    default_args={"conn_id": DB_CONN},
)
def example_dag_sql_check_operators():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # SQLColumnCheckOperator example: runs checks on 3 columns:
    #   - MY_DATE_COL is checked to only contain unique values ("unique_check")
    #   - MY_TEXT_COL is checked to contain no NULL values
    #     and at least 10 distinct values
    #   - MY_NUM_COL is checked to have a minimum value between 90 and 110
    column_checks = SQLColumnCheckOperator(
        task_id="column_checks",
        table=TABLE,
        column_mapping={
            "MY_DATE_COL": {
                "unique_check": {"equal_to": 0},
            },
            "MY_TEXT_COL": {
                "distinct_check": {"geq_to": 10},
                "null_check": {"equal_to": 0},
            },
            "MY_NUM_COL": {"max": {"equal_to": 100, "tolerance": 0.1}},
        },
    )

    # SQLTableCheckOperator example: This operator performs three checks:
    #   - a row count check, making sure the table has >= 10 rows
    #   - a columns comparison check to see that the value in MY_COL_1 plus
    #   the value in MY_COL_2 is 100
    #   - a date between check to see that the value in MY_DATE_COL is between
    #   2017-01-01 and 2022-01-01.
    table_checks = SQLTableCheckOperator(
        task_id="table_checks",
        table=TABLE,
        checks={
            "my_row_count_check": {"check_statement": "COUNT(*) >= 10"},
            "my_column_comparison_check": {
                "check_statement": "MY_COL_1 + MY_COL_2 = 100"
            },
            "date_between_check": {
                "check_statement": "MY_DATE_COL BETWEEN '2017-01-01' AND '2022-01-01'"
            },
        },
    )

    # SQLCheckOperator example: ensure categorical values in MY_COL_3
    # are one of a list of 4 options
    check_val_in_list = SQLCheckOperator(
        task_id="check_today_val_in_bounds",
        sql="""
                WITH

                not_in_list AS (

                SELECT COUNT(*) as count_not_in_list
                FROM {{ params.db_to_query }}.{{ params.schema }}.\
                     {{ params.table }}
                WHERE {{ params.col }} NOT IN {{ params.options_tuple }}
                )

                SELECT
                    CASE WHEN count_not_in_list = 0 THEN 1
                    ELSE 0
                    END AS testresult
                FROM not_in_list
            """,
        params={
            "db_to_query": DB,
            "schema": SCHEMA,
            "table": TABLE,
            "col": "MY_COL_3",
            "options_tuple": "('val1', 'val2', 'val3', 'val4')",
        },
    )

    (
        start
        >> [
            column_checks,
            table_checks,
            check_val_in_list,
        ]
        >> end
    )


example_dag_sql_check_operators()
