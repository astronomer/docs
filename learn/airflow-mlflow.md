---
title: "Use MLflow with Apache Airflow"
sidebar_label: "MLflow"
description: "How to use MLflow with Airflow in three different ways."
id: airflow-mlflow
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

import CodeBlock from '@theme/CodeBlock';
import mlflow_tutorial_dag from '!!raw-loader!../code-samples/dags/airflow-mlflow/mlflow_tutorial_dag.py';

[MLflow](https://mlflow.org/) is a popular tool for tracking and managing machine learning models. It can be used together with Airflow for ML orchestration (MLOx), leveraging both tools for what they do best. In this tutorial, you’ll learn about three different ways you can use MLflow with Airflow.

:::info

If you're already familiar with MLflow and Airflow and want to get a use case up and running, clone the [quickstart repository](https://github.com/astronomer/use-case-mlflow) to automatically start up Airflow and local MLflow and MinIO instances. After you clone the repository, configure the local MLflow connection as shown in [Step 2](#step-2-configure-your-airflow-connection) of this tutorial, and run the three example DAGs.

:::

## Three ways to use MLflow with Airflow

The DAG in this tutorial shows three different ways Airflow can interact with MLflow:

- Use an MLflow operator from the [MLflow Airflow provider](https://github.com/astronomer/airflow-provider-mlflow). The MLflow provider contains several operators that abstract over common actions you might want to perform in MLflow, such as creating a deployment with the [CreateDeploymentOperator](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/operators/deployment.py) or running predictions from an existing model with the [ModelLoadAndPredictOperator](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/operators/pyfunc.py). 
- Use an MLflow hook from the MLflow Airflow provider. The MLflow provider contains several [Airflow hooks](what-is-a-hook.md) that allow you to connect to MLflow using credentials stored in an Airflow connection. You can use these hooks if you need to perform actions in MLflow for which no dedicated operator exists. You can also use these hooks to create your own [custom operators](airflow-importing-custom-hooks-operators.md).
- Use the MLflow Python package directly in a [@task decorated task](airflow-decorators.md). The MLflow Python package contains functionality like tracking metrics and artifacts with [`mlflow.sklearn.autolog`](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html). You can use this package to write custom Airflow tasks for ML-related actions like feature engineering.

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
- An [MLflow instance](https://www.mlflow.org/docs/latest/quickstart.html). This tutorial uses a local instance.
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

1. Run `astro dev start` in your Astro project to start up Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, go to **Admin** -> **Connections** and click **+**.

3. Create a new connection named `mlflow_default` and choose the `HTTP` connection type. Enter the following values to create a connection to a local MLflow instance:

    - **Connection ID**: `mlflow_default`
    - **Connection Type**: `HTTP`
    - **Host**: `http://host.docker.internal`
    - **Port**: `5000`

:::info 

If you are using a remote MLflow instance, enter your MLflow instance URL as the **Host** and your username and password as the **Login** and **Password** in the connection. If you are running your MLflow instance via Databricks, enter your Databricks URL as the **Host**, enter `token` as the **Login** and your [Databricks personal access token](https://docs.databricks.com/dev-tools/auth.html#personal-access-tokens-for-users) as the **Password**.
Please note that the **Test** button might return a 405 error message even if your credentials are correct. 

:::

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `mlflow_tutorial_dag.py`.

2. Copy the following code into the file. Make sure to provide the name of a bucket in your object storage that is connected to your MLflow instance to the `ARTIFACT_BUCKET` variable.

    <CodeBlock language="python">{mlflow_tutorial_dag}</CodeBlock>

    This DAG consists of three tasks, each showing a different way to use MLflow with Airflow.

    - The `create_experiment` task creates a new experiment in MLflow by using the [MLflowClientHook](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/hooks/client.py) in a TaskFlow API task. The MLflowClientHook is one of several [hooks](https://github.com/astronomer/airflow-provider-mlflow/tree/main/mlflow_provider/hooks) in the MLflow provider that contains abstractions over calls to the MLflow API. 
    - The `scale_features` task uses the [mlflow](https://pypi.org/project/mlflow/) package in a Python decorated task with [scikit-learn](https://pypi.org/project/scikit-learn/) to log information about the scaler to MLflow. This functionality is not included in any modules of the MLflow provider, so a custom Python function is the best way to implement this task.
    - The `create_registered_model` task uses the [CreateRegisteredModelOperator](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/operators/registry.py) to register a new model in your MLflow instance.

## Step 4: Run your DAG

1. In the Airflow UI run the `mlflow_tutorial_dag` DAG by clicking the play button.

    ![DAGs overview](/img/guides/airflow-mlflow_dag_graph_view.png)

2. Open the MLflow UI (if you are running locally at `localhost:5000`) to see the data recorded by each task in your DAG.

    The `create_experiment` task created the `Housing` experiments, where your `Scaler` run from the `scale_features` task was recorded.

    ![MLflow UI experiments](/img/guides/airflow-mlflow_experiments.png)

    The `create_registered_model` task created a registered model with two tags.

    ![MLflow UI models](/img/guides/airflow-mlflow_registered_models.png)

3. Open your object storage (if you are using a local MinIO instance at `localhost:9001`) to see your MLflow artifacts.

    ![MinIO experiment artifacts](/img/guides/airflow-mlflow_experiment_artifacts_in_minio.png)

## Conclusion

Congratulations! You used MLflow and Airflow together in three different ways. Learn more about other operators and hooks in the MLflow Airflow provider in the [official GitHub repository](https://github.com/astronomer/airflow-provider-mlflow).