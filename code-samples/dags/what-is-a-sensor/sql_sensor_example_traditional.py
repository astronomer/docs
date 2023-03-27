from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor

from typing import Dict
from pendulum import datetime


def _success_criteria(record):
    return record


def _failure_criteria(record):
    return True if not record else False


with DAG(
    dag_id="partner",
    description="DAG in charge of processing partner data",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,
):
    waiting_for_partner = SqlSensor(
        task_id="waiting_for_partner",
        conn_id="postgres",
        sql="sql/CHECK_PARTNER.sql",
        parameters={"name": "partner_a"},
        success=_success_criteria,
        failure=_failure_criteria,
        fail_on_empty=False,
        poke_interval=20,
        mode="reschedule",
        timeout=60 * 5,
    )

    def validation_function() -> Dict[str, str]:
        return {"partner_name": "partner_a", "partner_validation": True}

    validation = PythonOperator(
        task_id="validation", python_callable=validation_function
    )

    def storing_function():
        print("storing")

    storing = PythonOperator(task_id="storing", python_callable=storing_function)

    waiting_for_partner >> validation >> storing
