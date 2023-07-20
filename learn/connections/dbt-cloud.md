---
title: "Create a dbt Cloud connection in Airflow"
id: dbt-cloud
sidebar_label: dbt Cloud
description: Learn how to create a dbt Cloud connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/dbt.png' }
---

[dbt Cloud](https://www.getdbt.com/product/what-is-dbt/) is a SaaS product that runs SQL-first transformation workflows. Integrating dbt Cloud with Airflow allows you to trigger dbt cloud jobs and check their status from an Airflow DAG.

This guide provides the basic setup for creating a dbt Cloud Airflow connection. For a complete integration tutorial, see [Orchestrate dbt Cloud jobs with Airflow](connections/airflow-dbt-cloud.md). For running your dbt core jobs using Airflow, see [Orchestrate dbt-core Jobs with Airflow](connections/airflow-dbt.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- A [dbt Cloud account](https://cloud.getdbt.com/)

## Get connection details

A connection from Airflow to dbt Cloud requires the following information:

- dbt Cloud URL
- API token
- Account ID

Complete the following steps to retrieve these values:

1. In the dbt Cloud UI, copy the URL of your dbt Cloud account. It should be formatted as `https://cloud.getdbt.com`. Your URL might be different based on the hosted region of your dbt Cloud. See [dbt Cloud URIs](https://docs.getdbt.com/docs/cloud/manage-access/sso-overview#auth0-multi-tenant-uris) for more details.

2. If you're using a dbt Developer account, follow the [dbt documentation](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens#user-api-tokens) to copy the API token for your user account. To generate a token for a service account, see [Generating service account tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens#generating-service-account-tokens).

3. To retrieve the Account ID of your dbt account, go to the settings page in dbt Cloud UI. Then, from the URL of the settings page, copy the account ID, which is an integer appearing after **Accounts**. For example, in the URL `https://cloud.getdbt.com/settings/accounts/88348`, the account ID is `88348`.

## Create your connection

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-dbt-cloud
    ```

    This will install the dbt Cloud provider package, which makes the dbt Cloud connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **dbt Cloud**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Tenant**: Enter the dbt Cloud URL.
    - **API Token**: Enter your user token or service access token.
    - **Account ID**: Enter your dbt cloud account ID. This field is optional. If you skip this, you must pass the account ID to the dbt cloud operator or hook. 

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![dbtcloud](/img/examples/connection-dbt-cloud.png)

:::info

Note that the connection test only tests the **Tenant** and **API Token** fields. It will not validate your **Account ID**.

:::

## How it works

Airflow uses Python's `requests` library to connect to dbt Cloud through the [dbtHook](https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/_api/airflow/providers/dbt/cloud/hooks/dbt/index.html).

## See also
- [Apache Airflow dbt cloud provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/connections.html)
- [dbt Cloud modules](https://registry.astronomer.io/modules?limit=24&sorts=updatedAt%3Adesc&query=dbt) and [example DAGs](https://registry.astronomer.io/dags?limit=24&sorts=updatedAt%3Adesc&query=dbt+cloud) in Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)