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

If you use Debian or Ubuntu as your operating system, Astronomer recommends to [install Docker from the upstream package](https://docs.docker.com/engine/install/ubuntu/#install-from-a-package). If you install Docker using [Snap Store](https://snapcraft.io/docker), you will not be able to create projects in the `/tmp` directory.

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

- `config`: This folder contains configurations for different environments for running SQL. These configurations store connections to external databases. Each SQL environment has one subfolder containing its own `configuration.yml`. The default SQL project includes `default` and `dev` environments.
    - `config/global.yml`: This file contains configurations that apply to all of your SQL environments.
- `workflows`: This folder contains independent SQL workflows. A workflow is a subfolder containing related SQL queries and data management tasks that run together. The default SQL project includes a few example workflows that you can run to test functionality.
- `data`: This folder can contain datasets to run your SQL workflows. The default SQL project includes sample film ranking and retail SQLite databases (`.db` files).

## Develop your SQL project 

If you have existing `.sql` files and datasets, you can develop a running SQL workflow by adding files to a few folders.

### Configure environments and connections

An environment requires a connection to the databases in which you run your SQL workflows. You can configure multiple connections to data sources and data destinations within a single `configuration.yml` file. 

[`default/configuration.yml`](https://github.com/astronomer/astro-sdk/blob/main/sql-cli/include/base/config/default/configuration.yml) contains templates for for each supported connection type. Use these templates to configure all required key-value pairs for your connection. 

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

An Astro project can't access the connections configured in this directory. Similarly, a SQL project can't access connections configured in an Astro project. Features for unifying these two project structures will be available in upcoming releases.

#### Test database connections

To test all configured databases within an environment, run the following command from your SQL project directory:

```sh
astro flow validate --env=<env-directory-name>
```

This command runs a connection test for all databases configured in the `configuration.yml` file of your environment subfolder. 

You can also test individual databases within an environment. For example, to test a `snowflake_conn` connection in the `dev/configuration.yml`, you run the following command to test the connection:

```sh
astro flow validate --connection=snowflake_conn --env=dev
```

### Create SQL workflows 

To run SQL as a workflow, add your `.sql` files to a workflow subfolder in `workflows`. All SQL files in a given workflow run together when you run `astro flow run`. See [Run a SQL workflow](#run-a-sql-workflow).

Each `.sql` file must have a database connection defined as `conn_id` in the front matter header of the file. This front matter tells the Astro CLI where to load the query results. In the following example, a SQL query runs against the `imdb.db` database in the `data` folder. The Astro CLI sends the results of the query to a Snowflake database defined in `snowflake_conn`.

```sql
---
conn_id: snowflake_conn
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

### Configure a local data source 

Configure a local data source to test your SQL queries using only a standard SQLite connection. 

1. Add the data source to your `data` directory. 
2. In your `config` directory, open the `configuration.yaml` for the environment where you want to use the data.
3. Configure a SQLite connection to your data source. For example:

    ```yaml
    ## Example of SQLite connection
      - conn_id: sqlite_conn
        conn_type: sqlite
        host: data/<your-data-file>.db
        schema:
        login:
        password:
    ```

    When you reference a table from your local data source in a workflow query, the SQL CLI automatically uses a local SQLite connection to load the table from your `data` directory. 

### Configure an external data source

To run a query against data hosted outside of your project, you create a `YAML` file describing how to load the data, then add the file to the workflow where you want to use the data.

1. Create connections for your data source and data destination. See [Configure environments and connections](#configure-environments-and-connections). 
2. Copy the `conn_id` for both connections.
3. In the workflow where you want to use the data, create a new `yaml` file that tells the CLI to load the contents of a specific database. For example, the following file gives the CLI instructions to load data from Amazon S3 and store the results of your SQL query in Amazon Redshift.

    ```yaml
    load_file:
      input_file:
        path: "s3://<your-data-filepath>.csv"
        conn_id: "aws_conn"
      output_table:
        conn_id: "redshift_conn"
        metadata:
          schema: "<your-schema>"
          database: "<your-database>"
      native_support_kwargs:
        IGNOREHEADER: 1
        REGION: "<your-region>"
        IAM_ROLE: "arn:aws:iam::<account_id>:role/redshift-s3-readonly"
    ```

4. In your SQL files, specify the table to query using one of the following options: 

    - Reference the name of your `yaml` file in your SQL files using Jinja templating. The SQL CLI assumes which table to use based on the information provided in your YAML file. For example, if the example YAML file in the previous step was named `load_s3.yaml`, your SQL query might look like the following: 

    ```sql
    ---
    conn_id: redshift_conn
    ---
    SELECT *
    FROM {{load_s3}}
    LIMIT 5;
    ```

    - Reference the table name directly in your queries. For example: 


    ```sql
    ---
    conn_id: redshift_conn
    ---
    SELECT *
    FROM <your-input-table>
    LIMIT 5;
    ```
    
    When you run your workflow, the CLI automatically uses the configured data source in your `YAML` file for all queries. This option does not work if you have multiple configured data sources in your workflow.

## Run a SQL workflow

To run a SQL workflow in your project, run the following command: 

```sh
astro flow run <workflow-directory> --env=<your-environment>
```

This command automatically builds and runs your project as an Airflow DAG based on the configurations in your project directory. For example, consider the following command using the default SQL project assets:

```sh
astro flow run example_templating --env=dev
```

The `example_templating` workflow contains two separate SQL queries: `filtered_orders.sql` and `joint_orders_customers.sql`. After running this command, the CLI:

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

### Export a SQL workflow to an Astro project

Export a SQL workflow to an Astro project to locally test the workflow as a DAG and view execution information in the Airflow UI. 

1. In the `config/global.yml` file of your SQL project, set `dags_folder` to the absolute file path of your Astro project `dags` folder. Set `data_dir` to the absolute file path of your Astro project `include` folder.
2. To export a DAG from an existing SQL project, copy the contents your SQL project `data` folder into your Astro project `include` folder. To export a DAG from a new SQL CLI project, run `astro flow init --data-dir` to copy the contents of the default `data` folder into your Astro project.
3. Run the following command to execute your SQL workflow and export the DAG to your Astro CLI `dags` folder:

    ```sh
    astro flow run <your-workflow> --project-dir <filepath-to-astro-project-directory>`
    ```

You can now run the SQL workflow as a DAG from your Astro project. See [Build and run a project locally](https://docs.astronomer.io/astro/develop-project#build-and-run-a-project-locally).

:::info 

If you configured databases in your SQL CLI project, you must manually reconfigure these databases in your Astro project through the Airflow UI. See [Manage connections in Apache Airflow](https://docs.astronomer.io/learn/connections).

:::
