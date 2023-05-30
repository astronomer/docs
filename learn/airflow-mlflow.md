---
title: "Use MLflow with Apache Airflow"
sidebar_label: "MLflow"
description: "How to produce to use the MLflow Airflow provider"
id: airflow-mlflow
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

import CodeBlock from '@theme/CodeBlock';
import feature_eng from '!!raw-loader!../code-samples/dags/airflow-mlflow/feature_eng.py';
import train from '!!raw-loader!../code-samples/dags/airflow-mlflow/train.py';
import predict from '!!raw-loader!../code-samples/dags/airflow-mlflow/predict.py';

MLflow is a commonly used tool for tracking and managing machine learning models. It can be used together with Airflow to orchestrate ML Ops leveraging both tools for what they do best. In this tutorial, you’ll learn how you can use the MLFlow provider in Airflow to manage model life cycles. There are many different use cases you can implement with MLFlow and Airflow, but in this tutorial we’ll focus on tracking feature engineering, model training and predictions.

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of MLflow. See [MLFlow Concepts](https://mlflow.org/docs/latest/concepts.html).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Quickstart

If you have a GitHub account, you can use the [quickstart repository](https://github.com/astronomer/learn-airflow-mlflow-tutorial) for this tutorial, which automatically starts up Airflow and initiates a local MLflow and Minio instance. Clone the quickstart repository, configure the local MLflow connection as shown in step X and then skip to step Y of this tutorial.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- An MLflow instance. This tutorial uses a local instance.
- A blob storage account. This tutorial uses a local Minio bucket.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-mlflow-tutorial && cd astro-mlflow-tutorial
    $ astro dev init
    ```

2. Add the following packages to your `packages.txt` file:

    ```text
    git
    gcc
    gcc python3-dev
    ```

3. Add the following packages to your `requirements.txt` file:

    ```text
    airflow-provider-mlflow==1.1.0
    apache-airflow-providers-amazon==8.0.0
    mlflow-skinny==2.3.2
    s3fs==2023.5.0
    ```

## Step 2: Configure your Airflow connections

To connect Airflow to your MLflow instance, you need to create a connection in Airflow. 

1. In the Airflow UI, go to **Admin** -> **Connections** and click **+**.

2. Create a new connection named `mlflow_default` and choose the `HTTP` connection type. Enter the following values to create a connection to a local MLflow instance:

    - **Connection ID**: `mlflow_default`.
    - **Connection Type**: `HTTP`.
    - **Host**: `http://host.docker.internal`
    - **Port**: `5000`

:::info 

If you are using a remote MLflow instance, you need to enter the host MLflow instance (`https://mlflow.myhost.com`) and provide your username to the **Login** and your password to the **Password** field. To run your MLflow instance via Databricks provide your Databricks URL to the **Host** field, `token` to the **Login** field and your [Databricks personal access token](https://docs.databricks.com/dev-tools/auth.html#personal-access-tokens-for-users) to the **Password** field.
Please note that the **Test** button might return a 405 error message even if your credentials are correct. 

:::

3. Create a connection to your blob storage. If you are using Minio or AWS S3 name the connection `aws_conn` and add the following credentials:

    - **Connection ID**: `aws_conn`.
    - **Connection Type**: Amazon Web Services.
    - **AWS Access Key ID**: Your [AWS Access Key ID](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html) or Minio login.
    - **AWS Secret Access Key**: Your AWS Secret Access Key or Minio password.


## Step 3: Create your feature engineering DAG

<CodeBlock language="python">{feature_eng}</CodeBlock>

## Step 4: Create your feature engineering DAG

<CodeBlock language="python">{train}</CodeBlock>

## Step 5: Create your prediction DAG

<CodeBlock language="python">{predict}</CodeBlock>

## Step 6: Run your DAGs