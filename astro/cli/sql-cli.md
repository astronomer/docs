---
sidebar_label: 'Run SQL models'
title: 'Run SQL models with the Astro CLI'
id: sql-cli
description: The Astro CLI can start up a local environment for testing SQL queries. Use YAML configuration and CLI commands to reliably run SQL without having to write Python. 
---

:::caution 

This feature is in alpha and is not yet recommended for production workflows.

:::

Use Astro CLI SQL commands to run SQL workflows without writing Python code or setting up Airflow. The Astro CLI takes care of all of the backend configuration required for running SQL locally. Configure your connections in YAML to run your SQL in a specific data warehouse.

## Prerequisites 

- [Astro CLI](install-cli.md) version 1.7 or later.
- [Docker Desktop](https://www.docker.com/).
- One of the following databases, hosted either locally or on an external service:
  
    - Postgres
    - SQlite
    - BigQuery
    - Snowflake
    - Redshift

:::info 

If you use Debian or Ubuntu as your operating system, Astronomer recommends to [install Docker from the upstream package](https://docs.docker.com/engine/install/ubuntu/#install-from-a-package). If you install Docker using [Snap Store](https://snapcraft.io/docker), you will not be able to create projects on the `/tmp` directory.

:::

## Enable Astro SQL commands 

To enable Astro SQL commands with the latest version of the Astro CLI, run:

```sh
astro config set -g beta.sql_cli true
```

## Create a new SQL project 

A SQL project contains the set of files necessary to run SQL queries from the Astro CLI, including YAML files for configuring your SQL environment and directories for storing SQL workflows. A SQL project can exist as its own top-level directory or within an existing Astro project. 

To create a SQL project, run the following command in either an empty directory or an existing Astro project:

```sh
astro flow init
```

This command uses Docker, and it can take up to five minutes to complete if this is the first time you're running the command and you're using a specific version of the Astro CLI. Subsequent runs with the same Astro CLI version typically complete in seconds. When the command finishes running, it generates the following files: 

```sh
new_proj/
├── config
│   ├── default
│   │   └── configuration.yml
│   └── dev
│       └── configuration.yml
├── data
│   ├── imdb.db
│   └── retail.db
└── workflows
    ├── example_basic_transform
    │   └── top_animations.sql
    └── example_templating
        ├── filtered_orders.sql
        └── joint_orders_customers.sql
```

Each SQL project is composed of three directories:

- `config`: This directory contains configurations for different environments for running SQL. These configurations  store connections to external databases. Each SQL environment has one subdirectory containing one file named `configuration.yml`. The default SQL project includes `default` and `dev` environments.
- `workflows`: Each subdirectory is used to define an independent SQL workflow. A workflow is a subdirectory that contains one or more related SQL files that should be run together. The default SQL project includes a few example workflows you can run immediately.
- `data`: This directory can contain datasets to run your SQL workflows. The default SQL project includes sample SQLite databases (`.db` files) for a film ranking and a simple retail platform.

## Develop your SQL project 

If you have existing `.sql` files and datasets, you can develop a running SQL workflow by adding files to a few directories.

### Configure environments and connections

An environment requires a connection to the external databases in which you will run your SQL workflows. You can configure one or multiple connections withing a single `configuration.yml` file.

[`dev/configuration.yml`](https://github.com/astronomer/astro-sdk/blob/main/sql-cli/include/base/config/dev/configuration.yml) contains templates for for each supported connection type. Use these templates to configure all required key-value pairs for your connection. 

For example, a Snowflake connection in `dev/configuration.yml` might look like the following: 

```yaml
connections:
  - conn_id: snowflake_conn
    conn_type: snowflake
    host: HOST_DNS
    port: 443
    login: Username
    password: Password
    schema: "SchemaName"
    extra:
      account: "AcountId"
      region: "us-east-1"
      role: "Role"
      warehouse: Warehouse
      database: Database
```

Your Astro project currently can't access the connections configured in this directory. Similarly, your SQL project can't access connections configured in your Astro project. Features for unifying these two sets of connections will be available in upcoming releases.

#### Test database connections

To test all configured databases within an environment, run the following command from your SQL project directory:

```sh
astro flow validate --environment=<env-directory-name>
```

This command runs a connection test for all databases configured in the `configuration.yml` file of your environment subdirectory. 

You can also test individual databases within an environment. For example, to test a `snowflake_default` connection in the `dev/configuration.yml`, you run the following command to test the connection:

```sh
astro flow validate --connection=snowflake_default --environment=dev
```

### Create SQL workflows 

To run SQL as a workflow, add your `.sql` files to one of your workflow subdirectories in `workflows`. All SQL files in a given workflow run together when you run `astro flow run`. See [Run a SQL workflow](#run-a-sql-workflow).

Each `.sql` file must have a database connection defined as `conn_id` in the front matter of the file. This front matter tells the Astro CLI where to extract and load data. In the following example, a SQL query runs against a Snowflake database: 

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

If your `.sql` file includes a `SELECT` statement, your SQL workflow creates a table in your target database with the name of the `.sql` file.

SQL files within a workflow can be dependent on each other using Jinja templating.

:::tip 

If you define a database connection in a `.sql` file with a downstream dependency, the downstream `.sql` file will automatically inherit the database connection information. 

::: 

## Run a SQL workflow

To run a SQL workflow in your project, run the following command: 

```sh
astro flow run <workflow-directory> --environment=<your-environment>
```

This command automatically builds and runs your project as an Airflow DAG based on the configurations in your project directory. For example, consider the following command using the default SQL project assets:

```sh
astro flow run example_templating --environment=dev
```

After running this command, the CLI:

- Connects to the `data` directory using the `sqlite_conn` connection that's defined in `dev/configuration.yml` and configured in `filtered_orders.sql`.
- Creates a table named `filtered_orders` and runs `filtered_orders.sql` to populate the table with data from `data/retail.db`.
- Creates a table named `joint_orders_customers` and runs `joint_orders_customers.sql` to populate the table using data from `filtered_orders`.

To view the implementation of this workflow in more detail, you can view the generated code. See [Export a SQL workflow as a DAG](#export-a-sql-workflow-as-a-dag).

## Export a SQL workflow as a DAG

Run the following command to export a SQL workflow as an Airflow DAG:

```
astro flow generate <your-sql-workflow> --env=<your-env>
```

This command automatically builds a DAG that runs your workflow and exports it to a hidden directory named `.airflow/dags` in your project. To export DAGs to a different directory, you must initialize a new project using the following command:

```sh
astro flow init --airflow-dags-folder=<your-dags-directory>
```

For example, to export a DAG that runs the `example_templating` workflow based on the `dev` environment, you run the following command: 

```sh
astro flow generate example_templating --env=dev
```

After you run this command, you can add the DAG to an existing Astro project and run it locally or deploy it to Astro.
