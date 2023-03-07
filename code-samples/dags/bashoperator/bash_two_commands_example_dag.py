from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime


@dag(start_date=datetime(2022, 8, 1), schedule=None, catchup=False)
def bash_two_commands_example_dag():
    say_hello_and_create_a_secret_number = BashOperator(
        task_id="say_hello_and_create_a_secret_number",
        bash_command="echo Hello $MY_NAME! && echo $A_LARGE_NUMBER | rev  2>&1\
                     | tee $AIRFLOW_HOME/include/my_secret_number.txt",
        env={"MY_NAME": "<my name>", "A_LARGE_NUMBER": "231942"},
        append_env=True,
    )

    say_hello_and_create_a_secret_number


bash_two_commands_example_dag()
