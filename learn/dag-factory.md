---
sidebar_label: 'DAG Factory'
title: 'Use DAG Factory to create DAGs'
id: dag-factory
description: "Learn how to dynamically convert YAML files into Apache Airflow® DAGs with the DAG Factory, an open source project that makes creating DAGs easy."
---

The DAG Factory is an open source tool managed by Astronomer that allows you to [dynamically generate](dynamically-generating-dags.md) [Apache Airflow®](https://airflow.apache.org/) DAGs from YAML. While Airflow DAGs are traditionally written exclusively in Python, the DAG Factory makes it easy for people who don't know Python to use Airflow.

This guide includes instructions for installing the DAG Factory package into your Astro project and a sample YAML configuration file that you can use to easily specify the details of your DAG, including its schedule, callbacks, and task names.

The DAG Factory can be used with all Astronomer products and any Apache Airflow installation. To view the source code of the project, see [DAG Factory](https://github.com/astronomer/dag-factory).

## Prerequisites

- Python version 3.6.0 or greater
- Apache Airflow version 2.0 or greater

If you're an Astronomer customer, you must have an Astro project with a supported version of Astro Runtime. See [Astro Runtime lifecycle schedule](https://www.astronomer.io/docs/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule) for a list of currently supported Runtime versions.

## Step 1: Install DAG Factory

To use the DAG Factory, install it as a Python package into your Apache Airflow environment.

If you're an Astronomer customer:

1. In your Astro project, open your `requirements.txt` file.
2. Add `dag-factory==0.19.0` to the file.
3. Save the changes to your `requirements.txt` file.

If you're not an Astronomer customer, install the Python package according to the standards at your organization:

```python

pip install dag-factory==0.19.0

```

## Step 2: Create a YAML file for your DAG

1. In the `dags` directory of your Astro project, create a new YAML file for each DAG you want to create. For example, `my_dag.yaml`. Astronomer recommends creating a new sub-directory for all of your DAGs defined in YAML and keeping them separate from standard DAG files written in Python.
2. Copy the contents of the following example configuration file into each YAML file.

```YAML
<your-DAG-id>:
  default_args:
    owner: 'example_owner'
    start_date: 2024-07-01  # or '2 days'
    end_date: 2030-01-01
    retries: 1
    retry_delay_sec: 300
  schedule_interval: '0 3 * * *'
  catchup: False
  concurrency: 1
  max_active_runs: 1
  dagrun_timeout_sec: 60
  default_view: 'grid'  # or 'graph', 'duration', 'gantt', 'landing_times' (for Run Duration in newer versions)
  orientation: 'LR'  # or 'TB', 'RL', 'BT'
  description: 'This is an example dag!'
  # to use callbacks you will need to complete Step 4 of this tutorial
  on_success_callback_name: placeholder_callback
  on_success_callback_file: /usr/local/airflow/dags/callback_func.py
  on_failure_callback_name: placeholder_callback
  on_failure_callback_file: /usr/local/airflow/dags/callback_func.py
  tasks:
    task_1:
      operator: airflow.operators.bash_operator.BashOperator
      bash_command: 'echo 1'
    task_2:
      operator: airflow.operators.bash_operator.BashOperator
      bash_command: 'echo 2'
      dependencies: [task_1]
    task_3:
      operator: airflow.operators.bash_operator.BashOperator
      bash_command: 'echo 3'
      dependencies: [task_1]

```

3. Modify the example configuration file with parameters for the DAG you want to create, including replacing `<your-DAG-id>` with a valid `dag_id`. See [DAG-level parameters in Airflow](airflow-dag-parameters.md) to learn more about each parameter.

4. (Optional) Delete any configurations that you don't want to specify. For parameters that aren't specified, your DAG will assume the default values that correspond with your current Apache Airflow or Astro Runtime version.

## Step 3: Create a DAG Factory file

All YAML files in your `dags` directory must be parsed and converted into Python in order to run on Apache Airflow. In this step, you will create a new DAG Factory file in your Astro project that includes the conversion logic. You only need to do this once and do not need a separate DAG Factory file for each of your DAGs or YAML files.

1. In the `dags` directory of your Astro project, create a new Python file called `dag_factory.py`.
2. Copy the following contents into your empty Python file. This file represents an Apache Airflow DAG and includes two commands that convert each of your YAML file(s) into DAGs. Make sure to replace `/path/to/dags/config_file.yml` with the absolute path to your config file. For Astro CLI users the absolute path to the DAG directory is `/usr/local/airflow/dags`. 

```python

from airflow import DAG
import dagfactory

dag_factory = dagfactory.DagFactory("/path/to/dags/config_file.yml")

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())

```

    :::tip Multiple config files

    If you have multiple YAML configuration files, you can import them with the following code:

    ```python

    # 'airflow' is required for the dagbag to parse this file - do not remove this comment
    from dagfactory import load_yaml_dags

    load_yaml_dags(globals_dict=globals(), suffix=['dag.yaml'])

    ```

## Step 4: Add a DAG-level callback

In order to use [DAG-level callbacks](https://www.astronomer.io/docs/learn/error-notifications-in-airflow#airflow-callbacks) you need to add the file referenced in the `on_success_callback_file` and `on_failure_callback_file` parameters of the YAML configuration file.

1. Create a new file `callback_func.py` in your `dags` directory. 
2. Copy the contents of the following placeholder callback into the file:

```python
def placeholder_callback():
    pass
```

3. Save the file.