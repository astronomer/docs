---
title: "Creating a Databricks Connection"
id: databricks
sidebar_label: Databricks
description: Learn how to create a Databricks connection.
---

[Databricks](https://www.databricks.com/) is a SaaS product for data processing using Apache Spark framework. Integrating Databricks with Airflow allows users to manage their Databricks clusters, execute, and monitor their databricks jobs. 

This guide provides the basic setup for creating a Databricks connection. For a complete integration tutorial, see [Databricks and Airflow integration](airflow-databricks.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A [Databricks Account](https://www.databricks.com/try-databricks?itm_data=NavBar-TryDatabricks-Trial#account).

## Get your connection details

A connection from Airflow to Databricks requires the following information:

- Databricks URL
- Personal access token

Complete the following steps to retrieve all of these values:

1. In your Databricks Cloud UI, copy the URL of your Databricks workspace where you login. For example, it should be in the format https://dbc-75fc7ab7-96a6.cloud.databricks.com/ or https://your-org.cloud.databricks.com/. 
2. If you want to use a personal access token for a user, follow the [Databricks documentation](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens-for-users) to generate a new token. Otherwise, to generate a personal access token for a Service Principal, follow the instructions given [here](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#manage-personal-access-tokens-for-a-service-principal). Copy the personal access token.

## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-databricks
    ```

    This will install the Databricks provider package, which makes the the Azure Data Factory connection type available in Airflow.

2. Restart or start your local Airflow using `astro dev restart` to apply the changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, select the connection type as **Databricks**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter the Databricks URL.
    - **Password**: Enter your personal access token.

5. Click **Test connection**. When the connection test succeeds, click then **Save**.

    ![databricks-connection](/img/examples/connection-databricks.png)

## How it works

Airflow uses Python's `requests` library to connect to Databricks using [BaseDatabricksHook](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/_api/airflow/providers/databricks/hooks/databricks/index.html).

## See also

- [Apache Airflow Databricks provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/index.html)
- [Databricks modules](https://registry.astronomer.io/modules?query=databricks) and [example DAGs](https://registry.astronomer.io/dags?limit=24&sorts=updatedAt%3Adesc&query=databricks) in Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
- [Databricks and Airflow integration](airflow-databricks.md)
