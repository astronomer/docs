---
title: 'Set up a custom XComs backend'
sidebar_label: 'Custom XComs backend'
id: cloud-ide-tutorial
description: 'Use this tutorial to learn how to set up a custom XComs backend in AWS, GCP and Azure.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow offers the possibility to use [XComs](airflow-passing-data-between-tasks.md) to pass information between your tasks, which is stored in the XCom backend. By default Airflow uses the [metadata database](airflow-database.md) as an XComs backend, which works well for local development purposes but can become limiting in a production environment. If your storage needs for XComs exceed the size of the Airflow metadatabase or you want to add custom functionality like retention policies, store data that is not JSON serializeable etc you can configure a custom XComs backend. To learn more about when and when not to use a custom XComs backend see the [Best practices](#best-practices) section and the end of this tutorial. 

After you complete this tutorial, you'll be able to:

- 

:::caution

While a custom XComs backend allows you to store virtually unlimited amounts of data as XComs, keep in mind that Airflow was not designed be a data processing framework and you might run into performance issue if you try to pass large amounts of data via XComs. Astronomer recommends to use an external processing framework such as [Apache Spark](https://spark.apache.org/) to handle heavy data processing and orchestrate the process with Airflow using the [Apache Spark provider](https://registry.astronomer.io/providers/spark).

:::

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- XComs basics. See the [Airflow documentation on XComs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html).
- Passing data between tasks. See [Passing data between Airflow tasks](airflow-passing-data-between-tasks.md).
- The TaskFlow API. See [the TaskFlow API in Airflow 2.0](https://www.astronomer.io/events/webinars/taskflow-api-airflow-2.0/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).


## Step 1: Set up your XComs backend 

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'Local', value: 'local'}
    ]}>
<TabItem value="aws">

To use an S3 bucket as your custom XCom backend follow these steps:

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html). In the creation settings, make sure to enable Bucket Versioning and that public access is blocked.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below (replace `<YOUR BUCKET NAME>` with the name of your S3 bucket) or use AWS' graphical user interface to replicate what you see in the screenhot.

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:ReplicateObject",
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:RestoreObject",
                    "s3:ListBucket",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::<YOUR BUCKET NAME>/*",
                    "arn:aws:s3:::<YOUR BUCKET NAME>"
                ]
            }
        ]
    }
    ```

    [AWS IAM policy for the XCom backend](/img/guides/xcom_backend_aws_policy.png)

3. Save your policy under the name `AirflowXComBackendAWSS3`. 

4. [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) called `airflow-xcoms` with the AWS credential type `Access key - Programmatic access`. Attach the `AirflowXComBackendAWSS3` policy to this user as shown in the screenshot below. Make sure to save the Access key ID and the Secret access key.

    [AWS IAM user for the XCom backend](/img/guides/xcom_backend_aws_user.png)


</TabItem>

<TabItem value="gcp">



</TabItem>

<TabItem value="azure">



</TabItem>

<TabItem value="local">



</TabItem>


</Tabs>

## Step 2: Create an Astro project

1. Set up Airflow by creating a new Astro project:

    ```sh
    $ mkdir astro-extra-link-tutorial && cd astro-extra-link-tutorial
    $ astro dev init
    ```

2. Start up Airflow by running:

    ```sh
    $ astro dev start
    ```

## Step 3: Create a connection

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'Local', value: 'local'}
    ]}>
<TabItem value="aws">

To give Airflow access to your S3 bucket you need to define an [Airflow connection](connections.md). 

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Amazon Web Service`. Provide the AWS Access Key ID and AWS Secret Access Key from the IAM user you created in [Step 1](#step-1-set-up-your-xcoms-backend). The screenshot below shows the connection using the Connection ID `s3_xcoms_backend_conn`.

    [Airflow Connection to S3](/img/guides/xcom_backend_aws_connection.png)

2. Save your connection.

:::tip

It is also possible to define a [connection using environment variables](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables). If Airflow is running in the same AWS environment as your custom XCom backend it is best practice to [assume a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) rather than provide credentials.

:::

</TabItem>

<TabItem value="gcp">



</TabItem>

<TabItem value="azure">



</TabItem>

<TabItem value="local">



</TabItem>


</Tabs>

## Step 4: Define a custom XCom class using JSON serialization

For Airflow to be able to use your custom XCom backend it is necessary to define an XCom backend class which inherits from the `BaseXCom` class.

1. In your Astro project create a new file in the `include` directory called `s3_xcom_backend_json.py`.

2. Copy paste the following code into the file:

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.amazon.aws.hooks.s3 import S3Hook
    import json
    import uuid

    class S3XComBackendJSON(BaseXCom):
        PREFIX = "xcom_s3://"
        BUCKET_NAME = "s3-xcom-backend-example"

        @staticmethod
        def serialize_value(
            value,
            key=None,
            task_id=None,
            dag_id=None,
            run_id=None,
            map_index= None,
            **kwargs
        ):
            
            hook        = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            filename    = "data_" + str(uuid.uuid4()) + ".json"
            s3_key      = f"{run_id}/{task_id}/{filename}"

            with open(filename, 'a+') as f:
                json.dump(value, f)

            hook.load_file(
                filename=filename,
                key=s3_key,
                bucket_name=S3XComBackend.BUCKET_NAME,
                replace=True
            )
            reference_string = S3XComBackend.PREFIX + s3_key

            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            reference_string = BaseXCom.deserialize_value(result=result)
            
            hook    = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            key     = reference_string.replace(S3XComBackend.PREFIX, "")

            filename = hook.download_file(
                key=key,
                bucket_name=S3XComBackend.BUCKET_NAME,
                local_path="/tmp"
            )

            with open(filename, 'r') as f:
                output = json.load(f)

            return output
    ```

    The code above defines a class called `S3XComBackendJSON`. The class has two methods: `.serialize_value()` defines how the `value` that is pushed to XComs from an Airflow task is handled, while `.deserialize_value()` contains the logic to retrieve information from the XComs backend.

    The `.serialize_value()` method accomplishes the following:

    - Instatiates an [`S3Hook`](https://registry.astronomer.io/providers/amazon/modules/s3hook) using the `s3_xcom_backend_conn` connection that was defined in [Step 3](#step-3-create-a-connection).
    - Creates a unique `filename` using the [`uuid` package](https://docs.python.org/3/library/uuid.html).
    - Uses the `run_id` and `task_id` from the Airflow context to define the `s3_key` under which the file will be saved in the S3 bucket.
    - Writes the `value` that is being pushed to XComs to a JSON file.
    - Uploads the JSON file to S3.
    - Creates a `reference_string` using the `s3_key` that is written to the Airflow metadata database as a regular XCom.

    The `.deserialize_value()` method:

    - Retrieves the `reference_string` for a given entry (`result`) from the Airflow metadata database using regular XComs.
    - Downloads the JSON file at the `key` contained in the `reference_string`.
    - Retrieves the information from the JSON file.

3. Open the `.env` file of your Astro Project and add the following line to set your XCom backend to the custom class:

    ```sh
    AIRFLOW__CORE__XCOM_BACKEND=include.s3_xcom_backend_json.S3XComBackendJSON
    ```

4. Restart your Airflow instance using `astro dev restart`.

## Step 5: Run a simple DAG using XComs




## Step 6: Create a custom serialization method to handle Pandas dataframes



## Step 7: Run a DAG passing Pandas dataframes via XComs


```python
from airflow.decorators import dag, task
from pendulum import datetime 
import pandas as pd
import requests

MY_FAVORITE_POKEMON = "pikachu"
MY_OTHER_FAVORITE_POKEMON = "vulpix"

@dag(
    start_date=datetime(2022, 12, 20),
    schedule="@daily",
    catchup=False
)
def fetch_pokemon_data_dag():

    @task 
    def extract_data():
        """Extracts data from the pokemon API. Returns a JSON serializeable dict."""

        r1 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{MY_FAVORITE_POKEMON}")
        r2 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{MY_OTHER_FAVORITE_POKEMON}")

        return {
            "pokemon": [f"{MY_FAVORITE_POKEMON}", f"{MY_OTHER_FAVORITE_POKEMON}"],
            "base_experience": [r1.json()["base_experience"], r2.json()["base_experience"]],
            "height" : [r1.json()["height"], r2.json()["height"]]
        }

    @task
    def calculate_xp_per_height(pokemon_data_dict):
        """Calculates base XP per height and returns a pandas dataframe."""

        df = pd.DataFrame(pokemon_data_dict)

        df["xp_per_height"] = df["base_experience"] / df["height"]

        return df

    @task 
    def print_xp_per_height(pokemon_data_df):
        """Retrieves information from a pandas dataframe in the custom XComs 
        backend. Prints out pokemon information."""

        for i in pokemon_data_df.index:
            pokemon = pokemon_data_df.loc[i, 'pokemon']
            xph = pokemon_data_df.loc[i, 'xp_per_height']
            print(f"{pokemon} has a base xp to height ratio of {xph}")

    print_xp_per_height(calculate_xp_per_height(extract_data()))

fetch_pokemon_data_dag()
```



## Best practices

Common reasons to use a custom XComs backend are:

- Needing more storage space for XComs than the metadata database can offer.
- Running a production environment that where custom retention, deletion and backup policies for XComs are desired. With a custom XComs backend you do not need to worry about periodically cleaning up the metadata database.
- The need for custom serialization and deserialization methods. By default Airflow uses JSON serialization which puts limits on the type of data that you can pass via XComs (pickling is available by setting `AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True` but has [known security implications](https://docs.python.org/3/library/pickle.html)).
- Having a custom setup where access to XComs is needed without accessing the metadata database. 
