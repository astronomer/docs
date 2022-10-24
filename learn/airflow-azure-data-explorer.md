---
title: "Orchestrate Azure Data Explorer Queries with Airflow"
sidebar_label: "Azure Data Explorer"
description: "How to orchestrate Azure Data Explorer queries with your Apache Airflow DAGs."
id: airflow-azure-data-explorer
tags: ["Integrations", "Azure", "DAGs"]
---

[Azure Data Explorer](https://azure.microsoft.com/en-us/services/data-explorer/) (ADX) is a managed data analytics service used for performing real-time analysis of large volumes of streaming data. It's particularly useful for IoT applications, big data logging platforms, and SaaS applications.

You can use the ADX [Hook](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerhook) and [Operator](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerqueryoperator) which are part of the Azure provider package, to integrate ADX queries into your DAGs. In this guide, you'll learn how to make your ADX cluster work with Airflow and walk through an example DAG that runs a query against a database in that cluster.

:::info

All code in this guide can be found on [the Astronomer Registry](https://registry.astronomer.io/dags/azure-data-explorer-tutorial).

:::

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of ADX. See [Quickstart: Create an Azure Data Explorer cluster and database](https://docs.microsoft.com/en-us/azure/data-explorer/create-cluster-database-portal).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Configuring ADX to work with Airflow

To allow Airflow to communicate with your ADX database, you need to configure service principal authentication. To do this, you create and register an Azure AD service principal, then give that principal permission to access your ADX database. See [Create an Azure Active Directory application registration in Azure Data Explorer](https://docs.microsoft.com/en-us/azure/data-explorer/provision-azure-ad-app).

## Running an ADX query with Airflow

Once you have your ADX cluster running and service principal authentication configured, you can get started querying a database with Airflow.

:::info

In Airflow 2.0, provider packages are separate from the core of Airflow. If you are running 2.0 with Astronomer, the [Microsoft Provider](https://registry.astronomer.io/providers/microsoft-azure) package is already included in our Airflow Certified Image; if you are not using Astronomer you may need to install this package separately to use the hooks, operators, and connections described here.

::: 

First, set up an Airflow connection to your ADX cluster. If you do this using the Airflow UI, it should look something like this:

![ADX Connection](/img/guides/adx_connection.png)

The required pieces for the connection are:

- **Host:** Your cluster URL
- **Login:** Your client ID
- **Password:** Your client secret
- **Extra:** Should include at least "tenant" with your tenant ID, and "auth_method" with your chosen authentication method. Based on the auth method, you may also need to specify "certificate" and/or "thumbprint" parameters.

For more information on setting up this connection, including available authentication methods, see the [ADX hook documentation](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerhook).

Next, we define our DAG:

```python
from airflow import DAG
from airflow.providers.microsoft.azure.operators.adx import AzureDataExplorerQueryOperator
from datetime import datetime, timedelta

adx_query = '''StormEvents
| sort by StartTime desc
| take 10'''

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

with DAG('azure_data_explorer',
         start_date=datetime(2020, 12, 1),
         max_active_runs=1,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:

    opr_adx_query = AzureDataExplorerQueryOperator(
        task_id='adx_query',
        query=adx_query,
        database='storm_demo',
        azure_data_explorer_conn_id='adx'
    )
```

We define the query we want to run, `adx_query`, and pass that into the `AzureDataExplorerQueryOperator` along with the name of the database and the connection ID. When we run this DAG, the results of the query will automatically be pushed to XCom. When we go to XComs in the Airflow UI, we can see the data is there:

![ADX Xcom Results](/img/guides/adx_xcom.png)

From here we can build out our DAG with any additional dependent or independent tasks as needed.
