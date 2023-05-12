from datetime import datetime
import os

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table
from airflow.decorators import dag, task_group

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import tempfile
import pickle
from pathlib import Path

import wandb
from wandb.sklearn import plot_precision_recall, plot_feature_importances
from wandb.sklearn import plot_class_proportions, plot_learning_curve, plot_roc

_POSTGRES_CONN = "postgres_default"
wandb_project = "demo"
wandb_team = "astro-demos"
local_data_dir = "include/data"
sources = ["subscription_periods", "util_months", "customers", "orders", "payments"]


@dag(schedule=None, start_date=datetime(2023, 1, 1), catchup=False)
def customer_analytics():
    @task_group()
    def extract_and_load(sources: list) -> dict:
        for source in sources:
            aql.load_file(
                task_id=f"load_{source}",
                input_file=File(f"{local_data_dir}/{source}.csv"),
                output_table=Table(
                    name=f"STG_{source.upper()}", conn_id=_POSTGRES_CONN
                ),
                if_exists="replace",
            )

    @task_group()
    def transform():
        aql.transform_file(
            task_id="transform_churn",
            file_path=f"{Path(__file__).parent.as_posix()}/../include/customer_churn_month.sql",
            parameters={
                "subscription_periods": Table(
                    name="STG_SUBSCRIPTION_PERIODS", conn_id=_POSTGRES_CONN
                ),
                "util_months": Table(name="STG_UTIL_MONTHS", conn_id=_POSTGRES_CONN),
            },
            op_kwargs={
                "output_table": Table(
                    name="CUSTOMER_CHURN_MONTH", conn_id=_POSTGRES_CONN
                )
            },
        )

        aql.transform_file(
            task_id="transform_customers",
            file_path=f"{Path(__file__).parent.as_posix()}/../include/customers.sql",
            parameters={
                "customers_table": Table(name="STG_CUSTOMERS", conn_id=_POSTGRES_CONN),
                "orders_table": Table(name="STG_ORDERS", conn_id=_POSTGRES_CONN),
                "payments_table": Table(name="STG_PAYMENTS", conn_id=_POSTGRES_CONN),
            },
            op_kwargs={"output_table": Table(name="CUSTOMERS", conn_id=_POSTGRES_CONN)},
        )

    @aql.dataframe()
    def features(customer_df: pd.DataFrame, churned_df: pd.DataFrame) -> pd.DataFrame:
        customer_df["customer_id"] = customer_df["customer_id"].apply(str)
        customer_df.set_index("customer_id", inplace=True)

        churned_df["customer_id"] = churned_df["customer_id"].apply(str)
        churned_df.set_index("customer_id", inplace=True)
        churned_df["is_active"] = churned_df["is_active"].astype(int).replace(0, 1)

        df = (
            customer_df[["number_of_orders", "customer_lifetime_value"]]
            .join(churned_df[["is_active"]], how="left")
            .fillna(0)
            .reset_index()
            )  # inplace=True)

        return df

    @aql.dataframe()
    def train(df: pd.DataFrame) -> dict:
        features = ["number_of_orders", "customer_lifetime_value"]
        target = ["is_active"]

        test_size = 0.3
        X_train, X_test, y_train, y_test = train_test_split(
            df[features], df[target], test_size=test_size, random_state=1883
        )
        X_train = np.array(X_train.values.tolist())
        y_train = np.array(y_train.values.tolist()).reshape(
            len(y_train),
        )
        y_train = y_train.reshape(
            len(y_train),
        )
        X_test = np.array(X_test.values.tolist())
        y_test = np.array(y_test.values.tolist())
        y_test = y_test.reshape(
            len(y_test),
        )

        model = RandomForestClassifier()
        _ = model.fit(X_train, y_train)
        model_params = model.get_params()

        y_pred = model.predict(X_test)
        y_probas = model.predict_proba(X_test)
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        wandb.login()
        run = wandb.init(
            project=wandb_project,
            config=model_params,
            entity=wandb_team,
            group="wandb-demo",
            name="jaffle_churn",
            dir="include",
            mode="online",
        )

        wandb.config.update(
            {"test_size": test_size, "train_len": len(X_train), "test_len": len(X_test)}
        )
        plot_class_proportions(y_train, y_test, ["not_churned", "churned"])
        plot_learning_curve(model, X_train, y_train)
        plot_roc(y_test, y_probas, ["not_churned", "churned"])
        plot_precision_recall(y_test, y_probas, ["not_churned", "churned"])
        plot_feature_importances(model)

        model_artifact_name = "churn_classifier"

        with tempfile.NamedTemporaryFile(delete=False) as tf:
            pickle.dump(model, tf)
            tf.close()
            artifact = wandb.Artifact(model_artifact_name, type="model")
            artifact.add_file(local_path=tf.name, name=model_artifact_name)
            wandb.log_artifact(artifact)
            os.remove(tf.name)

        wandb.finish()

        return {"run_id": run.id, "artifact_name": model_artifact_name}

    @aql.dataframe()
    def predict(model_info: dict, customer_df: pd.DataFrame) -> pd.DataFrame:
        wandb.login()
        run = wandb.init(
            project=wandb_project,
            entity=wandb_team,
            group="wandb-demo",
            name="jaffle_churn",
            dir="include",
            resume="must",
            id=model_info["run_id"],
        )

        customer_df.fillna(0, inplace=True)

        features = ["number_of_orders", "customer_lifetime_value"]

        artifact = run.use_artifact(
            f"{model_info['artifact_name']}:latest", type="model"
        )

        with tempfile.TemporaryDirectory() as td:
            with open(artifact.file(td), "rb") as mf:
                model = pickle.load(mf)
                customer_df["PRED"] = model.predict_proba(
                    np.array(customer_df[features].values.tolist())
                )[:, 0]

        wandb.finish()

        customer_df.reset_index(inplace=True)

        return customer_df

    _extract_and_load = extract_and_load(sources)

    _transformed = transform()

    _features = features(
        customer_df=Table(name="customers", conn_id=_POSTGRES_CONN),
        churned_df=Table(name="customer_churn_month", conn_id=_POSTGRES_CONN),
    )

    _model_info = train(df=_features)

    _predict_churn = predict(
        model_info=_model_info,
        customer_df=Table(name="customers", conn_id=_POSTGRES_CONN),
        output_table=Table(name=f"pred_churn", conn_id=_POSTGRES_CONN),
    )

    _extract_and_load >> _transformed >> _features


customer_analytics()
