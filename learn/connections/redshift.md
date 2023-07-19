---
title: "Create an Amazon Redshift Connection in Airflow"
id: redshift
sidebar_label: Redshift
description: Learn how to create an Amazon Redshift connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/redshift.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[Amazon Redshift](https://aws.amazon.com/redshift/) is a data warehouse product from AWS. Integrating Redshift with Airflow allows you to automate, schedule and monitor a variety of tasks. These tasks include creating, deleting, and resuming a cluster, ingesting or exporting data to and from Redshift, as well as running SQL queries against Redshift. 

This document covers two different methods to connect to Amazon Redshift:

- Using DB credentials
- Using IAM credentials

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- Permissions to access to your Redshift cluster. See [Using IAM authentication](https://docs.aws.amazon.com/redshift/latest/mgmt/generating-user-credentials.html) and [Authorizing Amazon Redshift to access other AWS services](https://docs.aws.amazon.com/redshift/latest/mgmt/authorizing-redshift-service.html).


## Get connection details

<Tabs
    defaultValue="db-creds"
    groupId= "redshift-connection"
    values={[
        {label: 'DB credendtials', value: 'db-creds'},
        {label: 'IAM credentials', value: 'iam-creds'},
    ]}>

<TabItem value="db-creds">

Database user credentials can be used to establish a connection to an Amazon Redshift cluster. While straight forward to use, this approach lacks the strong security and user access controls provided by Identity and access management (IAM). To connect to Redshift using this approach, following information is required:

- Cluster identifier
- Database name
- Port
- User
- Password

Complete the following steps to retrieve these values:

1. In your AWS console, select the region that contains your Redshift cluster and open Redshift cluster dashboard. Click your cluster, then from the **General information** tab, copy **Cluster identifier** and **Endpoint**.
2. Click on the **Properties** tab and copy **Database name** and **Port**.
3. Follow the AWS documentation to [Create a User](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html) and [Grant a Role](https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html). Copy the user and password.

</TabItem>

<TabItem value="iam-creds">

IAM Credentials can be supplied to your Airflow environment using an AWS profile. This approach allows users the option of using temporary credentials and limiting the permissions the connected user has.

Following information is required:

- Cluster identifier
- Database name
- Port
- Region
- IAM user
- AWS credentials file

Complete the following steps to retrieve these values:

1. In your AWS console, select the region that contains your Redshift cluster, and open your Redshift cluster dashboard. Click on your cluster, go to **General information**, then copy **Cluster identifier** and **Endpoint**.

2. Click on the **Properties** tab, then copy **Database name** and **Port**.

3. Open your IAM dashboard, go to **Users**, and select your user. Then, go to the **Permissions** and follow the [AWS documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-access-control-identity-based.html) to ensure that the IAM user is authorized to connect to Redshift and perform required SQL operations.

4. [Generate a new access key ID and secret access key](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).

</TabItem>
</Tabs>

## Create your connection

<Tabs
    defaultValue="db-creds"
    groupId= "redshift-connection"
    values={[
        {label: 'DB credendtials', value: 'db-creds'},
        {label: 'IAM credentials', value: 'iam-creds'},
    ]}>

<TabItem value="db-creds">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-amazon
    ```

    This will install the Amazon provider package, which makes the Amazon Redshift connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Redshift**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter the cluster **Endpoint**
    - **Database**: Enter the **Database name**
    - **User**: Enter the user
    - **Password**: Enter the password
    - **Port**: **Port**

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![aws-connection-db-creds](/img/examples/connection-aws-redshift.png)

</TabItem>

<TabItem value="iam-creds">


1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-microsoft-amazon
    ```

    This will install the Amazon provider package, which makes the Amazon Redshift connection type available in Airflow.

2. Copy the `aws` credentials file to the `include` directory of your Astro project. For example, it should be in the format:

    ```yaml

    # ~/.aws/credentials
    [<your-profile-name>]
    aws_access_key_id="your_aws_access_key_id"
    aws_secret_access_key="your_aws_secret_access_key"

    ```

3. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

4. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Redshift**.

5. Use the following `json` template and fill in the details retrieved in [Get connection details](#get-connection-details). Remember to use profile name from your `aws` credentials file. Copy the `json`. 

    ```json

    {
        "iam": true, 
        "cluster_identifier": "<your-cluster-identifier>", 
        "port": 5439, 
        "region": "<your-region>",
        "db_user": "<your-user>", 
        "database": "<your-database>", 
        "profile": "<your-profile-name>"
    }

    ```

6. Fill out the following connection fields:

    - **Connection Id**: Enter a name for the connection.
    - **Extra**: Enter the json from step #5.

7. Click **Test**. After the connection test succeeds, click **Save**.

    ![aws-connection-iam-creds](/img/examples/connection-aws-redshift-iam.png)

</TabItem>
</Tabs>

## How it works

Airflow uses the python package [Amazon Redshift Python Connector](https://docs.aws.amazon.com/redshift/latest/mgmt/python-configuration-options.html) to connect to Redshift through the [RedshiftSQLHook](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/redshift_sql/index.html).

## See also
- [Apache Airflow Amazon provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/redshift.html)
- [Redshift modules](https://registry.astronomer.io/modules?query=redshift) in Astronomer Registry.
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)