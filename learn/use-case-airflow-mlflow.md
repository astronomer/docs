---
title: "Analyze possum data with MLflow and Airflow"
description: "Use Airflow and MLflow to conduct and track a regression model."
id: use-case-airflow-mlflow
sidebar_label: "Regression with Airflow + MLflow"
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

[MLflow](https://mlflow.org/)  is a popular tool for tracking and managing machine learning models. It can be used together with Airflow for ML orchestration (MLOx), leveraging both tools for what they do best. 

This use case shows how to use MLflow with Airflow to engineer machine learning features, train a [sklearn Ridge regression model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html) and create predictions based on the trained model.

:::info

For more detailed instructions on using MLflow with Airflow, see the [MLflow tutorial](airflow-mlflow.md).

:::

![A line plot showing the output of the pipeline described in this use case: the actual and predicted lengths of possum tails plotted for each animal. There is a small cute possum next to the graph.](/img/examples/use-case-airflow-mlflow_possum_tails_linegraph.png)

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of MLflow. See [MLFlow Concepts](https://mlflow.org/docs/latest/concepts.html).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).

## Clone the project

Clone the example project from this [Astronomer GitHub](https://github.com/astronomer/use-case-mlflow). Make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory. The repository is configured to spin up and use a local MLflow and MinIO instance.

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, navigate to your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 6 Docker containers on your machine to run it:

- The Airflow webserver, which runs the Airflow UI and can be accessed at `https://localhost:8080/`.
- The Airflow scheduler.
- The Airflow triggerer.
- The Airflow metadata database, a Postgres database which runs on port `5432`.
- A local MinIO instance, which can be accessed at `https://localhost:9000/`.
- A local MLflow instance, which can be accessed at `https://localhost:5000/`.

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


    This DAG will first complete two setup tasks:

    - The `create_buckets_if_not_exists` tasks creates the data bucket `DATA_BUCKET_NAME` which will store the features engineered from the possum dataset and the MLflow artifact bucket `MLFLOW_ARTIFACT_BUCKET_NAME` which will store the MLflow artifacts using the [S3CreateBucketOperator](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest/modules/S3CreateBucketOperator). Additionally, the task also create a bucket to use as a [custom XCom backend](custom-xcom-backends-tutorial.md) if you have one defined.
    - The `prepare_mlflow_experiment` [task group](task-groups.md) checks all existing experiments in your MLflow instance for an experiment with the name `EXPERIMENT_NAME`. The `check_if_experiment_exists` task uses the [@task.branch decorator](airflow-decorators.md#list-of-available-airflow-decorators) to decide if creating the experiment is needed or not. In both cases the `get_current_experiment_id` task retrieves the correct experiment ID for `EXPERIMENT_NAME`. The tasks in this task group establish a connection to your MLflow instance using the [MLflowClientHook](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/hooks/client.py).

    After the setup is complete data processing takes place:

    - The `extract_data` task retrieves the data from the local CSV file using the [aql.dataframe decorator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) from the Astro Python SDK.
    - The `build_features` task uses methods from [pandas](https://pandas.pydata.org/docs/) and [scikit-learn](https://scikit-learn.org/stable/) to one-hot encode categorical features and scale all features. The [mlflow](https://pypi.org/project/mlflow/) package is used to track these feature engineering steps in MLflow.

    Lastly, `save_data_to_s3` task saves the dataframe containing the engineered features to the `DATA_BUCKET_NAME` S3 bucket using the [aql.export_file operator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html) from the Astro Python SDK.

## Step 5: Create a model training DAG

The second DAG will train a linear regression model on the engineered features, keeping track of the model in MLflow. This DAG runs as soon as the `s3://data_possum.csv` [Dataset](airflow-datasets.md) is updated.

1. In your `dags` folder, create a file called `train.py`.

2. Copy the following code into the file. 


    This DAG will train a [RidgeCV model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html#sklearn.linear_model.RidgeCV) on the features engineered in the previous DAG.

    - The `fetch_feature_df` task pulls the feature dataframe from [XCom](airflow-passing-data-between-tasks.md#what-is-xcom). 
    - The `fetch_experiment_id` task retrieves the experiment ID for the `EXPERIMENT_NAME` experiment from MLflow.
    - In the `train_model` task the RidgeCV model trains on the feature dataframe. Note that you can provide additional hyperparameters to the model by passing them to the `hyper_parameters` keyword argument of the `train_model` task. The model is tracked in MLflow using the [mlflow.sklearn.autolog](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html#mlflow.sklearn.autolog) method.

    After the model has been trained the `register_model` task group takes care of model registration and versioning. 
    
    - The `check_if_model_already_registered` task uses the @task.branch decorator to determine if a model of that name already exists in your MLflow registry.
    - The `create_registered_model` task [registers the model](https://mlflow.org/docs/latest/registry.html?highlight=register%20model) within MLflow if it does not exist yet.
    - The `create_model_version` task [creates a new version](https://mlflow.org/docs/latest/registry.html?highlight=register%20model#creating-a-new-version-of-a-registered-model) of the model in MLflow using the `CreateModelVersionOperator` of the MLflow Airflow provider. 
    - Finally, the `transition_model` task will put the latest model version into the `Staging` stage. This is done using the `TransitionModelVersionStageOperator` of the MLflow Airflow provider.

## Step 6: Create your prediction DAG

The final step of this pipeline is to create predictions based on the trained model and plot predictions and target values next to each other to visually evaluate how well the RidgeCV model can be fitted to the data at hand. This DAG runs as soon as the last task in the previous DAG updates the `model_trained` [Dataset](airflow-datasets.md).

1. In your `dags` folder, create a file called `predict.py`.

2. Copy the following code into the file. 


    - In a first step, the feature dataframe, target column and model ID are retrieved from XCom of the upstream DAGs.
    - Next, the `add_line_to_file` task adds the packages [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and pandas to the MLflow model artifact `requirements.txt` file in the `MLFLOW_ARTIFACT_BUCKET`. This is necessary because the model prediction happens in a virtual environment.
    - The `run_prediction` task uses the ModelLoadAndPredictOperator of the MLFlow Airflow provider to create predictions using the latest model run on the full feature dataframe.
    - The `plot_predictions` task uses [matplotlib](https://matplotlib.org/) to create a line graph visually comparing the predictions against the target values. And saves the resulting image to the `include` folder.
    - Lastly, the predictions are also saved as a CSV file in the `data` bucket.

## Step 7: Run your DAGs

1. Run `astro dev start` in your Astro project to start up Airflow.

2. Navigate to the Airflow UI at `localhost:8080` and unpause all three DAGs by clicking the toggle to the left of the DAG name.

3. Manually run the `feature_eng` DAG by clicking the play button. All your DAGs will run in the correct order based on [data driven scheduling](airflow-datasets.md).



4. Navigate to the **Grid** view of each of the three DAGs and click on the **Graph** button to see a full DAG graph next in the Grid view.


5. Open the MLflow UI (if you are running locally at `localhost:5000`) to see the data collected on your experiments and models.


6. Finally, open the `possum_tails.png` in `include/plots`.


## Conclusion

Congratulations! You ran a ML flow pipeline tracking model parameters and versions in MLflow using the MLflow Airflow provider. You can now use this pipeline as a template for your own MLflow projects.


