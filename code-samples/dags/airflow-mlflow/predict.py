"""
### Run predictions on a dataset using the MLFLow ModelLoadAndPredictOperator and plot the results

This DAG utilizes the ModelLoadAndPredictOperator to run predictions on a dataset using a trained MLFlow model. The resulting
predictions are plotted against the true values.
"""

from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime
from astro import sql as aql
from astro.files import File
from airflow.operators.empty import EmptyOperator
import os
from mlflow_provider.operators.pyfunc import ModelLoadAndPredictOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd


## AWS S3 parameters
AWS_CONN_ID = "aws_default"
BUCKET_NAME = "data"
MLFLOW_ARTIFACT_BUCKET = "mlflowdatapossums"

## Data parameters
TARGET_COLUMN = "taill"  # tail length in cm
FILE_TO_SAVE_PREDICTIONS = "possum_tail_length.csv"


@dag(
    schedule=[Dataset("model_trained")],
    start_date=datetime(2023, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
)
def predict():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task
    def fetch_feature_df_no_target(target_column, **context):
        feature_df = context["ti"].xcom_pull(
            dag_id="feature_eng", task_ids="build_features", include_prior_dates=True
        )
        feature_df.dropna(inplace=True)
        feature_df.drop(target_column, axis=1, inplace=True)
        return feature_df.to_numpy()

    @task
    def fetch_target(target_column, **context):
        feature_df = context["ti"].xcom_pull(
            dag_id="feature_eng", task_ids="build_features", include_prior_dates=True
        )
        feature_df.dropna(inplace=True)
        return feature_df[[target_column]]

    @task
    def fetch_model_run_id(**context):
        model_run_id = context["ti"].xcom_pull(
            dag_id="train", task_ids="train_model", include_prior_dates=True
        )
        return model_run_id

    fetched_feature_df = fetch_feature_df_no_target(target_column=TARGET_COLUMN)
    fetched_model_run_id = fetch_model_run_id()

    @task
    def add_line_to_file(**context):
        s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
        file_contents = s3_hook.read_key(
            key=context["ti"].xcom_pull(task_ids="fetch_model_run_id")
            + "/artifacts/model/requirements.txt",
            bucket_name=MLFLOW_ARTIFACT_BUCKET,
        )
        updated_contents = file_contents + "\nboto3" + "\npandas"
        s3_hook.load_string(
            updated_contents,
            key=context["ti"].xcom_pull(task_ids="fetch_model_run_id")
            + "/artifacts/model/requirements.txt",
            bucket_name=MLFLOW_ARTIFACT_BUCKET,
            replace=True,
        )

    run_prediction = ModelLoadAndPredictOperator(
        mlflow_conn_id="mlflow_default",
        task_id="run_prediction",
        model_uri=f"s3://{MLFLOW_ARTIFACT_BUCKET}/"
        + "{{ ti.xcom_pull(task_ids='fetch_model_run_id')}}"
        + "/artifacts/model",
        data=fetched_feature_df,
    )

    @task
    def list_to_dataframe(column_data):
        df = pd.DataFrame(
            column_data, columns=["Predictions"], index=range(len(column_data))
        )
        return df

    @task
    def plot_predictions(predictions, df):
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the prediction column in blue
        ax.plot(
            predictions.index,
            predictions["Predictions"],
            color="blue",
            label="Predicted tail length",
        )

        # Plot the target column in green
        ax.plot(df.index, df["taill"], color="green", label="True tail length")

        # Set the title and labels
        ax.set_title("Predicted vs True Possum Tail Lengths")
        ax.set_xlabel("Tail length")
        ax.set_ylabel("Animal number")

        # Add a legend
        ax.legend(loc="lower right")

        # Load and display the possum image in the upper right corner
        possum_img = mpimg.imread("include/opossum.jpeg")
        ax_img = fig.add_axes(
            [0.75, 0.7, 0.2, 0.3]
        )  # Adjust the coordinates and size as needed
        ax_img.imshow(possum_img)
        ax_img.axis("off")

        os.makedirs(os.path.dirname("include/plots/"), exist_ok=True)

        # Save the plot as a PNG file
        plt.savefig("include/plots/possum_tails.png")
        plt.close()

    target_data = fetch_target(target_column=TARGET_COLUMN)
    prediction_data = list_to_dataframe(run_prediction.output)

    pred_file = aql.export_file(
        task_id="save_predictions",
        input_data=prediction_data,
        output_file=File(os.path.join("s3://", BUCKET_NAME, FILE_TO_SAVE_PREDICTIONS)),
        if_exists="replace",
    )

    (
        start
        >> [fetched_feature_df, fetched_model_run_id]
        >> add_line_to_file()
        >> run_prediction
        >> plot_predictions(prediction_data, target_data)
        >> pred_file
        >> end
    )


predict()
