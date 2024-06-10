---
title: 'Set up a custom XCom backend using object storage'
sidebar_label: 'Set up an XCom backend'
id: xcom-backend-tutorial
description: 'Use this tutorial to learn how to set up a custom XCom backend with object storage.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import custom_xcom_backend_test from '!!raw-loader!../code-samples/dags/xcom-backend-tutorial/custom_xcom_backend_test.py';

By default, Airflow uses the [metadata database](airflow-database.md) to store XComs, which works well for local development but has limited performance. For production environments that use XCom to pass data between tasks, Astronomer recommends using a custom XCom backend. [Custom XCom backends](custom-xcom-backend-strategies.md) allow you to configure where Airflow stores information that is passed between tasks using [XComs](airflow-passing-data-between-tasks.md#xcom). 

The Object Storage XCom Backend available in the [Common IO provider](https://airflow.apache.org/docs/apache-airflow-providers-common-io/stable/index.html) is the easiest way to store XComs in a remote object storage solution.

This tutorial will show you how to set up a custom XCom backend using object storage for [AWS S3](https://aws.amazon.com/s3/), [GCP Cloud Storage](https://cloud.google.com/storage) or [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/).

To learn more about other options for setting custom XCom backends, see [Strategies for custom XCom backends in Airflow](custom-xcom-backend-strategies.md).

:::warning

While a custom XCom backend allows you to store virtually unlimited amounts of data as XComs, you will also need to scale other Airflow components to pass large amounts of data between tasks. For help running Airflow at scale, [reach out to Astronomer](https://www.astronomer.io/try-astro/?referral=docs-content-link&utm_medium=docs&utm_content=learn-xcom-backend-tutorial&utm_source=body).

:::

:::warning

Object storage is currently considered experimental and might be subject to breaking changes in future releases. For more information see [AIP-58](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=263430565). 

:::

## Time to complete

This tutorial takes approximately 45 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- XCom basics. See [Passing data between Airflow tasks](airflow-passing-data-between-tasks.md).
- Airflow connections. See [Manage connections in Apache Airflow](connections.md).

## Prerequisites

<<<<<<< xcom_backend_update
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) with an Astro project running Astro Runtime 11.5.0 or higher (Airflow 2.9.2 or higher). To set up a custom XCom backend with older versions of Airflow, see [Custom XCom backends](custom-xcom-backend-strategies.md).
- An account in either [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/), or [Azure](https://azure.microsoft.com/) with permissions to create and configure an object storage container.
=======
- The [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli).
- A local or cloud-based object storage account. This tutorial has instructions for AWS, GCP, Azure, and MinIO.

## Step 1: Create an Astro project

1. Set up Airflow by creating a new Astro project:

    ```sh
    $ mkdir airflow-custom-xcom-example && cd airflow-custom-xcom-example
    $ astro dev init
    ```

2. Ensure that the provider of your cloud-based object storage account is installed in your Airflow instance. If you are using the Astro CLI, the [Amazon](https://registry.astronomer.io/providers/amazon), [Google](https://registry.astronomer.io/providers/google), and [Azure](https://registry.astronomer.io/providers/microsoft-azure) provider packages come pre-installed in your Astro runtime image. If you are working with a local MinIO instance, add the [`minio` Python package](https://min.io/docs/minio/linux/developers/python/minio-py.html) to your `requirements.txt` file.
>>>>>>> main

## Step 1: Set up your object storage container

First, you need to set up the object storage container in your cloud provider where Airflow will store the XComs.

<Tabs
    defaultValue="aws"
    groupId= "step-1-set-up-your-object-storage-container"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'}
    ]}>
<TabItem value="aws">

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html). Ensure that public access to the bucket is blocked. You do not need to enable bucket versioning.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below or use the AWS GUI to replicate what you see in the screenshot. Replace `<your-bucket-name>` with the name of your S3 bucket.

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
                    "arn:aws:s3:::<your-bucket-name>/*",
                    "arn:aws:s3:::<your-bucket-name>"
                ]
            }
        ]
    }
    ```

3. Save your policy under the name `AirflowXComBackendAWSS3`. 

4. [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) called `airflow-xcom` with the AWS credential type `Access key - Programmatic access` and [attach](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) the `AirflowXComBackendAWSS3` policy to this user. 

5. [Create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) of the type `Third-party-service` for your `airflow-xcom` user. Make sure to save the Access Key ID and the Secret Access Key in a secure location to use in [Step 3](#step-3-set-up-your-airflow-connection).

:::info

For other ways to set up a connection between Airflow and AWS, see the [Amazon provider](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) documentation.

:::

</TabItem>

<TabItem value="gcp">

1. Log into your Google Cloud account and [create a new project](https://cloud.google.com/resource-manager/docs/creating-managing-projects). 

2. [Create a new bucket](https://cloud.google.com/storage/docs/creating-buckets) in your project with Uniform Access Control. Enforce public access prevention.

3. [Create a custom IAM role](https://cloud.google.com/iam/docs/creating-custom-roles) called `AirflowXComBackendGCS` for Airflow to access your bucket. Assign 6 permissions:

    - storage.buckets.list
    - storage.objects.create
    - storage.objects.delete
    - storage.objects.get
    - storage.objects.list
    - storage.objects.update

4. [Create a new service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) called `airflow-xcom` and grant it access to your project by granting it the `AirflowXComBackendGCS` role.

5. [Create a new key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your `airflow-xcom` service account and make sure to download the credentials in JSON format.

:::info

For other ways to set up a connection between Airflow and Google Cloud, see the [Google provider](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html) documentation.

:::

</TabItem>
<TabItem value="azure">

1. Log into your Azure account and [create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create). Ensure that public access to the bucket is blocked.

2. In the storage account, [create a new container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal). 

3. [Create a shared access token](https://learn.microsoft.com/en-us/azure/cognitive-services/Translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers) for your container. 

    In the **Permissions** dropdown menu, enable the following permissions:

    - Read
    - Add
    - Create
    - Write
    - Delete
    - List
    
    Set the duration the token will be valid and set **Allowed Protocols** to `HTTPS only`. Provide the IP address of your Airflow instance. If you are running Airflow locally with the Astro CLI, use the IP address of your computer.

4. Go to your Storage account and navigate to [**Access keys**](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage). Copy the **Key** and **Connection string** values and save them in a secure location to use in [step 3](#step-3-set-up-your-airflow-connection).


:::info

For other ways to set up a connection between Airflow and Azure Blob Storage, see the [Microsoft Azure provider](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/wasb.html) documentation.

:::

</TabItem>
</Tabs>

## Step 2: Install the required provider packages

To use the Object Storage XCom Backend, you need to install the Common IO provider package and the provider package for your object storage container provider.

<Tabs
    defaultValue="aws"
    groupId="step-2-install-the-required-provider-packages"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'}
    ]}>
<TabItem value="aws">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Amazon](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest) provider packages to your `requirements.txt` file. Note that you need to install the `s3fs` extra to use the Amazon provider package with the [object storage](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html) feature.

    ```text
    apache-airflow-providers-common-io==1.3.2
    apache-airflow-providers-amazon[s3fs]==8.19.0
    ```

</TabItem>

<TabItem value="gcp">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Google](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest) provider packages to your `requirements.txt` file.

    ```text
    apache-airflow-providers-common-io==1.3.2
    apache-airflow-providers-google==10.17.0
    ```

</TabItem>

<TabItem value="azure">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Microsoft Azure](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest) provider packages to your `requirements.txt` file.

    ```text
    apache-airflow-providers-common-io==1.3.2
    apache-airflow-providers-microsoft-azure==9.0.0
    ```

</TabItem>

</Tabs>

## Step 3: Set up your Airflow connection

An Airflow connection is necessary to connect Airflow with your object storage container provider. In this tutorial, you'll use the Airflow UI to configure your connection.

1. Start your Astro project by running:

    ```bash
    astro dev start
    ```

<Tabs
    defaultValue="aws"
    groupId="3-set-up-your-airflow-connection"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'}
    ]}>
<TabItem value="aws">

<<<<<<< xcom_backend_update
2. In the Airflow UI navigate to `Admin` -> `Connections` and click on `Create`. Fill in the following fields:
=======
```python
from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json
import uuid
import os

class CustomXComBackendJSON(BaseXCom):
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
            bucket_name=CustomXComBackendJSON.BUCKET_NAME,
            replace=True
        )

        # remove the local temporary JSON file
        os.remove(filename)

        # define the string that will be saved to the Airflow metadata 
        # database to refer to this XCom
        reference_string = CustomXComBackendJSON.PREFIX + s3_key

        # use JSON serialization to write the reference string to the
        # Airflow metadata database (like a regular XCom)
        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        # retrieve the relevant reference string from the metadata database
        reference_string = BaseXCom.deserialize_value(result=result)
        
        # create the S3 connection using the S3Hook and recreate the S3 key
        hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
        key = reference_string.replace(CustomXComBackendJSON.PREFIX, "")

        # download the JSON file found at the location described by the 
        # reference string to a temporary local folder
        filename = hook.download_file(
            key=key,
            bucket_name=CustomXComBackendJSON.BUCKET_NAME,
            local_path="/tmp"
        )

        # load the content of the local JSON file and return it to be used by
        # the operator
        with open(filename, 'r') as f:
            output = json.load(f)

        # remove the local temporary JSON file
        os.remove(filename)

        return output
```
</TabItem>
<TabItem value="gcp">

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import json
import uuid
import os

class CustomXComBackendJSON(BaseXCom):
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
            bucket_name=CustomXComBackendJSON.BUCKET_NAME,
        )

        # remove the local temporary JSON file
        os.remove(filename)

        # define the string that will be saved to the Airflow metadata 
        # database to refer to this XCom
        reference_string = CustomXComBackendJSON.PREFIX + gs_key

        # use JSON serialization to write the reference string to the
        # Airflow metadata database (like a regular XCom)
        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        # retrieve the relevant reference string from the metadata database
        reference_string = BaseXCom.deserialize_value(result=result)
        
        # create the GCS connection using the GCSHook and recreate the key
        hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
        gs_key = reference_string.replace(CustomXComBackendJSON.PREFIX, "")

        # download the JSON file found at the location described by the 
        # reference string to a temporary local folder
        filename = hook.download(
            object_name=gs_key,
            bucket_name=CustomXComBackendJSON.BUCKET_NAME,
            filename="my_xcom.json"
        )

        # load the content of the local JSON file and return it to be used by
        # the operator
        with open(filename, 'r') as f:
            output = json.load(f)

        # remove the local temporary JSON file
        os.remove(filename)

        return output
```
</TabItem>
<TabItem value="azure">

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
import json
import uuid
import os

class CustomXComBackendJSON(BaseXCom):
    # the prefix is optional and used to make it easier to recognize
    # which reference strings in the Airflow metadata database
    # refer to an XCom that has been stored in Azure Blob Storage
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

        # load the local JSON file into Azure Blob Storage
        hook.load_file(
            file_path=filename,
            container_name=CustomXComBackendJSON.CONTAINER_NAME,
            blob_name=blob_key
        )

        # remove the local temporary JSON file
        os.remove(filename)

        # define the string that will be saved to the Airflow metadata 
        # database to refer to this XCom
        reference_string = CustomXComBackendJSON.PREFIX + blob_key

        # use JSON serialization to write the reference string to the
        # Airflow metadata database (like a regular XCom)
        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        # retrieve the relevant reference string from the metadata database
        reference_string = BaseXCom.deserialize_value(result=result)
        
        # create the Wasb connection using the WasbHook and recreate the key
        hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
        blob_key = reference_string.replace(CustomXComBackendJSON.PREFIX, "")

        # download the JSON file found at the location described by the 
        # reference string to my_xcom.json
        hook.get_file(
            blob_name=blob_key,
            container_name=CustomXComBackendJSON.CONTAINER_NAME,
            file_path="my_xcom.json",
            offset=0,
            length=100000
        )

        # load the contents of my_xcom.json to return 
        with open("my_xcom.json", 'r') as f:
            output = json.load(f)

        # remove the local temporary JSON file
        os.remove("my_xcom.json")

        return output
```
</TabItem>
<TabItem value="local">

```python
from airflow.models.xcom import BaseXCom
import json
import uuid
from minio import Minio
import os
import io

class CustomXComBackendJSON(BaseXCom):
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
            CustomXComBackendJSON.BUCKET_NAME,
            minio_key,
            io.BytesIO(bytes(json.dumps(value), 'utf-8')),
            -1, # -1 = unknown file size
            part_size=10*1024*1024,
        )

        # define the string that will be saved to the Airflow metadata 
        # database to refer to this XCom
        reference_string = CustomXComBackendJSON.PREFIX + minio_key

        # use JSON serialization to write the reference string to the
        # Airflow metadata database (like a regular XCom)
        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        # retrieve the relevant reference string from the metadata database
        reference_string = BaseXCom.deserialize_value(result=result)

        # retrieve the key from the reference string 
        minio_key = reference_string.replace(CustomXComBackendJSON.PREFIX, "")

        # create the MinIO client with the credentials stored as env variables
        client = Minio(
            os.environ["MINIO_IP"],
            os.environ["MINIO_ACCESS_KEY"],
            os.environ["MINIO_SECRET_KEY"],
            secure=False
        )

        # get the object from the MinIO bucket
        response = client.get_object(
            CustomXComBackendJSON.BUCKET_NAME,
            minio_key
        )

        # return the contents of the retrieved object
        return json.loads(response.read())
```
</TabItem>
</Tabs>

3. Review the copied code. It defines a class called `CustomXComBackendJSON`. The class has two methods: `.serialize_value()` defines how to handle the `value` that is pushed to XCom from an Airflow task, and `.deserialize_value()` defines the logic to retrieve information from the XCom backend.

    The `.serialize_value()` method:

    - Creates the connection to the external tool, either by using the Hook from the tools' provider package ([S3Hook](https://registry.astronomer.io/providers/amazon/modules/s3hook), [GCSHook](https://registry.astronomer.io/providers/google/modules/gcshook), [WasbHook](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbhook)) or by providing credentials directly (MinIO).
    - Creates a unique `filename` using the [`uuid` package](https://docs.python.org/3/library/uuid.html).
    - Uses the `run_id` and `task_id` from the Airflow context to define the key under which the file will be saved in the object storage.
    - Writes the `value` that is being pushed to XCom to the object storage using JSON serialization.
    - Creates a unique `reference_string` that is written to the Airflow metadata database as a regular XCom.

    The `.deserialize_value()` method:

    - Retrieves the `reference_string` for a given entry (`result`) from the Airflow metadata database using regular XCom.
    - Downloads the JSON file at the key contained in the `reference_string`.
    - Retrieves the information from the JSON file.

4. Open the `.env` file of your Astro Project and add the following line to set your XCom backend to the custom class:

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.xcom_backend_json.CustomXComBackendJSON
    ```

    If you use Astro, set this environment variable in your Deployment instead. See [Environment variables](https://www.astronomer.io/docs/astro/environment-variables).

5. Restart your Airflow instance using `astro dev restart`. 

>>>>>>> main

    - **Conn Id**: `my_aws_conn`
    - **Conn Type**: `Amazon Web Services`
    - **AWS Access Key ID**: `<your access key>`
    - **AWS Secret Access Key**: `<your secret key>`

    To learn more about configuration options for the AWS connection, see the [Amazon provider](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) documentation.

</TabItem>
<TabItem value="gcp">

2. In the Airflow UI navigate to `Admin` -> `Connections` and click on `Create`. Fill in the following fields:

    - **Conn Id**: `my_gcp_conn`
    - **Conn Type**: `Google Cloud`
    - **Project Id**: `<your project id>`
    - **Keyfile JSON**: `<the contents from your keyfile JSON that you downloaded in step 1>`

    To learn more about configuration options for the Google connection, see the [Google provider](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html) documentation.

</TabItem>

<TabItem value="azure">

2. In the Airflow UI navigate to `Admin` -> `Connections` and click on `Create`. Fill in the following fields:

    - **Conn Id**: `my_azure_conn`
    - **Conn Type**: `Microsoft Azure Blob Storage`
    - **Account URL (Active Directory Auth)**: `<the URL of your Azure Storage account>`
    - **Blob Storage Key (optional)**: `<access key to your Azure Storage account>`
    - **Blob Storage Connection String (optional)**: `<connection string to your Azure Storage account>`

    To learn more about configuration options for the Azure connection, see the [Microsoft Azure provider](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/wasb.html) documentation.

</TabItem>
</Tabs>

## Step 4: Configure your custom XCom backend

Configuring a custom XCom backend with object storage can be done by setting environment variables in your Astro project.

:::info

If you are setting up a custom XCom backend for an Astro deployment, you have to set the following environment variables for your deployment. See [Environment variables](https://docs.astronomer.io/astro/environment-variables) for instructions.

:::

1. Add the `AIRFLOW__CORE__XCOM_BACKEND` environment variable to your `.env` file. It defines the class to use for the custom XCom backend implementation.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND="airflow.providers.common.io.xcom.backend.XComObjectStoreBackend"
    ```

<Tabs
    defaultValue="aws"
    groupId="step-4-configure-your-custom-xcom-backend"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'}
    ]}>
<TabItem value="aws">

2. Add the `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH` environment variable to your `.env` file to define the path in your S3 bucket where the XComs will be stored in the form of `<connection id>@<bucket name>/<path>`. Use the connection id of the Airflow connection you defined in [step 2](#step-2-set-up-your-airflow-connection) and replace `<my-bucket>` with your S3 bucket name.

    ```text
    AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH="s3://my_aws_conn@<my-bucket>/xcom"
    ```

</TabItem>

<TabItem value="gcp">

2. Add the `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH` environment variable to your `.env` file to define the path in your GCS bucket where the XComs will be stored in the form of `<connection id>@<bucket name>/<path>`. Use the connection id of the Airflow connection you defined in [step 2](#step-2-set-up-your-airflow-connection) and replace `<my-bucket>` with your GCS bucket name.

    ```text
    AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH="gs://my_gcp_conn@<my-bucket>/xcom"
    ```

</TabItem>

<TabItem value="azure">

2. Add the `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH` environment variable to your `.env` file to define the path in your GCS bucket where the XComs will be stored in the form of `<connection id>@<blob name>/<path>`. Use the connection id of the Airflow connection you defined in [step 2](#step-2-set-up-your-airflow-connection) and replace `<my-blob>` with your GCS bucket name.

    ```text
    AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_PATH="azblob://my_azure_conn@<my-blob>/xcom"
    ```

</TabItem>
</Tabs>

3. Add the `AIRFLOW__COMMON.IO__XCOM_OBJECTSTORAGE_THRESHOLD` environment variable to your `.env` file to determine when Airflow will store XComs in the object storage vs the metadata database. The default value is `-1` which will store all XComs in the metadata database. Set the value to `0` to store all XComs in the object storage. Any positive value means any XCom with a byte size greater than the threshold will be stored in the object storage and any XCom with a size equal to or less than the threshold will be stored in the metadata database. 
For this tutorial we will set the threshold to `1000` bytes, which means any XCom larger than 1KB will be stored in the object storage.

    ```text
    AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_THRESHOLD="1000"
    ```

4. Optional. Define the `AIRFLOW__COMMON_IO__XCOM_OBJECTSTORE_COMPRESSION` environment variable to compress the XComs stored in the object storage with [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) supported compression algorithms like `zip`. The default value is `None`.

    ```text
    AIRFLOW__COMMON_IO__XCOM_OBJECTSTORAGE_COMPRESSION="zip"
    ```

5. Restart your Airflow project by running:

    ```bash
    astro dev restart
    ```

## Step 5: Test your custom XCom backend

We will use a simple DAG to test your custom XCom backend. 

1. Create a new file in the `dags` directory of your Astro project called `custom_xcom_backend_test.py` and add the following code:

    <CodeBlock language="python">{custom_xcom_backend_test}</CodeBlock>

2. Manually trigger the `custom_xcom_backend_test` DAG in the Airflow UI and navigate to the XCom tab of the `push_objects` task. You should see that the `small_obj` XCom shows its value, meaning it was stored in the metadata database, since it is smaller than 1KB. The `big_dict` XCom shows shows the path to the object in the object storage containing the serialized value of the XCom. 

    ![XCom tab of the push_objects task showing two key-value pairs showing the "big_obj" being serialized to the custom XCom backend and the "small_obj": a dictionary containing'a': 23, which was stored in the metadata database.](/img/tutorials/custom-xcom-backends-tutorial_small_big_obj.png)

## Conclusion

Congratulations, you learned how to set up a custom XCom backend using object storage! Learn more about other options to set up custom XCom backends in the [Strategies for custom XCom backends in Airflow](custom-xcom-backend-strategies.md) guide.