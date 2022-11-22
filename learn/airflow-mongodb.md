---
title: "Run a MongoDB query with Airflow"
sidebar_label: "MongoDB"
description: "Learn how to orchestrate MongoDB queries with your Apache Airflow DAGs."
id: "airflow-mongodb"
---

[MongoDB](https://www.mongodb.com/) is a noSQL document database designed for workloads of any scale. By leveraging the [Mongo provider](https://registry.astronomer.io/providers/mongo), you can easily orchestrate many MongoDB use cases with Airflow such as:

- Machine learning pipelines.
- Automating database administration operations.
- Batch data pipelines.

In this tutorial, you'll learn how to use Airflow to load data from an API into MongoDB and analyze that data using MongoDB Charts.

:::note

This tutorial was developed in partnership with MongoDB. For more details on this integration, including additional instruction on using MongoDB Charts, check out MongoDB's post [Using MongoDB with Apache Airflow](https://www.mongodb.com/developer/products/mongodb/mongodb-apache-airflow/).

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of MongoDB. See [].
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

To complete this tutorial, you need:

- A MongoDB cluster. If you don't already have a cluster, we recommend using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), a hosted MongoDB cluster with integrated data services that offers a free trial.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

## Step 1: Create a MongoDB Atlas cluster and database

If you are new to MongoDB, register for a [MongoDB Atlas account](https://www.mongodb.com/cloud/atlas/register) and follow the quickstart instructions to create a free cluster. In the cluster setup, create a database user with a password and add your IP address to the IP access list so that your local Airflow project will be able to access MongoDB. 

Once your cluster is running, go to **Collections** and create a new database.

![Mongo database](/img/tutorials/mongo_create_database.png)

For more instructions, see [Get started with Atlas](https://www.mongodb.com/docs/atlas/getting-started/).

If you already have a MongoDB cluster you can skip this step.

## Step 2: Configure your Astro project

Use the Astro CLI to create and run an Airflow project locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-mongodb-tutorial && cd astro-mongodb-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    apache-airflow-providers-mongo==3.0.0
    ```

    This installs the [Mongo provider](https://registry.astronomer.io/providers/mongo) package that contains all of the relevant MongoDB modules.

3. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 3: Configure your Airflow connections

Add two connections that Airflow will use to connect to MongoDB and the API providing the data. In the Airflow UI, go to **Admin** -> **Connections**.

1. Create a new connection named `mongo_default` and choose the `MongoDB` connection type. Enter the following information: 

    - **Host:** Your MongoDB Atlas host name
    - **Schema:** Your MongoDB database name
    - **Login:** Your database user ID
    - **Password:** Your database user password
    - **Extra:** {"srv": true}

    Your connection should look something like this:

    ![Mongo connection](/img/tutorials/mongo_airflow_connection.png)
    
    For more on connecting to your MongoDB cluster, see [Connect to a database deployment](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/).

2. Create a second connection named `http_default` and choose the `HTTP` connection type. Enter the following information:

    - **Host:** api.frankfurter.app

    This is the API you will gather data from to load into MongoDB. You can also replace this connection with a different API of your choosing.

## Step 4: Create your DAG

In your Astro project `dags/` folder, create a new file called `mongo-pipeline.py`. Paste the following code into the file:

```python
import os
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime,timedelta

def uploadtomongo(ti, **context):
    hook = MongoHook(mongo_conn_id='mongo_default')
    client = hook.get_conn()
    db = client.MyDB
    currency_collection=db.currency_collection
    print(f"Connected to MongoDB - {client.server_info()}")
    d=json.loads(context["result"])
    currency_collection.insert_one(d)

with DAG(
    dag_id="load_data_to_mongodb",
    schedule_interval=None,
    start_date=datetime(2022,10,28),
    catchup=False,
    default_args={
        "retries": 0,
    }
):

    t1 = SimpleHttpOperator(
        task_id='get_currency',
        method='GET',
        endpoint='2022-01-01..2022-06-30',
        headers={"Content-Type": "application/json"},
        do_xcom_push=True
        )

    t2 = PythonOperator(
        task_id='upload-mongodb',
        python_callable=uploadtomongo,
        op_kwargs={"result": t1.output},
        )

    t1 >> t2
```

This DAG uses the SimpleHttpOperator to get currency data from an API, and a PythonOperator to run a Python function that uses the MongoHook to load the data into MongoDB.

## Step 5: Run the DAG and review the data

Go to the Airflow UI, unpause your `load_data_to_mongodb` DAG, and trigger it to grab data from the currency API and load it to your MongoDB cluster.

In the MongoDB Atlas UI, go to your cluster and click **Collections** to view the data you just loaded.

![Mongo Results](/img/tutorials/mongo_loaded_data.png)

## Conclusion
