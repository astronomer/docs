---
title: "Create a Snowflake Connection in Airflow"
id: snowflake
sidebar_label: Connection
description: Learn how to create a Snowflake connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/snowflake.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[Snowflake](https://www.snowflake.com/en/) is a cloud data warehouse where you can store and analyze your data. Integrating Snowflake with Airflow allows you to do all of the following and more from a DAG:

- Run SQL
- Monitor the status of SQL queries
- Run a SnowPark python function
- Load and export data to/from Snowflake

This guide provides the basic setup for creating a Snowflake connection. For a complete integration tutorial, see [Orchestrate Snowflake Queries with Airflow](airflow-snowflake.md). To run Snowpark queries in Airflow, see [Run Snowpark queries with the ExternalPythonOperator in Apache Airflow](external-python-operator.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A [Snowflake account](https://trial.snowflake.com/?owner=SPN-PID-365384).

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

<Tabs
    defaultValue="snowsight"
    groupId="get-connection-details"
    values={[
        {label: 'Snowsight', value: 'snowsight'},
        {label: 'Snowflake classic console syntax', value: 'classic'},
    ]}>
<TabItem value="snowsight">

1. Open [Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight). Follow the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/ui-snowsight-gs#using-snowsight) to open the account selector at the bottom of the left nav. Hover over your account to see more details, then click the **Copy URL** icon to copy the account URL. The URL should be in the format `https://<account-identifier>.<region>.snowflakecomputing.com/`.

    ![Screenshot of the bottom of the left nav in Snowsight showing how to copy the account URL.](/img/tutorials/connections-snowflake_snowsight_url.png)

2. Copy `<account-identifier>` and `<region>` from the URL.

  :::info

  When you copy your `region`, you might have to additionally copy the cloud provider identifier after the region name for some GCP and some AWS regions. For example, if your account URL is `https://ZS86751.europe-west4.gcp.snowflakecomputing.com`, then your `region` will be `europe-west4.gcp`. See [Account identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier) to learn more about Snowflake's account types and their identifiers.

  :::

3. Click on the user menu at the top of the left nav to see your current `role`. You can click on **Switch Role** to see all the available roles.

    ![Screenshot of the user menu in Snowsight showing how to copy the role.](/img/tutorials/connections-snowflake_snowsight_role.png)

4. Copy the name of your **Warehouse**. To see all available warehouses, open a new **Worksheet** and click on the [context selector menu](https://docs.snowflake.com/en/user-guide/ui-snowsight-worksheets#change-the-session-context-for-a-worksheet) on the right side of the screen. 

    ![Screenshot of the context selector menu in Snowsight showing how to copy the warehouse.](/img/tutorials/connections-snowflake_snowsight_warehouse.png)

</TabItem>

<TabItem value="classic">

1. Open the [Snowflake classic console](https://docs.snowflake.com/en/user-guide/ui-using) and locate the URL for the page. The URL should be in the format `https://<account-identifier>.<region>.snowflakecomputing.com/`.
2. Copy `<account-identifier>` and `<region>` from the URL.

  :::info

  When you copy your `region`, you might have to additionally copy the cloud provider identifier after the region name for some GCP and some AWS regions. For example, if your account URL is `https://ZS86751.europe-west4.gcp.snowflakecomputing.com`, then your `region` will be `europe-west4.gcp`. See [Account identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier) to learn more about Snowflake's account types and their identifiers.

  :::

3. Follow the [Snowflake documentation](https://community.snowflake.com/s/article/How-to-Capture-Snowflake-Users-Roles-and-Grants-Into-a-Table#:~:text=Snowflake%20Users%20and%20Roles%20via,Roles%20tab%2C%20as%20shown%20below) to copy your **Role**.
4. Copy your **Warehouse** from the **Warehouses** tab.

    ![Screenshot warehouses tab in Snowflake.](/img/tutorials/connections-snowflake_classic_warehouse_tab.png)

</TabItem>
</Tabs>

4. Copy the names for your **Database**, and **Schema**.
5. [Create a new user](https://docs.snowflake.com/en/sql-reference/sql/create-user) that Airflow can use to access Snowflake. Copy the username and password.

## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-snowflake
    ```

    This will install the Snowflake provider package, which makes the Snowflake connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Snowflake**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Schema**: Enter your **Schema**.
    - **Login**: Enter your username.
    - **Password**: Enter your password.
    - **Account**: Enter your `account-identifier`.
    - **Warehouse**: Enter your **Warehouse**.
    - **Database**: Enter your **Database**.
    - **Region**: Enter your `region`.
    - **Role**: Enter your **Role**.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![snowflake-connection-extra](/img/examples/connection-snowflake-aws.png)

## How it works

Airflow uses the [Snowflake connector](https://github.com/snowflakedb/snowflake-connector-python) python package to connect to Snowflake through the [SnowflakeHook](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/_api/airflow/providers/snowflake/hooks/snowflake/index.html).

## See also

- [Apache Airflow Snowflake provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html)
- [Snowflake Modules](https://registry.astronomer.io/modules?limit=24&sorts=updatedAt%3Adesc&query=snowflake) and [example DAGs](https://registry.astronomer.io/dags?query=snowflake) in the Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)
