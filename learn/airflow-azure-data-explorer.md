---
title: "Run an Azure Data Explorer query with Airflow"
sidebar_label: "Azure Data Explorer"
description: "Learn how to orchestrate Azure Data Explorer queries with your Apache Airflow DAGs."
id: airflow-azure-data-explorer
sidebar_custom_props: { icon: 'img/integrations/azure-data-explorer.png' }
---

[Azure Data Explorer](https://azure.microsoft.com/en-us/services/data-explorer/) (ADX) is a managed data analytics service used for performing real-time analysis of large volumes of streaming data. It's particularly useful for IoT applications, big data logging platforms, and SaaS applications.

You can use the ADX [Hook](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerhook) and [Operator](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerqueryoperator) which are part of the Azure provider package, to integrate ADX queries into your DAGs. In this tutorial, you'll learn how to make your ADX cluster work with Airflow and create a DAG that runs a query against a database in that cluster.

:::info

All code in this tutorial can be found on [the Astronomer Registry](https://registry.astronomer.io/dags/azure-data-explorer/versions/latest).

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of ADX. See [Quickstart: Create an Azure Data Explorer cluster and database](https://docs.microsoft.com/en-us/azure/data-explorer/create-cluster-database-portal).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

To complete this tutorial, you need:

- A running ADX cluster with a database. See [Quickstart: Create an Azure Data Explorer cluster and database](https://docs.microsoft.com/en-us/azure/data-explorer/create-cluster-database-portal) for instructions. If you don't already have an ADX cluster, Azure offers a $200 credit when you sign up for a free Azure account.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

## Step 1: Configure your ADX cluster to work with Airflow

To allow Airflow to communicate with your ADX database, you need to configure service principal authentication. To do this, create and register an Azure AD service principal, then give that principal permission to access your ADX database. See [Create an Azure Active Directory application registration in Azure Data Explorer](https://docs.microsoft.com/en-us/azure/data-explorer/provision-azure-ad-app) for more details.

## Step 2: Populate your ADX database

Populate your ADX database with demo data. See [Quickstart: Ingest sample data into ADX](https://learn.microsoft.com/en-us/azure/data-explorer/ingest-sample-data?tabs=ingestion-wizard) for instructions on ingesting the `StormEvents` sample dataset. If you are working with an existing ADX cluster that already contains data, you can skip this step.

## Step 3: Configure your Astro project

Now that you have your Azure resources configured, you can move on to setting up Airflow.

1. Create a new Astro project:

    ```sh
    mkdir astro-adx-tutorial && cd astro-adx-tutorial
    astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Azure provider package that contains all of the relevant ADX modules.

3. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 4: Add an Airflow connection to ADX

Add a connection that Airflow will use to connect to ADX. In the Airflow UI, go to **Admin** -> **Connections**.

Create a new connection named `adx` and choose the `Azure Data Explorer` connection type. Enter the following information:

- **Host:** Your cluster URL
- **Login:** Your client ID
- **Password:** Your client secret
- **Extra:** Include at least "tenant" with your tenant ID, and "auth_method" with your chosen authentication method. The method will correspond to how you set up your service principle in Step 1. Based on the auth method, you may also need to specify "certificate" and/or "thumbprint" parameters.

For more information on setting up this connection, including available authentication methods, see the [ADX hook documentation](https://registry.astronomer.io/providers/microsoft-azure/modules/azuredataexplorerhook).

Your connection should look similar to this:

![ADX Connection](/img/guides/adx_connection.png)

## Step 5: Create your DAG

In your Astro project `dags/` folder, create a new file called `adx-pipeline.py`. Paste the following code into the file:

```python
from airflow import DAG
from airflow.providers.microsoft.azure.operators.adx import AzureDataExplorerQueryOperator
from datetime import datetime, timedelta

adx_query = '''StormEvents
| sort by StartTime desc
| take 10'''

with DAG('azure_data_explorer',
         start_date=datetime(2020, 12, 1),
         max_active_runs=1,
         schedule='@daily',
         default_args={
            'depends_on_past': False,
            'retries': 0,
        },
         catchup=False
         ) as dag:

    opr_adx_query = AzureDataExplorerQueryOperator(
        task_id='adx_query',
        query=adx_query,
        database='storm_demo',
        azure_data_explorer_conn_id='adx'
    )
```

Update the `database` parameter in the `AzureDataExplorerQueryOperator` to be the name of your database. If you are not working with the `StormEvents` demo dataset, you can also update the `adx_query` to something appropriate for your data.

## Step 6: Run your DAG and review XComs

Go to the Airflow UI, unpause your `azure_data_explorer` DAG, and trigger it to run the query in your ADX cluster. The results of the query will automatically be pushed to XCom. Go to **Admin** -> **XComs** to view the results.

![ADX Xcom Results](/img/guides/adx_xcom.png)

## Conclusion

After finishing this tutorial you should know how to configure an ADX cluster to work with Airflow and run a query against an ADX database from your Airflow DAG. From here you can build out your DAG with any additional dependent or independent tasks as needed.
