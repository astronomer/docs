from airflow import DAG
from pendulum import datetime

from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import (
    SQLColumnCheckOperator,
    SQLTableCheckOperator,
    SQLCheckOperator,
)

example_connection = "my_db_conn"
example_database = "my_db"
example_schema = "my_schema"
example_table = "my_table"

with DAG(
    dag_id="example_dag_sql_check_operators",
    schedule="@daily",
    start_date=datetime(2022, 7, 15),
    catchup=False,
    doc_md="""
    Example DAG for SQL Check operators.
    """,
    default_args={"conn_id": example_connection},
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # SQLColumnCheckOperator example: runs checks on 3 columns:
    #   - MY_DATE_COL is checked to only contain unique values ("unique_check")
    #     and to have dates greater than 2017-01-01 and lesser than 2022-01-01.
    #   - MY_TEXT_COL is checked to contain no NULL values
    #     and at least 10 distinct values
    #   - MY_NUM_COL is checked to have a minimum value between 90 and 110
    column_checks = SQLColumnCheckOperator(
        task_id="column_checks",
        table=example_table,
        column_mapping={
            "MY_DATE_COL": {
                "min": {"greater_than": datetime.date(2017, 1, 1)},
                "max": {"less_than": datetime.date(2022, 1, 1)},
                "unique_check": {"equal_to": 0},
            },
            "MY_TEXT_COL": {
                "distinct_check": {"geq_to": 10},
                "null_check": {"equal_to": 0},
            },
            "MY_NUM_COL": {"max": {"equal_to": 100, "tolerance": 0.1}},
        },
    )

    # SQLTableCheckOperator example: This operator performs one check:
    #   - a row count check, making sure the table has >= 1000 rows
    table_checks_aggregated = SQLTableCheckOperator(
        task_id="table_checks_aggregated",
        table=example_table,
        checks={"my_row_count_check": {"check_statement": "COUNT(*) >= 1000"}},
    )

    # SQLTableCheckOperator example: This operator performs one check:
    #   - a columns comparison check to see that the value in MY_COL_1 plus
    #   the value in MY_COL_2 is 100
    table_checks_not_aggregated = SQLTableCheckOperator(
        task_id="table_checks_not_aggregated",
        table=example_table,
        checks={
            "my_column_comparison_check": {
                "check_statement": "MY_COL_1 + MY_COL_2 = 100"
            }
        },
    )

    # SQLCheckOperator example: ensure categorical values in MY_COL_3
    # are one of a list of 4 options
    check_val_in_list = SQLCheckOperator(
        task_id="check_today_val_in_bounds",
        conn_id=example_connection,
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
            "db_to_query": example_database,
            "schema": example_schema,
            "table": example_table,
            "col": "MY_COL_3",
            "options_tuple": "('val1', 'val2', 'val3', 'val4')",
        },
    )

    (
        start
        >> [
            column_checks,
            table_checks_aggregated,
            table_checks_not_aggregated,
            check_val_in_list,
        ]
        >> end
    )
