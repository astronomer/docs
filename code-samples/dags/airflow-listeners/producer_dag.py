"""
## DAG to produce to a Dataset showcasing the on_dataset_changed listener

This DAG will produce to a Dataset, updating it which triggers the 
on_dataset_changed listener define as an Airflow Plugin.

The DAG also shows the difference between a Dataset and ObjectStoragePath.
"""

from airflow.datasets import Dataset
from airflow.decorators import dag, task
from airflow.io.path import ObjectStoragePath
from pendulum import datetime
import requests


URI = "file://include/bears"
MY_DATASET = Dataset(URI)
base_local = ObjectStoragePath(URI)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * 0",
    catchup=False,
    doc_md=__doc__,
    tags=["on_dataset_changed listener", "2-8"],
)
def producer_dag():
    @task(
        outlets=[MY_DATASET],
    )
    def get_bear(base):
        r = requests.get("https://placebear.com/200/300")
        file_path = base / "bear.jpg"

        if r.status_code == 200:
            base.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(r.content)
            file_path.replace("bear.jpg")
        else:
            print(f"Failed to retrieve image. Status code: {r.status_code}")

    get_bear(base=base_local)


producer_dag()
