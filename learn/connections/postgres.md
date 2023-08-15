---
title: "Create a Postgres connection in Airflow"
id: postgres
sidebar_label: Postgres
description: Learn how to create a Postgres connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/postgres.png' }
---

[Postgres](https://www.postgresql.org/) is a free and open source relational database system. Integrating Postgres with Airflow allows you to interact with your Postgres database, run queries, ans load or export data from an Airflow DAG.

This guide provides the basic setup for creating a Postgres connection. 

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A Postgres database running in the cloud or on-premises.
- [Permission](https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps-2) to access your Postgres database from your local Airflow environment.

## Get connection details

A connection from Airflow to Postgres requires the following information:

- Host (also known as the endpoint URL, server name, or instance ID based on your cloud provider)
- Port (default is 5432)
- Username 
- Password
- Schema (default is `public`)

The method to retrieve these values will vary based which cloud provider you use to host Microsoft SQL Server. Refer to the following documents to for more information about retrieveing these values:

- AWS: Connect to Postgres running on [RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html)
- GCP: Connect to Postgres running on [ Cloud SQL](https://cloud.google.com/sql/docs/postgres/connect-instance-local-computer)
- Azure: Connect to Postgres running on an [Azure database](https://learn.microsoft.com/en-us/training/modules/create-connect-to-postgres/4-connect-develop-your-database)

For example, if you're running Postgres in a Relational Data Store (RDS) in AWS, complete the following steps to retrieve these values:

1. In your AWS console, select your region, then go to the RDS service and select your Postgres database.
2. Open the **Connectivity & security** tab and copy the **Endpoint** and **Port**.
3. Follow the AWS instructions to [create a user](https://www.postgresql.org/docs/8.0/sql-createuser.html) and [grant a role to the user](https://www.postgresql.org/docs/current/sql-grant.html) that Airflow will use to connect to Postgres. Copy the username and password.
4. (Optional) To use a specific schema, copy the name of the schema. If you skip this, the default schema `public` will be used.

## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-postgres
    ```

    This will install the Postgres provider package, which makes the Postgres connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose **Postgres** as the connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter your Postgres server's host/ endpoint URL/ server name/ instance ID.
    - **Schema**: Enter your schema name.
    - **Login**: Enter your username.
    - **Password**: Enter your password.
    - **Port**: Enter your Postgres server's **Port**.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![connection-postgres](/img/examples/connection-postgres.png)

## How it works

Airflow uses the [psycopg2](https://pypi.org/project/psycopg2/) python library to connect to Postgres through the [PostgresHook](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/hooks/postgres/index.html). You can also directly use the PostgresHook to create your own custom operators.

## See also

- [Apache Airflow Postgres provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html)
- [Postgres modules](https://registry.astronomer.io/modules?limit=24&sorts=updatedAt%3Adesc&query=postgres) and [example DAGs](https://registry.astronomer.io/dags?query=postgres) in the Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
