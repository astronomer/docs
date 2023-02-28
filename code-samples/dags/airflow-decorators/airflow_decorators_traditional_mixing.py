import logging
from datetime import datetime
from typing import Dict

import requests
from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator

API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"


@dag(schedule="@daily", start_date=datetime(2021, 12, 1), catchup=False)
def taskflow():
    @task(task_id="extract", retries=2)
    def extract_bitcoin_price() -> Dict[str, float]:
        return requests.get(API).json()["bitcoin"]

    @task(multiple_outputs=True)
    def process_data(response: Dict[str, float]) -> Dict[str, float]:
        logging.info(response)
        return {"usd": response["usd"], "change": response["usd_24h_change"]}

    @task
    def store_data(data: Dict[str, float]):
        logging.info(f"Store: {data['usd']} with change {data['change']}")

    email_notification = EmailOperator(
        task_id="email_notification",
        to="noreply@astronomer.io",
        subject="dag completed",
        html_content="the dag has finished",
    )

    store_data(process_data(extract_bitcoin_price())) >> email_notification


taskflow()
