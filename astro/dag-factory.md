---
sidebar_label: 'DAG Factory'
title: 'Use DAG Factory to create DAGs'
id: dag-factory
description: "Learn how to dynamically generate DAGs using YAML and Python configuration files with DAG Factory"
---

DAG Factory is an open source tool that allows you to dynamically generate DAGs by using YAML files instead of creating DAGs with Python. See more about [DAG Factory](https://github.com/astronomer/dag-factory).

## Prerequisites

- Python version 3.6.0 or greater
- Airflow version 2.0 or greater

## Step 1: Install DAG Factory

```python

pip install dag-factory

```

## Step 2: Install DAG Facotry in your Airflow environment

- this step is missing from GitHub

## Step 3: Create a DAG using DAG Factory

1. Create a YAML configuration file in your Airflow project. The following YAML file shows an example configuration file.

```YAML
example_dag1:
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

2. Create a Python file with the `dag_factory.clean_dags(globals())` and `dag_factory.generate_dags(globals())` commands. This Python script generates DAGs from your YAML file.

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
