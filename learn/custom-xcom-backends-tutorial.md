---
title: 'Set up a custom XComs backend using cloud-based or local object storage'
sidebar_label: 'Set up a custom XComs backend'
id: xcoms-backend-tutorial
description: 'Use this tutorial to learn how to set up a custom XComs backend in AWS, GCP and Azure.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow offers the possibility to use [XComs](airflow-passing-data-between-tasks.md) to pass information between your tasks, which is stored in the XCom backend. By default Airflow uses the [metadata database](airflow-database.md) as an XComs backend, which works well for local development purposes but can become limiting in a production environment. There are many use cases for custom XCom backend solutions, you can learn more about them in the [Best practices](#best-practices) section and the end of this tutorial. 

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
- You can follow this tutorial using an AWS, GCP or Azure account. If you want to work locally follow the steps under the `MinIO` tabs.

## Step 1: Set up your XComs backend 

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

To use an S3 bucket as your custom XCom backend follow these steps:

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) called `s3-xcom-backend-example`. In the creation settings, make sure to enable Bucket Versioning and that public access is blocked.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below or use AWS' graphical user interface to replicate what you see in the screenshot.

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

<TabItem value="gcp">

To use a bucket in Google Cloud storage as your custom XCom backend follow these steps:

1. Log into your Google Cloud account and [create a new project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) called `custom-xcom-backend-example`.

2. [Create a new bucket](https://cloud.google.com/storage/docs/creating-buckets) called `gcs-xcom-backend-example`. Consider enabling object versioning.

3. [Create a custom IAM role](https://cloud.google.com/iam/docs/creating-custom-roles) called `AirflowXComBackendGCS` for Airflow to access your bucket. With 6 permissions assigned:

    - storage.buckets.list
    - storage.objects.create
    - storage.objects.delete
    - storage.objects.get
    - storage.objects.list
    - storage.objects.update

    ![GCS IAM role](/img/guides/xcom_backend_gcs_role.png)

4. [Create a new service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) called `airflow-xcoms` and grant it access to your project via the `AirflowXComBackendGCS` role.

    ![GCS IAM role](/img/guides/xcom_backend_gcs_service_account.png)

5. [Create a new key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your `airflow-xcoms` service account and make sure to download the credentials in JSON format.

</TabItem>
<TabItem value="azure">

To use an Azure blob storage as your custom XCom backend follow these steps:

1. Log into your Azure account and if you do not have one, [create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create). We recommend to disable public access.

2. Within the storage account. [Create a new container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-porta) called `custom-xcom-backend`. 

3. [Create a shared access token](https://learn.microsoft.com/en-us/azure/cognitive-services/Translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers) for the `custom-xcom-backend` container. In the dropdown menu for permissions make sure to enable: Read, Add, Create, Write, Delete and List. Select the duration during which the token will be valid and `HTTPS only` for allowed protocols. Provide the IP address of your Airflow instance. If you are running Airflow locally with the Astro CLI this is the IP address of your computer.

    ![Shared access token](/img/guides/xcom_backend_shared_access_token.png)

4. Click on `Generate SAS token and URL` and copy the Blob SAS URL. This URL contains a secret and you will need it again in [Step 3](#step-3-create-a-connection) of this tutorial.

</TabItem>
<TabItem value="local">

There are several local object storage solutions available to configure as a custom XCom backend. In this tutorial we are going to use MinIO running in Docker. 

1. [Start a MinIO container](https://min.io/docs/minio/container/index.html). 

2. Go to `http://127.0.0.1:9090/`, log in and create a new bucket called `custom-xcom-backend`.

3. Create a new Access Key and store it in a secure location.


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
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

To give Airflow access to your S3 bucket you need to define an [Airflow connection](connections.md). 

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Amazon Web Service`. Provide the AWS Access Key ID and AWS Secret Access Key from the IAM user you created in [Step 1](#step-1-set-up-your-xcoms-backend). The screenshot below shows the connection using the Connection ID `s3_xcom_backend_conn`.

    ![Airflow Connection to S3](/img/guides/xcom_backend_aws_connection.png)

2. Test and save your connection.

:::tip

It is also possible to define a [connection using environment variables](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables). If Airflow is running in the same AWS environment as your custom XCom backend it is best practice to [assume a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) rather than provide credentials.

:::

</TabItem>

<TabItem value="gcp">

To give Airflow access to your GCS bucket you need to define an [Airflow connection](connections.md). 

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Google Cloud`. Provide the name of your project (`custom-xcom-backend-example`). Open the JSON file with the credentials you downloaded in [Step 1](#step-1-set-up-your-xcoms-backend) and copy paste it in full into the field `Keyfile JSON`. The screenshot below shows the connection using the Connection ID `gcs_xcoms_backend_conn`.

    ![Airflow Connection to GCS bucket](/img/guides/xcom_backend_gcs_connection.png)

2. Test and save your connection.

:::tip

It is also possible to define a [connection using environment variables](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables).

:::

</TabItem>
<TabItem value="azure">

To give Airflow access to your Azure container you need to define an [Airflow connection](connections.md).

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Azure Blob Storage`. Provide the full Blob SAS URL to the `SAS Token` field. The screenshot below shows the connection using the Connection ID `azure_xcoms_backend_conn`.

    ![Airflow Connection to Azure container](/img/guides/xcom_backend_azure_connection.png)

2. Test and save your connection.

:::tip

It is also possible to define a [connection using environment variables](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables).

:::

</TabItem>
<TabItem value="local">

To give Airflow access to your MinIO bucket you will need to use the credentials created in [Step 1](#step-1-set-up-your-xcoms-backend). 

1. In your Astro project's `.env` file set the following environment variables. You may need to adjust your `MINIO_IP` if you have chosen a custom API port.

    ```text
    MINIO_ACCESS_KEY=<your access key>
    MINIO_SECRET_KEY=<your secret key>
    MINIO_IP=host.docker.internal:9000
    ```

2. In order to be able to use the `minio` Python package in Airflow, add it to the `requirements.txt` file of your Astro project.

    ```text
    minio
    ```

</TabItem>

</Tabs>

## Step 4: Define a custom XCom class using JSON serialization

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
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
    import os

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
            hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename = "data_" + str(uuid.uuid4()) + ".json"
            # define the full S3 key where the file should be stored
            s3_key = f"{run_id}/{task_id}/{filename}"

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

            os.remove(filename)

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
            hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
            key = reference_string.replace(S3XComBackendJSON.PREFIX, "")

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

            os.remove(filename)

            return output
    ```

    The code above defines a class called `S3XComBackendJSON`. The class has two methods: `.serialize_value()` defines how the `value` that is pushed to XComs from an Airflow task is handled, while `.deserialize_value()` contains the logic to retrieve information from the XComs backend.

    The `.serialize_value()` method accomplishes the following:

    - Instantiates an [`S3Hook`](https://registry.astronomer.io/providers/amazon/modules/s3hook) using the `s3_xcom_backend_conn` connection that was defined in [Step 3](#step-3-create-a-connection).
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

<TabItem value="gcp">

For Airflow to be able to use your custom XCom backend it is necessary to define an XCom backend class which inherits from the `BaseXCom` class.

1. In your Astro project create a new file in the `include` directory called `gcs_xcom_backend_json.py`.

2. Copy paste the following code into the file:

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.google.cloud.hooks.gcs import GCSHook
    import json
    import uuid
    import os

    class GCSXComBackendJSON(BaseXCom):
        # the prefix is optional and used to make it easier to recognize
        # which reference strings in the Airflow metadata database
        # refer to an XCom that has been stored in a GCS bucket
        PREFIX = "xcom_gcs://"
        BUCKET_NAME = "gcs-xcom-backend-example"

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
            
            # the connection to GCS is created by using the GCShook with 
            # the conn id configured in Step 3
            hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename = "data_" + str(uuid.uuid4()) + ".json"
            # define the full GCS key where the file should be stored
            gs_key = f"{run_id}/{task_id}/{filename}"

            # write the value to a local temporary JSON file
            with open(filename, 'a+') as f:
                json.dump(value, f)

            # load the local JSON file into the GCS bucket
            hook.upload(
                filename=filename,
                object_name=gs_key,
                bucket_name=GCSXComBackendJSON.BUCKET_NAME,
            )

            os.remove(filename)

            # define the string that will be saved to the Airflow metadata 
            # database to refer to this XCom
            reference_string = GCSXComBackendJSON.PREFIX + gs_key

            # use JSON serialization to write the reference string to the
            # Airflow metadata database (like a regular XCom)
            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            # retrieve the relevant reference string from the metadata database
            reference_string = BaseXCom.deserialize_value(result=result)
            
            # create the GCS connection using the GCSHook and recreate the key
            hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
            gs_key = reference_string.replace(GCSXComBackendJSON.PREFIX, "")

            # download the JSON file found at the location described by the 
            # reference string to a temporary local folder
            filename = hook.download(
                object_name=gs_key,
                bucket_name=GCSXComBackendJSON.BUCKET_NAME,
                filename="my_xcom.json"
            )

            # load the content of the local JSON file and return it to be used by
            # the operator
            with open(filename, 'r') as f:
                output = json.load(f)

            os.remove(filename)

            return output
    ```

    The code above defines a class called `GCSXComBackendJSON`. The class has two methods: `.serialize_value()` defines how the `value` that is pushed to XComs from an Airflow task is handled, while `.deserialize_value()` contains the logic to retrieve information from the XComs backend.

    The `.serialize_value()` method accomplishes the following:

    - Instantiates an [`GCSHook`](https://registry.astronomer.io/providers/google/modules/gcshook) using the `gcs_xcom_backend_conn` connection that was defined in [Step 3](#step-3-create-a-connection).
    - Creates a unique `filename` using the [`uuid` package](https://docs.python.org/3/library/uuid.html).
    - Uses the `run_id` and `task_id` from the Airflow context to define the `gs_key` under which the file will be saved in the GCS bucket.
    - Writes the `value` that is being pushed to XComs to a JSON file.
    - Uploads the JSON file to the bucket.
    - Creates a `reference_string` using the `gs_key` that is written to the Airflow metadata database as a regular XCom.

    The `.deserialize_value()` method:

    - Retrieves the `reference_string` for a given entry (`result`) from the Airflow metadata database using regular XComs.
    - Downloads the JSON file at the `gs_key` contained in the `reference_string`.
    - Retrieves the information from the JSON file.

3. Open the `.env` file of your Astro Project and add the following line to set your XCom backend to the custom class:

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.gcs_xcom_backend_json.GCSXComBackendJSON
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>
<TabItem value="azure">

For Airflow to be able to use your custom XCom backend it is necessary to define an XCom backend class which inherits from the `BaseXCom` class.

1. In your Astro project create a new file in the `include` directory called `azure_xcom_backend_json.py`.

2. Copy paste the following code into the file:

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
    import json
    import uuid
    import os

    class WasbXComBackendJSON(BaseXCom):
        # the prefix is optional and used to make it easier to recognize
        # which reference strings in the Airflow metadata database
        # refer to an XCom that has been stored in a blob
        PREFIX = "xcom_wasb://"
        CONTAINER_NAME = "custom-xcom-backend"

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
            
            # the connection to Wasb is created by using the WasbHook with 
            # the conn id configured in Step 3
            hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename = "data_" + str(uuid.uuid4()) + ".json"
            # define the full blob key where the file should be stored
            blob_key = f"{run_id}/{task_id}/{filename}"

            # write the value to a local temporary JSON file
            with open(filename, 'a+') as f:
                json.dump(value, f)

            # load the local JSON file into the blob
            hook.load_file(
                file_path=filename,
                container_name=WasbXComBackendJSON.CONTAINER_NAME,
                blob_name=blob_key
            )

            os.remove(filename)

            # define the string that will be saved to the Airflow metadata 
            # database to refer to this XCom
            reference_string = WasbXComBackendJSON.PREFIX + blob_key

            # use JSON serialization to write the reference string to the
            # Airflow metadata database (like a regular XCom)
            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            # retrieve the relevant reference string from the metadata database
            reference_string = BaseXCom.deserialize_value(result=result)
            
            # create the Wasb connection using the WasbHook and recreate the key
            hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
            blob_key = reference_string.replace(WasbXComBackendJSON.PREFIX, "")

            # download the JSON file found at the location described by the 
            # reference string to my_xcom.json
            hook.get_file(
                blob_name=blob_key,
                container_name=WasbXComBackendJSON.CONTAINER_NAME,
                file_path="my_xcom.json",
                offset=0,
                length=100000
            )

            # load the contents of my_xcom.json to return 
            with open("my_xcom.json", 'r') as f:
                output = json.load(f)

            os.remove("my_xcom.json")

            return output
    ```

    The code above defines a class called `WasbXComBackendJSON`. The class has two methods: `.serialize_value()` defines how the `value` that is pushed to XComs from an Airflow task is handled, while `.deserialize_value()` contains the logic to retrieve information from the XComs backend.

    The `.serialize_value()` method accomplishes the following:

    - Instantiates an [`WasbHook`](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbhook) using the `azure_xcom_backend_conn` connection that was defined in [Step 3](#step-3-create-a-connection).
    - Creates a unique `filename` using the [`uuid` package](https://docs.python.org/3/library/uuid.html).
    - Uses the `run_id` and `task_id` from the Airflow context to define the `blob_key` under which the file will be saved in the blob.
    - Writes the `value` that is being pushed to XComs to a JSON file.
    - Uploads the JSON file to the blob.
    - Creates a `reference_string` using the `blob_key` that is written to the Airflow metadata database as a regular XCom.

    The `.deserialize_value()` method:

    - Retrieves the `reference_string` for a given entry (`result`) from the Airflow metadata database using regular XComs.
    - Downloads the JSON file at the `blob_key` contained in the `reference_string`.
    - Retrieves the information from the JSON file.

3. Open the `.env` file of your Astro Project and add the following line to set your XCom backend to the custom class:

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.azure_xcom_backend_json.WasbXComBackendJSON
    ```

4. Restart your Airflow instance using `astro dev restart`.


</TabItem>
<TabItem value="local">

For Airflow to be able to use your custom XCom backend it is necessary to define an XCom backend class which inherits from the `BaseXCom` class.

1. In your Astro project create a new file in the `include` directory called `minio_xcom_backend_json.py`.

2. Copy paste the following code into the file:

    ```python
    from airflow.models.xcom import BaseXCom
    import json
    import uuid
    from minio import Minio
    import os
    import io

    class MinIOXComBackendJSON(BaseXCom):
        # the prefix is optional and used to make it easier to recognize
        # which reference strings in the Airflow metadata database
        # refer to an XCom that has been stored in a MinIO bucket
        PREFIX = "xcom_minio://"
        BUCKET_NAME = "custom-xcom-backend"

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
            
            # create the MinIO client with the credentials stored as env variables
            client = Minio(
                os.environ["MINIO_IP"],
                os.environ["MINIO_ACCESS_KEY"],
                os.environ["MINIO_SECRET_KEY"],
                secure=False
            )

            # make sure the file_id is unique, either by using combinations of
            # the task_id, run_id and map_index parameters or by using a uuid
            filename = "data_" + str(uuid.uuid4()) + ".json"
            # define the full key where the file should be stored
            minio_key = f"{run_id}/{task_id}/{filename}"

            # write the value to MinIO
            client.put_object(
                MinIOXComBackendJSON.BUCKET_NAME,
                minio_key,
                io.BytesIO(bytes(json.dumps(value), 'utf-8')),
                -1, # -1 = unknown file size
                part_size=10*1024*1024,
            )

            # define the string that will be saved to the Airflow metadata 
            # database to refer to this XCom
            reference_string = MinIOXComBackendJSON.PREFIX + minio_key

            # use JSON serialization to write the reference string to the
            # Airflow metadata database (like a regular XCom)
            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            # retrieve the relevant reference string from the metadata database
            reference_string = BaseXCom.deserialize_value(result=result)

            # retrieve the key from the reference string 
            minio_key = reference_string.replace(MinIOXComBackendJSON.PREFIX, "")

            # create the MinIO client with the credentials stored as env variables
            client = Minio(
                os.environ["MINIO_IP"],
                os.environ["MINIO_ACCESS_KEY"],
                os.environ["MINIO_SECRET_KEY"],
                secure=False
            )

            # get the object from the MinIO bucket
            response = client.get_object(
                MinIOXComBackendJSON.BUCKET_NAME,
                minio_key
            )

            # return the contents of the retrieved object
            return json.loads(response.read())
    ```

    The code above defines a class called `MinIOXComBackendJSON`. The class has two methods: `.serialize_value()` defines how the `value` that is pushed to XComs from an Airflow task is handled, while `.deserialize_value()` contains the logic to retrieve information from the XComs backend.

    The `.serialize_value()` method accomplishes the following:

    - Creates a MinIO client using the credentials you saved in the `.env` file in [Step 3](#step-3-create-a-connection).
    - Creates a unique `filename` using the [`uuid` package](https://docs.python.org/3/library/uuid.html).
    - Uses the `run_id` and `task_id` from the Airflow context to define the `minio_key` under which the file will be saved in the bucket.
    - Writes the `value` that is being pushed to XComs to a JSON file.
    - Uploads the JSON file to the bucket.
    - Creates a `reference_string` using the `minio_key` that is written to the Airflow metadata database as a regular XCom.

    The `.deserialize_value()` method:

    - Retrieves the `reference_string` for a given entry (`result`) from the Airflow metadata database using regular XComs.
    - Downloads the JSON file at the `minio_key` contained in the `reference_string`.
    - Reads the information from the JSON file.

3. Open the `.env` file of your Astro Project and add the following line to set your XCom backend to the custom class:

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.minio_xcom_backend_json.MinIOXComBackendJSON
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>

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

4. View the logs of both tasks, they include information about the custom XComs backend. The `print_a_number` task includes the full path to the file stored in the custom backend.

    ![Logs mentioning custom XCom backend](/img/guides/xcom_backend_task_logs_simple.png)

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

5. View the XCom in your S3 bucket.

    ![XComs in the S3 bucket](/img/guides/xcom_backend_S3_json.png)

</TabItem>

<TabItem value="gcp">

5. View the XCom in your GCS bucket.

    ![XComs in the GCS bucket](/img/guides/xcom_backend_gcs_json.png)

</TabItem>
<TabItem value="azure">

5. View the XCom in your blob.

    ![XComs in the blob](/img/guides/xcom_backend_azure_blob.png)

</TabItem>
<TabItem value="local">

5. View the XCom in your bucket.

    ![XComs in the MinIO bucket](/img/guides/xcom_backend_minio_file.png)

</TabItem>

</Tabs>

## Step 6: Create a custom serialization method to handle Pandas dataframes

<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
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
    import os

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
                filename = "data_" + str(uuid.uuid4()) + ".csv"
                s3_key = f"{run_id}/{task_id}/{filename}"

                value.to_csv(filename)

            # if the value passed is not a Pandas dataframe, attempt to use
            # JSON serialization
            else:
                filename = "data_" + str(uuid.uuid4()) + ".json"
                s3_key = f"{run_id}/{task_id}/{filename}"

                with open(filename, 'a+') as f:
                    json.dump(value, f)

            hook.load_file(
                filename=filename,
                key=s3_key,
                bucket_name=S3XComBackendPandas.BUCKET_NAME,
                replace=True
            )

            os.remove(filename)

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

            os.remove(filename)

            return output
    ```

    The code above creates a second custom XCom backend called `S3XComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to the S3 bucket and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

3. In the `.env` file of your Astro project, change the XCom backend variable to use the newly created `S3XComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.s3_xcom_backend_pandas.S3XComBackendPandas
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>

<TabItem value="gcp">

A powerful feature of custom XCom backends is the possibility to adjust serialization and deserialization methods to be able to handle object that cannot be JSON-serialized. In this step you will create a custom XCom backend that can save the contents of a [Pandas](https://pandas.pydata.org/) dataframe as a CSV file.

1. Create a second file in your `include` folder called `gcs_xcom_backend_pandas.py`.

2. Copy and paste the following code into the file.

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.google.cloud.hooks.gcs import GCSHook
    import pandas as pd
    import json
    import uuid
    import os

    class GCSXComBackendPandas(BaseXCom):
        PREFIX = "xcom_gcs://"
        BUCKET_NAME = "gcs-xcom-backend-example"

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

            hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
            
            # added serialization method if the value passed is a Pandas dataframe
            # the contents are written to a local temporary csv file
            if isinstance(value, pd.DataFrame):
                filename    = "data_" + str(uuid.uuid4()) + ".csv"
                gs_key      = f"{run_id}/{task_id}/{filename}"

                value.to_csv(filename)

            # if the value passed is not a Pandas dataframe, attempt to use
            # JSON serialization
            else:
                filename    = "data_" + str(uuid.uuid4()) + ".json"
                gs_key      = f"{run_id}/{task_id}/{filename}"

                with open(filename, 'a+') as f:
                    json.dump(value, f)

            hook.upload(
                filename=filename,
                object_name=gs_key,
                bucket_name=GCSXComBackendPandas.BUCKET_NAME,
            )

            os.remove(filename)

            reference_string = GCSXComBackendPandas.PREFIX + gs_key

            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            result = BaseXCom.deserialize_value(result)

            hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
            gs_key = result.replace(GCSXComBackendPandas.PREFIX, "")

            filename = hook.download(
                object_name=gs_key,
                bucket_name=GCSXComBackendPandas.BUCKET_NAME,
                filename="my_xcom"
            )

            # added deserialization option to convert a CSV back to a dataframe
            if gs_key.split(".")[-1] == "csv":
                output = pd.read_csv(filename)
            # if the key does not end in 'csv' use JSON deserialization
            else:
                with open(filename, 'r') as f:
                    output = json.load(f)

            os.remove(filename)

            return output
    ```

    The code above creates a second custom XCom backend called `GCSXComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to the GCS bucket and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

3. In the `.env` file of your Astro project, change the XCom backend variable to use the newly created `GCSXComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.gcs_xcom_backend_pandas.GCSXComBackendPandas
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>
<TabItem value="azure">

A powerful feature of custom XCom backends is the possibility to adjust serialization and deserialization methods to be able to handle object that cannot be JSON-serialized. In this step you will create a custom XCom backend that can save the contents of a [Pandas](https://pandas.pydata.org/) dataframe as a CSV file.

1. Create a second file in your `include` folder called `azure_xcom_backend_pandas.py`.

2. Copy and paste the following code into the file.

    ```python
    from airflow.models.xcom import BaseXCom
    from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
    import pandas as pd
    import json
    import uuid
    import os

    class WasbXComBackendPandas(BaseXCom):
        PREFIX = "xcom_wasb://"
        CONTAINER_NAME = "custom-xcom-backend"

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

            hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
            
            # added serialization method if the value passed is a Pandas dataframe
            # the contents are written to a local temporary csv file
            if isinstance(value, pd.DataFrame):
                filename = "data_" + str(uuid.uuid4()) + ".csv"
                blob_key = f"{run_id}/{task_id}/{filename}"

                value.to_csv(filename)

            # if the value passed is not a Pandas dataframe, attempt to use
            # JSON serialization
            else:
                filename = "data_" + str(uuid.uuid4()) + ".json"
                blob_key = f"{run_id}/{task_id}/{filename}"

                with open(filename, 'a+') as f:
                    json.dump(value, f)

            hook.load_file(
                file_path=filename,
                container_name=WasbXComBackendPandas.CONTAINER_NAME,
                blob_name=blob_key
            )

            os.remove(filename)

            reference_string = WasbXComBackendPandas.PREFIX + blob_key

            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            result = BaseXCom.deserialize_value(result)

            hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
            blob_key = result.replace(WasbXComBackendPandas.PREFIX, "")

            hook.get_file(
                blob_name=blob_key,
                container_name=WasbXComBackendPandas.CONTAINER_NAME,
                file_path="my_xcom_file",
                offset=0,
                length=100000
            )

            # added deserialization option to convert a CSV back to a dataframe
            if blob_key.split(".")[-1] == "csv":
                output = pd.read_csv("my_xcom_file")
            # if the key does not end in 'csv' use JSON deserialization
            else:
                with open("my_xcom_file", 'r') as f:
                    output = json.load(f)

            os.remove("my_xcom_file")

            return output
    ```

    The code above creates a second custom XCom backend called `WasbXComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to the GCS bucket and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

3. In the `.env` file of your Astro project, change the XCom backend variable to use the newly created `WasbXComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.azure_xcom_backend_pandas.WasbXComBackendPandas
    ```

4. Restart your Airflow instance using `astro dev restart`.


</TabItem>
<TabItem value="local">

A powerful feature of custom XCom backends is the possibility to adjust serialization and deserialization methods to be able to handle object that cannot be JSON-serialized. In this step you will create a custom XCom backend that can save the contents of a [Pandas](https://pandas.pydata.org/) dataframe as a CSV file.

1. Create a second file in your `include` folder called `minion_xcom_backend_pandas.py`.

2. Copy and paste the following code into the file.

    ```python
    from airflow.models.xcom import BaseXCom
    import pandas as pd
    import json
    import uuid
    from minio import Minio
    import os
    import io

    class MinIOXComBackendPandas(BaseXCom):
        # the prefix is optional and used to make it easier to recognize
        # which reference strings in the Airflow metadata database
        # refer to an XCom that has been stored in a MinIO bucket
        PREFIX = "xcom_minio://"
        BUCKET_NAME = "custom-xcom-backend"

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
            
            # create the MinIO client with the credentials stored as env variables
            client = Minio(
                os.environ["MINIO_IP"],
                os.environ["MINIO_ACCESS_KEY"],
                os.environ["MINIO_SECRET_KEY"],
                secure=False
            )

            # added serialization method if the value passed is a Pandas dataframe
            # the contents are written to a local temporary csv file
            if isinstance(value, pd.DataFrame):
                filename = "data_" + str(uuid.uuid4()) + ".csv"
                minio_key = f"{run_id}/{task_id}/{filename}"

                value.to_csv(filename)

                with open(filename, 'r') as f:
                    string_file = f.read()
                    bytes_to_write = io.BytesIO(bytes(string_file, 'utf-8'))

                os.remove(filename)
            # if the value passed is not a Pandas dataframe, attempt to use
            # JSON serialization
            else:
                filename = "data_" + str(uuid.uuid4()) + ".json"
                minio_key = f"{run_id}/{task_id}/{filename}"

                bytes_to_write = io.BytesIO(bytes(json.dumps(value), 'utf-8'))

            client.put_object(
                MinIOXComBackendPandas.BUCKET_NAME,
                minio_key,
                bytes_to_write,
                -1, # -1 = unknown filesize
                part_size=10*1024*1024,
            )

            reference_string = MinIOXComBackendPandas.PREFIX + minio_key

            return BaseXCom.serialize_value(value=reference_string)

        @staticmethod
        def deserialize_value(result):
            reference_string = BaseXCom.deserialize_value(result=result)
            key = reference_string.replace(MinIOXComBackendPandas.PREFIX, "")

            client = Minio(
                os.environ["MINIO_IP"],
                os.environ["MINIO_ACCESS_KEY"],
                os.environ["MINIO_SECRET_KEY"],
                secure=False
            )

            response = client.get_object(
                MinIOXComBackendPandas.BUCKET_NAME,
                key
            )

            # added deserialization option to convert a CSV back to a dataframe
            if key.split(".")[-1] == "csv":

                with open("csv_xcom.csv", "w") as f:
                    f.write(response.read().decode("utf-8"))
                output = pd.read_csv("csv_xcom.csv")
                os.remove("csv_xcom.csv")

            # if the key does not end in 'csv' use JSON deserialization
            else:
                output = json.loads(response.read())

            return output
    ```

    The code above creates a second custom XCom backend called `MinIOXComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to the S3 bucket and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

3. In the `.env` file of your Astro project, change the XCom backend variable to use the newly created `MinIOXComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.minio_xcom_backend_pandas.MinIOXComBackendPandas
    ```

4. Restart your Airflow instance using `astro dev restart`.

</TabItem>

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

    The `extract_data` task will push a dictionary to XCom, which will be saved to your blob storage as a JSON file and retrieved by the `calculate_xp_per_height` task. This second task pushes a Pandas dataframe to XComs which is only possible when using a custom XCom backend with a serialization option for this type of object. The last task `print_xp_per_height` retrieves the csv and recreates the Pandas dataframe before printing out the Pokemon and their base experience to height ratio.

3. View the information about your favorite pokemon in the task log of the `print_xp_per_height` task.

    ![Pokemon Information in logs](/img/guides/xcom_backend_task_logs_pokemon.png)

## Best practices

Common reasons to use a custom XComs backend are:

- Needing more storage space for XComs than the metadata database can offer.
- Running a production environment that where custom retention, deletion and backup policies for XComs are desired. With a custom XComs backend you do not need to worry about periodically cleaning up the metadata database.
- The need for custom serialization and deserialization methods. By default Airflow uses JSON serialization which puts limits on the type of data that you can pass via XComs (pickling is available by setting `AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True` but has [known security implications](https://docs.python.org/3/library/pickle.html)).
- Having a custom setup where access to XComs is needed without accessing the metadata database. 

## Overriding additional BaseXCom methods

In this tutorial we've show how to add custom logic to the `.serialize_value()` and  `.deserialize_value()` methods. If you want to further expand the functionality for your custom XComs backend you can override additional methods of the [XCom module](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/xcom/index.html) ([source code](https://github.com/apache/airflow/blob/main/airflow/models/xcom.py)). 

A common use case is to want to remove stored XComs upon clearing and rerunning a task in both the Airflow metadata database and the custom XCom backend. To do so the `.clear()` method needs to be overridden to include the removal of the referenced XCom in the custom XCom backend. The code below shows an example of a `.clear()` method that includes the deletion of an XCom stored in a custom S3 backend with the serialization method from the tutorial.

```python
from airflow.utils.helpers import exactly_one
from airflow.utils.session import NEW_SESSION, provide_session
import warnings
from airflow.exceptions import RemovedInAirflow3Warning

@classmethod
@provide_session
def clear(
    cls,
    execution_date = None,
    dag_id = None,
    task_id =  None,
    session = NEW_SESSION,
    *,
    run_id = None,
    map_index = None,
) -> None:

    from airflow.models import DagRun

    if dag_id is None:
        raise TypeError("clear() missing required argument: dag_id")
    if task_id is None:
        raise TypeError("clear() missing required argument: task_id")

    if not exactly_one(execution_date is not None, run_id is not None):
        raise ValueError(
            f"Exactly one of run_id or execution_date must be passed. "
            f"Passed execution_date={execution_date}, run_id={run_id}"
        )

    if execution_date is not None:
        message = "Passing 'execution_date' to 'XCom.clear()' is deprecated. Use 'run_id' instead."
        warnings.warn(message, RemovedInAirflow3Warning, stacklevel=3)
        run_id = (
            session.query(DagRun.run_id)
            .filter(DagRun.dag_id == dag_id, DagRun.execution_date == execution_date)
            .scalar()
        )

    # get the reference string from the Airflow metadata database
    reference_string = session.query(cls.value).filter_by(dag_id=dag_id, task_id=task_id, run_id=run_id).scalar()

    if reference_string is not None:

        # decode the XComs binary to UTF-8
        reference_string = reference_string.decode('utf-8')
        
        hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
        key = reference_string.replace(S3XComBackendJSON.PREFIX, '')

        # use the reference string to delete the object from the S3 bucket
        hook.delete_objects(
            bucket=S3XComBackendJSON.BUCKET_NAME,
            keys=json.loads(key)
        )

    # retrieve the XCom record from the metadata database containing the reference string
    query = session.query(cls).filter_by(dag_id=dag_id, task_id=task_id, run_id=run_id)
    if map_index is not None:
        query = query.filter_by(map_index=map_index)

    # delete the XComs containing the reference string from metadata database
    query.delete()
```

## Conclusion

Congratulations! You learned how to set up a custom XCom backend and how to define your own serialization and deserialization methods. 