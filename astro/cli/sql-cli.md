---
sidebar_label: 'Run SQL models'
title: 'Run SQL models with the Astro CLI'
id: sql-cli
description: The Astro CLI can start up a local environment for testing SQL queries. Use YAML configuration and CLI commands to reliably run SQL in Airflow without having to write python. 
---

:::caution 

This feature is in alpha and is not yet recommended for production workflows.

:::

Use the Astro CLI's SQL commands to run SQL workflows without having to write Python or set up Airflow. The Astro CLI handles all of the required backend configuration for running SQL locally using Airflow's reliability and observability. Using an Airflow connection, you can output the results of your SQL queries to the database of your choice. 

## Prerequisites 

To use the Astro CLI's SQL commands, you need

- The Astro CLI
- Docker
- An external database service which uses one of the following databases:
- 
    - Postgres
    - SQlite
    - BigQuery
    - Snowflake
    - Redshift

## Enable Astro SQL commands 

To enable Astro SQL commands, run the following command: 

```sh
astro config set -g beta.sql_cli true
```

## Create a new SQL project 

A SQL project contains the set of files necessary to run SQL queries from the Astro CLI, including YAML files for configuring your SQL environment and directories for storing SQL workflows. A SQL project can exist as its own top-level directory or within an existing Astro project. 

To create a SQL project, run the following command in either an empty directory or an existing Astro project:

```sh
astro flow init
```

The command generates the following files: 

```sh
new_proj/
├── config
│   ├── default
│   │   └── configuration.yml
│   └── dev
│       └── configuration.yml
├── data
│   ├── imdb.db
│   └── retail.db
└── workflows
    ├── example_basic_transform
    │   └── top_animations.sql
    └── example_templating
        ├── filtered_orders.sql
        └── joint_orders_customers.sql
```

Each SQL project is composed of three directories:

- `config`: This directory contains configurations for different **environments** for running SQL. These configurations are mainly used for storing Airflow connections to external databases. Each SQL environment has one subdirectory containing exactly one file named `configuration.yml`. The default SQL project includes `default` and `dev` environments.
- `workflows`: This directory contains subdirectories for SQL **workflows**. Each workflow subdirectory contains one or more related SQL files that should be run together. The default SQL project includes a few example workflows that you can run out of the box. 
- `data`: This directory contains the data for which to run your SQL workflows, formatted as `.db` files. The default SQL project includes example data for films and a simple retail platform.

## Develop your SQL project 

If you have existing `.sql` files and datasets, developing a SQL project that runs with Airflow is as simple as adding files to a few directories.

### Create SQL workflows 

To run SQL as workflows, add your `.sql` files to one of your workflow subdirectories in `workflows`. All SQL files in a given workflow run together when you run `astro flow run`. See [Run a SQL workflow](#run-a-sql-workflow).

If your `.sql` file has a `SELECT` statement, your SQL workflow will create a table in your target database named after the `.sql` file.

SQL files within a workflow can be dependent on each other using Jinja templating.

### Add data to test

Add all data to run your SQL workflows with in the `data` directory of your project.

### Configure environments and Airflow connections

An environment is a set of configurations that define the Airflow environment in which your SQL will run. Each environment is defined as a subdirectory in the `config` directory containing a single `configuration.yml` file. 

An environment requires an Airflow connection to the external databases where you will load the results of your SQL workflows. You can configure one or multiple connections withing a single `configuration.yml` file. To configure a connection for an environment, add the connection's key value pairs in YAML format to the environment's `configuration.yml` file. 

See [Managing connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) for a list of connection types and required values for each type. For example, a Snowflake connection in `dev/configuration.yml` might look like the following: 

```yaml
snowflake_default:
  login: mylogin
  password: mypassword
  schema: myschema
  account: myaccount
  database: MYDATABASE
  region: us-east-1
  warehouse: MYWAREHOUSE
  role: ADMIN
```

Note that Airflow connections configured in this directory are not accessible to your Astro project. Similarly, connections configured in your Astro project are not accessible to your SQL project. 

#### Test Airflow connections

To test all configured connections within an environment, run the following command from your SQL project directory:

```sh
astro flow validate --environment=<env-directory-name>
```

This command runs Airflow's [connection testing tool](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#testing-connections) for all connections configured in the `configuration.yml` file of your environment subdirectory. 

You can also test individual connections within an environment. For example, to test a `snowflake_default` connection in the `dev/configuration.yml`, you would run the following command to test the connection:

```sh
astro flow validate --connection=snowflake_default --environment=dev
```

## Run a SQL workflow

To run a SQL workflow in your project, run the following command: 

```sh
astro flow run <workflow-directory> --connection=<your-connection> --environment=<your-environment>
```

This command automatically builds and runs a DAG based solely on the configurations in your project directory. For example, consider the following command using the default SQL project assets:

```sh
astro flow run example_templating --connection=snowflake_default --environment=dev
```

After running this command, the CLI:

- Creates a DAG based on the provided information. Because the SQL files in `example_templating` are dependent on each other, the CLI creates a DAG with two tasks based on jinja templating. The DAG is available to view in `<your-sql-project/.airflow/dags`.
- Runs the DAG. If the SQL project exists in an Astro project, the CLI uses the Astro project's `airflow.cfg` and `airflow.db` files to start an Airflow environment. If the SQL project exists on its own, the CLI uses default `airflow.cfg` and `airflow.db` files from the SQL project. Specifically, the DAG:
    - Connects to Snowflake using the `snowflake_default` connection configured in `dev/configuration.yml`.
    - Creates a table named `filtered_orders` and runs `filtered_orders.sql` to populate the table with data from `data/retail.db`. A table is named after the `.sql` file which includes the `SELECT` statement that creates the table. 
    - Creates a table named `joint_orders_customers` and runs `joint_orders_customers.sql` to populate the table using data from `filtered_orders`.

## Export a SQL workflow as a DAG

Export a SQL workflow as a DAG using the following command: 

```
astro flow generate <your-sql-workflow> --env=<your-env> --airflow-dags-folder=<your-dags-folder>
```

This command automatically builds a DAG that runs your workflow and exports it to `<your-dags-folder>` in your SQL project. If the DAGs directory doesn't already exist, the CLI creates it for you. 

For example, to export a DAG that runs the `example_templating` workflow based on the `dev` environment to a directory named `sql_dags`, you would run: 

```sh
astro flow generate example_templating --env=dev --airflow-dags-folder=sql_dags
```

After you run this command, you can add the DAG to an existing Astro project and run it locally or deploy it to Astro.
