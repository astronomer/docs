"""
### Show three ways to use MLFlow with Airflow

This DAG shows how you can use the MLflowClientHook to create an experiment in MLFlow,
directly log metrics and parameters to MLFlow in a TaskFlow task via mlflow.sklearn.autolog() and
create a new model.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from astro.dataframes.pandas import DataFrame
from mlflow_provider.hooks.client import MLflowClientHook
from mlflow_provider.operators.registry import CreateRegisteredModelOperator

## MLFlow parameters
MLFLOW_CONN_ID = "mlflow_default"
MAX_RESULTS_MLFLOW_LIST_EXPERIMENTS = 100
EXPERIMENT_NAME = "Housing"
EXPERIMENT_ID = 1  # adjust as necessary
REGISTERED_MODEL_NAME = "<your-registered-model-name>"
ARTIFACT_BUCKET = "<your-bucket-name>"


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
def mlflow_tutorial_dag():
    # 1. Use a hook from the MLFlow provider to interact with MLFlow within a TaskFlow task
    @task
    def create_experiment(experiment_name, artifact_bucket, **context):
        """Create a new MLFlow experiment with a specified name.
        Save artifacts to the specified S3 bucket."""

        ts = context["ts"]

        mlflow_hook = MLflowClientHook(mlflow_conn_id=MLFLOW_CONN_ID)
        new_experiment_information = mlflow_hook.run(
            endpoint="api/2.0/mlflow/experiments/create",
            request_params={
                "name": ts + "_" + experiment_name,
                "artifact_location": f"s3://{artifact_bucket}/",
            },
        ).json()

        return new_experiment_information

    # 2. Use a mlflow.sklearn autologging in a TaskFlow task
    @task
    def scale_features(experiment_id: str) -> DataFrame:
        """Track feature scaling by sklearn in Mlflow."""
        from sklearn.datasets import fetch_california_housing
        from sklearn.preprocessing import StandardScaler
        import mlflow
        import pandas as pd

        df = fetch_california_housing(download_if_missing=True, as_frame=True).frame

        mlflow.sklearn.autolog()

        target = "MedHouseVal"
        X = df.drop(target, axis=1)
        y = df[target]

        scaler = StandardScaler()

        with mlflow.start_run(experiment_id=experiment_id, run_name="Scaler") as run:
            X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
            mlflow.sklearn.log_model(scaler, artifact_path="scaler")
            mlflow.log_metrics(pd.DataFrame(scaler.mean_, index=X.columns)[0].to_dict())

        X[target] = y

    # 3. Use an operator from the MLFlow provider to interact with MLFlow directly
    create_registered_model = CreateRegisteredModelOperator(
        task_id="create_registered_model",
        name="{{ ts }}" + "_" + REGISTERED_MODEL_NAME,
        tags=[
            {"key": "model_type", "value": "regression"},
            {"key": "data", "value": "housing"},
        ],
    )

    (
        create_experiment(
            experiment_name=EXPERIMENT_NAME, artifact_bucket=ARTIFACT_BUCKET
        )
        >> scale_features(experiment_id=EXPERIMENT_ID)
        >> create_registered_model
    )


mlflow_tutorial_dag()
