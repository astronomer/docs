---
title: "Use MLflow with Apache Airflow"
sidebar_label: "MLflow"
description: "How to produce to use the MLflow Airflow provider"
id: airflow-mlflow
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

import CodeBlock from '@theme/CodeBlock';
import mlflow_tutorial_dag from '!!raw-loader!../code-samples/dags/airflow-mlflow/mlflow_tutorial_dag.py';

MLflow is a commonly used tool for tracking and managing machine learning models. It can be used together with Airflow to orchestrate MLOps, leveraging both tools for what they do best. In this tutorial, you’ll learn about three different ways you can use MLflow with Airflow.

:::info

If you are already familiar with MLflow and Airflow and want to get a use case up and running check out this [quickstart repository](https://github.com/astronomer/learn-airflow-mlflow-tutorial) which automatically starts up Airflow and initiates a local MLflow and MinIO instance. Clone the quickstart repository, configure the local MLflow connection as shown in step 2 of this tutorial and run the three example DAGs.

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of MLflow. See [MLflow Concepts](https://mlflow.org/docs/latest/concepts.html).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- An MLflow instance. This tutorial uses a local instance.
- An object storage connected to your MLflow instance. This tutorial uses [MinIO](https://min.io/).

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
    mlflow-skinny==2.3.2
    ```

## Step 2: Configure your Airflow connection

To connect Airflow to your MLflow instance, you need to create a [connection in Airflow](connections.md). 

1. Run `astro dev start` in your Astro project to start up Airflow and navigate to the Airflow UI at `localhost:8080`.

2. In the Airflow UI, go to **Admin** -> **Connections** and click **+**.

3. Create a new connection named `mlflow_default` and choose the `HTTP` connection type. Enter the following values to create a connection to a local MLflow instance:

    - **Connection ID**: `mlflow_default`.
    - **Connection Type**: `HTTP`.
    - **Host**: `http://host.docker.internal`
    - **Port**: `5000`

:::info 

If you are using a remote MLflow instance, you need to enter the MLflow instance (`https://mlflow.myhost.com`) as a **Host** and provide your username to the **Login** and your password to the **Password** field. To run your MLflow instance via Databricks provide your Databricks URL to the **Host** field, enter the string `token` in the **Login** field and your [Databricks personal access token](https://docs.databricks.com/dev-tools/auth.html#personal-access-tokens-for-users) in the **Password** field.
Please note that the **Test** button might return a 405 error message even if your credentials are correct. 

:::

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `mlflow_tutorial_dag.py`.

2. Copy the following code into the file. Make sure to provide the name of a bucket in your object storage that is connected to your MLflow instance to the `ARTIFACT_BUCKET` variable.

    <CodeBlock language="python">{mlflow_tutorial_dag}</CodeBlock>

    This DAG consists of three tasks, each showing a different way to use MLflow with Airflow.

    - The `create_experiment` task creates a new experiment in MLflow by using the [MLflowClientHook](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/hooks/client.py) in a TaskFlow API task. The MLflowClientHook is one of several [hooks](https://github.com/astronomer/airflow-provider-mlflow/tree/main/mlflow_provider/hooks) in the MLflow provider that contains abstractions over calls to the MLflow API. 
    - The `scale_features` task shows a way to use MLflow and Airflow without the MLflow provider. In this task the [mlflow](https://pypi.org/project/mlflow/) package is used directly with [scikit-learn](https://pypi.org/project/scikit-learn/) to log information about the scaler to MLflow.
    - The `create_registered_model` task shows how to use the [CreateRegisteredModelOperator](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/operators/registry.py) to register a new model in your MLflow instance.

## Step 4: Run your DAG

1. Manually run the `mlflow_tutorial_dag` DAG by clicking the play button.

    ![DAGs overview](/img/guides/mlflow_tutorial_dag_graph_view.png)

2. Open the MLflow UI (if you are running locally at `localhost:5000`) to see the data recorded by eat task in your DAG.

    The `create_experiment` task created the `Housing` experiments, where your `Scaler` run from the `scale_features` task was recorded.

    ![MLflow UI experiments](/img/guides/mlflow_experiments.png)

    The `create_registered_model` task created a registered model with two tags.

    ![MLflow UI models](/img/guides/mlflow_registered_models.png)

3. Open your object storage (if you are using a local MinIO instance at `localhost:9000`) to see your MLflow artifacts.

    ![MinIO experiment artifacts](/img/guides/mlflow_experiment_artifacts_in_minio.png)

## Conclusion

Congratulations! You used MLflow and Airflow together in three different ways. Learn more about other operators and hooks in the MLflow Airflow provider in the [documentation](https://github.com/astronomer/airflow-provider-mlflow).