---
title: "Create an ODBC connection in Airflow"
id: odbc
sidebar_label: ODBC
description: Learn how to create an ODBC connection in Airflow.
---

[Open Database Connectivity (ODBC)](https://en.wikipedia.org/wiki/Open_Database_Connectivity) is a protocol that you can use to connect to a Database Management System (DBMS) which uses an ODBC driver. Integrating Airflow with ODBC allows users to connect and manage jobs in a data source that supports ODBC connectivity. This includes connecting Airflow to Synapse, MS SQL Server, etc.

This document provides the basic setup for creating an ODBC connection to use with Synapse SQL.

## Prerequisites
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- An [Azure Synapse workspace](https://learn.microsoft.com/en-us/azure/synapse-analytics/get-started).
- [Permissions to access](https://learn.microsoft.com/en-us/azure/synapse-analytics/security/how-to-set-up-access-control) your Synapse Database from Airflow.

## Get Connection details

A connection from Airflow to Azure data factory requires the following information:

- Subscription ID
- Data factory name
- Resource group name
- Application Client ID
- Tenant ID
- Client secret

1. In your Azure portal, navigate to Synapse Analytics and select your subscription. Then, click on your Synapse workspace.
2. Follow [Azure documentation](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/connect-overview#find-your-server-name) to retrieve your **SQL Endpoint**, **SQL admin username**, **Name** of your SQL pool, and your password.


## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-odbc
    ```

    This will install the ODBC provider package, which makes the ODBC connection type available in Airflow.

2. Add the following OS-level packages to your `packages.txt`:
    
    ```bash

      gcc
      g++
      unixodbc
      unixodbc-dev

    ```

    These are required for installation of the ODBC driver in your docker containers. 

3. Append the following lines to your `Dockerfile`:

    ```docker

      USER root
      RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

      #Debian 11
      RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

      RUN apt-get update
      RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
      # optional: for bcp and sqlcmd
      RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
      # optional: for unixODBC development headers
      RUN apt-get install -y unixodbc-dev
      
      USER astro
      
    ```

    Refer to the [Microsoft documentation](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline) for other OS types and versions.


4. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose **ODBC** as the connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter your **SQL Endpoint**.
    - **Schema**: Enter your SQL pool **Name**.
    - **Login**: Enter your **SQL admin username**
    - **Password**: Enter your password.
    - **Port**: Enter `1433` as port.
    - **Extra**: Enter the string `{"Driver": "ODBC Driver 18 for SQL Server"}`.

5. Click **Test**. After the connection test succeeds, click **Save**.

    <!-- ![connection-odbc-synapse](/img/examples/connection-odbc-synapse.png) -->


## How it works

Airflow uses [PyODBC](https://github.com/mkleehammer/pyodbc) to connect to the ODBC data sources through the [ODBCHook](https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/_api/airflow/providers/odbc/hooks/odbc/index.html). You can directly use this hook to create your own custom hooks or operators.


## References
- [Apache Airflow ODBC provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/connections/odbc.html)
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
