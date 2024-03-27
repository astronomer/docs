"""
## Toy DAG to show size dependant custom XCom serialization

This DAG pushes two dicts to XCom, one below, one above 1000 bytes. It then pulls them and prints their sizes.
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["xcom", "2-9", "toy"],
)
def custom_xcom_backend_test():
    @task
    def push_objects(**context) -> None:
        """Create a small and a big dictionary, print their sizes and push them to XCom."""

        small_obj = {"a": 23}
        big_obj = {f"key{i}": "x" * 100 for i in range(100)}
        print(f"Size of small object: {small_obj.__sizeof__()}")
        print(f"Size of big object: {big_obj.__sizeof__()}")

        context["ti"].xcom_push(key="small_obj", value=small_obj)
        context["ti"].xcom_push(key="big_obj", value=big_obj)

    @task
    def pull_objects(**context) -> None:
        """Pull the small and big dictionaries from XCom and print their sizes."""

        small_obj = context["ti"].xcom_pull(task_ids="push_objects", key="small_obj")
        big_obj = context["ti"].xcom_pull(task_ids="push_objects", key="big_obj")

        print(f"Size of small object: {small_obj.__sizeof__()}")
        print(f"Size of big object: {big_obj.__sizeof__()}")

    chain(push_objects(), pull_objects())


custom_xcom_backend_test()
