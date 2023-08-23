---
title: "Create a BigQuery connection in Airflow"
id: bigquery
sidebar_label: BigQuery
description: Learn how to create a BigQuery connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/bigquery.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[BigQuery](https://cloud.google.com/bigquery) is Google's fully managed and serverless data warehouse. Integrating BigQuery with Airflow lets you execute BigQuery jobs from a DAG. 

There are multiple ways to connect Airflow and BigQuery, all of which require a [GCP Service Account](https://cloud.google.com/docs/authentication#service-accounts):

- Use the contents of a service account key file directly in an Airflow connection.
- Copy the service account key file to your Airflow project.
- Store the contents of a service account key file in a secrets backend.
- Use a Kubernetes service account to integrate Airflow and BigQuery. This is possible only if you run Airflow on Astro or Google Kubernetes Engine (GKE).

Using a Kubernetes service account is the most secure method because it doesn't require storing a secret in Airflow's metadata database, on disk, or in a secrets backend. The next most secure connection method is to store the contents of your service account key file in a secrets backend.

:::tip

If you're an Astro user, Astronomer recommends using workload identity to authorize to your Deployments to BigQuery. This eliminates the need to specify secrets in your Airflow connections or copying credentials file to your Astro project. See [Authorize Deployments to your cloud](https://docs.astronomer.io/astro/authorize-deployments-to-your-cloud?tab=gcp#cloud-provider).

:::

## Prerequisites
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A Google Cloud project with [BigQuery API](https://cloud.google.com/bigquery/docs/enable-transfer-service#enable-api) enabled.
- Permissions to create an IAM service account or use an existing one. See [Google documentation](https://cloud.google.com/iam/docs/manage-access-service-accounts).

## Get connection details

A connection from Airflow to Google BigQuery requires the following information:

- Service account name
- Service account key file
- Google Cloud Project ID

Complete one of the following sets of steps to retrieve these values:

<Tabs
    defaultValue="key-file-value"
    groupId= "bigquery-connection"
    values={[
        {label: 'Key file value', value: 'key-file-value'},
        {label: 'Key file in container', value: 'key-file-in-container'},
        {label: 'Key file in secrets backend', value: 'key-file-in-secrets-backend'},
        {label: 'Kubernetes service account', value: 'kubernetes-service-account'}
    ]}>

<TabItem value="key-file-value">

This method requires you to save the contents of your service account key file in your Airflow connection. 

1. In your Google Cloud console, select your Google Cloud project and copy its **ID**.
2. [Create a new service account](https://cloud.google.com/iam/docs/service-accounts-create). 
3. [Grant roles](https://cloud.google.com/iam/docs/grant-role-console) to your service account so that it can access BigQuery. See [BigQuery roles](https://cloud.google.com/bigquery/docs/access-control#bigquery) for a list of available roles and the permissions.
4. [Add a new JSON key file](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console) to the service account.
5. Copy the contents of the key file.

</TabItem>

<TabItem value="key-file-in-container">

This method requires you to mount your service account key file to your Airflow containers.

1. In your Google Cloud console, select your Google Cloud project and copy its **ID**.
2. [Create a new service account](https://cloud.google.com/iam/docs/service-accounts-create). 
3. [Grant roles](https://cloud.google.com/iam/docs/grant-role-console) to your service account so that it can access BigQuery. See [BigQuery roles](https://cloud.google.com/bigquery/docs/access-control#bigquery) for a list of available roles and the permissions.
4. [Add a new JSON key file](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console) to the service account.
5. Download the key file.

</TabItem>

<TabItem value="key-file-in-secrets-backend">

You can save your service account key file to any secrets backend. See [Configure a secrets backend](https://docs.astronomer.io/astro/secrets-backend) for steps on how to configure several popular secrets backend services to use with Airflow on Astro. For example, if you use Google Secret Manager as a secrets backend:

1. In the Google Cloud console, select your Google Cloud project and copy its **ID**.
2. [Create a new service account](https://cloud.google.com/iam/docs/service-accounts-create). 
3. [Grant roles](https://cloud.google.com/iam/docs/grant-role-console) to your service account so that it can access BigQuery. See [BigQuery roles](https://cloud.google.com/bigquery/docs/access-control#bigquery) for a list of available roles and the permissions.
4. [Add a new JSON key file](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console) to the service account.
5. Download the key file.
6. [Create a secret](https://cloud.google.com/secret-manager/docs/create-secret-quickstart) in Google Secret Manager and upload the key file from Step 5 as a secret value. Then, copy the ID of your secret name.
7. Follow Astronomer's documentation to [configure secrets backend](https://docs.astronomer.io/astro/secrets-backend) for your Astro project.

You can now use this secret in your Airflow connections.

</TabItem>

<TabItem value="kubernetes-service-account">

A [Kubernetes service account](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/) provides an identity to the processes running in a Pod. The process running inside a Pod can use this identity of its associated service account to authenticate cluster's API server. This is also referred to as Workload Identity in [GCP](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity) and [Azure](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity).

This method cannot be used in a local Airflow environment. It is available to use with Airflow on Astro or OSS Airflow running on Kubernetes clusters. 

If you're running Airflow in a GKE cluster, complete the following steps:

1. In your Google Cloud console, open the Google Cloud project where you're running BigQuery and copy its **ID**.
2. [Enable Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) and [configure Airflow to use workload identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to). Copy the name for the Kubernetes service account that you create. 
3. Go to **IAM**, then click **Service Accounts** and search for your Kubernetes service account. If you don't see your service account, click **+ ADD** to add your service account to your Google Cloud project.
4. [Grant roles](https://cloud.google.com/iam/docs/grant-role-console) to your service account to access BigQuery. See [BigQuery roles](https://cloud.google.com/bigquery/docs/access-control#bigquery) for a list of available roles and the permissions.

After you complete these steps, any Google Cloud connection you create in the Deployment will use your workload identity by default to access BigQuery.

</TabItem>

</Tabs>

## Create your connection

<Tabs
    defaultValue="key-file-value"
    groupId= "bigquery-connection"
    values={[
        {label: 'Key file value', value: 'key-file-value'},
        {label: 'Key file in container', value: 'key-file-in-container'},
        {label: 'Key file in secrets backend', value: 'key-file-in-secrets-backend'},
        {label: 'Kubernetes service account', value: 'kubernetes-service-account'}
    ]}>

<TabItem value="key-file-value">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-google
    ```

    This installs the Google Cloud provider package, which makes the Google Cloud connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Google Cloud** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Keyfile JSON**: Enter the contents of the key file.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![gcp-connection-key-in-ui](/img/examples/connection-gcp-key-in-ui.png)

</TabItem>

<TabItem value="key-file-in-container">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-google
    ```

    This installs the Google Cloud provider package, which makes the Google Cloud connection type available in Airflow.

2. Add the key file to your `include` folder. This will make it available to Airflow at `/usr/local/airflow/include/<your-key-file>.json`.

3. Restart or start your local Airflow using `astro dev restart` to apply your changes in `requirements.txt`.

4. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Google Cloud** connection type.

5. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):
    
    - **Connection Id**: Enter a name for the connection.
    - **Keyfile Path**: Enter the path of your key file.

6. Click **Test connection**. After the connection test succeeds, click **Save**.

    ![gcp-connection-key-in-airflow-container](/img/examples/connection-gcp-key-in-airflow-container.png)

</TabItem>

<TabItem value="key-file-in-secrets-backend">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-google
    ```

    This will install the Google Cloud provider package, which makes the Google Cloud connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then choose the **Google Cloud** connection type.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Keyfile Secret Project Id**: Enter the **ID** of the Google Cloud project.
    - **Keyfile Secret Name**: Enter the ID of your secret name.

5. Click **Test connection**. After the connection test succeeds, click **Save**.

    ![gcp-connection-key-in-secret-manager](/img/examples/connection-gcp-key-in-secret-manager.png)

</TabItem>

<TabItem value="kubernetes-service-account">

1. Open your Airflow project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-google
    ```

    This will install the Google Cloud provider package, which makes the Google Cloud connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In your Airflow UI, go to **Admin** > **Connections**. Click the **+** sign to add a new connection, select the connection type as **Google Cloud**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):
    
    - **Connection Id**: Enter a name for the connection.
    - **Project Id**: Enter the **ID** of the Google Cloud project.

5. Click **Test connection**. After the connection test succeeds, click **Save**.

    ![gcp-connection-using-workload-identity](/img/examples/connection-gcp-workload-identity.png)


</TabItem>

</Tabs>

## How it works

Airflow uses the [`python-bigquery`](https://github.com/googleapis/python-bigquery) library to connect to GCP BigQuery through the [BigQueryHook](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/hooks/bigquery/index.html). If you don't define specific key credentials in the connection, Google defaults to using [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials). This means when you use Workload Identity to connect to BigQuery, Airflow relies on ADC to authenticate.

## See also

- [Apache Airflow Google provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)
- [BigQuery Modules](https://registry.astronomer.io/modules?query=bigquery) and [Example DAGs](https://registry.astronomer.io/dags?limit=24&sorts=updatedAt%3Adesc&query=bigquery) in the Astronomer Registry
- [Import and export Airflow connections using the Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)