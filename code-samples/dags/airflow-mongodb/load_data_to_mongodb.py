import json
from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from pendulum import datetime


@dag(
    dag_id="load_data_to_mongodb",
    schedule=None,
    start_date=datetime(2022, 10, 28),
    catchup=False,
    default_args={
        "retries": 0,
    },
)
def load_data_to_mongodb():
    t1 = SimpleHttpOperator(
        task_id="get_currency",
        method="GET",
        endpoint="2022-01-01..2022-06-30",
        headers={"Content-Type": "application/json"},
        do_xcom_push=True,
    )

    @task
    def uploadtomongo(result):
        hook = MongoHook(mongo_conn_id="mongo_default")
        client = hook.get_conn()
        db = (
            client.MyDB
        )  # Replace "MyDB" if you want to load data to a different database
        currency_collection = db.currency_collection
        print(f"Connected to MongoDB - {client.server_info()}")
        d = json.loads(result)
        currency_collection.insert_one(d)

    t1 >> uploadtomongo(result=t1.output)


load_data_to_mongodb()
