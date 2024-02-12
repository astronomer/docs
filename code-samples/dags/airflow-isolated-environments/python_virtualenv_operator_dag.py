"""
## Toy example of using the PythonVirtualenvOperator

The PythonVirtualenvOperator is used to run any Python code in a new isolated Python environment.
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonVirtualenvOperator
import pandas as pd
import sys


def my_isolated_function(num: int, word: str) -> dict:
    """
    This function will be passed to the PythonVirtualenvOperator to
    run in an isolated environment.
    Args:
        num (int): An integer to be incremented by 1.
        word (str): A string to have an exclamation mark added to it.
    Returns:
        pd.DataFrame: A dictionary containing the transformed inputs.
    """
    import pandas as pd

    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num_plus_one = num + 1
    word_plus_exclamation = word + "!"

    df = pd.DataFrame(
        {
            "num_plus_one": [num_plus_one],
            "word_plus_exclamation": [word_plus_exclamation],
        },
    )

    return df


@dag(
    start_date=None,
    schedule=None,
    doc_md=__doc__,
    description="PythonVirtualenvOperator",
    render_template_as_native_obj=True,
    default_args={
        "owner": "airflow",
        "retries": 0,
    },
    tags=["PythonVirtualenvOperator"],
)
def python_virtualenv_operator_dag():

    @task
    def upstream_task():
        print(f"The python version in the upstream task is: {sys.version}")
        print(f"The pandas version in the upstream task is: {pd.__version__}")
        return {"num": 1, "word": "hello"}

    my_isolated_task = PythonVirtualenvOperator(
        task_id="my_isolated_task",
        python_callable=my_isolated_function,
        requirements=[
            "pandas==1.5.1",
        ],
        op_kwargs={
            "num": "{{ ti.xcom_pull(task_ids='upstream_task')['num']}}",  # note that render_template_as_native_obj=True in the DAG definition
            "word": "{{ ti.xcom_pull(task_ids='upstream_task')['word']}}",
        },
    )

    @task
    def downstream_task(arg):
        print(f"The python version in the downstream task is: {sys.version}")
        print(f"The pandas version in the downstream task is: {pd.__version__}")
        return arg

    chain(upstream_task(), my_isolated_task, downstream_task(my_isolated_task.output))


python_virtualenv_operator_dag()
