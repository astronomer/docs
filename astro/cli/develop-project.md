---
sidebar_label: 'Develop your project'
title: 'Develop your Astro project'
id: develop-project
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

An Astro project contains all of the files necessary to test and run DAGs in a local Airflow environment and on Astro. This guide provides information about adding and organizing Astro project files, including:

- Adding DAGs
- Adding Python and OS-level packages
- Setting environment variables
- Applying changes
- Running on-build commands

For information about running your Astro project in a local Airflow, see [Run Airflow locally](cli/run-airflow-locally.md).

:::tip

As you add to your Astro project, Astronomer recommends reviewing the [Astronomer Registry](https://registry.astronomer.io/), a library of Airflow modules, providers, and DAGs that serve as the building blocks for data pipelines.

The Astronomer Registry includes:

- Example DAGs for many data sources and destinations. For example, you can create a data quality use case with Snowflake and Great Expectations using the [Great Expectations Snowflake Example DAG](https://legacy.registry.astronomer.io/dags/great-expectations-snowflake).
- Documentation for Airflow providers, such as [Databricks](https://registry.astronomer.io/providers/databricks), [Snowflake](https://registry.astronomer.io/providers/snowflake), and [Postgres](https://registry.astronomer.io/providers/postgres). This documentation is comprehensive and based on Airflow source code.
- Documentation for Airflow modules, such as the [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator), [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator), and [S3ToRedshiftOperator](https://registry.astronomer.io/providers/amazon/modules/s3toredshiftoperator). These modules provide guidance on setting Airflow connections and their parameters.

:::

## Prerequisites

- The [Astro CLI](cli/overview.md)

## Create an Astro project

In an empty folder, run the following command to create an Astro project:

```sh
astro dev init
```

This command generates the following files in your directory:

```
.
├── .env # Local environment variables
├── dags # Where your DAGs go
│   ├── example-dag-basic.py # Example DAG that showcases a simple ETL data pipeline
│   └── example-dag-advanced.py # Example DAG that showcases more advanced Airflow features, such as the TaskFlow API
├── Dockerfile # For the Astro Runtime Docker image, environment variables, and overrides
├── include # For any other files you'd like to include
├── plugins # For any custom or community Airflow plugins
│   └── example-plugin.py
├── tests # For any DAG unit test files to be run with pytest
│   └── test_dag_example.py # Test that checks for basic errors in your DAGs
├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
├── packages.txt # For OS-level packages
└── requirements.txt # For Python packages
```

Use the rest of this document to understand how to interact with each of these folders and files. 

## Add DAGs

In Apache Airflow, data pipelines are defined in Python code as Directed Acyclic Graphs (DAGs). A DAG is a collection of tasks and dependencies between tasks that are defined as code. See [Introduction to Airflow DAGs](https://docs.astronomer.io/learn/dags).

DAGs are stored in the `dags` folder of your Astro project. To add a DAG to your project:

1. Add the `.py` file to the `dags` folder.
2. Save your changes. If you're using a Mac, use **Command-S**.
3. Refresh your Airflow browser.

:::tip

Use the `astro run <dag-id>` command to run and debug a DAG from the command line without starting a local Airflow environment. This is an alternative to testing your entire Astro project with the Airflow webserver and scheduler. See [Test your Astro project locally](cli/test-your-astro-project-locally.md).

:::

## Add utility files

Airflow DAGs sometimes require utility files to run workflows. This can include:
 
- SQL files.
- Custom Airflow operators.
- Python functions.
 
When more than one DAG in your Astro project needs a certain function or query, creating a shared utility file helps make your DAGs idempotent, more readable, and minimizes the amount of code you have in each DAG.

You can store utility files in the `/dags` directory of your Astro project. In most cases, Astronomer recommends adding your utility files to the `/dags` directory and organizing them into sub-directories based on whether they're needed for a single DAG or for multiple DAGs.

In the following example, the `dags` folder includes both types of utility files:

```text
└── dags
    ├── my_dag
    │   ├── my_dag.py
    │   └── my_dag_utils.py  # specific DAG utils
    └── utils
        └── common_utils.py # common utils
```

1. To add utility files which are shared between all your DAGs, create a folder named `utils` in the `dags` directory of your Astro project. To add utility files only for a specific DAG, create a new folder in `dags` to store both your DAG file and your utility file. 
2. Add your utility files to the folder you created.
3. Reference your utility files in your DAG code.
4. Apply your changes. If you're developing locally, refresh the Airflow UI in your browser.

Utility files in the `/dags` directory will not be parsed by Airflow, so you don't need to specify them in `.airflowignore` to prevent parsing. If you're using [DAG-only deploys](https://docs.astronomer.io/astro/deploy-code#deploy-dags-only) on Astro, changes to this folder are deployed when you run `astro deploy --dags` and do not require rebuilding your Astro project into a Docker image and restarting your Deployment. 

## Add Airflow connections, pools, variables

Airflow connections connect external applications such as databases and third-party services to Apache Airflow. See [Manage connections in Apache Airflow](https://docs.astronomer.io/learn/connections#airflow-connection-basics) or [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

To add Airflow [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html), [pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html), and [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) to your local Airflow environment, you have the following options:

- Use the Airflow UI. In **Admin**, click **Connections**, **Variables** or **Pools**, and then add your values. These values are stored in the metadata database and are deleted when you run the [`astro dev kill` command](/astro/cli/astro-dev-kill.md), which can sometimes be used for troubleshooting.
- Modify the `airflow_settings.yaml` file of your Astro project. This file is included in every Astro project and permanently stores your values in plain-text. To prevent you from committing sensitive credentials or passwords to your version control tool, Astronomer recommends adding this file to `.gitignore`.
- Use the Cloud UI to create connections that can be shared across Deployments in a Workspace. These connections are not visible in the Airflow UI. See [Create Airflow connections in the Astro Cloud UI](/astro/create-and-link-connections.md).
- Use a secret backend, such as AWS Secrets Manager, and access the secret backend locally. See [Configure an external secrets backend on Astro](/astro/secrets-backend.md).

When you add Airflow objects to the Airflow UI of a local environment or to your `airflow_settings.yaml` file, your values can only be used locally. When you deploy your project to a Deployment on Astro, the values in this file are not included.

Astronomer recommends using the `airflow_settings.yaml` file so that you don’t have to manually redefine these values in the Airflow UI every time you restart your project. To ensure the security of your data, Astronomer recommends [configuring a secrets backend](/astro/secrets-backend.md).

## Add test data or files for local testing

Use the `include` folder of your Astro project to store files for testing locally, such as test data or a dbt project file. The files in your `include` folder are included in your deploys to Astro, but they are not parsed by Airflow. Therefore, you don't need to specify them in `.airflowignore` to prevent parsing. 

If you're running Airflow locally, apply your changes by refreshing the Airflow UI.

### Configure `airflow_settings.yaml` (Local development only)

The `airflow_settings.yaml` file includes a template with the default values for all possible configurations. To add a connection, variable, or pool, replace the default value with your own.

1. Open the `airflow_settings.yaml` file and replace the default value with your own.

    ```yaml

    airflow:
      connections: ## conn_id and conn_type are required
        - conn_id: my_new_connection
          conn_type: postgres
          conn_host: 123.0.0.4
          conn_schema: airflow
          conn_login: user
          conn_password: pw
          conn_port: 5432
          conn_extra:
      pools: ## pool_name and pool_slot are required
        - pool_name: my_new_pool
          pool_slot: 5
          pool_description:
      variables: ## variable_name and variable_value are required
        - variable_name: my_variable
          variable_value: my_value
    
    ```

2. Save the modified `airflow_settings.yaml` file in your code editor. If you use a Mac computer, for example, use **Command-S**.
3. Import these objects to the Airflow UI. Run:

    ```sh
    astro dev object import
    ```

4. In the Airflow UI, click **Connections**, **Pools**, or **Variables** to see your new or modified objects.
5. Optional. To add another connection, pool, or variable, you append it to this file within its corresponding section. To create another variable, add it under the existing `variables` section of the same file. For example:

  ```yaml
  
  variables:
    - variable_name: <my-variable-1>
      variable_value: <my-variable-value>
    - variable_name: <my-variable-2>
      variable_value: <my-variable-value-2>
  
  ```

## Add Python, OS-level packages, and Airflow providers

Most DAGs need additional OS or Python packages to run. There are two primary kinds of Python packages that you might have to add to your Astro project:

- Python libraries. If you’re using Airflow for a data science project, for example, you might use a data science library such as [pandas](https://pandas.pydata.org/) or [NumPy (`numpy`)](https://numpy.org/).
- Airflow providers. Airflow providers are Python packages that contain all relevant Airflow modules for a third-party service. For example, `apache-airflow-providers-amazon` includes the hooks, operators, and integrations you need to access services on Amazon Web Services (AWS) with Airflow. See [Provider packages](https://airflow.apache.org/docs/apache-airflow-providers/).

Adding the name of a package to the `packages.txt` or `requirements.txt` files of your Astro project installs the package to your Airflow environment. Python packages are installed from your `requirements.txt` file using [pip](https://pypi.org/project/pip/).

1. Add the package name to your Astro project. If it’s a Python package, add it to `requirements.txt`. If it’s an OS-level package, add it to `packages.txt`. The latest version of the package that’s publicly available is installed by default.

    To pin a version of a package, use the following syntax:

    ```text
    <package-name>==<version>
    ```

    For example, to install NumPy version 1.23.0, add the following to your `requirements.txt` file:

    ```text
    numpy==1.23.0
    ```

2. [Restart your local environment](#restart-your-local-environment).
3. Confirm that your package was installed:

    ```sh
    astro dev bash --scheduler "pip freeze | grep <package-name>"
    ```

To learn more about the format of the `requirements.txt` file, see [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/#requirements-file-format) in pip documentation. To browse Python libraries, see [PyPi](https://pypi.org/). To browse Airflow providers, see the [Astronomer Registry](https://registry.astronomer.io/providers/).

## Set environment variables locally

For local development, Astronomer recommends setting environment variables in your Astro project’s `.env` file. You can then push your environment variables from the `.env` file to a Deployment on Astro. To manage environment variables in the Cloud UI, see [Environment variables](/astro/environment-variables.md).

If your environment variables contain sensitive information or credentials that you don’t want to expose in plain-text, you can add your `.env` file to `.gitignore` when you deploy these changes to your version control tool.

1. Open the `.env` file in your Astro project directory.
2. Add your environment variables to the `.env` file or run `astro deployment variable list --save` to copy environment variables from an existing Deployment to the file.

    Use the following format when you set environment variables in your `.env` file:

    ```text
    KEY=VALUE
    ```

    Environment variables should be in all-caps and not include spaces.

3. [Restart your local environment](cli/develop-project.md#restart-your-local-environment).
4. Run the following command to confirm that your environment variables were applied locally:
   
    ```sh
    astro dev bash --scheduler "/bin/bash && env"
    ```

   These commands output all environment variables that are running locally. This includes environment variables set on Astro Runtime by default.

5. Optional. Run `astro deployment variable create --load` or `astro deployment variable update --load` to export environment variables from your `.env` file to a Deployment. You can view and modify the exported environment variables in the Cloud UI page for your Deployment.

:::info

For local environments, the Astro CLI generates an `airflow.cfg` file at runtime based on the environment variables you set in your `.env` file. You can’t create or modify `airflow.cfg` in an Astro project.

To view your local environment variables in the context of the generated Airflow configuration, run:

```sh
astro dev bash --scheduler "/bin/bash && cat airflow.cfg"
```

These commands output the contents of the generated `airflow.cfg` file, which lists your environment variables as human-readable configurations with inline comments.

:::

### Use multiple .env files

The Astro CLI looks for `.env` by default, but if you want to specify multiple files, make `.env` a top-level directory and create sub-files within that folder.

A project with multiple `.env` files might look like the following:

```
my_project
├── Dockerfile
├── dags
│   └── my_dag
├── plugins
│   └── my_plugin
├── airflow_settings.yaml
└── .env
    ├── dev.env
    └── prod.env
```

## Add Airflow plugins 

If you need to build a custom view in the Airflow UI or build an application on top of the Airflow metadata database, you can use Airflow plugins. To use an Airflow plugin, add your plugin files to the `plugins` folder of your Astro project. To apply changes from this folder to a local Airflow environment, [restart your local environment](cli/develop-project.md#restart-your-local-environment).

To learn more about Airflow plugins and how to build them, see [Airflow Plugins](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html) in Airflow documentation or the Astronomer [Airflow plugins](https://docs.astronomer.io/learn/using-airflow-plugins) guide.

## Unsupported project configurations 

You can't use `airflow.cfg` or `airflow_local_settings.py` files in an Astro project. `airflow_local_settings.py` has no effect on Astro Deployments, and `airflow.cfg` has no effect on local environments and Astro Deployments. 

An alternative to using `airflow.cfg` is to set Airflow environment variables in your `.env` file. See [Set environment variables locally](#set-environment-variables-locally).
