import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from pendulum import datetime


def uploadtomongo(ti, **context):
    hook = MongoHook(mongo_conn_id="mongo_default")
    client = hook.get_conn()
    db = client.MyDB  # Replace "MyDB" if you want to load data to a different database
    currency_collection = db.currency_collection
    print(f"Connected to MongoDB - {client.server_info()}")
    d = json.loads(context["result"])
    currency_collection.insert_one(d)


with DAG(
    dag_id="load_data_to_mongodb",
    schedule=None,
    start_date=datetime(2022, 10, 28),
    catchup=False,
    default_args={
        "retries": 0,
    },
):
    t1 = SimpleHttpOperator(
        task_id="get_currency",
        method="GET",
        endpoint="2022-01-01..2022-06-30",
        headers={"Content-Type": "application/json"},
        do_xcom_push=True,
    )

    t2 = PythonOperator(
        task_id="upload-mongodb",
        python_callable=uploadtomongo,
        op_kwargs={"result": t1.output},
    )

    t1 >> t2
