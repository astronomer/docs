---
sidebar_label: 'Run SQL models'
title: 'Run SQL models with the Astro CLI'
id: sql-cli
description: The Astro CLI can start up a local environment for testing SQL queries. Use YAML configuration and CLI commands to reliably run SQL without having to write Python. 
---

:::caution 

This feature is in alpha and is not yet recommended for production workflows.

:::

Use the Astro CLI's SQL commands to run SQL workflows without having to write Python or set up Airflow. The Astro CLI handles all of the required backend configuration for running SQL locally and reliably. Using a connection configured in YAML, you can output the results of your SQL queries to the database of your choice. 

## Prerequisites 

To use the Astro CLI's SQL commands, you need

- The [Astro CLI](overview.md) version 1.7+.
- [Docker Desktop](https://www.docker.com/).
- One of the following databases, hosted either locally or on an external service:
  
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

- `config`: This directory contains configurations for different **environments** for running SQL. These configurations are mainly used for storing connections to external databases. Each SQL environment has one subdirectory containing exactly one file named `configuration.yml`. The default SQL project includes `default` and `dev` environments.
- `workflows`: Each subdirectory is used to define an independent SQL **workflow**. A workflow is a subdirectory that should contain one or more related SQL files that should be run together. The default SQL project includes a few example workflows you can run out of the box. 
- `data`: This directory can contain datasets to run your SQL workflows. The default SQL project includes sample SQLite databases (`.db` files) for a film ranking and a simple retail platform.

## Develop your SQL project 

If you have existing `.sql` files and datasets, developing a running SQL workflow is as simple as adding files to a few directories.

### Configure environments and connections

An environment is a set of configurations that define the environment in which your SQL will run. Each environment is defined as a subdirectory in the `config` directory containing a single `configuration.yml` file. 

An environment requires a connection to the external databases where you will extract and load the results of your SQL workflows. You can configure one or multiple connections withing a single `configuration.yml` file.

[`dev/configuration.yml`](https://github.com/astronomer/astro-sdk/blob/main/sql-cli/include/base/config/dev/configuration.yml) contains templates for for each supported connection type. Use these templates to configure all required key-value pairs for your connection. 

For example, a Snowflake connection in `dev/configuration.yml` might look like the following: 

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

Note that connections configured in this directory are not accessible to your Astro project. Similarly, connections configured in your Astro project are not accessible to your SQL project. 

#### Test database connections

To test all configured databases within an environment, run the following command from your SQL project directory:

```sh
astro flow validate --environment=<env-directory-name>
```

This command runs a connection test for all databases configured in the `configuration.yml` file of your environment subdirectory. 

You can also test individual databases within an environment. For example, to test a `snowflake_default` connection in the `dev/configuration.yml`, you would run the following command to test the connection:

```sh
astro flow validate --connection=snowflake_default --environment=dev
```

### Create SQL workflows 

To run SQL as a workflow, add your `.sql` files to one of your workflow subdirectories in `workflows`. All SQL files in a given workflow run together when you run `astro flow run`. See [Run a SQL workflow](#run-a-sql-workflow).

Each `.sql` file must have a database connection defined as `conn_id` in the front matter of the file. This front matter tells the Astro CLI where to extract and load data from. For example, a SQL query that runs against a Snowflake database would look like the following: 

```sql
---
conn_id: snowflake_default
---
SELECT Title, Rating
FROM movies
WHERE Genre1=='Animation'
ORDER BY Rating desc
LIMIT 5;
```

If your `.sql` file has a `SELECT` statement, your SQL workflow will create a table in your target database named after the `.sql` file.

SQL files within a workflow can be dependent on each other using Jinja templating.


## Run a SQL workflow

To run a SQL workflow in your project, run the following command: 

```sh
astro flow run <workflow-directory> --environment=<your-environment>
```

This command automatically builds and runs your project based on the configurations in your project directory. For example, consider the following command using the default SQL project assets:

```sh
astro flow run example_templating --environment=dev
```

After running this command, the CLI:

- Connects to the `data` directory using the `sqlite_conn` connection that's defined in `dev/configuration.yml` and configured in `filtered_orders.sql`.
- Creates a table named `filtered_orders` and runs `filtered_orders.sql` to populate the table with data from `data/retail.db`.
- Creates a table named `joint_orders_customers` and runs `joint_orders_customers.sql` to populate the table using data from `filtered_orders`.

## Export a SQL workflow as a DAG

Export a SQL workflow as an Airflow DAG using the following command: 

```
astro flow generate <your-sql-workflow> --env=<your-env>
```

This command automatically builds a DAG that runs your workflow and exports it to a hidden directory named `.airflow/dags` in your project. To export DAGs to a different directory, you must initialize a new project using the following command:

```sh
astro flow init --airflow-dags-folder=<your-dags-directory>
```

For example, to export a DAG that runs the `example_templating` workflow based on the `dev` environment, you would run: 

```sh
astro flow generate example_templating --env=dev
```

After you run this command, you can add the DAG to an existing Astro project and run it locally or deploy it to Astro.
