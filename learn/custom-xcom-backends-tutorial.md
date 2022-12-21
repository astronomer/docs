---
title: 'Set up a custom XComs backend'
sidebar_label: 'Custom XComs backend'
id: xcoms-backend-tutorial
description: 'Use this tutorial to learn how to set up a custom XComs backend in AWS, GCP and Azure.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow offers the possibility to use [XComs](airflow-passing-data-between-tasks.md) to pass information between your tasks, which is stored in the XCom backend. By default Airflow uses the [metadata database](airflow-database.md) as an XComs backend, which works well for local development purposes but can become limiting in a production environment. If your storage needs for XComs exceed the size of the Airflow metadatabase or you want to add custom functionality like retention policies, store data that is not JSON serializeable etc you can configure a custom XComs backend. To learn more about when and when not to use a custom XComs backend see the [Best practices](#best-practices) section and the end of this tutorial. 

This tutorial uses the TaskFlow API to pass information between tasks. Learn more in our [Airflow decorators](airflow-decorators.md) guide and in the [TaskFlow API in Airflow 2.0 webinar](https://www.astronomer.io/events/webinars/taskflow-api-airflow-2.0/).

After you complete this tutorial, you'll be able to:

- Create a custom XCom backend using an S3 bucket.
- Use JSON serialization and deserialization in a custom XCom backend.
- Add a custom logic to the serialization and deserialization methods to store Pandas dataframes as CSV.
- Know best practices of using custom XCom backends.

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

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) called `s3-xcom-backend-example`. In the creation settings, make sure to enable Bucket Versioning and that public access is blocked.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below or use AWS' graphical user interface to replicate what you see in the screenhot.

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
                    "arn:aws:s3:::s3-xcom-backend-example/*",
                    "arn:aws:s3:::s3-xcom-backend-example"
                ]
            }
        ]
    }
    ```

    ![AWS IAM policy for the XCom backend](/img/guides/xcom_backend_aws_policy.png)

3. Save your policy under the name `AirflowXComBackendAWSS3`. 

4. [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) called `airflow-xcoms` with the AWS credential type `Access key - Programmatic access`. Attach the `AirflowXComBackendAWSS3` policy to this user as shown in the screenshot below. Make sure to save the Access key ID and the Secret access key.

    ![AWS IAM user for the XCom backend](/img/guides/xcom_backend_aws_user.png)

</TabItem>

<TabItem value="gcp"></TabItem>
<TabItem value="azure"></TabItem>
<TabItem value="local"></TabItem>

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

    ![Airflow Connection to S3](/img/guides/xcom_backend_aws_connection.png)

2. Save your connection.

:::tip

It is also possible to define a [connection using environment variables](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables). If Airflow is running in the same AWS environment as your custom XCom backend it is best practice to [assume a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) rather than provide credentials.

:::

</TabItem>

<TabItem value="gcp"></TabItem>
<TabItem value="azure"></TabItem>
<TabItem value="local"></TabItem>

</Tabs>

## Step 4: Define a custom XCom class using JSON serialization

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

For Airflow to be able to use your custom XCom backend it is necessary to define an XCom backend class which inherits from the `BaseXCom` class.

1. In your Astro project create a new file in the `include` directory called `s3_xcom_backend_json.py`.

2. Copy paste the following code into the file:

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.amazon.aws.hooks.s3 import S3Hook
    import json
    import uuid

    class S3XComBackendJSON(BaseXCom):
        # the prefix is optional and used to make it easier to recognize
        # which reference strings in the Airflow metadata database
        # refer to an XCom that has been stored in an S3 bucket
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
            
            # the connection to AWS is created by using the S3 hook with 
            # the conn id configured in Step 3
            hook        = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename    = "data_" + str(uuid.uuid4()) + ".json"
            # define the full S3 key where the file should be stored
            s3_key      = f"{run_id}/{task_id}/{filename}"

            # write the value to a local temporary JSON file
            with open(filename, 'a+') as f:
                json.dump(value, f)

            # load the local JSON file into the S3 bucket
            hook.load_file(
                filename=filename,
                key=s3_key,
                bucket_name=S3XComBackendJSON.BUCKET_NAME,
                replace=True
            )

            # define the string that will be saved to the Airflow metadata 
            # database to refer to this XCom
            reference_string = S3XComBackendJSON.PREFIX + s3_key

            # use JSON serialization to write the reference string to the
            # Airflow metadata database (like a regular XCom)
            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            # retrieve the relevant reference string from the metadata database
            reference_string = BaseXCom.deserialize_value(result=result)
            
            # create the S3 connection using the S3Hook and recreate the S3 key
            hook    = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            key     = reference_string.replace(S3XComBackendJSON.PREFIX, "")

            # download the JSON file found at the location described by the 
            # reference string to a temporary local folder
            filename = hook.download_file(
                key=key,
                bucket_name=S3XComBackendJSON.BUCKET_NAME,
                local_path="/tmp"
            )

            # load the content of the local JSON file and return it to be used by
            # the operator
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

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.s3_xcom_backend_json.S3XComBackendJSON
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>

<TabItem value="gcp"></TabItem>
<TabItem value="azure"></TabItem>
<TabItem value="local"></TabItem>

</Tabs>

## Step 5: Run a simple DAG using XComs

To test your custom XCom backend you will run a simple DAG which pushes a random number to your custom XCom backend and then retrieves it again.

1. Create a new file in your `dags` folder named `simple_xcom_dag.py`.

2. Copy and paste the code below into the file.

    ```python
        from airflow.decorators import dag, task
        from pendulum import datetime
        import random

        @dag(
            start_date=datetime(2022, 12, 20),
            schedule="@daily",
            catchup=False
        )
        def simple_xcom_dag():

            @task
            def pick_a_random_number():
                return random.randint(1, 10) # push to XCom

            @task
            def print_a_number(num): # retrieve from XCom
                print(num) 

            print_a_number(pick_a_random_number())

        simple_xcom_dag()
    ```

3. Run the DAG.

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

4. View the logs of both tasks, they include information about the custom XComs backend. The `print_a_number` task includes the full path to the file stored in the S3 bucket.

    ![Logs mentioning custom XCom backend](/img/guides/xcom_backend_task_logs_simple.png)

5. View the XCom in your S3 bucket.

    ![XComs in the S3 bucket](/img/guides/xcom_backend_S3_json.png)

</TabItem>

<TabItem value="gcp"></TabItem>
<TabItem value="azure"></TabItem>
<TabItem value="local"></TabItem>

</Tabs>

## Step 6: Create a custom serialization method to handle Pandas dataframes

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

A powerful feature of custom XCom backends is the possibility to adjust serialization and deserialization methods to be able to handle object that cannot be JSON-serialized. In this step you will create a custom XCom backend that can save the contents of a [Pandas](https://pandas.pydata.org/) dataframe as a CSV file.

1. Create a second file in your `include` folder called `s3_xcom_backend_pandas.py`.

2. Copy and paste the following code into the file.

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.amazon.aws.hooks.s3 import S3Hook

    import pandas as pd
    import json
    import uuid

    class S3XComBackendPandas(BaseXCom):
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

            hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            
            # added serialization method if the value passed is a Pandas dataframe
            # the contents are written to a local temporary csv file
            if isinstance(value, pd.DataFrame):
                filename    = "data_" + str(uuid.uuid4()) + ".csv"
                s3_key      = f"{run_id}/{task_id}/{filename}"

                value.to_csv(filename)

            # if the value passed is not a Pandas dataframe, attempt to use
            # JSON serialization
            else:
                filename    = "data_" + str(uuid.uuid4()) + ".json"
                s3_key      = f"{run_id}/{task_id}/{filename}"

                with open(filename, 'a+') as f:
                    json.dump(value, f)

            hook.load_file(
                filename=filename,
                key=s3_key,
                bucket_name=S3XComBackendPandas.BUCKET_NAME,
                replace=True
            )

            reference_string = S3XComBackendPandas.PREFIX + s3_key

            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            result = BaseXCom.deserialize_value(result)

            hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            key = result.replace(S3XComBackendPandas.PREFIX, "")

            filename = hook.download_file(
                key=key,
                bucket_name=S3XComBackendPandas.BUCKET_NAME,
                local_path="/tmp"
            )

            # added deserialization option to convert a CSV back to a dataframe
            if key.split(".")[-1] == "csv":
                output = pd.read_csv(filename)
            # if the key does not end in 'csv' use JSON deserialization
            else:
                with open(filename, 'r') as f:
                    output = json.load(f)

            return output

    ```

    The code above creates a second custom XCom backend called `S3XComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to the S3 bucket and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

3. In the `.env` file of your Astro project, change the XCom backend variable to use the newly created `S3XComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.s3_xcom_backend_pandas.S3XComBackendPandas
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>

<TabItem value="gcp"></TabItem>
<TabItem value="azure"></TabItem>
<TabItem value="local"></TabItem>

</Tabs>

## Step 7: Run a DAG passing Pandas dataframes via XComs

Test the new custom XCom backend by running a DAG that pushes a Pandas dataframe to and pulls a Pandas dataframe from XComs.

1. Create a new file called `fetch_pokemon_data_dag.py` in the `dags` folder of your Astro project.

2. Copy and paste the DAG below. Make sure to enter your favorite Pokemon.

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

    The `extract_data` task will push a dictionary to XCom, which will be saved to your blob storage as a JSON file and retrieved by the `calculate_xp_per_height` task. This second task pushes a Pandas dataframe to XComs which is only possible when using a custom XCom backend with a serialization option for this type of object. The last task `print_xp_per_height` retrives the csv and recreates the Pandas dataframe before printing out the Pokemon and their base experience to height ratio.

3. View the information about your favorite pokemon in the task log of the `print_xp_per_height` task.

    ![Pokemon Information in logs](/img/guides/xcom_backend_task_logs_pokemon.png)

## Best practices

Common reasons to use a custom XComs backend are:

- Needing more storage space for XComs than the metadata database can offer.
- Running a production environment that where custom retention, deletion and backup policies for XComs are desired. With a custom XComs backend you do not need to worry about periodically cleaning up the metadata database.
- The need for custom serialization and deserialization methods. By default Airflow uses JSON serialization which puts limits on the type of data that you can pass via XComs (pickling is available by setting `AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True` but has [known security implications](https://docs.python.org/3/library/pickle.html)).
- Having a custom setup where access to XComs is needed without accessing the metadata database. 

## Conclustion

Congratulation! You learned how to set up a custom XCom backend and how to define your own serialization and deserialization methods. 