---
sidebar_label: 'Authorize using workload identity'
title: 'Authorize your Deployment using workload identity'
id: authorize-using-workload-identity
description: Connect Astro Deployments to your existing Cloud resources using Kubernetes workload identity
toc_min_heading_level: 2
toc_max_heading_level: 2
---

Authorization is the process of verifying a user or service's permissions before allowing them access to organizational applications and resources. 

Astro Deployments can be authorized to access external resources running in your cloud to avoid storing your credentials on disk or in an Airflow connection. Astronomer recommends using this method for all your Deployments because this method is the most secure.

## What is workload identity?

A Kubernetes service account provides an identity to the processes running in a Pod. The process running inside a Pod can use this identity of its associated service account to authenticate cluster's API server. This identity can be used to authorize your Deployment. Astro refers to this service account as workload identity. 

Workload identity is enabled by default on all your Astro Deployments running on AWS and GCP. You can authorize your Deployment's workload identity to access services running in your cloud. After this is enabled for a Deployment, you don't need to store secrets in your Airflow connection to access your services.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<!-- <Tabs
    defaultValue="aws"
    groupId="cloud-provider"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
    ]}>
<TabItem value="aws"> -->

## AWS 

To grant an Astro Deployment access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles along with your Deployment's workload identity. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource. This includes an Amazon S3 bucket, Redshift instance, or secrets backend, etc. 

To create an IAM role that is assumed by the workload identity of your Deployment, follow the below steps:

1. In the Cloud UI, select your Deployment and then click **Details**. Copy the `arn` given under **Workload Identity**.
2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.
4. Click **Roles** and in the **Role name** column, select the role you created in step 2.
5. Click the **Trust relationships** tab.
6. Click **Edit trust policy** and paste the `arn` you copied from Step 1 in the trust policy as your `<workload-identity-role>`.

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

    Refer to the tab Role ARN in  to create an Airflow connection using this `arn`.

7. Click **Update policy**.

These steps need to be repeated for each Astro Deployment that needs to access your AWS resources running in non-Astronomer managed account. 

### Use workload identity in Airflow connection

To use this role to access your external services or resources, you need to specify the role in your Airflow connection. 

1. In the Airflow UI for your Deployment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Amazon Web Services**. 

2. Fill out the following fields:
    - **Connection Id**: Enter a name for the connection.
    - **Extra**: 

        ```json
        {
        "role_arn": "<your-role-arn>",
        "region_name": "<your-region>"
        }
        ```
3. Click **Save**. 
    
    If you don't see **Amazon Web Services** as a connection type, ensure you have installed its package in your `requirements.txt`. See **Use Provider** in [Astronomer Registry](https://registry.astronomer.io/providers/Amazon/versions/latest) for the latest package.


<!-- </TabItem>

<TabItem value="gcp">
</TabItem>

</Tabs> -->

## GCP

To allow data pipelines running on GCP to access Google Cloud services in a secure and manageable way, Google recommends using [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity). All Astro clusters on GCP have Workload Identity enabled by default. Each Astro Deployment is associated with a Google service account that's created by Astronomer and is bound to an identity from your Google Cloud project's fixed workload identity pool.

To grant a Deployment on Astro access to external data services on GCP, such as BigQuery:

1. In the Cloud UI, select your Deployment, then click **Details**. Copy the service account shown under **Workload Identity**.

2. Grant the Google service account for your Astro Deployment an IAM role that has access to your external data service. With the Google Cloud CLI, run:

    ```bash
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:<your-astro-service-account> --role=roles/viewer
    ```

    For instructions on how to grant your service account an IAM role in the Google Cloud console, see [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console#grant_an_iam_role).


These steps need to be repeated for each Astro Deployment that needs to access your GCP resources running in non-Astronomer managed account. 


### Use workload identity in Airflow connection

To access your external services or resources in your non-Astronomer managed GCP account, you need to create an Airflow connection:

1. In the Airflow UI for your Deployment, go to **Admin** > **Connections**. Click **+** to add a new connection, then select the connection type as **Google Cloud**. 

2. Fill out the following fields:

    - **Connection Id**: Enter a name for the connection.
    - **Project Id**: Enter the ID of your Google Cloud Project where your services are running.

3. Click **Save**. 
    
    If you don't see **Google Cloud** as a connection type, ensure you have installed its package in your `requirements.txt`. See **Use Provider** in [Astronomer Registry](https://registry.astronomer.io/providers/Google/versions/latest) for the latest package.
