---
title: "Create an Azure Blob Storage connection in Airflow"
id: azure-blob-storage
sidebar_label: "Azure Blob Storage"
description: Learn how to create an Azure Blob Storage connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/azure-blob-storage.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview) provides the storage for all of your Azure Storage data objects, including blobs, files, queues, and tables. Integrating your Azure storage account with Airflow lets you perform different kind of operations on blob objects stored in the cloud. For example, you can create or delete a container, upload or read a blob, or download blobs using Airflow.

This guide explains how to set up an Azure Blob Storage connection using the **Azure Blob Storage** connection type. Astronomer recommends using this connection type because it utilizes the `wasb` protocol, which means you can connect with any Azure Storage account including Azure Data Lake Gen 1 and Azure Data Lake Gen 2.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- An [Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal).
- [Permissions to access](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access?tabs=portal) blob data from your local Airflow environment.

## Get connection details

To create an Azure Blob Storage connection in Airflow, you can use any of the following methods:

<Tabs
    defaultValue="shared-access-key"
    groupId= "azure-blob-storage"
    values={[
        {label: 'Shared access key', value: 'shared-access-key'},
        {label: 'Connection string', value: 'connection-string'},
        {label: 'SAS token', value: 'sas-token'},
        {label: 'Azure app service principal', value: 'azure-app-service-principal'},
    ]}>

<TabItem value="shared-access-key">

Microsoft generates two [shared access keys](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal) by default for every storage account. You can use them to give Airflow access to the data in your storage account. 

An Azure Blob Storage connection using a shared access key requires the following information:

- Name of the storage account
- Shared access key

Complete the following steps to retrieve these values:

1. In your Azure portal, open your storage account. 
2. Copy the name of your storage account.
3. Follow [Microsoft documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) to copy the storage account **Key**.

</TabItem>

<TabItem value="connection-string">

A [connection string](https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string) for a storage account includes the authorization information required to access data in your storage account. 

An Azure blob storage connection using connection string requires the following information:

- Storage account name
- Storage account connection string

Complete the following steps to retrieve these values:

1. In your Azure portal, open your storage account. 
2. Copy the name of your storage account.
3. Follow [Microsoft documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-get-info?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=portal#get-a-connection-string-for-the-storage-account) to copy the **Connection string**. 

</TabItem>

<TabItem value="sas-token">

A [shared access signature (SAS) token](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview) provides granular access for a storage account. 

An Azure blob storage connection using SAS token requires the following information:

- Storage account name
- SAS token

Complete the following steps to retrieve these values:

1. In your Azure portal, navigate to your Storage account view and select your subscription. 
2. Copy the name of your storage account.
3. Follow the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers#create-sas-tokens-in-the-azure-portal) to generate your SAS token. Copy the SAS token.

</TabItem>

<TabItem value="azure-app-service-principal">

A [service principal for an Azure app](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview) provides granular access for a storage account. 

An Azure Blob Storage connection using a service principal requires the following information:

- Storage account URL
- Application Client ID
- Tenant ID
- Client secret

Complete the following steps to retrieve these values:

1. In your Azure portal, open your storage account.
2. Follow [Azure documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-get-info?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json&tabs=portal#get-service-endpoints-for-the-storage-account) to copy your **Blob Service URL**. It should be in the format `https://mystorageaccount.blob.core.windows.net/`.
3. Open your Azure AD application. Then, from the **Overview** tab, copy the **Application (client) ID** and **Directory (tenant) ID**.
4. [Create a new client secret](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-3-create-a-new-application-secret) for your application to be used in the Airflow connection. Copy the **VALUE** of the client secret that appears.
5. [Assign](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#assign-a-role-to-the-application) the [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor) role to your app so that Airflow can access blob objects in your storage account.

</TabItem>
</Tabs>

## Create your connection

<Tabs
    defaultValue="shared-access-key"
    groupId= "azure-blob-storage"
    values={[
        {label: 'Shared access key', value: 'shared-access-key'},
        {label: 'Connection string', value: 'connection-string'},
        {label: 'SAS token', value: 'sas-token'},
        {label: 'Azure app service principal', value: 'azure-app-service-principal'},
    ]}>

<TabItem value="shared-access-key">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Microsoft Azure provider package, which makes the Azure Blob Storage connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Azure Blob Storage** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Blob Storage Login**: Enter your storage account name. 
    - **Blog Storage Key**: Enter your storage account **Key**.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![azure-connection-storage-access-key](/img/examples/connection-azure-blob-storage-key.png)

</TabItem>

<TabItem value="connection-string">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Microsoft Azure provider package, which makes the Azure Blob Storage connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Azure Blob Storage** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Blob Storage Connection String**: Enter your storage account connection string.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![azure-connection-storage-conn-string](/img/examples/connection-azure-blob-storage-conn-string.png)

:::tip

If you want, you can replace the value in **Blob Storage Connection String** with the connection string for an SAS token.

:::

</TabItem>

<TabItem value="sas-token">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Microsoft Azure provider package, which makes the Azure Blob Storage connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Azure Blob Storage** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Blob Storage Login**: Enter the name of your storage account.
    - **SAS Token**: Enter your SAS token.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![azure-connection-storage-sas-token](/img/examples/connection-azure-blob-storage-sas-token.png)

</TabItem>

<TabItem value="azure-app-service-principal">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Microsoft Azure provider package, which makes the Azure Blob Storage connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Azure Blob Storage** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Account Name**: Enter **Blob Service URL** for your storage account.
    - **Blob Storage Login**: Enter your **Application (client) ID**.
    - **Blob Storage Key**: Enter your client secret **Value**.
    - **Tenant Id**: Enter your **Directory (tenant) ID**. 

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![azure-blob-storage-app-secret](/img/examples/connection-azure-blob-storage-app-secret.png)

</TabItem>
</Tabs>

## How it works

Airflow uses the [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python) to connect to Azure services through the [WasbHook](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/_api/airflow/providers/microsoft/azure/hooks/wasb/index.html).

## See also

- [Apache Airflow Microsoft Azure provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/wasb.html).
- [Azure blob storage modules](https://registry.astronomer.io/modules?query=wasb) and [example DAGs](https://registry.astronomer.io/dags/covid_to_azure_blob/versions/1.2.0) in the Astronomer Registry.
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#from-environment-variables).