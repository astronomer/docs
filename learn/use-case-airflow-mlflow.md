---
title: "Predict possum tail length using linear regression with MLflow and Airflow"
description: "Use Airflow and MLflow to conduct and track a regression model."
id: use-case-airflow-mlflow
sidebar_label: "Regression with Airflow + MLflow"
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

[MLflow](https://mlflow.org/) is a popular tool for tracking and managing machine learning models. It can be used together with Airflow for ML orchestration (MLOx), leveraging both tools for what they do best.

This use case shows how to use MLflow with Airflow to engineer machine learning features, train a [scikit-learn Ridge linear regression model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html), and create predictions based on the trained model.

:::info

For more detailed instructions on using MLflow with Airflow, see the [MLflow tutorial](airflow-mlflow.md).

:::

![A line plot showing the output of the pipeline described in this use case: the actual and predicted lengths of possum tails plotted for each animal. There is a small cute possum next to the graph.](/img/examples/use-case-airflow-mlflow_possum_tails_linegraph.png)

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).

## Clone the project

Clone the example project from this [Astronomer GitHub](https://github.com/astronomer/use-case-mlflow). Make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory. The repository is configured to spin up and use local MLflow and MinIO instances without you needing to define any extra connections or have access to external tools.

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, navigate to your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 6 Docker containers on your machine to run it:

- The Airflow webserver, which runs the Airflow UI and can be accessed at `https://localhost:8080/`.
- The Airflow scheduler, which is responsible for monitoring and triggering tasks.
- The Airflow triggerer, an Airflow component used to run deferrable operators (not used in this use case).
- The Airflow metadata database, a Postgres database which runs on port `5432`.
- A local MinIO instance, which can be accessed at `https://localhost:9000/`.
- A local MLflow instance, which can be accessed at `https://localhost:5000/`.

## Project contents

### Data source

This example uses the [Possum Regression dataset](https://www.kaggle.com/datasets/abrambeyer/openintro-possum) from Kaggle. It contains measurements of different attributes of 104 possums, such as total length, skull width, or age. This data was originally published by Lindenmayer et al. (1995) in the Australian Journal of Zoology and is commonly used to teach linear regression.

### Project overview

This project consists of three DAGs, which depend on each other using [Airflow datasets](airflow-datasets.md).

![Datasets view of the use case project showing the DAG feature_eng updating the datasets astro+s://data/possum.csv and s3://data_possum.csv. The train DAG is scheduled to run as soon as the s3://data_possum.csv is updated and updates the model_trained dataset. The predict DAG is scheduled to run on updates to the model_trained dataset and updates the astro+s3://data/possum_tail_length.csv](/img/examples/use-case-airflow-mlflow_datasets_view.png)

The [`feature_eng`](https://github.com/astronomer/use-case-mlflow/blob/main/dags/feature_eng.py) DAG prepares the MLflow experiment and builds prediction features from the possum data.

![Graph view of the feature_eng DAG showing a task creating the necessary MinIO buckets, a task group that prepares the MLflow experiment if it does not yet exist and data extraction and feature building tasks.](/img/examples/use-case-airflow-mlflow_feature_eng_dag_graph.png)

The [`train`](https://github.com/astronomer/use-case-mlflow/blob/main/dags/train.py) DAG trains a RidgeCV model on the features engineered in the previous DAG and then registers the model with MLflow using operators from the [MLflow Airflow provider](https://github.com/astronomer/airflow-provider-mlflow).

![Graph view of the train DAG showing tasks fetching data and experiment information and training the model. Afterwards a task group contains tasks to register the model with MLflow, create a model version and transition the model version.](/img/examples/use-case-airflow-mlflow_train_dag_graph.png)

The [`predict`](https://github.com/astronomer/use-case-mlflow/blob/main/dags/predict.py) DAG uses the trained model from the previous DAG to create predictions and plots them against the target values. 

![Graph view of the predict DAG showing the model and features being fetched. Afterwards the ModelLoadAndPredictOperator is used to run predictions with are plotted and saved as a file.](/img/examples/use-case-airflow-mlflow_predict_dag_graph.png)

Note that the model is trained on the whole dataset and predictions are made on the same data. In a real world scenario you'd want to split the data into a training, validation, and test set.

### Project code

This use case shows many Airflow features and ways to interact with MLflow. The following sections will highlight a couple of relevant code snippets in each DAG and explain them in more detail.

#### Feature engineering DAG

The feature engineering DAG starts with a task that creates the necessary object storage buckets in the resource provided as `AWS_CONN_ID` using the [S3CreateBucketOperator](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest/modules/S3CreateBucketOperator). By default, the project uses a local MinIO instance, which is created when starting the Astro project. If you want to use remote object storage, you can change the `AWS_CONN_ID` in the `.env` file and provide your AWS credentials credentials.
The operator is [dynamically mapped](dynamic-tasks.md) over a list of bucket names to create all buckets in parallel.

```python
create_buckets_if_not_exists = S3CreateBucketOperator.partial(
    task_id="create_buckets_if_not_exists",
    aws_conn_id=AWS_CONN_ID,
).expand(bucket_name=[DATA_BUCKET_NAME, MLFLOW_ARTIFACT_BUCKET, XCOM_BUCKET])
```

The `prepare_mlflow_experiment` [task group](task-groups.md) contains a pattern that lists all existing experiments in the MLflow instance connected via the `MLFLOW_CONN_ID`. It also creates a new experiment with a specified name if it does not exist yet using the [@task.branch decorator](airflow-branch-operator.md). The [MLflowClientHook](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/hooks/client.py) contains the `run` method that creates the new experiment by making a call to the MLflow API.

```python
@task
def create_experiment(experiment_name, artifact_bucket):
    """Create a new MLFlow experiment with a specified name.
    Save artifacts to the specified S3 bucket."""

    mlflow_hook = MLflowClientHook(mlflow_conn_id=MLFLOW_CONN_ID)
    new_experiment_information = mlflow_hook.run(
        endpoint="api/2.0/mlflow/experiments/create",
        request_params={
            "name": experiment_name,
            "artifact_location": f"s3://{artifact_bucket}/",
        },
    ).json()

    return new_experiment_information
```

Feature engineering in the `build_features` task uses [Pandas for one hot encoding](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html) of categorical features and [scikit-learn to scale](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) numeric features.
The [mlflow](https://pypi.org/project/mlflow/) package is used to [track](https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=start_run#mlflow.start_run) the scaler run in MLflow.
The task is defined using the [`@aql.dataframe`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator from the [Astro Python SDK](astro-python-sdk.md).

```python
@aql.dataframe()
def build_features(
    raw_df: DataFrame,
    experiment_id: str,
    target_column: str,
    categorical_columns: list,
    numeric_columns: list,
) -> DataFrame:

    # ...

    scaler = StandardScaler()

    with mlflow.start_run(experiment_id=experiment_id, run_name="Scaler") as run:
        X_encoded = pd.DataFrame(
            scaler.fit_transform(X_encoded), columns=X_encoded.columns
        )
        mlflow.sklearn.log_model(scaler, artifact_path="scaler")
        mlflow.log_metrics(
            pd.DataFrame(scaler.mean_, index=X_encoded.columns)[0].to_dict()
        )

    # ...

    return X_encoded  # return a pandas DataFrame

```

You can view the Scaler run in the MLflow UI at `localhost:5000`.

![Experiments tab of the MLflow UI showing the Possum_tails experiment with the Scaler run.](/img/examples/use-case-airflow-mlflow_experiments_scaler.png)

#### Model training DAG

The model training DAG is scheduled to run as soon as the last task in the feature engineering DAG completes using a [dataset](airflow-datasets.md).

```python
@dag(
    schedule=[Dataset("s3://" + DATA_BUCKET_NAME + "_" + FILE_PATH)],
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
```

The `fetch_feature_df` task pulls the feature dataframe that was pushed to [XCom](airflow-passing-data-between-tasks.md) in the previous DAG.


```python
@task
def fetch_feature_df(**context):
    "Fetch the feature dataframe from the feature engineering DAG."

    feature_df = context["ti"].xcom_pull(
        dag_id="feature_eng", task_ids="build_features", include_prior_dates=True
    )
    return feature_df
```

The ID number of the MLflow experiment is retrieved using the MLflowClientHook in the `fetch_experiment_id` task in order to track model training in the same experiment. 

The `train_model` task, defined with the `@aql.dataframe` decorator, shows how model training can be parameterized when using Airflow. In this example, the hyperparameters, the `target_colum`, and the model class are hardcoded, but they could also be retrieved from upstream tasks via [XCom](airflow-passing-data-between-tasks.md) or passed into manual runs of the DAG via [DAG params](airflow-params.md).

The project is set up to train the [scikit-learn RidgeCV model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html) to predict the tail length of possums using information such as their age, total length, or skull width.

```python
@aql.dataframe()
def train_model(
    feature_df: DataFrame,
    experiment_id: str,
    target_column: str,
    model_class: callable,
    hyper_parameters: dict,
    run_name: str,
) -> str:
    "Train a model and log it to MLFlow."

    # ...

    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
        model.fit(feature_df.drop(target, axis=1), feature_df[target])

    run_id = run.info.run_id

    return run_id

# ...

model_trained = train_model(
    feature_df=fetched_feature_df,
    experiment_id=fetched_experiment_id,
    target_column=TARGET_COLUMN,
    model_class=RidgeCV,
    hyper_parameters={"alphas": np.logspace(-3, 1, num=30)},
    run_name="RidgeCV",
)
```

The run of the RidgeCV model can be viewed in the MLflow UI at `localhost:5000`.

![Experiments tab of the MLflow UI showing the Possum_tails experiment with the RidgeCV run.](/img/examples/use-case-airflow-mlflow_experiments_ridgecv.png)

Lastly, the model training DAG registers the model and its version with MLflow using three operators from the MLflow Airflow provider. Note how information like the `run_id` or `version` of the model is pulled from XCom using [Jinja templates](templating.md).

```python
create_registered_model = CreateRegisteredModelOperator(
    task_id="create_registered_model",
    name=REGISTERED_MODEL_NAME,
    tags=[
        {"key": "model_type", "value": "regression"},
        {"key": "data", "value": "possum"},
    ],
)

create_model_version = CreateModelVersionOperator(
    task_id="create_model_version",
    name=REGISTERED_MODEL_NAME,
    source="s3://"
    + MLFLOW_ARTIFACT_BUCKET
    + "/"
    + "{{ ti.xcom_pull(task_ids='train_model') }}",
    run_id="{{ ti.xcom_pull(task_ids='train_model') }}",
    trigger_rule="none_failed",
)

transition_model = TransitionModelVersionStageOperator(
    task_id="transition_model",
    name=REGISTERED_MODEL_NAME,
    version="{{ ti.xcom_pull(task_ids='register_model.create_model_version')['model_version']['version'] }}",
    stage="Staging",
    archive_existing_versions=True,
)
```

You can view the registered models in the **Models** tab of the MLflow UI at `localhost:5000`.

![Models tab of the MLflow UI showing that the registered RidgeCV model has 3 Versions with the latest being in the Staging Stage.](/img/examples/use-case-airflow-mlflow_models_ridgecv.png)

#### Prediction DAG

After retrieving the feature dataframe, the target column, and the `model_run_id` from XCom, the `run_prediction` task uses the [ModelLoadAndPredictOperator](https://github.com/astronomer/airflow-provider-mlflow/blob/main/mlflow_provider/operators/pyfunc.py) to run a prediction on the whole dataset using the latest version of the registered RidgeCV model. 

```python
run_prediction = ModelLoadAndPredictOperator(
    mlflow_conn_id="mlflow_default",
    task_id="run_prediction",
    model_uri=f"s3://{MLFLOW_ARTIFACT_BUCKET}/"
    + "{{ ti.xcom_pull(task_ids='fetch_model_run_id')}}"
    + "/artifacts/model",
    data=fetched_feature_df,
)
```

The predicted possum tail length values are converted to a dataframe and then plotted against the true tail lengths using matplotlib. The resulting graph offers a visual representation of how much variation of possum tail length can be explained by a linear regression model using the features in the dataset in this specific possum population of 104 animals.

Congratulations! You ran a ML flow pipeline tracking model parameters and versions in MLflow using the MLflow Airflow provider. You can now use this pipeline as a template for your own MLflow projects.

## See also

- Documentation: [MLflow](https://mlflow.org/docs).
- Tutorial: [Use MLflow with Apache Airflow](airflow-mlflow.md).
- Provider: [MLflow Airflow provider](https://github.com/astronomer/airflow-provider-mlflow).