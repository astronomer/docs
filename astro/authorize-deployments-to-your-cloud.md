---
sidebar_label: 'Authorize Deployments to cloud resources'
title: 'Authorize an Astro Deployment to cloud resources using workload identity'
id: authorize-deployments-to-your-cloud
description: Give Astro Deployments access to your cloud resources using a Kubernetes workload identity
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

When you create an Airflow connection from a Deployment to access cloud resources, Airflow uses your connection details to access those services. You can add credentials to your Airflow connections to authenticate, but it can be risky to add secrets like passwords or API keys to your Airflow environment. 

To avoid adding secrets to your Airflow connection, you can directly authorize your Astro Deployment to access AWS or GCP cloud services using workload identity. Astronomer recommends using a workload identity in most cases to improve security and avoid managing credentials across your Deployments. If you have less strict security requirements, you can still use any of the methods described in [Airflow connection guides](https://docs.astronomer.io/learn/connections) to manage your connection authorization. 

This guide explains how to authorize your Deployment to a cloud using workload identity. For each Deployment, you will:

- Authorize your Deployment to your cloud services.
- Create an Airflow connection to access your cloud services.

## Prerequisites

The Astro cluster running your Deployment must be connected to your cloud's network. See [Connect clusters](https://docs.astronomer.io/astro/category/connect-to-external-resources).

## What is workload identity?

A workload identity is a Kubernetes service account that provides an identity to your Deployment. The Deployment can use this identity to authenticate to a cloud's API server, and the cloud can use this identity to authorize the Deployment to access different resources.

## Setup 

<Tabs
    defaultValue="aws"
    groupId="cloud-provider"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
    ]}>
<TabItem value="aws">

#### Step 1: Authorize the Deployment in your cloud

To grant a Deployment access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles to authorize your Deployment's workload identity. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource, such as Amazon S3 buckets, Redshift instances, and secrets backends.

To authorize your Deployment, create an IAM role that is assumed by the Deployment's workload identity:

1. In the Cloud UI, select your Deployment and then click **Details**. Copy the Deployment's **Workload Identity**.
2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.
4. Click **Roles** and in the **Role name** column, select the role you created in Step 2.
5. Click **Trust relationships**.
6. Click **Edit trust policy** and paste the workload identity you copied from Step 1 in the trust policy. Your policy should look like the following:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "<workload-identity-role>"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    ```

7. Click **Update policy**.

Repeat these steps for each Astro Deployment that needs to access your AWS resources.

#### Step 2: Create an Airflow connection

Now that your Deployment is authorized, you can connect it to your cloud using an Airflow connection.

1. In the Airflow UI for your Deployment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Web Services**. 

2. Complete the following fields:
    - **Connection Id**: Enter a name for the connection.
    - **Extra**: 

        ```json
        {
        "role_arn": "<your-role-arn>",
        "region_name": "<your-region>"
        }
        ```

3. Click **Save**. 
    
    If you don't see **Amazon Web Services** as a connection type, ensure you have installed its provider package in your Astro project's `requirements.txt` file. See **Use Provider** in the [Astronomer Registry](https://registry.astronomer.io/providers/Amazon/versions/latest) for the latest package.


</TabItem>

<TabItem value="gcp">

#### Step 1: Authorize the Deployment in your cloud

To grant a Deployment access to a service that is running in a GCP account not managed by Astronomer, use your Deployment's workload identity. Workload identity is basically a service account in GCP that's used to manage the level of access for a specific user, object, or group of users to a resource, such as Google BigQuery, GCS bucket, etc.

To authorize your Deployment, grant the required access to your Deployment's workload identity:

1. In the Cloud UI, select your Deployment, then click **Details**. Copy the Deployment's **Workload Identity**.

2. Grant your Deployment's workload identity an IAM role that has access to your external data service. To do this with the Google Cloud CLI, run:

    ```bash
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:<workload-identity> --role=roles/viewer
    ```

    To grant your workload identity an IAM role using the Google Cloud console, see [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console#grant_an_iam_role).

Repeat these steps for each Deployment that needs to access your GCP resources.

#### Step 2: Create an Airflow connection

Now that your Deployment is authorized, you can connect it to your cloud using an Airflow connection.

1. In the Airflow UI for your Deployment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Google Cloud**. 

2. Fill out the following fields:

    - **Connection Id**: Enter a name for the connection.
    - **Project Id**: Enter the ID of your Google Cloud Project where your services are running.

3. Click **Save**. 
    
    If you don't see **Google Cloud** as a connection type, ensure you have installed its provider package in your Astro project's `requirements.txt` file. See **Use Provider** in the [Astronomer Registry](https://registry.astronomer.io/providers/Google/versions/latest) for the latest package.
    
</TabItem>
</Tabs>

## See also
- [Manage Airflow connections and variables](manage-connections-variables.md)
- [Deploy code to Astro](deploy-code.md)