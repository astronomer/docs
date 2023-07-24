---
title: "Create a Microsoft SQL Server Connection in Airflow"
id: ms-sqlserver
sidebar_label: Microsoft SQL Server
description: Learn how to create a Microsoft SQL Server connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/ms-sqlserver.png' }
---

[Microsoft SQL Server](https://www.microsoft.com/en-in/sql-server/sql-server-downloads) is a proprietary relational database management system developed by Microsoft. Integrating SQL Server with Airflow allows you to interact with the database or export the data from SQL server to an external system.

This guide provides the basic setup for creating a Microsft SQL Server connection. 

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A Microsoft SQL Server database hosted in cloud or on-premises.
- [Permissions to access](https://www.w3computing.com/sqlserver2012/managing-permissions-using-management-studio/) Microsoft SQL Server from your local Airflow environment.

## Get Connection details

A connection from Airflow to Microsoft SQL Server requires the following information:

- Host (also known as endpoint URL or server name or Instance ID depending on your Cloud provider)
- Port (default is 1433)
- Username
- Password
- Schema (default is `dbo`)

The method to retrieve these values will depend on the cloud provider where your Microsoft SQL Server is hosted. Based on your cloud provider, refer to the following links to retrieve these values:

- AWS: Connect to SQL Server running [on RDS](https://aws.amazon.com/getting-started/hands-on/create-microsoft-sql-db/)
- GCP: Connect to SQL Server running [on Cloud SQL](https://cloud.google.com/sql/docs/sqlserver/quickstarts)
- Azure: Connect to SQL Server running on [Azure SQL database](https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-ssms?view=azuresql-mi) or [on a VM](https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/ways-to-connect-to-sql?view=azuresql-vm)

For example, if you are running Microsoft SQL Server in a Relational Data Store (RDS) in AWS, complete the following steps to retrieve these values:

1. In your AWS console, select your region, then go to the RDS service and select your SQL Server database.
2. From the **Connectivity & security** tab, copy the **Endpoint** and **Port**.
3. Follow the instructions for Microsoft SQL server to [create a new database user](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-user?view=sql-server-ver16). Copy the username and password.
4. (Optional) To use a specific schema, copy the name of the schema. If you skip this, the default schema `dbo` will be used.


## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-mssql
    ```

    This will install the Microsoft provider package, which makes the MS SQL Server connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose **Microsoft SQL Server** as the connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter your MSSQL server's endpoint
    - **Schema**: Enter your schema name
    - **Login**: Enter your username
    - **Password**: Enter your password
    - **Port**: Enter your MSSQL server's port

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![connection-mssqlserver](/img/examples/connection-ms-sqlserver.png)

:::tip Important

For installing `apache-airflow-providers-microsoft-mssql` to Airflow version 2.6+, add the following to `packages.txt` and restart your Astro project.

```

build-essential
freetds-dev
libkrb5-dev
default-libmysqlclient-dev

```

:::

## How it works

Airflow uses [PyMSSQL](https://pypi.org/project/pymssql/) to connect to Microsoft SQL Server through the [MsSqlhook](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/1.0.0/_api/airflow/providers/microsoft/mssql/hooks/mssql/index.html). You can also directly use the MsSqlhook to create your own custom operators.

## See also

- [Apache Airflow Microsoft provider OSS docs](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/index.html)
- [MS SQL Server Modules](https://registry.astronomer.io/modules?query=mssql) in the Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
