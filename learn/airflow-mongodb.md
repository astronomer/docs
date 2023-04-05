---
title: "Load data to MongoDB with Apache Airflow"
sidebar_label: "MongoDB"
description: "Learn how to load data into MongoDB with your Apache Airflow DAGs."
id: "airflow-mongodb"
sidebar_custom_props: { icon: 'img/integrations/mongodb.png' }
---

[MongoDB](https://www.mongodb.com/) is an open-source general purpose database built by developers, for developers. MongoDB's popularity is driven by its use of flexible document schemas and horizontal scalability. By leveraging the [Mongo provider](https://registry.astronomer.io/providers/mongo), you can easily orchestrate many use cases with Airflow such as:

- Machine learning pipelines.
- Automating database administration operations.
- Batch data pipelines.

In this tutorial, you'll learn how to use Airflow to load data from an API into MongoDB.

:::note

This tutorial was developed in partnership with MongoDB. For more details on this integration, including additional instruction on using MongoDB Charts, check out MongoDB's post [Using MongoDB with Apache Airflow](https://www.mongodb.com/developer/products/mongodb/mongodb-apache-airflow/).

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of MongoDB. See [Getting started](https://www.mongodb.com/docs/manual/tutorial/getting-started/).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your connections in Apache Airflow](connections.md).

## Prerequisites

- A MongoDB cluster. Astronomer recommends using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), a hosted MongoDB cluster with integrated data services that offers a free trial. See [Getting started with MongoDB Atlas](https://www.mongodb.com/docs/atlas/getting-started/).
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Step 1: Configure your MongoDB Atlas cluster and database

First you will need to configure your MongoDB Atlas cluster so Airflow can connect to it.

1. In your MongoDB Atlas account under **Security**, go to **Database Access** and create a database user with a password. Make sure the user has privileges to write data to the database.

    ![Mongo user](/img/tutorials/mongo_create_user.png)

2. Go to **Security** -> **Network Access** and add your public IP address to the IP access list. You can find your public IP address on Mac and Linux by running `curl ifconfig.co/`, or on Windows by running `ipconfig /all`.

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

The connections you configure will connect to MongoDB and the API providing sample data.

1. In the Airflow UI, go to **Admin** -> **Connections**.

2. Create a new connection named `mongo_default` and choose the `MongoDB` connection type. Enter the following information:

    - **Host:** Your MongoDB Atlas host name
    - **Login:** Your database user ID
    - **Password:** Your database user password
    - **Extra:** {"srv": true}

    Your connection should look something like this:

    ![Mongo connection](/img/tutorials/mongo_airflow_connection.png)

    If you don't know your MongoDB Atlas host name, go to your database in the Atlas UI and click on **Connect**. Any of the connection options in this section will give you a connection URI that will include your host name. For more on connecting to your MongoDB cluster, see [Connect to a database deployment](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/).

3. Create a second connection named `http_default` and choose the `HTTP` connection type. Enter the following information:

    - **Host:** api.frankfurter.app

    This is the API you will gather data from to load into MongoDB. You can also replace this connection with a different API of your choosing.

## Step 4: Create your DAG

In your Astro project `dags` folder, create a new file called `mongo-pipeline.py`. Paste the following code into the file:

```python
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from pendulum import datetime

def uploadtomongo(ti, **context):
    hook = MongoHook(mongo_conn_id='mongo_default')
    client = hook.get_conn()
    db = client.MyDB # Replace "MyDB" if you want to load data to a different database
    currency_collection=db.currency_collection
    print(f"Connected to MongoDB - {client.server_info()}")
    d=json.loads(context["result"])
    currency_collection.insert_one(d)

with DAG(
    dag_id="load_data_to_mongodb",
    schedule=None,
    start_date=datetime(2022, 10, 28),
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

This DAG gets currency data from an API using the SimpleHttpOperator and loads the data into MongoDB using the MongoHook and the PythonOperator. The data will be loaded as a new collection in a database called `MyDB`.

## Step 5: Run the DAG and review the data

Go to the Airflow UI, unpause your `load_data_to_mongodb` DAG, and trigger it to grab data from the currency API and load it to your MongoDB cluster.

In the MongoDB Atlas UI, go to your cluster and click **Collections** to view the data you just loaded.

![Mongo Results](/img/tutorials/mongo_loaded_data.png)

## Conclusion

Congratulations! You now know how to use Airflow to load data to your MongoDB cluster. A great next step is to analyze that data using MongoDB Charts in Mongo Atlas. For more on this, see Mongo's complementary [tutorial](https://www.mongodb.com/developer/products/mongodb/mongodb-apache-airflow/).
