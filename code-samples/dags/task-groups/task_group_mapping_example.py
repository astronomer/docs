from airflow.decorators import dag, task_group, task
from pendulum import datetime


@dag(
    start_date=datetime(2022, 12, 1),
    schedule=None,
    catchup=False,
)
def task_group_mapping_example():
    # creating a task group using the decorator with the dynamic input my_num
    @task_group(group_id="group1")
    def tg1(my_num):
        @task
        def print_num(num):
            return num

        @task
        def add_42(num):
            return num + 42

        print_num(my_num) >> add_42(my_num)

    # a downstream task to print out resulting XComs
    @task
    def pull_xcom(**context):
        pulled_xcom = context["ti"].xcom_pull(
            # reference a task in a task group with task_group_id.task_id
            task_ids=["group1.add_42"],
            # only pull Xcom from specific mapped task group instances (2.5 feature)
            map_indexes=[2, 3],
            key="return_value",
        )

        # will print out a list of results from map index 2 and 3 of the add_42 task
        print(pulled_xcom)

    # creating 6 mapped task group instances of the task group group1 (2.5 feature)
    tg1_object = tg1.expand(my_num=[19, 23, 42, 8, 7, 108])

    # setting dependencies
    tg1_object >> pull_xcom()


task_group_mapping_example()
