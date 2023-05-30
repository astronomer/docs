"""
### Train a RidgeCV model using sklearn and track model versions with the MLFlow provider

This DAG utilizes the Astro Python SDK, MLFlow and Sklearn to train a machine learning model on a provided dataset.
"""

from airflow import Dataset
from airflow.decorators import dag, task_group, task
from pendulum import datetime
from astro import sql as aql
from astro.dataframes.pandas import DataFrame
from mlflow_provider.hooks.client import MLflowClientHook
from airflow.operators.empty import EmptyOperator
from sklearn.linear_model import RidgeCV
from mlflow_provider.operators.registry import (
    CreateRegisteredModelOperator,
    CreateModelVersionOperator,
    TransitionModelVersionStageOperator,
)
import numpy as np

FILE_PATH = "possum.csv"

## AWS S3 parameters
AWS_CONN_ID = "aws_default"
DATA_BUCKET_NAME = "data"
MLFLOW_ARTIFACT_BUCKET = "mlflowdatapossums"

## MLFlow parameters
MLFLOW_CONN_ID = "mlflow_default"
EXPERIMENT_NAME = "Possum_tails"
REGISTERED_MODEL_NAME = "Reg_RidgeCV_possums"
MAX_RESULTS_MLFLOW_LIST_EXPERIMENTS = 1000

## Data parameters
TARGET_COLUMN = "taill"  # tail length in cm


@dag(
    schedule=[Dataset("s3://" + DATA_BUCKET_NAME + "_" + FILE_PATH)],
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
def train():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", outlets=[Dataset("model_trained")])

    @task
    def fetch_feature_df(**context):
        "Fetch the feature dataframe from the feature engineering DAG."

        feature_df = context["ti"].xcom_pull(
            dag_id="feature_eng", task_ids="build_features", include_prior_dates=True
        )
        return feature_df

    @task
    def fetch_experiment_id(experiment_name, max_results=1000):
        "Get the ID of the specified MLFlow experiment."

        mlflow_hook = MLflowClientHook(mlflow_conn_id=MLFLOW_CONN_ID)
        experiments_information = mlflow_hook.run(
            endpoint="api/2.0/mlflow/experiments/search",
            request_params={"max_results": max_results},
        ).json()

        for experiment in experiments_information["experiments"]:
            if experiment["name"] == experiment_name:
                return experiment["experiment_id"]
            else:
                raise ValueError(f"{experiment_name} not found in MLFlow experiments.")

    # Train a model
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

        import mlflow

        mlflow.sklearn.autolog()

        feature_df = feature_df.dropna()

        target = target_column
        model = model_class(**hyper_parameters)

        with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
            model.fit(feature_df.drop(target, axis=1), feature_df[target])

        run_id = run.info.run_id

        return run_id

    fetched_feature_df = fetch_feature_df()
    fetched_experiment_id = fetch_experiment_id(experiment_name=EXPERIMENT_NAME)

    model_trained = train_model(
        feature_df=fetched_feature_df,
        experiment_id=fetched_experiment_id,
        target_column=TARGET_COLUMN,
        model_class=RidgeCV,
        hyper_parameters={"alphas": np.logspace(-3, 1, num=30)},
        run_name="RidgeCV",
    )

    @task_group
    def register_model():
        @task.branch
        def check_if_model_already_registered(reg_model_name):
            "Get information about existing registered MLFlow models."

            mlflow_hook = MLflowClientHook(mlflow_conn_id=MLFLOW_CONN_ID, method="GET")
            get_reg_model_response = mlflow_hook.run(
                endpoint="api/2.0/mlflow/registered-models/get",
                request_params={"name": reg_model_name},
            ).json()

            if "error_code" in get_reg_model_response:
                if get_reg_model_response["error_code"] == "RESOURCE_DOES_NOT_EXIST":
                    reg_model_exists = False
                else:
                    raise ValueError(
                        f"Error when checking if model is registered: {get_reg_model_response['error_code']}"
                    )
            else:
                reg_model_exists = True

            if reg_model_exists:
                return "register_model.model_already_registered"
            else:
                return "register_model.create_registered_model"

        model_already_registered = EmptyOperator(task_id="model_already_registered")

        create_registered_model = CreateRegisteredModelOperator(
            task_id="create_registered_model",
            name=REGISTERED_MODEL_NAME,
            tags=[
                {"key": "model_type", "value": "regression"},
                {"key": "data", "value": "housing"},
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

        (
            check_if_model_already_registered(reg_model_name=REGISTERED_MODEL_NAME)
            >> [model_already_registered, create_registered_model]
            >> create_model_version
            >> transition_model
        )

    (
        start
        >> [fetched_feature_df, fetched_experiment_id]
        >> model_trained
        >> register_model()
        >> end
    )


train()
