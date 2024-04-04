---
title: "Cleaning up your Airflow Database with a Cleanup DAG"
sidebar_label: "Cleanup DAG"
id: cleanup-dag
---

```python
"""A Cleanup DAG maintained by Astronomer. Note that the database statement timeout is set to 5 minutes. This is to prevent the cleanup from hindering other operations. If you have large tables you want to clean, you may need to run the cleanup in smaller batches."""

from datetime import UTC, datetime, timedelta

from airflow.cli.commands.db_command import all_tables
from airflow.decorators import dag
from airflow.models.param import Param
from airflow.operators.bash import BashOperator


@dag(
    dag_id="astronomer_cleanup_dag",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    is_paused_upon_creation=False,
    description=__doc__,
    doc_md=__doc__,
    tags=["cleanup"],
    params={
        "clean_before_timestamp": Param(
            default=datetime.now(tz=UTC) - timedelta(days=90),
            type="string",
            format="date-time",
            description="Delete records older than this timestamp. Default is 90 days ago.",
        ),
        "tables": Param(
            default=[],
            type=["null", "array"],
            examples=all_tables,
            description="List of tables to clean. Default is all tables.",
        ),
        "dry_run": Param(
            default=False,
            type="boolean",
            description="Print the SQL queries that would be run, but do not execute them. Default is False.",
        ),
    },
)
def astronomer_cleanup_dag():
    BashOperator(
        task_id="clean_db",
        bash_command="""\
            airflow db clean \
             --clean-before-timestamp {{ params.clean_before_timestamp }} \
        {% if params.dry_run -%}
             --dry-run \
        {% endif -%}
             --skip-archive \
        {% if params.tables -%}
             --tables {{ params.tables|join(', ') }} \
        {% endif -%}
             --verbose \
             --yes \
        """,
        do_xcom_push=False,
    )


astronomer_cleanup_dag()

```
