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
- An object storage. This tutorial uses [Amazon S3](https://aws.amazon.com/s3/). For local testing you can also connect to [Minio](https://min.io/).

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

## Step 3: Get the data 

In this tutorial we will predict the length of a possum's tail based on other attributes of the animal such as age, skull width, foot and head length. 

1. Download [the dataset](https://github.com/astronomer/learn-tutorials-data/blob/main/possum.csv) and save it in your `include` folder as `possum.csv`.
2. Add a picture of a possum in your `include` folder and name it `possum.jpeg`. If you don't have a possum picture ready you can use [this one from wikipedia](https://commons.wikimedia.org/wiki/File:Opossum_%2816701021016%29.jpg).

## Step 4: Create a feature engineering DAG

The Airflow pipeline presented in this tutorial consists of three DAGs. The first DAG will create the necessary object storage buckets, MLflow experiment and perform feature engineering on the possum dataset.

1. In your `dags` folder, create a file called `feature_eng.py`.

2. Copy the following code into the file. 

    <CodeBlock language="python">{feature_eng}</CodeBlock>

    This DAG will first complete two setup tasks:

    - The `create_buckets_if_not_exists` tasks creates the data bucket `DATA_BUCKET_NAME` which will store the features engineered from the possum dataset and the MLflow artifact bucket `MLFLOW_ARTIFACT_BUCKET_NAME` which will store the MLflow artifacts using the [S3CreateBucketOperator](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest/modules/S3CreateBucketOperator).
    - The `prepare_mlflow_experiment` [task group](task-groups.md) checks all existing experiments in your MLflow instance for an experiment with the name `EXPERIMENT_NAME`. The `check_if_experiment_exists` task uses the [@task.branch decorator](airflow-decorators.md#list-of-available-airflow-decorators) to decide if creating the experiment is needed or not. In both cases the `get_current_experiment_id` task retrieves the correct experiment ID for `EXPERIMENT_NAME`. The tasks in this task group establish a connection to your MLflow instance using the [MLflowClientHook](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/hooks/client.py).

    After the setup is complete data processing takes place:

    - The `extract_data` task retrieves the data from the local CSV file using the [aql.dataframe decorator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) from the Astro Python SDK.
    - The `build_features` task uses methods from [pandas](https://pandas.pydata.org/docs/) and [scikit-learn](https://scikit-learn.org/stable/) to one-hot encode categorical features and scale all features. The [mlflow](https://pypi.org/project/mlflow/) package is used to track these feature engineering steps in MLflow.

    Lastly, `save_data_to_s3` task saves the dataframe containing the engineered features to the `DATA_BUCKET_NAME` S3 bucket using the [aql.export_file operator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html) from the Astro Python SDK.

## Step 5: Create a model training DAG

The second DAG will train a linear regression model on the engineered features, keeping track of the model in MLflow. 

<CodeBlock language="python">{train}</CodeBlock>

## Step 6: Create your prediction DAG

<CodeBlock language="python">{predict}</CodeBlock>

## Step 7: Run your DAGs