from airflow.decorators import dag, task
from pendulum import datetime
from include.custom_task_group import MyCustomMathTaskGroup


@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
    tags=["@task_group", "task_group"],
)
def custom_tg():
    @task
    def get_num_1():
        return 5

    tg1 = MyCustomMathTaskGroup(group_id="my_task_group", num1=get_num_1(), num2=19)

    @task
    def downstream_task():
        return "hello"

    tg1 >> downstream_task()


custom_tg()