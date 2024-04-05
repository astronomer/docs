---
title: 'Set up a custom XCom backend using object storage'
sidebar_label: 'Set up an XCom backend'
id: xcom-backend-tutorial
description: 'Use this tutorial to learn how to set up a custom XCom backend with Object Storage.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import custom_xcom_backend_test from '!!raw-loader!../code-samples/dags/xcom-backend-tutorial/custom_xcom_backend_test.py';

By default, Airflow uses the [metadata database](airflow-database.md) to store XComs, which works well for local development but has limited performance. For production environments that use XCom to pass data between tasks, Astronomer recommends using a custom XCom backend. [Custom XCom backends](custom-backend-strategies.md) allow you to configure where Airflow stores information that is passed between tasks using [XComs](airflow-passing-data-between-tasks.md#xcom). 

The Object Storage Custom XCom Backend available in the [Common IO provider](https://airflow.apache.org/docs/apache-airflow-providers-common-io/stable/index.html) is the easiest way to store XComs in remote object storage solution.

This tutorial will show you how to set up a custom XCom backend using Object Storage for [AWS S3](https://aws.amazon.com/s3/), [GCP Cloud Storage](https://cloud.google.com/storage) or [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/).

To learn more about other options for setting custom XCom backends, see [Strategies for custom XCom backends in Airflow](custom-backend-strategies.md).

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

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) with an Astro project running Astro Runtime 11.0.0 or higher (Airflow 2.9.0 or higher). To set up a custom XCom backend with older versions of Airflow, see [Custom XCom backends](custom-backend-strategies.md).
- An account in either [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/), or [Azure](https://azure.microsoft.com/) with permissions to create and configure an object storage container.

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

To use the Object Storage Custom XCom Backend, you need to install the Common IO provider package and the provider package for your object storage container provider.

<Tabs
    defaultValue="aws"
    groupId="step-2-install-the-required-provider-packages"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'}
    ]}>
<TabItem value="aws">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Amazon](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest) provider packages to your `requirements.txt` file. Note that you need to install the `s3fs` extra to use the Amazon provider package with the [Object Storage](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html) feature.

    ```text
    apache-airflow-providers-common-io==1.3.0
    apache-airflow-providers-amazon[s3fs]==8.19.0
    ```

</TabItem>

<TabItem value="gcp">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Google](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest) provider packages to your `requirements.txt` file.

    ```text
    apache-airflow-providers-common-io==1.3.0
    apache-airflow-providers-google==10.17.0
    ```

</TabItem>

<TabItem value="azure">

Add the [Common IO](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest) and [Microsoft Azure](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest) provider packages to your `requirements.txt` file.

    ```text
    apache-airflow-providers-common-io==1.3.0
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

2. In the Airflow UI navigate to `Admin` -> `Connections` and click on `Create`. Fill in the following fields:

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

Configuring a custom XCom backend with Object Storage can be done by setting environment variables in your Astro project.

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

    ![XCom tab of the push_objects task showing two key-value pairs: "big_obj": "s3://ce-2-9-examples-bucket/xcom/custom_xcom_backend_test/manual__2024-03-27T13:18:52.642382+00:00/push_objects/8cf94ef7-b92e-4c65-a775-4e338c941f58.zip", "small_obj": a dictionary containing'a': 23.](/img/tutorials/custom-xcom-backends-tutorial_small_big_obj.png)

## Conclusion

Congratulations, you learned how to set up a custom XCom backend using Object Storage! Learn more about other options to set up custom XCom backends in the [Strategies for custom XCom backends in Airflow](custom-backend-strategies.md) guide.