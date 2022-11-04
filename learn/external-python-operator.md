---
title: "Use the ExternalPythonOperator"
sidebar_label: "ExternalPythonOperator"
description: "Learn how to run Airflow tasks in virtual Python environments using the ExternalPythonOperator."
id: external-python-operator
---

It is very common in data science and data engineering use cases to need to run a task with different requirements from your Airflow environment. Your task may need a different Python version than Airflow, or require packages that conflict with core Airflow or your other tasks. In these cases, running tasks in an isolated environment can help manage dependency conflicts and enable compatibility with your execution environments.

In this tutorial, you'll learn how to use the [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#externalpythonoperator) to run a task that leverages the Snowpark API for data transformations. Snowpark requires Python 3.8, while Airflow will be using Python 3.9. The ExternalPythonOperator will run a task in an existing Python virtual environment, allowing you to choose a different Python version for a particular task. Note that the general steps presented here could be applied to any other use case for running a task in an isolated Python virtual environment.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Python virtual environments. See [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).

## Prerequisites

To complete this tutorial, you need:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Snowflake Enterprise account. If you don't already have an account, Snowflake has a [free Snowflake trial](https://signup.snowflake.com/) for 30 days.

## Step 1: Set up your data stores

## Step 2: Create your Astro project

Now that you have your Snowflake resources configured, you can move on to setting up Airflow.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowpark-tutorial && cd astro-snowpark-tutorial
    $ astro dev init
    ```

2. Update the `Dockerfile` of your Astro project to install `pyenv` and its requirements:

    ```text
    FROM quay.io/astronomer/astro-runtime:5.0.9

    ##### Docker Customizations below this line #####

    ## The directory where `pyenv` will be installed. You can update the path as needed
    ENV PYENV_ROOT="/home/astro/.pyenv" 
    ENV PATH=${PYENV_ROOT}/bin:${PATH}

    # RUN pip-compile -h
    # RUN pip-compile snowpark_requirements.txt

    ## Install the required version of pyenv and create the virtual environment
    RUN curl https://pyenv.run | bash  && \
        eval "$(pyenv init -)" && \
        pyenv install 3.8.14 && \
        pyenv virtualenv 3.8.14 snowpark_env && \
        pyenv activate snowpark_env && \
        pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir -r snowpark_requirements.txt
    ```

    These commands install `pyenv` in your Airflow environment and create a virtual environment called `snowpark_env` that will be used by the ExternalPythonOperator. The `pyenv` environment will be created when you start your Airflow project, and can be used by any number of ExternalPythonOperator tasks. If you use a different virtual environment package (e.g. `venv` or `conda`) you may need to update this step.

3. Add the following to your `packages.txt` file:

    ```text
    git
    make
    build-essential
    libssl-dev
    zlib1g-dev
    libbz2-dev
    libreadline-dev
    libsqlite3-dev
    wget
    curl
    llvm
    libncurses5-dev
    libncursesw5-dev
    xz-utils
    tk-dev
    libpq-dev
    krb5-config
    ```

    This installs all the needed packages to run `pyenv` in your Airflow environment.

4. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 3: Create your DAG

## Step 4: Run your DAG to execute your Snowpark query in a virtual environment

1. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```



## Other methods for running tasks in isolated environments

Airflow has several other options for running tasks in isolated environments. Which you choose will depend on your use case and your Airflow infrastructure.

- [The KubernetesPodOperator](https://docs.astronomer.io/learn/kubepod-operator). This operator is ideal for users who are running Airflow on Kubernetes and want more control over the resources and infrastructure used to run the task in addition to package management. Downsides include more complex setup and higher task latency.
- [The PythonVirtualenvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator). This operator works similarly to the ExternalPythonOperator, but it creates and destroys a new virtual environment for each task. This operator is ideal if you don't want to persist your virtual environment. Downsides include higher task latency since the environment must be created each time the task is run.
