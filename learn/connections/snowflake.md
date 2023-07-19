---
title: "Create a Snowflake Connection in Airflow"
id: snowflake
sidebar_label: Snowflake
description: Learn how to create a Snowflake connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/snowflake.png' }
---

[Snowflake](https://www.snowflake.com/en/) is a cloud data warehouse to store and analyze your data. Integrating Snowflake with Airflow allows you to interact with Snowflake. This includes running SQL, monitoring the status of SQL, running a SnowPark python function, load/export the data to/from Snowflake, etc.

This guide provides the basic setup for creating a Snowflake connection. For a complete integration tutorial, see [Orchestrate Snowflake Queries with Airflow](../airflow-snowflake.md). To run Snowpark queries in Airflow, see [Run Snowpark queries with the ExternalPythonOperator in Apache Airflow](../external-python-operator.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- [Snowflake account](https://signup.snowflake.com/).

## Get Connection details

A connection from Airflow to Snowflake requires the following information:

- Host
- Account
- Region
- Role
- Database
- Warehouse
- Username
- Password

Complete the following steps to retrieve these values:

1. In your Snowflake classic console, copy the URL. Your URL should be of the format `https://<account-identifier>.<region>.snowflakecomputing.com/`. If you are using the new Snowsight console (`https://app.snowflake.com`), follow the [Snowflake instructions](https://docs.snowflake.com/en/user-guide/admin-account-identifier#finding-the-organization-and-account-name-for-an-account) to retrieve your URL.
2. From the URL copied in step #1, copy your `account-identifier` and `region`.
3. Follow the [Snowflake documentation](https://community.snowflake.com/s/article/How-to-Capture-Snowflake-Users-Roles-and-Grants-Into-a-Table#:~:text=Snowflake%20Users%20and%20Roles%20via,Roles%20tab%2C%20as%20shown%20below) to copy your **Role**.
4. Copy the values for **Warehouse**, **Database**, and **Schema**.
5. [Create a new user](https://docs.snowflake.com/en/sql-reference/sql/create-user) for Airflow to connect to Snowflake. Copy the username and password.

## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-snowflake
    ```

    This will install the Snowflake provider package, which makes the Snowflake connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Snowflake**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Schema**: Enter your **Schema**
    - **Login**: Enter your username
    - **Password**: Enter your password
    - **Account**: Enter your `account-identifier`
    - **Warehouse**: Enter your **Warehouse**
    - **Database**: Enter your **Database**
    - **Region**: Enter your `region`
    - **Role**: Enter your **Role**

5. Click on **Test** connection to test and then **Save** the connection.

4. Paste the values copied in [Get connection details](#get-connection-details) for your Snowflake account to the connection fields:
    - **Schema**: `<my-schema>`
    - **Login**: `<my-user>`
    - **Password**: `<my-password>`
    - **Account**: `<my-account>`
    - **Warehouse**: `<my-warehouse>`
    - **Database**: `<my-database>`
    - **Region**: `<my-region>`
    - **Role**: `<my-role>`

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![snowflake-connection-extra](/img/examples/connection-snowflake-aws.png)

For GCP or some AWS regions, Airflow connection's **Region** might look different. For example, if your account URL is `https://ZS86751.europe-west4.gcp.snowflakecomputing.com`, then your `region` for Airflow connection will be `europe-west4.gcp`. See [Account identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier) to learn more about Snowflake's account types and their identiders.

## How it works

Airflow uses the python package [Snowflake connector](https://github.com/snowflakedb/snowflake-connector-python) to connect to Snowflake through the [SnowflakeHook](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_api/airflow/providers/snowflake/hooks/snowflake/index.html).

## See also

- [Apache Airflow Snowflake provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html).
- [Snowflake Modules](https://registry.astronomer.io/modules?limit=24&sorts=updatedAt%3Adesc&query=snowflake) and [example DAGs](https://registry.astronomer.io/dags?query=snowflake) in the Astronomer Registry.
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
