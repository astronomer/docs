-
sidebar_label: 'Run SQL models'
title: 'Run SQL models with the Astro CLI'
id: sql-cli
description: The Astro CLI can start up a local environment for testing SQL queries. Use YAML configuration and CLI commands to reliably run SQL in Airflow without having to write python. 
---

:::caution 

This feature is in alpha and is not yet recommended for production workflows.

:::

The Astro CLI `sql` or `flow` plugin offers a set of tools for those who want to create SQL workflows without having to use Python or and run them locally without having to setup Airflow.

## Concepts

### Project

A directory containing necessary files and paths to run the SQL CLI. Its main contents are configurations per environment and SQL workflows.

### Environment

A set of configurations (mostly connections) specific to an environment. It allows users to run pipelines locally, with the flexibility of using databases available in different environments (e.g. dev, QA, staging, production).

### Connection

The details necessary to connect to a SQL database. Usually this includes hosts and passwords. The SQL plugin supports the following databases
* Postgres
* SQite
* BigQuery
* Snowflake
* Redshift

Examples of how to configure them are detailed at the [sample configuration](https://github.com/astronomer/astro-sdk/blob/main/sql-cli/include/base/config/dev/configuration.yml).

### Workflow

A folder containing one or more SQL models which define a pipeline. These models may depend on each other or may be independent. Workflows can be seen as an abstraction to Airflow DAGs.

### SQL model

A SQL file declaring a transformation that can be run independently or in conjunction to other SQL models. SQL models can be seen as an abstraction to Airflow tasks.


## 1. Installation

The SQL features are available since Astro CLI 1.7. To install it, [follow the instructions](install-cli.md).

Once the SQL CLI is installed, enable the SQL plugin by running:

```
astro config set -g beta.sql_cli true
```

## 2. Usage

### 2.1. Basic commands

Check the version of the SQL plugin:

```
$ astro flow version
Astro SQL CLI 0.1.
```

Find out more about it:
```
$ astro flow about
Find out more: https://github.com/astronomer/astro-sdk/sql-cli
```

Learn about the existing commands:
```
astro flow --help
```

### 2.2. Initialize a SQL project

Learn about the project initialization by running:

```
astro flow --help
```

It is also possible to initialise a SQL CLI project inside or outside the existing Astro CLI project.

During initialization, the version 0.1 of the SQL plugin creates sample databases, configurations and workflows.

#### 2.2.1. Initializing a SQL project in a new directory

If the user did not initialise an Astro CLI project, this is the recommended approach for them to initialise the SQL CLI project:

```
astro flow init new_proj
```

Or

```
mkdir new_proj
cd new_proj
astro flow init 
```

This command creates the following directories and files:

```
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

####  2.2.2. Existing Astro CLI project

If a user has an existing Astro CLI project and would like to extend it with the SQL plugin experience, it is possible to accomplish this by running the following command:

```
# Assuming the following commands were previously run:
# mkdir new_proj
# cd new_proj
# astro dev init

astro flow init --airflow-dags-folder dags
```

It will create the same directories and files as 2.2.1.

### 2.3. Validate the database connections

Find out more about the validate command by running

```
astro flow validate --help
```

It is possible to run validate from within and from outside the project directory.

The connections declared in the default environment can be tested without using the flag `--env`.

#### Requirements for this command to work

It assumes the user has already initialised a SQL CLI project.

The SQL CLI project should contain:

a) a folder `config` containing a sub-folder with the environment of interest. Each subfolder contains a `configuration.yaml` file that has information about how to access databases.

#### 2.3.1. From outside the project directory
It is possible to validate all the connections from a particular environment. This is how to validate all the connections from the `dev` environment:

```
astro flow validate new_proj --env dev
```

#### 2.3.2. From within the directory

The following command allows users to validate the `default` environment connections from within the SQL CLI project directory.

```
astro flow validate
```

### 2.4. Run a SQL workflow

It is possible to run workflows locally independent of Airflow.

As of 0.1, each SQL model is being materialised as a table in the database being referenced, with the same name as the SQL file.

Find out more about the run command by running

```
astro flow run --help
```

Users can run it from within and from outside the project folder by using the flag `project_dir`. Unless specified, it uses the default environment.

#### Requirements for this command to work

It assumes the user has already initialised a SQL CLI project.

The SQL CLI project directory should contain:

a) a folder `config` containing a sub-folder with the environment of interest. Each subfolder contains a `configuration.yaml` file that has information about how to access databases.

b) a folder within `workflows` with the name of the workflow we're attempting to run. It should contain at least one SQL file. 

Unless the user initialised the project with the parameters `--airflow-home` and `--airflow-dags-folder`, it will also assume there is a folder `.airflow` in the root of the project directory. By default, this directory will have a folder per environment containing their `airflow.cfg` and `airflow.db`. As part of the run procedure, SQL workflows are converted into Airflow Python DAGs and stored in the folder `.airflow/dags` (or `--airflow-dags-folder`).


#### 2.4.1. From outside the project directory

It is possible to run the `example_templating` workflow using the database credentials declared in the **dev** environment by running:

```
astro flow run example_templating --env dev --project-dir new_proj
```

This workflow uses the sample SQlite database `data/imdb.db`. It selects some of the rows of `movies` and creates a new table called `top_animations`, since that is the name of the `.sql` file with the `SELECT` statemnet.

```
$ sqlite3 data/imdb.db  
SQLite version 3.38.2 2022-03-26 13:51:10
Enter ".help" for usage hints.
sqlite> .tables
movies          top_animations
sqlite> select * from top_animations;
Toy Story 3 (2010)|8.3
Inside Out (2015)|8.2
How to Train Your Dragon (2010)|8.1
Zootopia (2016)|8.1
How to Train Your Dragon 2 (2014)|7.9
```

#### 2.4.2. From within the directory


The following command allows users to run the `example_basic_transform` using the **default** database connections:

```
astro flow run example_basic_transform
```


### 2.5. Export a SQL workflow as an Airflow DAG


An alternative to running the workflow using the SQL CLI command line is to export it as a DAG, which Airflow can run like any other DAG.

The DAG export can happen implicitly or explicitly. The implicit generation can be configured during initialisation by using the flag `--airflow-dags-folder`. If this flag is set, all DAGs will be exported to the desired folder when flow run  is used.

The explicit approach consists in using the flow generate command.

Find out more about the run command by running

```
astro flow generate --help
```

#### 2.5.1. From outside the project directory

It is possible to export the `example_templating` as a DAG by running:

```
astro flow generate example_templating --env dev --project-dir new_proj
```

6.2. From within the directory
The following command allows users to run the `example_basic_transform` using the **default** database connections:

```
astro flow generate example_basic_transform
```

