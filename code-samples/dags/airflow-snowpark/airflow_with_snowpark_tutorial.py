"""
### Orchestrate data transformation and model training in Snowflake using Snowpark

This DAG shows how to use specialized decorators to run Snowpark code in Airflow.
Note that it uses the Airflow 2.7 feature of setup/ teardown tasks to create
and clean up a Snowflake custom XCom backend.
If you want to use regular XCom or are running on an older version set
`SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND` to `False`.
"""

from datetime import datetime
from airflow.decorators import dag, task
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table
from airflow.models.baseoperator import chain
from astronomer.providers.snowflake.utils.snowpark_helpers import SnowparkTable


# toggle this to False if you are NOT using the Snowflake XCOM backend or
# had the necessary objects created already
SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND = False
MY_SNOWFLAKE_XCOM_DATABASE = "SNOWPARK_XCOM_DB"
MY_SNOWFLAKE_XCOM_SCHEMA = "SNOWPARK_XCOM_SCHEMA"
MY_SNOWFLAKE_XCOM_STAGE = "XCOM_STAGE"
MY_SNOWFLAKE_XCOM_TABLE = "XCOM_TABLE"

# provide your Snowflake database name, schema name, connection ID
# and path to the Snowpark environment binary
MY_SNOWFLAKE_DATABASE = "MY_SKI_DATA_DATABASE"  # an existing database
MY_SNOWFLAKE_SCHEMA = "MY_SKI_DATA_SCHEMA"  # an existing schema
MY_SNOWFLAKE_TABLE = "MY_SKI_DATA_TABLE"
SNOWFLAKE_CONN_ID = "snowflake_default"
SNOWPARK_BIN = "/home/astro/.venv/snowpark/bin/python"

# while this tutorial will run with the default Snowflake warehouse, larger
# datasets may require a Snowpark optimized warehouse. Set the following toggle to true to
# use such a warehouse. And provide your Snowpark and regular warehouses' names.
USE_SNOWPARK_WAREHOUSE = False
MY_SNOWPARK_WAREHOUSE = "SNOWPARK_WH"
MY_SNOWFLAKE_REGULAR_WAREHOUSE = "HUMANS"


@dag(
    start_date=datetime(2023, 9, 1),
    schedule=None,
    catchup=False,
)
def airflow_with_snowpark_tutorial():
    if SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND:

        @task.snowpark_python(
            snowflake_conn_id=SNOWFLAKE_CONN_ID,
        )
        def create_snowflake_objects(
            snowflake_xcom_database,
            snowflake_xcom_schema,
            snowflake_xcom_table,
            snowflake_xcom_table_stage,
            use_snowpark_warehouse=False,
            snowpark_warehouse=None,
        ):
            from snowflake.snowpark.exceptions import SnowparkSQLException

            try:
                snowpark_session.sql(
                    f"""CREATE DATABASE IF NOT EXISTS
                        {snowflake_xcom_database};
                    """
                ).collect()
                print(f"Created database {snowflake_xcom_database}.")

                snowpark_session.sql(
                    f"""CREATE SCHEMA IF NOT EXISTS 
                        {snowflake_xcom_database}.
                        {snowflake_xcom_schema};
                    """
                ).collect()
                print(f"Created schema {snowflake_xcom_schema}.")

                if use_snowpark_warehouse:
                    snowpark_session.sql(
                        f"""CREATE WAREHOUSE IF NOT EXISTS 
                        {snowpark_warehouse} 
                            WITH 
                                WAREHOUSE_SIZE = 'MEDIUM'
                                WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
                        """
                    ).collect()
                    print(f"Created warehouse {snowpark_warehouse}.")
            except SnowparkSQLException as e:
                print(e)
                print(
                    f"""You do not have the necessary privileges to create objects in Snowflake.
                    If they do not exist already, please contact your Snowflake administrator
                    to create the following objects for you: 
                        - DATABASE: {snowflake_xcom_database},
                        - SCHEMA: {snowflake_xcom_schema},
                        - WAREHOUSE: {snowpark_warehouse} (if you want to use a Snowpark warehouse) 
                    """
                )

            snowpark_session.sql(
                f"""CREATE TABLE IF NOT EXISTS
                    {snowflake_xcom_database}.
                    {snowflake_xcom_schema}.
                    {snowflake_xcom_table}
                        ( 
                            dag_id varchar NOT NULL, 
                            task_id varchar NOT NULL, 
                            run_id varchar NOT NULL,
                            multi_index integer NOT NULL,
                            key varchar NOT NULL,
                            value_type varchar NOT NULL,
                            value varchar NOT NULL
                        ); 
                """
            ).collect()
            print(f"Table {snowflake_xcom_table} is ready!")

            snowpark_session.sql(
                f"""CREATE STAGE IF NOT EXISTS
                    {snowflake_xcom_database}.\
                    {snowflake_xcom_schema}.\
                    {snowflake_xcom_table_stage} 
                        DIRECTORY = (ENABLE = TRUE)
                        ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
                    """
            ).collect()
            print(f"Stage {snowflake_xcom_table_stage} is ready!")

        create_snowflake_objects_obj = create_snowflake_objects(
            snowflake_xcom_database=MY_SNOWFLAKE_XCOM_DATABASE,
            snowflake_xcom_schema=MY_SNOWFLAKE_XCOM_SCHEMA,
            snowflake_xcom_table=MY_SNOWFLAKE_XCOM_TABLE,
            snowflake_xcom_table_stage=MY_SNOWFLAKE_XCOM_STAGE,
            use_snowpark_warehouse=USE_SNOWPARK_WAREHOUSE,
            snowpark_warehouse=MY_SNOWPARK_WAREHOUSE,
        )

    # use the Astro Python SDK to load data from a CSV file into Snowflake
    load_file_obj = aql.load_file(
        task_id="load_file",
        input_file=File("include/data/ski_dataset.csv"),
        output_table=Table(
            metadata={
                "database": MY_SNOWFLAKE_DATABASE,
                "schema": MY_SNOWFLAKE_SCHEMA,
            },
            conn_id=SNOWFLAKE_CONN_ID,
            name=MY_SNOWFLAKE_TABLE,
        ),
        if_exists="replace",
    )

    # create a model registry in Snowflake
    @task.snowpark_python(
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
    )
    def create_model_registry(demo_database, demo_schema):
        from snowflake.ml.registry import model_registry

        model_registry.create_model_registry(
            session=snowpark_session,
            database_name=demo_database,
            schema_name=demo_schema,
        )

    # Tasks using the @task.snowpark_python decorator run in
    # the regular Snowpark Python environment
    @task.snowpark_python(
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
    )
    def transform_table_step_one(df: SnowparkTable):
        from snowflake.snowpark.functions import col
        import pandas as pd

        filtered_data = df.filter(
            (col("AFTERNOON_BEVERAGE") == "coffee")
            | (col("AFTERNOON_BEVERAGE") == "tea")
            | (col("AFTERNOON_BEVERAGE") == "snow_mocha")
            | (col("AFTERNOON_BEVERAGE") == "hot_chocolate")
            | (col("AFTERNOON_BEVERAGE") == "wine")
        ).collect()
        filtered_df = pd.DataFrame(filtered_data, columns=df.columns)

        return filtered_df

    # Tasks using the @task.snowpark_ext_python decorator can use an
    # existing python environment
    @task.snowpark_ext_python(snowflake_conn_id=SNOWFLAKE_CONN_ID, python=SNOWPARK_BIN)
    def transform_table_step_two(df):
        df_serious_skiers = df[df["HOURS_SKIED"] >= 1]

        return df_serious_skiers

    # Tasks using the @task.snowpark_virtualenv decorator run in a virtual
    # environment created on the spot using the requirements specified
    @task.snowpark_virtualenv(
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        requirements=["pandas", "scikit-learn"],
    )
    def train_beverage_classifier(
        df,
        database_name,
        schema_name,
        use_snowpark_warehouse=False,
        snowpark_warehouse=None,
        snowflake_regular_warehouse=None,
    ):
        from sklearn.model_selection import train_test_split
        import pandas as pd
        from snowflake.ml.registry import model_registry
        from snowflake.ml.modeling.linear_model import LogisticRegression
        from uuid import uuid4
        from snowflake.ml.modeling.preprocessing import OneHotEncoder, StandardScaler

        registry = model_registry.ModelRegistry(
            session=snowpark_session,
            database_name=database_name,
            schema_name=schema_name,
        )

        df.columns = [str(col).replace("'", "").replace('"', "") for col in df.columns]
        X = df.drop(columns=["AFTERNOON_BEVERAGE", "SKIER_ID"])
        y = df["AFTERNOON_BEVERAGE"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        categorical_features = ["RESORT", "SKI_COLOR", "JACKET_COLOR", "HAD_LUNCH"]
        numeric_features = ["HOURS_SKIED", "SNOW_QUALITY", "CM_OF_NEW_SNOW"]
        label_col = ["AFTERNOON_BEVERAGE"]

        scaler = StandardScaler(
            input_cols=numeric_features,
            output_cols=numeric_features,
            drop_input_cols=True,
        )
        scaler.fit(train_data)
        train_data_scaled = scaler.transform(train_data)
        test_data_scaled = scaler.transform(test_data)

        one_hot_encoder = OneHotEncoder(
            input_cols=categorical_features,
            output_cols=categorical_features,
            drop_input_cols=True,
        )
        one_hot_encoder.fit(train_data_scaled)
        train_data_scaled_encoded = one_hot_encoder.transform(train_data_scaled)
        test_data_scaled_encoded = one_hot_encoder.transform(test_data_scaled)

        feature_cols = train_data_scaled_encoded.drop(
            columns=["AFTERNOON_BEVERAGE"]
        ).columns

        classifier = LogisticRegression(
            max_iter=10000, input_cols=feature_cols, label_cols=label_col
        )

        feature_cols = [
            str(col).replace("'", "").replace('"', "") for col in feature_cols
        ]

        if use_snowpark_warehouse:
            snowpark_session.use_warehouse(snowpark_warehouse)

        classifier.fit(train_data_scaled_encoded)
        score = classifier.score(test_data_scaled_encoded)
        print(f"Accuracy: {score:.4f}")

        y_pred = classifier.predict(test_data_scaled_encoded)
        y_pred_proba = classifier.predict_proba(test_data_scaled_encoded)

        # register the Snowpark model in the Snowflake model registry
        model_id = registry.log_model(
            model=classifier,
            model_version=uuid4().urn,
            model_name="Ski Beverage Classifier",
            tags={"stage": "dev", "model_type": "LogisticRegression"},
        )

        if use_snowpark_warehouse:
            snowpark_session.use_warehouse(snowflake_regular_warehouse)
            snowpark_session.sql(
                f"""ALTER WAREHOUSE
                {snowpark_warehouse}
                SUSPEND;"""
            ).collect()

        prediction_results = pd.concat(
            [
                y_pred_proba[
                    [
                        "predict_proba_snow_mocha",
                        "predict_proba_tea",
                        "predict_proba_coffee",
                        "predict_proba_hot_chocolate",
                        "predict_proba_wine",
                    ]
                ],
                y_pred[["OUTPUT_AFTERNOON_BEVERAGE"]],
                y_test,
            ],
            axis=1,
        )

        classes = classifier.to_sklearn().classes_
        classes_df = pd.DataFrame(classes)

        # convert to string column names for parquet serialization
        prediction_results.columns = [
            str(col).replace("'", "").replace('"', "")
            for col in prediction_results.columns
        ]
        classes_df.columns = ["classes"]

        return {
            "prediction_results": prediction_results,
            "classes": classes_df,
        }

    # using a regular Airflow task to plot the results
    @task
    def plot_results(prediction_results):
        import matplotlib.pyplot as plt
        from sklearn.metrics import roc_curve, auc, ConfusionMatrixDisplay
        from sklearn.preprocessing import label_binarize

        y_pred = prediction_results["prediction_results"]["OUTPUT_AFTERNOON_BEVERAGE"]
        y_test = prediction_results["prediction_results"]["AFTERNOON_BEVERAGE"]
        y_proba = prediction_results["prediction_results"][
            [
                "predict_proba_coffee",
                "predict_proba_hot_chocolate",
                "predict_proba_snow_mocha",
                "predict_proba_tea",
                "predict_proba_wine",
            ]
        ]
        y_score = y_proba.to_numpy()
        classes = prediction_results["classes"].iloc[:, 0].values
        y_test_bin = label_binarize(y_test, classes=classes)

        fig, ax = plt.subplots(1, 2, figsize=(15, 6))

        ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax[0], cmap="Blues")
        ax[0].set_title(f"Confusion Matrix")

        fpr = dict()
        tpr = dict()
        roc_auc = dict()

        for i, cls in enumerate(classes):
            fpr[cls], tpr[cls], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc[cls] = auc(fpr[cls], tpr[cls])

            ax[1].plot(
                fpr[cls],
                tpr[cls],
                label=f"ROC curve (area = {roc_auc[cls]:.2f}) for {cls}",
            )

        ax[1].plot([0, 1], [0, 1], "k--")
        ax[1].set_xlim([0.0, 1.0])
        ax[1].set_ylim([0.0, 1.05])
        ax[1].set_xlabel("False Positive Rate")
        ax[1].set_ylabel("True Positive Rate")
        ax[1].set_title(f"ROC Curve")
        ax[1].legend(loc="lower right")

        fig.suptitle("Predicting afternoon beverage based on skiing data")

        plt.tight_layout()
        plt.savefig(f"include/metrics.png")

    if SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND:
        # clean up the XCOM table
        @task.snowpark_ext_python(
            snowflake_conn_id=SNOWFLAKE_CONN_ID,
            python="/home/astro/.venv/snowpark/bin/python",
        )
        def cleanup_xcom_table(
            snowflake_xcom_database,
            snowflake_xcom_schema,
            snowflake_xcom_table,
            snowflake_xcom_stage,
        ):
            snowpark_session.database = snowflake_xcom_database
            snowpark_session.schema = snowflake_xcom_schema

            snowpark_session.sql(
                f"""DROP TABLE IF EXISTS 
                {snowflake_xcom_database}.
                {snowflake_xcom_schema}.
                {snowflake_xcom_table};"""
            ).collect()

            snowpark_session.sql(
                f"""DROP STAGE IF EXISTS                
                {snowflake_xcom_database}.
                {snowflake_xcom_schema}.
                {snowflake_xcom_stage};"""
            ).collect()

        cleanup_xcom_table_obj = cleanup_xcom_table(
            snowflake_xcom_database=MY_SNOWFLAKE_XCOM_DATABASE,
            snowflake_xcom_schema=MY_SNOWFLAKE_XCOM_SCHEMA,
            snowflake_xcom_table=MY_SNOWFLAKE_XCOM_TABLE,
            snowflake_xcom_stage=MY_SNOWFLAKE_XCOM_STAGE,
        )

    # set dependencies
    create_model_registry_obj = create_model_registry(
        demo_database=MY_SNOWFLAKE_DATABASE, demo_schema=MY_SNOWFLAKE_SCHEMA
    )

    train_beverage_classifier_obj = train_beverage_classifier(
        transform_table_step_two(transform_table_step_one(load_file_obj)),
        database_name=MY_SNOWFLAKE_DATABASE,
        schema_name=MY_SNOWFLAKE_SCHEMA,
        use_snowpark_warehouse=USE_SNOWPARK_WAREHOUSE,
        snowpark_warehouse=MY_SNOWPARK_WAREHOUSE,
        snowflake_regular_warehouse=MY_SNOWFLAKE_REGULAR_WAREHOUSE,
    )

    chain(create_model_registry_obj, train_beverage_classifier_obj)

    plot_results_obj = plot_results(train_beverage_classifier_obj)

    if SETUP_TEARDOWN_SNOWFLAKE_CUSTOM_XCOM_BACKEND:
        chain(create_snowflake_objects_obj, load_file_obj)
        chain(
            plot_results_obj,
            cleanup_xcom_table_obj.as_teardown(setups=create_snowflake_objects_obj),
        )


airflow_with_snowpark_tutorial()
