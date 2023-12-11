"""
## Move files between object storage system locations in an MLOps pipeline

This DAG shows the basic use of the Airflow 2.8 Object Storage feature to
copy files between object storage system locations in an MLOps pipeline training
a Naive Bayes Classifier to distinguish between quotes from Captain Kirk and
Captain Picard and provide a prediction for a user-supplied quote.

To be able to run this DAG you will need to add the contents of
`include/ingestion_data_object_store_use_case` to your object storage system, 
install the relevant provider package for your object storage and define an
Airflow connection to it.
If you do not want to use remote storage you can use `file://` for local object
storage and adjust the paths accordingly.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath
from airflow.models.baseoperator import chain
from airflow.models.param import Param
import joblib
import base64
import io

OBJECT_STORAGE_INGEST = "s3"
CONN_ID_INGEST = "my_aws_conn"
PATH_INGEST = "astro-object-storage-tutorial/ingest/"

OBJECT_STORAGE_TRAIN = "s3"
CONN_ID_TRAIN = "my_aws_conn"
PATH_TRAIN = "astro-object-storage-tutorial/train/"

OBJECT_STORAGE_ARCHIVE = "file"
CONN_ID_ARCHIVE = None
PATH_ARCHIVE = "include/archive/"


base_path_ingest = ObjectStoragePath(
    f"{OBJECT_STORAGE_INGEST}://{PATH_INGEST}", conn_id=CONN_ID_INGEST
)

base_path_train = ObjectStoragePath(
    f"{OBJECT_STORAGE_TRAIN}://{PATH_TRAIN}", conn_id=CONN_ID_TRAIN
)

base_path_archive = ObjectStoragePath(
    f"{OBJECT_STORAGE_ARCHIVE}://{PATH_ARCHIVE}", conn_id=CONN_ID_ARCHIVE
)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
    doc_md=__doc__,
    params={
        "my_quote": Param(
            "Time and space are creations of the human mind.",
            type="string",
            description="Enter a quote to be classified as Kirk-y or Picard-y.",
        )
    },
)
def object_storage_use_case():
    @task
    def list_files_ingest(base: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage including subdirectories."""

        labels = [obj for obj in base.iterdir() if obj.is_dir()]
        files = [f for label in labels for f in label.iterdir() if f.is_file()]
        return files

    @task
    def copy_files_ingest_to_train(src: ObjectStoragePath, dst: ObjectStoragePath):
        """Copy a file from one remote system to another.
        The file is streamed in chunks using shutil.copyobj"""

        src.copy(dst=dst)

    @task
    def list_files_train(base: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage."""

        files = [f for f in base.iterdir() if f.is_file()]
        return files

    @task
    def get_text_from_file(file: ObjectStoragePath) -> dict:
        """Read files in remote object storage."""

        bytes = file.read_block(offset=0, length=None)
        text = bytes.decode("utf-8")

        key = file.key
        filename = key.split("/")[-1]
        label = filename.split("_")[-2]
        return {"label": label, "text": text}

    @task
    def train_model(train_data: list[dict]):
        """Train a Naive Bayes Classifier using the files in the train folder."""

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import make_pipeline
        from sklearn.model_selection import train_test_split

        text_data = [d["text"] for d in train_data]
        labels = [d["label"] for d in train_data]

        X_train, X_test, y_train, y_test = train_test_split(
            text_data, labels, test_size=0.2, random_state=42
        )

        model = make_pipeline(CountVectorizer(), MultinomialNB())

        model.fit(X_train, y_train)

        buffer = io.BytesIO()
        joblib.dump(model, buffer)
        buffer.seek(0)

        encoded_model = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return encoded_model

    @task
    def use_model(encoded_model: str, **context):
        """Load the model and use it for prediction."""
        my_quote = context["params"]["my_quote"]

        model_binary = base64.b64decode(encoded_model)

        buffer = io.BytesIO(model_binary)
        model = joblib.load(buffer)

        predictions = model.predict([my_quote])

        print(f"The quote: '{my_quote}'") 
        print(f"sounds like it could have been said by {predictions[0].capitalize()}")

    @task
    def copy_files_train_to_archive(src: ObjectStoragePath, dst: ObjectStoragePath):
        """Copy a file from a remote system to local storage."""

        src.copy(dst=dst)

    @task
    def empty_train(base: ObjectStoragePath):
        """Empty the train folder."""

        for file in base.iterdir():
            file.unlink()

    # call tasks
    files_ingest = list_files_ingest(base=base_path_ingest)
    files_copied = copy_files_ingest_to_train.partial(dst=base_path_train).expand(
        src=files_ingest
    )
    files_train = list_files_train(base=base_path_train)
    chain(files_copied, files_train)
    train_data = get_text_from_file.expand(file=files_train)
    encoded_model = train_model(train_data=train_data)
    use_model(encoded_model=encoded_model)
    chain(
        encoded_model,
        copy_files_train_to_archive.partial(dst=base_path_archive).expand(
            src=files_train
        ),
        empty_train(base=base_path_train),
    )


object_storage_use_case()
