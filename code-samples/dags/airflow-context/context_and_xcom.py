from pendulum import datetime
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
)
def context_and_xcom():
    @task
    def upstream_task(**context):
        context["ti"].xcom_push(key="my_explicitly_pushed_xcom", value=23)
        return 19

    @task
    def downstream_task(passed_num, **context):
        returned_num = context["ti"].xcom_pull(
            task_ids="upstream_task", key="return_value"
        )
        explicit_num = context["ti"].xcom_pull(
            task_ids="upstream_task", key="my_explicitly_pushed_xcom"
        )

        print("Returned Num: ", returned_num)
        print("Passed Num: ", passed_num)
        print("Explicit Num: ", explicit_num)

    downstream_task(upstream_task())


context_and_xcom()
