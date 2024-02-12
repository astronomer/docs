"""
## Toy example of using the @task.external_python decorator

The @task.external_python decorator is used to run any Python code in an existing isolated Python environment.
"""

from airflow.decorators import dag, task
import pandas as pd
import sys
import os


@dag(
    start_date=None,
    schedule=None,
    doc_md=__doc__,
    description="@task.external_python",
    default_args={
        "owner": "airflow",
        "retries": 0,
    },
    tags=["@task.external_python"],
)
def external_python_decorator_dag():

    @task
    def upstream_task():
        print(f"The python version in the upstream task is: {sys.version}")
        print(f"The pandas version in the upstream task is: {pd.__version__}")
        return {"num": 1, "word": "hello"}

    @task.external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
    def my_isolated_task(
        upstream_task_output: dict, logical_date
    ):  # note that not all objects from the context can be used!
        """
        This function runs in an isolated environment.
        Args:
            upstream_task_output (dict): contains a number and a word.
            logical_date: The logical_date of the DAG.
        Returns:
            pd.DataFrame: A dictionary containing the transformed inputs.
        """
        import pandas as pd
        import sys

        print(f"The python version in the virtual env is: {sys.version}")
        print(f"The pandas version in the virtual env is: {pd.__version__}")
        print(f"The logical_date is {logical_date}")

        num = upstream_task_output["num"]
        word = upstream_task_output["word"]

        num_plus_one = num + 1
        word_plus_exclamation = word + "!"

        df = pd.DataFrame(
            {
                "num_plus_one": [num_plus_one],
                "word_plus_explamation": [word_plus_exclamation],
            },
        )

        return df

    @task
    def downstream_task(arg):
        print(f"The python version in the downstream task is: {sys.version}")
        print(f"The pandas version in the downstream task is: {pd.__version__}")
        return arg

    downstream_task(my_isolated_task(upstream_task()))


external_python_decorator_dag()
