from airflow.decorators import dag
from pendulum import datetime
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table
from astro_databricks.operators.notebook import DatabricksNotebookOperator
from astro_databricks.operators.workflow import DatabricksWorkflowTaskGroup
from airflow.providers.amazon.aws.operators.s3 import S3DeleteObjectsOperator
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------- #
# Setting variables #
# ----------------- #

# ------- ENTER YOUR INFORMATION HERE ------ #
COUNTRY = "Switzerland"
DATABRICKS_LOGIN_EMAIL = "<your Databricks login email>"
S3_BUCKET = "databricks-tutorial-bucket"
OBJECT_STORAGE_CONN_ID = "aws_conn"
# ------- \ENTER YOUR INFORMATION HERE ------ #

DATABRICKS_NOTEBOOK_NAME_1 = "join_data"
DATABRICKS_NOTEBOOK_NAME_2 = "transform_data"
DATABRICKS_NOTEBOOK_PATH_JOIN_DATA = (
    f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_1}"
)
DATABRICKS_NOTEBOOK_PATH_TRANSFORM_DATA = (
    f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_2}"
)
SOLAR_CSV_PATH = "include/share-electricity-solar.csv"
HYDRO_CSV_PATH = "include/share-electricity-hydro.csv"
WIND_CSV_PATH = "include/share-electricity-wind.csv"
S3_FOLDER_COUNTRY_SUBSET = "country_subset"
S3_FOLDER_TRANSFORMED_DATA = "transformed_data"
DATABRICKS_RESULT_FILE_PATH = (
    f"s3://{S3_BUCKET}/{S3_FOLDER_TRANSFORMED_DATA}/{COUNTRY}.csv"
)
DATABRICKS_JOB_CLUSTER_KEY = "tutorial-cluster"

DATABRICKS_CONN_ID = "databricks_conn"
DB_CONN_ID = "db_conn"

S3_FOLDER_COUNTRY_SUBSET = "country_subset"

job_cluster_spec = [
    {
        "job_cluster_key": DATABRICKS_JOB_CLUSTER_KEY,
        "new_cluster": {
            "cluster_name": "",
            "spark_version": "11.3.x-scala2.12",
            "aws_attributes": {
                "first_on_demand": 1,
                "availability": "SPOT_WITH_FALLBACK",
                "zone_id": "eu-central-1",
                "spot_bid_price_percent": 100,
                "ebs_volume_count": 0,
            },
            "node_type_id": "i3.xlarge",
            "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
            "enable_elastic_disk": False,
            "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
            "runtime_engine": "STANDARD",
            "num_workers": 1,
        },
    }
]

# -------------------------- #
# Astro SDK transformations  #
# -------------------------- #


@aql.transform
def select_countries(in_table, country):
    return """SELECT * FROM {{ in_table }} WHERE "Entity" = {{ country }}"""


@aql.dataframe
def create_graph(df: pd.DataFrame):
    sns.set_style("whitegrid")
    sns.lineplot(x="Year", y="SHW%", data=df)
    plt.title(f"% of Solar, Hydro and Wind in {COUNTRY}")
    plt.xlabel("Year")
    plt.ylabel("Combined SHW (in %)")
    plt.savefig("include/shw.png")


# --- #
# DAG #
# --- #


@dag(start_date=datetime(2023, 1, 1), schedule=None, catchup=False)
def renewable_analysis_dag():
    # load files from the `include` directory into a temporary table each
    # by using dynamic task mapping over the LoadFileOperator
    in_tables = aql.LoadFileOperator.partial(
        task_id="in_tables",
        output_table=Table(
            conn_id=DB_CONN_ID,
        ),
    ).expand(
        input_file=[
            File(path=SOLAR_CSV_PATH),
            File(path=HYDRO_CSV_PATH),
            File(path=WIND_CSV_PATH),
        ]
    )

    # select the data from `COUNTRY` for each temporary table, store in
    # another temporary table
    country_tables = select_countries.partial(country=COUNTRY).expand(
        in_table=in_tables.output
    )

    # export the information from each temporary table into a CSV file in S3
    save_files_to_S3 = aql.ExportToFileOperator.partial(
        task_id="save_files_to_S3",
        if_exists="replace",
    ).expand_kwargs(
        country_tables.map(
            lambda x: {
                "input_data": x,
                "output_file": File(
                    path=f"s3://{S3_BUCKET}/{S3_FOLDER_COUNTRY_SUBSET}/{x.name}.csv",
                    conn_id=OBJECT_STORAGE_CONN_ID,
                ),
            }
        )
    )

    # ------------------------------------ #
    # Astro Databricks provider task group #
    # ------------------------------------ #

    task_group = DatabricksWorkflowTaskGroup(
        group_id="databricks_workflow",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_clusters=job_cluster_spec,
    )

    with task_group:
        notebook_1 = DatabricksNotebookOperator(
            task_id="join_data",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path=DATABRICKS_NOTEBOOK_PATH_JOIN_DATA,
            source=S3_BUCKET,
            job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
        )
        notebook_2 = DatabricksNotebookOperator(
            task_id="transform_data",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path=DATABRICKS_NOTEBOOK_PATH_TRANSFORM_DATA,
            source=S3_BUCKET,
            job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
        )
        notebook_1 >> notebook_2

    # delete files from ingestion bucket in S3
    delete_intake_files_S3 = S3DeleteObjectsOperator(
        task_id="delete_intake_files_S3",
        bucket=S3_BUCKET,
        prefix=f"{S3_FOLDER_COUNTRY_SUBSET}/",
        aws_conn_id=OBJECT_STORAGE_CONN_ID,
    )

    # load CSV file containing the result from the transformation in the
    # Databricks job into the relational database
    load_file_to_db = aql.load_file(
        input_file=File(
            path=DATABRICKS_RESULT_FILE_PATH, conn_id=OBJECT_STORAGE_CONN_ID
        ),
        output_table=Table(conn_id=DB_CONN_ID),
    )

    (
        save_files_to_S3
        >> task_group
        >> [load_file_to_db, delete_intake_files_S3]
        >> create_graph(load_file_to_db)  # use the Astro SDK to graph the results
    )

    # cleanup temporary tables in the relational database
    aql.cleanup()


renewable_analysis_dag()
