"""
## Toy example of using the @task.virtualenv decorator

The @task.virtualenv decorator is used to run any Python code in a new isolated Python environment.
"""

from airflow.decorators import dag, task
import pandas as pd


@dag(
    start_date=None,
    schedule=None,
    doc_md=__doc__,
    description="@task.virtualenv",
    default_args={
        "owner": "airflow",
        "retries": 0,
    },
    tags=["@task.virtualenv"],
)
def virtualenv_decorator_dag():

    @task
    def upstream_task():
        print(f"The pandas version in the upstream task is: {pd.__version__}")
        return {"num": 1, "word": "hello"}

    @task.virtualenv(requirements=["pandas==1.5.1"])
    def my_isolated_task(upstream_task_output: dict):
        """
        This function runs in an isolated environment.
        Args:
            upstream_task_output (dict): contains a number and a word.
        Returns:
            pd.DataFrame: A dictionary containing the transformed inputs.
        """
        import pandas as pd

        print(f"The pandas version in the virtual env is: {pd.__version__}")

        num = upstream_task_output["num"]
        word = upstream_task_output["word"]

        num_plus_one = num + 1
        word_plus_exclamation = word + "!"

        df = pd.DataFrame(
            {
                "num_plus_one": [num_plus_one],
                "word_plus_exclamation": [word_plus_exclamation],
            },
        )

        return df

    @task
    def downstream_task(arg):
        print(f"The pandas version in the downstream task is: {pd.__version__}")
        return arg

    downstream_task(my_isolated_task(upstream_task_output=upstream_task()))


virtualenv_decorator_dag()
