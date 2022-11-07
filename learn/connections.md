---
title: "Manage connections in Apache Airflow"
sidebar_label: "Connections"
id: connections
---

<head>
  <meta name="description" content="Learn how to set up, manage, and maintain different types of connections in Apache Airflow. Use example connection configurations as the basis for your own connections." />
  <meta name="og:description" content="Learn how to set up, manage, and maintain different types of connections in Apache Airflow. Use example connection configurations as the basis for your own connections." />
</head>

Connections in Airflow are sets of configurations used to connect with other tools in the data ecosystem. Because most hooks and operators rely on connections to send and retrieve data from external systems, understanding how to create and configure them is essential for running Airflow in a production environment.

In this concept guide you'll:

- Learn about Airflow connections.
- Learn how to define connections using the Airflow UI.
- Learn how to define connections using environment variables.
- Add sample Snowflake and Slack Webhook connections to a DAG.

## Assumed knowledge

To get the most out of this concept guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md/).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).

## Airflow connection basics

An Airflow connection is a set of configurations that send requests to the API of an external tool. In most cases, a connection requires login credentials or a private key to authenticate Airflow to the external tool.

Airflow connections can be created by using one of the following methods:

- The [Airflow UI](airflow-ui.md)
- [Environment variables](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#environment-variables)
- The [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Connection)
- A [secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html) (a system for managing secrets external to Airflow)
- The [`airflow.cfg` file](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
- The [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/usage-cli.html)

This concept guide focuses on adding connections using the Airflow UI and environment variables. For more in-depth information on configuring connections using other methods, see the [REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Connection), [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) and [Secrets Backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html).

Each connection has a unique `conn_id` which can be provided to operators and [hooks](what-is-a-hook.md) that require a connection.

To standardize connections, Airflow includes many different connection types. There are general connection types for connecting to large clouds, such as `aws_default` and `gcp_default`, as well as connection types for specific services like `azure_service_bus_default`.

Each connection type requires different configurations and values based on the service it's connecting to. There are a couple of ways to find the information you need to provide for a particular connection type:

- Open the relevant provider's page in the [Astronomer Registry](https://registry.astronomer.io/providers/) and go to the **Docs** tab to access the Apache Airflow documentation for the provider. Most commonly used providers will have documentation on each of their associated connection types. For example, you can find information on how to set up different connections to Azure in the [Azure provider docs](https://registry.astronomer.io/providers/microsoft-azure).
- Check the documentation of the external tool you are connecting to and see if it offers guidance on how to authenticate.
- Refer to the source code of the hook that is being used by your operator.

## Defining connections in the Airflow UI

The most common way of defining a connection is using the Airflow UI. Go to **Admin** > **Connections**.

![Connections seen from the DAG view](/img/guides/DAGview_connections_cropped.png)

Airflow doesn't provide any preconfigured connections. To create a new connection, click the blue **+** button.

![Empty Connection](/img/guides/EmptyConnection.png)

As you update the **Connection Type** field, notice how the other available fields change. Each connection type requires different kinds of information. Specific connection   types are only available in the dropdown list when the relevant provider is installed in your Airflow environment.  

You don't have to specify every field for most connections. However, the values marked as required in the Airflow UI can be misleading. For example, to set up a connection to a PostgreSQL database, you need to reference the [PostgreSQL provider documentation](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html) to learn that the connection requires a `Host`, a user name as `login`, and a password in the `password` field.

![Example PostgreSQL connection](/img/guides/PostgreSQLconnection.png)

Any parameters that don't have specific fields in the connection form can be defined in the **Extra** field as a JSON dictionary. For example, you can add the `sslmode` or a client `sslkey` in the **Extra** field of your PostgreSQL connection.

Starting in Airflow 2.2, you can test some connection types from the Airflow UI with the **Test** button. After running a connection test, a message appears on the top of the screen showing either a success confirmation or an error message.

## Define connections with environment variables

Connections can also be defined using environment variables. If you use the Astro CLI, you can use the `.env` file for local development or specify environment variables in your project's Dockerfile.

> **Note**: If you are synchronizing your project to a remote repository, don't save sensitive information in your Dockerfile. In this case, using either a secrets backend, Airflow connections defined in the UI, or `.env` locally are preferred to avoid exposing secrets in plain text.

The environment variable used for the connection must be formatted as `AIRFLOW_CONN_YOURCONNID` and can be provided as a Uniform Resource Identifier (URI) or, starting in Airflow 2.3, in JSON.

[URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) is a format designed to contain all necessary connection information in one string, starting with the connection type, followed by login, password, and host. In many cases a specific port, schema, and additional parameters must be added.

```Dockerfile

# the general format of a URI connection that is defined in your Dockerfile
ENV AIRFLOW_CONN_MYCONNID='my-conn-type://login:password@host:port/schema?param1=val1&param2=val2'

# an example of a connection to snowflake defined as a URI
ENV AIRFLOW_CONN_SNOWFLAKE_CONN='snowflake://LOGIN:PASSWORD@/?account=xy12345&region=eu-central-1'

```

In Airflow 2.3+, connections can be provided to an environment variable as a JSON dictionary:

```json
# example of a connection defined as a JSON file in your `.env` file
AIRFLOW_CONN_MYCONNID='{
    "conn_type": "my-conn-type",
    "login": "my-login",
    "password": "my-password",
    "host": "my-host",
    "port": 1234,
    "schema": "my-schema",
    "extra": {
        "param1": "val1",
        "param2": "val2"
    }
}'
```
Connections that are defined using environment variables do not appear in the list of available connections in the Airflow UI.

## Masking sensitive information

Connections often contain sensitive credentials. By default, Airflow hides the `password` field in the UI and in the Airflow logs. If `AIRFLOW__CORE__HIDE_SENSITIVE_VAR_CONN_FIELDS` is set to `True`, values from the connection's `Extra` field are also hidden if their keys contain any of the words listed in `AIRFLOW__CORE__SENSITIVE_VAR_CONN_NAMES`. You can find more information on masking, including a list of the default values in this environment variable, in the Airflow documentation on [Masking sensitive data](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/mask-sensitive-values.html).

## Example: Configuring the SnowflakeToSlackOperator

In this example, you'll configure the `SnowflakeToSlackOperator`, which requires connections to Snowflake and Slack. You'll define the connections using the Airflow UI.

Before starting Airflow, you need to install the [Snowflake](https://registry.astronomer.io/providers/snowflake) and the [Slack](https://registry.astronomer.io/providers/slack) providers. If you use the Astro CLI, you can install the packages by adding the following lines to your Astro project's `requirements.txt` file:

```text
apache-airflow-providers-snowflake
apache-airflow-providers-slack
```

Open the Airflow UI and create a new connection. Set the **Connection Type** to `Snowflake`. This connection type requires the following parameters:

- Connection Id: `snowflake_conn` or any other string that is not already in use by an existing connection
- Connection Type: `Snowflake`
- Account: Your Snowflake account in the format `xy12345.region`
- Login: Your Snowflake login name.
- Password: Your Snowflake login password.

You can leave the other fields empty. Click **Test** to test the connection.

The following image shows the connection to Snowflake was successful.

![Successful Connection to Snowflake](/img/guides/SuccessfulSnowflakeConn.png)

Next you'll set up a connection to Slack. To post a message to a Slack channel, you need to create a Slack app for your server and configure incoming webhooks. See the [Slack Documentation](https://api.slack.com/messaging/webhooks) for setup steps.

To connect to Slack from Airflow, you need to provide the following parameters:

- Connection Id: `slack_conn` (or another string that has not been used for a different connection already)
- Connection Type: `Slack Webhook`
- Host: `https://hooks.slack.com.services`, which is the first part of your Webhook URL
- Password: The second part of your Webhook URL in the format `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`

Click **Test** to test the connection.

The last step is writing the DAG using the `SnowflakeToSlackOperator` to run a SQL query on a Snowflake table and post the result as a message to a Slack channel. The `SnowflakeToSlackOperator` requires both the connection id for the Snowflake connection (`snowflake_conn_id`) and the connection id for the Slack connection (`slack_conn_id`).

```python
from airflow import DAG
from datetime import datetime
from airflow.providers.snowflake.transfers.snowflake_to_slack import (
    SnowflakeToSlackOperator
)

with DAG(
    dag_id="snowflake_to_slack_dag",
    start_date=datetime(2022, 7, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    transfer_task = SnowflakeToSlackOperator(
        task_id="transfer_task",

        # the two connections are passed to the operator here:
        snowflake_conn_id="snowflake_conn",
        slack_conn_id="slack_conn",

        params={
            "table_name": "ORDERS",
            "col_to_sum": "O_TOTALPRICE"
        },
        sql="""
            SELECT
              COUNT(*) AS row_count,
              SUM({{ params.col_to_sum }}) AS sum_price
            FROM {{ params.table_name }}
        """,
        slack_message="""The table {{ params.table_name }} has
            => {{ results_df.ROW_COUNT[0] }} entries
            => with a total price of {{results_df.SUM_PRICE[0]}}"""
    )
```
