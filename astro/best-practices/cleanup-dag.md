---
title: 'Cleaning up your Airflow Database with a Cleanup DAG'
sidebar_label: 'Cleanup DAG'
id: cleanup-dag
---

```python
"""A Cleanup DAG used and maintained by Astronomer. All tasks in this DAG are executed by workers in the default worker queue."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="astronomer_cleanup_dag",
    schedule_interval=None,
    start_date=days_ago(2),
    catchup=False,
    is_paused_upon_creation=False,
    dagrun_timeout=timedelta(minutes=30),
    description=__doc__,
    doc_md=__doc__,
    tags=["cleanup"],
) as dag:
    clean_db = BashOperator(
        task_id="clean_db",
        bash_command="airflow db clean --clean-before-timestamp {{ macros.ds_add(ds, -90) }} --verbose --yes",
        depends_on_past=False,
        priority_weight=2**31 - 1,
        do_xcom_push=False,
    )

```
