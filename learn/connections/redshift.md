---
title: "Create an Amazon Redshift Connection in Airflow"
id: redshift
sidebar_label: Connection 
description: Learn how to create an Amazon Redshift connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/redshift.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[Amazon Redshift](https://aws.amazon.com/redshift/) is a data warehouse product from AWS. Integrating Redshift with Airflow allows you to automate, schedule and monitor a variety of tasks. These tasks include creating, deleting, and resuming a cluster, ingesting or exporting data to and from Redshift, as well as running SQL queries against Redshift. 

This document covers two different methods to connect Airflow to Amazon Redshift:

- Using database (DB) user credentials
- Using IAM credentials
- Using IAM role

:::tip

If you're an Astro user, Astronomer recommends using workload identity to authorize to your Deployments to Redshift. This eliminates the need to specify secrets in your Airflow connections or copying credentials file to your Airflow project. See [Authorize Deployments to your cloud](https://docs.astronomer.io/astro/authorize-deployments-to-your-cloud).

:::

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- Permissions to access to your Redshift cluster. See [Using IAM authentication](https://docs.aws.amazon.com/redshift/latest/mgmt/generating-user-credentials.html) and [Authorizing Amazon Redshift to access other AWS services](https://docs.aws.amazon.com/redshift/latest/mgmt/authorizing-redshift-service.html).

## Get connection details

<Tabs
    defaultValue="db-creds"
    groupId= "redshift-connection"
    values={[
        {label: 'DB user credentials', value: 'db-creds'},
        {label: 'IAM credentials', value: 'iam-creds'},
        {label: 'IAM role (Recommended)', value: 'iam-role'},
    ]}>

<TabItem value="db-creds">

DB user credentials can be used to establish a connection to an Amazon Redshift cluster. While straightforward to use, this approach lacks the strong security and user access controls provided by identity and access management (IAM). Connecting this way requires the following information:

- Cluster identifier
- Database name
- Port
- User
- Password

Complete the following steps to retrieve these values:

1. In your AWS console, select the region that contains your Redshift cluster, open the Redshift cluster dashboard, then open your cluster. 
   
2. From the **General information** section, copy the **Cluster identifier** and **Endpoint**.
   
3. Open the **Properties** tab and copy the **Database name** and **Port**.
   
4. [Create a Redshift user](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html) and [grant a role](https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html) so that Airflow can access Redshift through the user. Copy the username and password.

</TabItem>

<TabItem value="iam-creds">

You can use IAM credentials to connect Airflow to Redshift. This approach lets you use IAM credentials and limits Airflow's permissions. The limitation of this method is that you must include an AWS credentials file in your Airflow project.

Following information is required:

- Cluster identifier
- Database name
- Port
- Region
- IAM user
- AWS credentials file

Complete the following steps to retrieve these values:

1. In your AWS console, select the region that contains your Redshift cluster, open the Redshift cluster dashboard, then open your cluster. 
   
2. Open the **General information** tab, then copy the **Cluster identifier** and **Endpoint**.

3. Open the **Properties** tab and copy the **Database name** and **Port**.

4. Open your IAM dashboard, go to **Users** and select your user. Then, go to **Permissions** and follow the [AWS documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-access-control-identity-based.html) to ensure that the IAM user is authorized to connect to Redshift and perform SQL operations.

5. [Generate a new access key ID and secret access key](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).

</TabItem>

<TabItem value="iam-role">

You can use AWS's [Assume Role](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) method to automatically generate temporary credentials to connect to Redshift. This is useful to grant temporary access to limited-privilege IAM users or roles without storing any credentials on disk. The following information is required to create the connection:

- Cluster identifier
- Database name
- Port
- Region
- IAM role ARN

Complete the following steps to retrieve these values:

1. In your AWS console, select the region that contains your Redshift cluster, open the Redshift cluster dashboard, then open your cluster. 

2. Open the **General information** tab, then copy the **Cluster identifier** and **Endpoint**.

3. Open the **Properties** tab and copy the **Database name** and **Port**.

4. Open your IAM dashboard, and [follow the AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions_create-policies.html) to create an IAM role and attach an IAM Policy to access the required services, for example AWS Redshift. 

5. Edit the trust relationship of the role created in Step 4 to add a trust policy that allows the IAM role to assume your new role.

    ```json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<your-aws-account>:role/<your-role-name>"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    ```

6. Copy the **ARN** of the role.


</TabItem>

</Tabs>

## Create your connection

<Tabs
    defaultValue="db-creds"
    groupId= "redshift-connection"
    values={[
        {label: 'DB credentials', value: 'db-creds'},
        {label: 'IAM credentials', value: 'iam-creds'},
        {label: 'IAM role (Recommended)', value: 'iam-role'},
    ]}>

<TabItem value="db-creds">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-amazon
    ```

    This will install the Amazon provider package, which makes the Amazon Redshift connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Redshift**.

4. Fill out the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter the cluster **Endpoint**.
    - **Database**: Enter the **Database name**.
    - **User**: Enter the DB user username.
    - **Password**: Enter the DB user password.
    - **Port**: Enter the **Port**.

5. Click **Test**. After the connection test succeeds, click **Save**.

    ![aws-connection-db-creds](/img/examples/connection-aws-redshift.png)

</TabItem>

<TabItem value="iam-creds">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-amazon
    ```

    This will install the Amazon provider package, which makes the Amazon Redshift connection type available in Airflow.

2. Copy the `aws` credentials file to the `include` directory of your Astro project. It should have the following format:

    ```yaml
    # ~/.aws/credentials
    [<your-profile-name>]
    aws_access_key_id="your_aws_access_key_id"
    aws_secret_access_key="your_aws_secret_access_key"
    ```

3. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

4. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Redshift**.

5. Enter a name for the connection in the **Connection Id** field.

6. Copy the following JSON template into the **Extra** field, then replace the placeholder values with the information you retrieved in [Get connection details](#get-connection-details). 

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

7. Click **Test**. After the connection test succeeds, click **Save**.

    ![aws-connection-iam-creds](/img/examples/connection-aws-redshift-iam.png)

</TabItem>

<TabItem value="iam-role">

1. Open your Astro project and add the following line to your `requirements.txt` file:

    ```
    apache-airflow-providers-amazon
    ```

    This will install the Amazon provider package, which makes the Amazon Redshift connection type available in Airflow.

2. Run `astro dev restart` to restart your local Airflow environment and apply your changes in `requirements.txt`.

3. In the Airflow UI for your local Airflow environment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Redshift**.

4. Complete the following connection fields using the information you retrieved from [Get connection details](#get-connection-details):

    - **Connection Id**: Enter a name for the connection.
    - **Host**: Enter the cluster **Endpoint**.
    - **Database**: Enter the **Database name**.
    - **Port**: Enter the **Port**.
    - **Extra**: 
        ```json

            {
            "role_arn": "<your-role-arn>",
            "region_name": "<your-region>"
            }

        ```

5. Click **Test**. After the connection test succeeds, click **Save**.

</TabItem>

</Tabs>

## How it works

Airflow uses the [Amazon Redshift Python Connector](https://docs.aws.amazon.com/redshift/latest/mgmt/python-configuration-options.html) to connect to Redshift through the [RedshiftSQLHook](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/redshift_sql/index.html).

## See also

- [Apache Airflow Amazon provider package documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/redshift.html)
- [Redshift modules](https://registry.astronomer.io/modules?query=redshift) in the Astronomer Registry
- [Import and export Airflow connections using Astro CLI](https://docs.astronomer.io/astro/import-export-connections-variables#using-the-astro-cli-local-environments-only)