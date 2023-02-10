from __future__ import annotations

import logging
import os
import sys
import tempfile
import time
import shutil
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

PYTHON = sys.executable

BASE_DIR = tempfile.gettempdir()

with DAG(
    dag_id="py_virtual_env",
    schedule=None,
    start_date=pendulum.datetime(2022, 10, 10, tz="UTC"),
    catchup=False,
    tags=["pythonvirtualenv"],
):

    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        print(kwargs)
        print(ds)
        return "Whatever you return gets printed in the logs"

    @task.external_python(
        task_id="external_python",
        python="/home/astro/.pyenv/versions/snowpark_env/bin/python",
    )
    def callable_external_python():
        from time import sleep
        import pkg_resources
        from snowflake.snowpark import Session

        import boto3
        import json

        ## Checking for the correct venv packages - this is useful for debugging
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(
            ["%s==%s" % (i.key, i.version) for i in installed_packages]
        )
        print(installed_packages_list)

        # Retrieving connection information from the external secrets manager
        ssm = boto3.client("ssm", region_name="us-east-1")
        parameter = ssm.get_parameter(
            Name="/airflow/connections/snowflake", WithDecryption=True
        )
        conn = json.loads(parameter["Parameter"]["Value"])

        # Defining parameters for Airflow's Snowpark connection
        connection_parameters = {
            "account": conn["extra"]["account"],
            "user": conn["login"],
            "password": conn["password"],
            "role": conn["extra"]["role"],
            "warehouse": conn["extra"]["warehouse"],
            "database": conn["extra"]["database"],
            "schema": conn["schema"],
            "region": conn["extra"]["region"],
        }
        # Creating a connection session between Snowpark and Airflow
        session = Session.builder.configs(connection_parameters).create()
        # Running a SQL query in Snowpark
        df = session.sql(
            "select avg(reps_upper), avg(reps_lower) from dog_intelligence;"
        )
        print(df.collect())
        # Closing the connection session
        session.close()

    task_print = print_context()
    task_external_python = callable_external_python()

    task_print >> task_external_python
