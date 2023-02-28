from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain
from pendulum import datetime


@dag(start_date=datetime(2023, 1, 1), schedule="@daily", catchup=False)
def dependencies():
    t0 = EmptyOperator(task_id="t0")
    t1 = EmptyOperator(task_id="t1")
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")
    t4 = EmptyOperator(task_id="t4")
    t5 = EmptyOperator(task_id="t5")
    t6 = EmptyOperator(task_id="t6")

    chain(t0, t1, [t2, t3], [t4, t5], t6)


dependencies()
