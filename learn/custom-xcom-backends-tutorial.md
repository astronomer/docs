---
title: 'Set up a custom XComs backend'
sidebar_label: 'Custom XComs backend'
id: cloud-ide-tutorial
description: 'Use this tutorial to learn how to set up a custom XComs backend in AWS, GCP and Azure.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow offers the possibility to use [XComs](airflow-passing-data-between-tasks.md) to pass information between your tasks, which is stored in the XCom backend. By default Airflow uses the [metadata database](airflow-database.md) as an XComs backend, which works well for local development purposes but can become limiting in a production environment. If your storage needs for XComs exceed the size of the Airflow metadatabase or you want to add custom functionality like retention policies, store data that is not JSON serializeable etc you can configure a custom XComs backend. To learn more about when and when not to use a custom XComs backend see the [Best practices](#best-practices) section and the end of this tutorial. 

After you complete this tutorial, you'll be able to:

- 

:::caution

While a custom XComs backend allows you to store virtually unlimited amounts of data as XComs, keep in mind that Airflow was not designed be a data processing framework and you might run into performance issue if you try to pass large amounts of data via XComs. Astronomer recommends to use an external processing framework such as [Apache Spark](https://spark.apache.org/) to handle heavy data processing and orchestrate the process with Airflow using the [Apache Spark provider](https://registry.astronomer.io/providers/spark).

:::

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- XComs basics. See the [Airflow documentation on XComs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html).
- Passing data between tasks. See [Passing data between Airflow tasks](airflow-passing-data-between-tasks.md).
- The TaskFlow API. See [the TaskFlow API in Airflow 2.0](https://www.astronomer.io/events/webinars/taskflow-api-airflow-2.0/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).




<Tabs
    defaultValue="aws"
    groupId= "github-actions-image-only-deploys"
    values={[
        {label: 'AWS S3', value: 'aws'},
        {label: 'GCP Cloud Storage', value: 'gcp'},
        {label: 'Azure Blob Storage', value: 'azure'},
        {label: 'Local', value: 'local'}
    ]}>
<TabItem value="aws">

## Step 1: Set up your XComs backend 

To use an S3 bucket as your custom XCom backend follow these steps:

1. Log into your AWS account and [create a new S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html). In the creation settings, make sure to enable Bucket Versioning and that public access is blocked.

2. [Create a new IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) for Airflow to access your bucket. You can use the JSON configuration below (replace `<YOUR BUCKET NAME>` with the name of your S3 bucket) or use AWS' graphical user interface to replicate what you see in the screenhot.

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
                    "arn:aws:s3:::<YOUR BUCKET NAME>/*",
                    "arn:aws:s3:::<YOUR BUCKET NAME>"
                ]
            }
        ]
    }
    ```

    [AWS IAM policy for the XCom backend](/img/guides/xcom_backend_aws_policy.png)

3. Save your policy under the name `AirflowXComBackendAWSS3`. 

4. [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) called `airflow-xcoms` with the AWS credential type `Access key - Programmatic access`. Attach the `AirflowXComBackendAWSS3` policy to this user as shown in the screenshot below. Make sure to save the Access key ID and the Secret access key.

    [AWS IAM user for the XCom backend](/img/guides/xcom_backend_aws_user.png)

## Step 2: Create a connection


</TabItem>

<TabItem value="aws">



</TabItem>

<TabItem value="aws">



</TabItem>

<TabItem value="aws">



</TabItem>


</Tabs>







## Step X: Create an Astro project

Set up Airflow by creating a new Astro project:

```sh
$ mkdir astro-extra-link-tutorial && cd astro-extra-link-tutorial
$ astro dev init
```


## Best practices

Common reasons to use a custom XComs backend are:

- Needing more storage space for XComs than the metadata database can offer.
- Running a production environment that where custom retention, deletion and backup policies for XComs are desired. With a custom XComs backend you do not need to worry about periodically cleaning up the metadata database.
- The need for custom serialization and deserialization methods. By default Airflow uses JSON serialization which puts limits on the type of data that you can pass via XComs (pickling is available by setting `AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True` but has [known security implications](https://docs.python.org/3/library/pickle.html)).
- Having a custom setup where access to XComs is needed without accessing the metadata database. 
