from pendulum import datetime
from airflow.decorators import dag
from airflow.operators.python import PythonOperator


def print_color_func(**context):
    print(context["params"]["upstream_color"])


@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
    params={"upstream_color": "Manual run, no upstream color available."},
)
def tdro_example_downstream_traditional():
    PythonOperator(
        task_id="print_color",
        python_callable=print_color_func,
    )


tdro_example_downstream_traditional()
