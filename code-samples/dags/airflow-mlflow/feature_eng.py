"""
### Build machine learning features using the Astro Python SDK and MLFlow

This DAG utilizes the Astro Python SDK, MLFlow and Sklearn to build machine learning features from an existing dataset about possums.

Original Source of the dataset:
Lindenmayer, D. B., Viggers, K. L., Cunningham, R. B., and Donnelly, C. F. 1995. 
Morphological variation among columns of the mountain brushtail possum, 
Trichosurus caninus Ogilby (Phalangeridae: Marsupiala). Australian Journal of Zoology 43: 449-458.
Available on Kaggle: https://www.kaggle.com/datasets/abrambeyer/openintro-possum
"""

from airflow import Dataset
from airflow.decorators import dag, task_group, task
from pendulum import datetime
from astro import sql as aql
from astro.files import File
from astro.dataframes.pandas import DataFrame
from mlflow_provider.hooks.client import MLflowClientHook
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
import os

# -------------- #
# Set parameters #
# -------------- #

FILE_PATH = "possum.csv"

## AWS S3 parameters
AWS_CONN_ID = "aws_default"
DATA_BUCKET_NAME = "data"
MLFLOW_ARTIFACT_BUCKET = "mlflowdatapossums"

## MLFlow parameters
MLFLOW_CONN_ID = "mlflow_default"
EXPERIMENT_NAME = "Possum_tails"
MAX_RESULTS_MLFLOW_LIST_EXPERIMENTS = 1000

## Data parameters
TARGET_COLUMN = "taill"  # tail length in cm
CATEGORICAL_COLUMNS = ["site", "Pop", "sex"]
NUMERIC_COLUMNS = ["age", "hdlngth", "skullw", "totlngth", "footlgth"]
XCOM_BUCKET = "localxcom"


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
def feature_eng():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(
        task_id="end",
        outlets=[Dataset("s3://" + DATA_BUCKET_NAME + "_" + FILE_PATH)],
    )

    # --------------------- #
    # Create all S3 buckets #
    # --------------------- #

    create_buckets_if_not_exists = S3CreateBucketOperator.partial(
        task_id="create_buckets_if_not_exists",
        aws_conn_id=AWS_CONN_ID,
    ).expand(bucket_name=[DATA_BUCKET_NAME, MLFLOW_ARTIFACT_BUCKET, XCOM_BUCKET])

    # ------------------------------------------- #
    # Task group to prepare the MLflow experiment #
    # and retrieve the experiment ID              #
    # ------------------------------------------- #

    @task_group
    def prepare_mlflow_experiment():
        @task
        def list_existing_experiments(max_results=1000):
            "Get information about existing MLFlow experiments."

            mlflow_hook = MLflowClientHook(mlflow_conn_id=MLFLOW_CONN_ID)
            existing_experiments_information = mlflow_hook.run(
                endpoint="api/2.0/mlflow/experiments/search",
                request_params={"max_results": max_results},
            ).json()

            return existing_experiments_information

        @task.branch
        def check_if_experiment_exists(
            experiment_name, existing_experiments_information
        ):
            "Check if the specified experiment already exists."

            if existing_experiments_information:
                existing_experiment_names = [
                    experiment["name"]
                    for experiment in existing_experiments_information["experiments"]
                ]
                if experiment_name in existing_experiment_names:
                    return "prepare_mlflow_experiment.experiment_exists"
                else:
                    return "prepare_mlflow_experiment.create_experiment"
            else:
                return "prepare_mlflow_experiment.create_experiment"

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

        experiment_already_exists = EmptyOperator(task_id="experiment_exists")

        @task(
            trigger_rule="none_failed",
        )
        def get_current_experiment_id(experiment_name, max_results=1000):
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
                    raise ValueError(
                        f"{experiment_name} not found in MLFlow experiments."
                    )

        experiment_id = get_current_experiment_id(
            experiment_name=EXPERIMENT_NAME,
            max_results=MAX_RESULTS_MLFLOW_LIST_EXPERIMENTS,
        )

        (
            check_if_experiment_exists(
                experiment_name=EXPERIMENT_NAME,
                existing_experiments_information=list_existing_experiments(
                    max_results=MAX_RESULTS_MLFLOW_LIST_EXPERIMENTS
                ),
            )
            >> [
                experiment_already_exists,
                create_experiment(
                    experiment_name=EXPERIMENT_NAME,
                    artifact_bucket=MLFLOW_ARTIFACT_BUCKET,
                ),
            ]
            >> experiment_id
        )

    # ------------------------------------------- #
    # Extracting the data from the local CSV file #
    # ------------------------------------------- #

    @aql.dataframe()
    def extract_data(data_file_path) -> DataFrame:
        import pandas as pd

        df = pd.read_csv(f"include/{data_file_path}")
        return df.iloc[:, 1:]

    # ------------------- #
    # Feature engineering #
    # ------------------- #

    @aql.dataframe()
    def build_features(
        raw_df: DataFrame,
        experiment_id: str,
        target_column: str,
        categorical_columns: list,
        numeric_columns: list,
    ) -> DataFrame:
        """Build machine learning features using the Astro Python SDK
        and track them in MLFlow."""

        import mlflow
        from sklearn.preprocessing import StandardScaler
        import pandas as pd

        mlflow.sklearn.autolog()

        target = target_column
        X = raw_df.drop(target, axis=1)
        y = raw_df[target]

        # One-hot encode the 'category' and 'color' columns
        X_encoded = pd.get_dummies(X, columns=categorical_columns)

        # Add the non-dummy columns back to the DataFrame
        X_encoded[numeric_columns] = X[numeric_columns]

        scaler = StandardScaler()

        with mlflow.start_run(experiment_id=experiment_id, run_name="Scaler") as run:
            X_encoded = pd.DataFrame(
                scaler.fit_transform(X_encoded), columns=X_encoded.columns
            )
            mlflow.sklearn.log_model(scaler, artifact_path="scaler")
            mlflow.log_metrics(
                pd.DataFrame(scaler.mean_, index=X_encoded.columns)[0].to_dict()
            )

        X_encoded[target] = y

        return X_encoded

    extracted_df = extract_data(data_file_path=FILE_PATH)

    # ----------------------- #
    # Save the features in S3 #
    # ----------------------- #

    save_data_to_s3 = aql.export_file(
        task_id="save_data_to_s3",
        input_data=extracted_df,
        output_file=File(os.path.join("s3://", DATA_BUCKET_NAME, FILE_PATH)),
        if_exists="replace",
    )

    (
        start
        >> create_buckets_if_not_exists
        >> prepare_mlflow_experiment()
        >> build_features(
            raw_df=extracted_df,
            experiment_id="{{ ti.xcom_pull(task_ids='prepare_mlflow_experiment.get_current_experiment_id') }}",
            target_column=TARGET_COLUMN,
            categorical_columns=CATEGORICAL_COLUMNS,
            numeric_columns=NUMERIC_COLUMNS,
        )
        >> end
    )

    start >> extracted_df >> save_data_to_s3 >> end


feature_eng()
