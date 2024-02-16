from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime


@dag(start_date=datetime(2022, 8, 1), schedule=None, catchup=False)
def bash_script_example_dag():
    execute_my_script = BashOperator(
        task_id="execute_my_script",
        # Note the space at the end of the command!
        bash_command="$AIRFLOW_HOME/include/my_bash_script.sh ",
        # since the env argument is not specified, this instance of the
        # BashOperator has access to the environment variables of the Airflow
        # instance like AIRFLOW_HOME
    )

    execute_my_script


bash_script_example_dag()
