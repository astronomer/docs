from pendulum import datetime
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
    params={"upstream_color": "Manual run, no upstream color available."},
)
def tdro_example_downstream():
    @task
    def print_color(**context):
        print(context["params"]["upstream_color"])

    print_color()


tdro_example_downstream()
