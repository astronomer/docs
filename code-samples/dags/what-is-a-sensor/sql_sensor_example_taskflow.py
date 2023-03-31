from airflow.decorators import task, dag
from airflow.providers.common.sql.sensors.sql import SqlSensor

from typing import Dict
from pendulum import datetime


def _success_criteria(record):
    return record


def _failure_criteria(record):
    return True if not record else False


@dag(
    description="DAG in charge of processing partner data",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,
)
def partner():
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

    @task
    def validation() -> Dict[str, str]:
        return {"partner_name": "partner_a", "partner_validation": True}

    @task
    def storing():
        print("storing")

    waiting_for_partner >> validation() >> storing()


partner()
