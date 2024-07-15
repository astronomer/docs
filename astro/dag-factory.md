---
sidebar_label: 'DAG Factory'
title: 'Use DAG Factory to create DAGs'
id: dag-factory
description: "Learn how to dynamically convert YAML files into Apache Airflow DAGs with the DAG Factory, an open source project that makes creating DAGs easy.
---

The DAG Factory is an open source tool managed by Astronomer that allows you to dynamically generate Apache Airflow DAGs from YAML. While Airflow DAGs are traditionally written exclusively in Python, the DAG Factory makes it easy for people who don't know Python to use Airflow.

This guide includes instructions for installing the DAG Factory package into your Astro project and a sample YAML configuration file that you can use to easily specify the details of your DAG, including schedule interval, callbacks, and task names.

The DAG Factory can be used with all Astronomer products and any Apache Airflow installation. To view the source code of the project, see [DAG Factory](https://github.com/astronomer/dag-factory).

## Prerequisites

- Python version 3.6.0 or greater
- Apache Airflow version 2.0 or greater

If you're an Astronomer customer, you must have an Astro project with a supported version of Astro Runtime.

## Step 1: Install DAG Factory

To use the DAG Factory, install it as a Python package into your Apache Airflow environment.

If you're an Astronomer customer:

1. In your Astro project, open your `requirements.txt` file.
2. Add `dag-factory` to the file.
3. Save the changes to your `requirements.txt`.

If you're not an Astronomer customer, install the Python package according to the standards at your organization:

```python

pip install dag-factory

```

## Step 2: Create a YAML file for your DAG

1. In the `dags` directory of your Astro project, create a new YAML file for each DAG you want to create. For example, `my_dag.yaml`. Astronomer recommends creating a new sub-directory for all of your DAGs defined in YAML and keeping them separate from standard DAG files written in Python.
2. Copy the contents of the following example configuration file into each YAML file.

```YAML
<your-DAG-name>:
  default_args:
    owner: 'example_owner'
    start_date: 2018-01-01  # or '2 days'
    end_date: 2018-01-05
    retries: 1
    retry_delay_sec: 300
  schedule_interval: '0 3 * * *'
  concurrency: 1
  max_active_runs: 1
  dagrun_timeout_sec: 60
  default_view: 'tree'  # or 'graph', 'duration', 'gantt', 'landing_times'
  orientation: 'LR'  # or 'TB', 'RL', 'BT'
  description: 'this is an example dag!'
  on_success_callback_name: print_hello
  on_success_callback_file: /usr/local/airflow/dags/print_hello.py
  on_failure_callback_name: print_hello
  on_failure_callback_file: /usr/local/airflow/dags/print_hello.py
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

3. Modify the example configuration file with details for the DAG you want to create, including replacing `<your-DAG-name>`. In order for your DAG to run, the following fields are required:

- DAG name
- `start_date`
- `end_date`
- `schedule_interval`
- `tasks`

4. (Optional) Delete any configurations that you don't want or need to specify. For configurations that aren't specified, your DAG will assume the default values that correspond with your current Apache Airflow or Astro Runtime version.

## Step 3. Create a DAG Factory file

All YAML files in your `dags` directory must be parsed and converted into Python in order to run on Apache Airflow. In this step, you will create a new DAG Factory file in your Astro project that includes the conversion logic. You only need to do this once and do not need a separate DAG Factory file for each of your DAGs or YAML files.

1. In the `dags` directory of your Astro project, create a new Python file called `dag_factory.py`.
2. Copy the following contents into your empty Python file. This file represents an Apache Airflow DAG and includes two commands that convert each of your YAML file(s) into DAGs.

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

    # 'airflow' is required for the dagbag to parse this file
    from dagfactory import load_yaml_dags

    load_yaml_dags(globals_dict=globals(), suffix=['dag.yaml'])

    ```
