---
title: 'Set up a custom XCom backend using cloud-based or local object storage'
sidebar_label: 'Set up a custom XCom backend'
id: xcom-backend-tutorial
description: 'Use this tutorial to learn how to set up a custom XCom backend in AWS, GCP, Azure or MinIO.'
---

import CodeBlock from '@theme/CodeBlock';
import simple_xcom from '!!raw-loader!../code-samples/dags/xcom-backend-tutorial/simple_xcom.py';

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow [XComs](airflow-passing-data-between-tasks.md) allow you to pass data between tasks. By default, Airflow uses the [metadata database](airflow-database.md) to store XComs, which works well for local development but has limited performance. For production environments, you can configure a custom XCom backend.

This allows you to push and pull XComs to and from an external system such as [AWS S3](https://aws.amazon.com/s3/), [GCP Cloud Storage](https://cloud.google.com/storage), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), or a [MinIO](https://min.io/) instance.

Common reasons to use a custom XCom backend include:

- Needing more storage space for XCom than the metadata database can offer.
- Running a production environment where you require custom retention, deletion, and backup policies for XComs. With a custom XCom backend, you don't need to worry about periodically cleaning up the metadata database.
- Utilizing custom serialization and deserialization methods. By default, Airflow uses JSON serialization and, as of Airflow 2.6 can serialize Pandas dataframes via [pyarrow](https://pypi.org/project/pyarrow/). To circumvent this limitation in local development there is the option to serialize data via [pickling](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#enable-xcom-pickling), which is often not suitable for production due to [known security implications](https://docs.python.org/3/library/pickle.html). A custom XCom backend allows you to implement your own serialization and deserialization methods.
- Accessing XCom without accessing the metadata database.

After you complete this tutorial, you'll be able to:

- Create a custom XCom backend using cloud-based or local object storage.
- Use JSON serialization and deserialization in a custom XCom backend.
- Add custom logic to the serialization and deserialization methods to store Pandas dataframes as CSVs in your custom XCom backend.
- Explain best practices of using custom XCom backends.
- Explain the possibility of customizing other BaseXCom methods for extended functionality.

:::caution

While a custom XCom backend allows you to store virtually unlimited amounts of data as XCom, you will also need to scale other Airflow components to pass large amounts of data between tasks. For help running Airflow at scale, [reach out to Astronomer](https://www.astronomer.io/try-astro/?referral=docs-content-link).

:::

## Time to complete

This tutorial takes approximately 1.5 hours to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- XCom basics. See the [Airflow documentation on XCom](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html).
- Passing data between tasks. See [Passing data between Airflow tasks](airflow-passing-data-between-tasks.md).
- The TaskFlow API. See [the TaskFlow API in Airflow 2.0](https://www.astronomer.io/events/webinars/taskflow-api-airflow-2.0/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).
- A local or cloud-based object storage account. This tutorial has instructions for AWS, GCP, Azure, and MinIO.

## Step 1: Create an Astro project

1. Set up Airflow by creating a new Astro project:

    ```sh
    $ mkdir airflow-custom-xcom-example && cd airflow-custom-xcom-example
    $ astro dev init
    ```

2. Ensure that the provider of your cloud-based object storage account is installed in your Airflow instance. If you are using the Astro CLI, the [Amazon](https://registry.astronomer.io/providers/amazon), [Google](https://registry.astronomer.io/providers/google), and [Azure](https://registry.astronomer.io/providers/microsoft-azure) provider packages come pre-installed in your Astro runtime image. If you are working with a local MinIO instance, add the [`minio` Python package](https://min.io/docs/minio/linux/developers/python/minio-py.html) to your `requirements.txt` file.

2. Start your Airflow project by running:

    ```sh
    $ astro dev start
    ```

## Step 2: Set up your object storage account

<Tabs
    defaultValue="aws"
    groupId= "step-2-set-up-your-object-storage-account"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) called `s3-xcom-backend-example`. Ensure that public access to the bucket is blocked.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below or use the AWS GUI to replicate what you see in the screenshot.

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

4. [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) called `airflow-xcom` with the AWS credential type `Access key - Programmatic access`. Attach the `AirflowXComBackendAWSS3` policy to this user as shown in the screenshot below. Make sure to save the Access Key ID and the Secret Access Key.

    ![AWS IAM user for the XCom backend](/img/guides/xcom_backend_aws_user.png)

</TabItem>

<TabItem value="gcp">

1. Log into your Google Cloud account and [create a new project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) called `custom-xcom-backend-example`.

2. [Create a new bucket](https://cloud.google.com/storage/docs/creating-buckets) called `gcs-xcom-backend-example`.

3. [Create a custom IAM role](https://cloud.google.com/iam/docs/creating-custom-roles) called `AirflowXComBackendGCS` for Airflow to access your bucket. Assign 6 permissions:

    - storage.buckets.list
    - storage.objects.create
    - storage.objects.delete
    - storage.objects.get
    - storage.objects.list
    - storage.objects.update

    ![GCS IAM role](/img/guides/xcom_backend_gcs_role.png)

4. [Create a new service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) called `airflow-xcom` and grant it access to your project by granting it the `AirflowXComBackendGCS` role.

    ![GCS IAM role](/img/guides/xcom_backend_gcs_service_account.png)

5. [Create a new key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your `airflow-xcom` service account and make sure to download the credentials in JSON format.

</TabItem>
<TabItem value="azure">

1. Log into your Azure account and if you do not have one, [create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create). Astronomer recommends preventing public access to the storage account.

2. In the storage account, [create a new container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal) called `custom-xcom-backend`. 

3. [Create a shared access token](https://learn.microsoft.com/en-us/azure/cognitive-services/Translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers) for the `custom-xcom-backend` container. 

    In the **Permissions** dropdown menu, enable the following permissions:

    - Read
    - Add
    - Create
    - Write
    - Delete
    - List
    
    Set the duration the token will be valid and set **Allowed Protocols** to `HTTPS only`. Provide the IP address of your Airflow instance. If you are running Airflow locally with the Astro CLI, use the IP address of your computer.

    ![Shared access token](/img/guides/xcom_backend_shared_access_token.png)

4. Click on `Generate SAS token and URL` and copy the `Blob SAS URL`. This URL contains a secret and you will need it again in [Step 3](#step-3-create-a-connection) of this tutorial.

</TabItem>
<TabItem value="local">

There are several local object storage solutions available to configure as a custom XCom backend. This tutorial uses [MinIO](https://min.io/docs/minio/kubernetes/upstream/) running in Docker. 

1. [Start a MinIO container](https://min.io/docs/minio/container/index.html). 

2. Go to `http://127.0.0.1:9090/`, log in, and create a new bucket called `custom-xcom-backend`.

3. Create a new Access Key and store it in a secure location.

    ![MinIO Access Key](/img/guides/xcom_backend_minio_access_key.png)

</TabItem>
</Tabs>

## Step 3: Create a connection

<Tabs
    defaultValue="aws"
    groupId= "step-3-create-a-connection"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

To give Airflow access to your S3 bucket you need to define an [Airflow connection](connections.md). 

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Amazon Web Service`. Provide the AWS Access Key ID and AWS Secret Access Key from the IAM user you created in [Step 2](?tab=aws#step-2-set-up-your-object-storage-account). The following screenshot shows how you would configure a connection with the ID `s3_xcom_backend_conn`.

    ![Airflow Connection to S3](/img/guides/xcom_backend_aws_connection.png)

2. Test and save your connection.

</TabItem>

<TabItem value="gcp">

To give Airflow access to your GCS bucket you need to define an [Airflow connection](connections.md). 

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Google Cloud`. Provide the name of your project (`custom-xcom-backend-example`). Open the JSON file with the credentials you downloaded in [Step 2](?tab=gcp#step-2-set-up-your-object-storage-account) and copy paste it in full into the field `Keyfile JSON`. The following screenshot shows how you would configure a connection with the ID `gcs_xcom_backend_conn`.

    ![Airflow Connection to GCS bucket](/img/guides/xcom_backend_gcs_connection.png)

2. Test and save your connection.

</TabItem>
<TabItem value="azure">

To give Airflow access to your Azure Blob Storage container you need to define an [Airflow connection](connections.md).

1. In the Airflow UI go to **Admin** -> **Connections** and create a new a connection (**+**) with the Connection Type `Azure Blob Storage`. Provide the full Blob SAS URL to the `SAS Token` field. The following screenshot below shows how you would configure a connection with the ID `azure_xcom_backend_conn`.

    ![Airflow Connection to Azure Blob Storage container](/img/guides/xcom_backend_azure_connection.png)

2. Test and save your connection.

</TabItem>
<TabItem value="local">

To give Airflow access to your MinIO bucket you will need to use the credentials created in [Step 2](?tab=local#step-2-set-up-your-object-storage-account). 

In your Astro project's `.env` file set the following environment variables. You may need to adjust your `MINIO_IP` if you have a custom API port.

```text
MINIO_ACCESS_KEY=<your access key>
MINIO_SECRET_KEY=<your secret key>
MINIO_IP=host.docker.internal:9000
```

</TabItem>
</Tabs>

## Step 4: Define a custom XCom class using JSON serialization

For Airflow to use your custom XCom backend, you need to define an XCom backend class which inherits from the `BaseXCom` class.

:::info

The Astronomer provider package contains a pre-built XCom backend for AWS S3 and GCP Cloud Storage, with a set of added serialization methods. Refer to the [Use pre-built XCom backends](#use-pre-built-xcom-backends) section for implementation details. When you use a pre-built XCom backend, you don't need to create any new files in the `include` folder and you can skip both Step 4 and [Step 6](#step-6-create-a-custom-serialization-method-to-handle-pandas-dataframes) of this tutorial.

:::

1. In your Astro project, create a new file in the `include` directory called `xcom_backend_json.py`.

2. Copy paste the following code into the file:

<Tabs
    defaultValue="aws"
    groupId= "step-4-define-a-custom-xcom-class-using-json-serialization"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

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

    If you use Astro, set this environment variable in your Deployment instead. See [Environment variables](https://docs.astronomer.io/astro/environment-variables).

5. Restart your Airflow instance using `astro dev restart`. 


## Step 5: Create and run your DAG to generate XComs

To test your custom XCom backend you will run a simple DAG which pushes a random number to your custom XCom backend and then retrieves it again.

1. Create a new file in your `dags` folder named `simple_xcom_dag.py`.

2. Copy and paste the code below into the file.

    <CodeBlock language="python">{simple_xcom}</CodeBlock>

3. Run the DAG.

4. View the logs of both tasks. The logs will include information about the custom XCom backend. The `print_a_number` task includes the full path to the file stored in the custom backend.

    ![Logs mentioning custom XCom backend](/img/guides/xcom_backend_task_logs_simple.png)


5. View the XCom in your local object storage.

<Tabs
    defaultValue="aws"
    groupId= "step-5-create-and-run-your-dag-to-generate-xcoms"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

![XCom in the S3 bucket](/img/guides/xcom_backend_S3_json.png)

</TabItem>

<TabItem value="gcp">

![XCom in the GCS bucket](/img/guides/xcom_backend_gcs_json.png)

</TabItem>
<TabItem value="azure">

![XCom in the blob](/img/guides/xcom_backend_azure_blob.png)

</TabItem>
<TabItem value="local">

![XCom in the MinIO bucket](/img/guides/xcom_backend_minio_file.png)

</TabItem>
</Tabs>

## Step 6: Create a custom serialization method to handle Pandas dataframes

A powerful feature of custom XCom backends is the possibility to create custom serialization and deserialization methods. This is particularly useful for handling objects that cannot be JSON-serialized or if you want to serialize Pandas dataframes using a different method than `pyarrow`. In this step, you will create a new custom XCom backend that can save the contents of a [Pandas](https://pandas.pydata.org/) dataframe as a CSV file. Being serialized as CSV, the content of the XCom becomes accessible to CSV query tools like [csvq](https://mithrandie.github.io/csvq/).

:::info

The Astronomer provider package contains a pre-built XCom backend for AWS S3 and GCP Cloud Storage with added serialization methods for Pandas dataframes and datetime date objects. Refer to the [Use pre-built XCom backends](#use-pre-built-xcom-backends) section for implementation details. 
When using a pre-built XCom backend you do not have to create any new files in the `include` folder and you can skip [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization) and Step 6 of this tutorial.

:::

1. Create a second file in your `include` folder called `xcom_backend_pandas.py`.

2. Copy and paste the following code into the file.

<Tabs
    defaultValue="aws"
    groupId= "step-6-create-a-custom-serialization-method-to-handle-pandas-dataframes"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'MinIO (local)', value: 'local'}
    ]}>
<TabItem value="aws">

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import json
import uuid
import os

class CustomXComBackendPandas(BaseXCom):
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
            bucket_name=CustomXComBackendPandas.BUCKET_NAME,
            replace=True
        )

        # remove the local temporary file
        os.remove(filename)

        reference_string = CustomXComBackendPandas.PREFIX + s3_key

        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        result = BaseXCom.deserialize_value(result)

        hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
        key = result.replace(CustomXComBackendPandas.PREFIX, "")

        filename = hook.download_file(
            key=key,
            bucket_name=CustomXComBackendPandas.BUCKET_NAME,
            local_path="/tmp"
        )

        # added deserialization option to convert a CSV back to a dataframe
        if key.split(".")[-1] == "csv":
            output = pd.read_csv(filename)
        # if the key does not end in 'csv' use JSON deserialization
        else:
            with open(filename, 'r') as f:
                output = json.load(f)

        # remove the local temporary file
        os.remove(filename)

        return output
```
</TabItem>
<TabItem value="gcp">

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import pandas as pd
import json
import uuid
import os

class CustomXComBackendPandas(BaseXCom):
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
            filename = "data_" + str(uuid.uuid4()) + ".csv"
            gs_key = f"{run_id}/{task_id}/{filename}"

            value.to_csv(filename)

        # if the value passed is not a Pandas dataframe, attempt to use
        # JSON serialization
        else:
            filename = "data_" + str(uuid.uuid4()) + ".json"
            gs_key = f"{run_id}/{task_id}/{filename}"

            with open(filename, 'a+') as f:
                json.dump(value, f)

        hook.upload(
            filename=filename,
            object_name=gs_key,
            bucket_name=CustomXComBackendPandas.BUCKET_NAME,
        )

        # remove the local temporary file
        os.remove(filename)

        reference_string = CustomXComBackendPandas.PREFIX + gs_key

        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        result = BaseXCom.deserialize_value(result)

        hook = GCSHook(gcp_conn_id="gcs_xcom_backend_conn")
        gs_key = result.replace(CustomXComBackendPandas.PREFIX, "")

        filename = hook.download(
            object_name=gs_key,
            bucket_name=CustomXComBackendPandas.BUCKET_NAME,
            filename="my_xcom.csv"
        )

        # added deserialization option to convert a CSV back to a dataframe
        if gs_key.split(".")[-1] == "csv":
            output = pd.read_csv(filename)
        # if the key does not end in 'csv' use JSON deserialization
        else:
            with open(filename, 'r') as f:
                output = json.load(f)

        # remove the local temporary file
        os.remove(filename)

        return output
```

</TabItem>
<TabItem value="azure">

```python
from airflow.models.xcom import BaseXCom
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
import pandas as pd
import json
import uuid
import os

class CustomXComBackendPandas(BaseXCom):
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
            container_name=CustomXComBackendPandas.CONTAINER_NAME,
            blob_name=blob_key
        )

        # remove the local temporary file
        os.remove(filename)

        reference_string = CustomXComBackendPandas.PREFIX + blob_key

        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        result = BaseXCom.deserialize_value(result)

        hook = WasbHook(wasb_conn_id="azure_xcom_backend_conn")
        blob_key = result.replace(CustomXComBackendPandas.PREFIX, "")

        hook.get_file(
            blob_name=blob_key,
            container_name=CustomXComBackendPandas.CONTAINER_NAME,
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

        # remove the local temporary file
        os.remove("my_xcom_file")

        return output
```

</TabItem>
<TabItem value="local">

```python
from airflow.models.xcom import BaseXCom
import pandas as pd
import json
import uuid
from minio import Minio
import os
import io

class CustomXComBackendPandas(BaseXCom):
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

            # remove the local temporary file
            os.remove(filename)

        # if the value passed is not a Pandas dataframe, attempt to use
        # JSON serialization
        else:
            filename = "data_" + str(uuid.uuid4()) + ".json"
            minio_key = f"{run_id}/{task_id}/{filename}"

            bytes_to_write = io.BytesIO(bytes(json.dumps(value), 'utf-8'))

        client.put_object(
            CustomXComBackendPandas.BUCKET_NAME,
            minio_key,
            bytes_to_write,
            -1, # -1 = unknown filesize
            part_size=10*1024*1024,
        )

        reference_string = CustomXComBackendPandas.PREFIX + minio_key

        return BaseXCom.serialize_value(value=reference_string)

    @staticmethod
    def deserialize_value(result):
        reference_string = BaseXCom.deserialize_value(result=result)
        key = reference_string.replace(CustomXComBackendPandas.PREFIX, "")

        client = Minio(
            os.environ["MINIO_IP"],
            os.environ["MINIO_ACCESS_KEY"],
            os.environ["MINIO_SECRET_KEY"],
            secure=False
        )

        response = client.get_object(
            CustomXComBackendPandas.BUCKET_NAME,
            key
        )

        # added deserialization option to convert a CSV back to a dataframe
        if key.split(".")[-1] == "csv":

            with open("csv_xcom.csv", "w") as f:
                f.write(response.read().decode("utf-8"))
            output = pd.read_csv("csv_xcom.csv")

            # remove the local temporary file
            os.remove("csv_xcom.csv")

        # if the key does not end in 'csv' use JSON deserialization
        else:
            output = json.loads(response.read())

        return output
```

</TabItem>
</Tabs>

3. Review the copied code. It creates a custom XCom backend called `CustomXComBackendPandas` with added logic to convert a Pandas dataframe to a CSV file, which gets written to object storage and converted back to a Pandas dataframe upon retrieval. If the value passed is not a Pandas dataframe, the `.serialize()` and `.deserialize` methods will use JSON serialization like the custom XCom backend in [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization).

4. In the `.env` file of your Astro project, replace the XCom backend variable to use the newly created `CustomXComBackendPandas`.

    ```text
    AIRFLOW__CORE__XCOM_BACKEND=include.xcom_backend_pandas.CustomXComBackendPandas
    ```

5. Restart your Airflow instance by running `astro dev restart`.

:::tip

You can add custom logic inside your `.serialize()` and `.deserialize()` methods to send XComs to several custom XCom backend solutions, for example based on their object type.

:::

## Step 7: Run a DAG passing Pandas dataframes via XCom

Test the new custom XCom backend by running a DAG that passes a Pandas dataframe between tasks.

1. Create a new file called `fetch_pokemon_data_dag.py` in the `dags` folder of your Astro project.

2. Copy and paste the DAG below. Make sure to enter your favorite Pokémon.

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
            """Extracts data from the Pokémon API. Returns a JSON serializeable dict."""

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
            """Retrieves information from a pandas dataframe in the custom XCom
            backend. Prints out Pokémon information."""

            for i in pokemon_data_df.index:
                pokemon = pokemon_data_df.loc[i, 'pokemon']
                xph = pokemon_data_df.loc[i, 'xp_per_height']
                print(f"{pokemon} has a base xp to height ratio of {xph}")

        print_xp_per_height(calculate_xp_per_height(extract_data()))

    fetch_pokemon_data_dag()
    ```

    The `extract_data` task will push a dictionary to XCom, which will be saved to your blob storage as a JSON file and retrieved by the `calculate_xp_per_height` task. This second task pushes a Pandas dataframe to XCom, which is only possible when using a custom XCom backend with a serialization method for this type of object. The last task, `print_xp_per_height`, retrieves the CSV and recreates the Pandas dataframe before printing out the Pokémon and their base experience to height ratio.

3. View the information about your favorite Pokémon in the task log of the `print_xp_per_height` task.

    ![Pokémon Information in logs](/img/guides/xcom_backend_task_logs_pokemon.png)

## Overriding additional BaseXCom methods

In this tutorial, you added custom logic to the `.serialize_value()` and  `.deserialize_value()` methods. If you want to further customize the functionality for your custom XCom backend, you can override additional methods of the [XCom module](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/xcom/index.html) ([source code](https://github.com/apache/airflow/blob/main/airflow/models/xcom.py)). 

A common use case for this is removing stored XComs upon clearing and rerunning a task in both the Airflow metadata database and the custom XCom backend. To do so, the `.clear()` method needs to be overridden to include the removal of the referenced XCom in the custom XCom backend. The code below shows an example of a `.clear()` method that includes the deletion of an XCom stored in a custom S3 backend, using the AWS version of the CustomXComBackendJSON XCom backend from [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization) of the tutorial.

```python
from airflow.utils.session import NEW_SESSION, provide_session

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
    from airflow.utils.helpers import exactly_one
    import warnings
    from airflow.exceptions import RemovedInAirflow3Warning

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

    #### Customization start

    # get the reference string from the Airflow metadata database
    if map_index is not None:
        reference_string = session.query(cls.value).filter_by(
            dag_id=dag_id,
            task_id=task_id,
            run_id=run_id,
            map_index=map_index
        ).scalar()
    else:
        reference_string = session.query(cls.value).filter_by(
            dag_id=dag_id,
            task_id=task_id,
            run_id=run_id
        ).scalar()

    if reference_string is not None:

        # decode the XCom binary to UTF-8
        reference_string = reference_string.decode('utf-8')
        
        hook = S3Hook(aws_conn_id="s3_xcom_backend_conn")
        key = reference_string.replace(CustomXComBackendJSON.PREFIX, '')

        # use the reference string to delete the object from the S3 bucket
        hook.delete_objects(
            bucket=CustomXComBackendJSON.BUCKET_NAME,
            keys=json.loads(key)
        )

    # retrieve the XCom record from the metadata database containing the reference string
    query = session.query(cls).filter_by(
        dag_id=dag_id,
        task_id=task_id,
        run_id=run_id
    )
    if map_index is not None:
        query = query.filter_by(map_index=map_index)

    # delete the XCom containing the reference string from metadata database
    query.delete()
```

## Use pre-built XCom backends

The [Astronomer provider package](https://registry.astronomer.io/providers/astronomer-providers/versions/latest) includes alternative XComs backends for AWS S3 and GCP Cloud Storage. In addition to saving your XComs in a remote storage, these XCom backends contain serialization methods for `pandas.DataFrame` and `datetime.date` objects, so you don't have to write them yourself.

To use these pre-built XCom backends, modify the core tutorial with the following changes:

- In [Step 1](#step-1-create-an-astro-project), add the Astronomer provider to your Astro project `requirements.txt` file:

    ```text
    astronomer-providers
    ```

- In [Step 3](#step-3-create-a-connection), use the connection ID `aws_default` for an AWS S3 connection and `google_cloud_default` for a GCP Cloud Storage connection. You can override which connection ID the backend uses by setting the Airflow environment variable `CONNECTION_NAME` for AWS or `XCOM_BACKEND_CONNECTION_NAME` for GCS.

- In [Step 4](#step-4-define-a-custom-xcom-class-using-json-serialization), do not define your own custom XCom class. When you open the Astro project `.env`, add the following lines to use the pre-built XCom backend instead of your own:

<Tabs
    defaultValue="aws"
    groupId= "use-pre-built-xcom-backends"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
    ]}>
<TabItem value="aws">

```text
AIRFLOW__CORE__XCOM_BACKEND=astronomer.providers.amazon.aws.xcom_backends.s3.S3XComBackend
XCOM_BACKEND_BUCKET_NAME=<your-bucket-name>
```

</TabItem>

<TabItem value="gcp">

```text
AIRFLOW__CORE__XCOM_BACKEND=astronomer.providers.google.cloud.xcom_backends.gcs.GCSXComBackend
XCOM_BACKEND_BUCKET_NAME=<your-bucket-name>
```

</TabItem>

</Tabs>

- Skip [Step 6](#step-6-create-a-custom-serialization-method-to-handle-pandas-dataframes). The pre-built XCom backend includes a serialization method for `pandas.DataFrame` objects out of the box.

:::tip

The Astronomer provider XCom backends support gzip compression for all XComs. To enable gzip compression, set `UPLOAD_CONTENT_AS_GZIP=True` in your Astro project  `.env` file.

:::

## Conclusion

Congratulations! You learned how to set up a custom XCom backend and how to define your own serialization and deserialization methods. 