from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime


@dag(
    dag_id="print_ISS_info_dag",
    start_date=datetime(2022, 8, 1),
    schedule=None,
    catchup=False,
)
def print_ISS_info_dag():
    # Use the node command to execute the JavaScript file from the command line
    get_ISS_coordinates = BashOperator(
        task_id="get_ISS_coordinates",
        bash_command="node $AIRFLOW_HOME/include/my_java_script.js",
    )

    # Use the Rscript command to execute the R file which is being provided
    # with the result from task one via an environment variable via XComs
    print_ISS_coordinates = BashOperator(
        task_id="print_ISS_coordinates",
        bash_command="Rscript $AIRFLOW_HOME/include/my_R_script.R $ISS_COORDINATES",
        env={
            "ISS_COORDINATES": "{{ task_instance.xcom_pull(\
                               task_ids='get_ISS_coordinates', \
                               key='return_value') }}"
        },
        # set append_env to True to be able to use env variables
        # like AIRFLOW_HOME from the Airflow environment
        append_env=True,
    )

    get_ISS_coordinates >> print_ISS_coordinates


print_ISS_info_dag()
