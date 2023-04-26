from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime, duration


@dag(
    start_date=datetime(2023, 4, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 3,
        "retry_delay": duration(seconds=10),
        "retry_exponential_backoff": True,
        "max_retry_delay": duration(hours=2),
    },
)
def retry_example():
    t1 = BashOperator(task_id="t1", bash_command="echo I get 3 retries!")

    t2 = BashOperator(
        task_id="t2",
        bash_command="echo I get 6 retries and never wait long!",
        retries=6,
        max_retry_delay=duration(seconds=20),
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo I wait exactly an hour between each of my 4 retries!",
        retries=4,
        retry_delay=duration(hours=1),
        retry_exponential_backoff=False,
    )

    t4 = BashOperator(
        task_id="t4",
        bash_command="echo I have to get it right the first time!",
        retries=0,
    )


retry_example()
