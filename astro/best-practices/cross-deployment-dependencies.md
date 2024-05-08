---
title: "Cross-deployment dependencies"
sidebar_label: "Cross-deployment dependencies"
description: "How to implement dependencies between your Airflow deployments."
id: cross-deployment-dependencies
---

import CodeBlock from '@theme/CodeBlock';

[Cross-DAG dependencies](https://docs.astronomer.io/learn/cross-dag-dependencies.md) serve a common use case: configuring a DAG to run when a separate DAG or a task in another DAG completes or updates a dataset. But what about situations in which a dataset or DAG you are monitoring exists in a separate deployment? For example, you might want to make a task dependent on a dataset's being updated by a DAG that is owned by a different team and, hence, located in a separate deployment. Astro also supports the orchestration of tasks via this kind of relationship, which is referred to as a cross-deployment dependency.  

In this guide, the following terms are used to describe cross-deployment dependencies:

- **Upstream deployment**: a deployment in which a DAG must reach a specified state before a DAG in another deployment can run.
- **Downstream deployment**: a deployment in which a DAG cannot run until a DAG in an upstream deployment reaches a specified state.

Cross-deployment dependencies require special implementation because some of the methods used for creating cross-DAG dependencies – for example, TriggerDagRunOperator or ExternalTaskSensor – are only designed for DAGs in the same deployment. On Astro, there are two recommended methods available for implementing cross-deployment dependencies: Astro Alerts and Airflow Datasets.

In this guide, you'll learn how to use Astro Alerts and Airflow Datasets to create cross-deployment dependencies. Astro supports cross-deployment dependencies in any Workspace or cluster. 

## Feature overview

This guide explains when to use the following Astro and Airflow features to create dependencies across Astro deployments:

- [Astro Alerts](https://docs.astronomer.io/astro/alerts). Recommended for most Astro use cases as no code modification is required.
- [Airflow Datasets](https://docs.astronomer.io/learn/airflow-datasets.md). Can be used to trigger a DAG after a task in another DAG updates a dataset.

## Best practice guidance

Astro Alerts and Airflow Datasets are the best methods for implementing cross-deployment dependencies. The `dagRuns` endpoint of the Airflow API can also be used for this purpose, but it is less flexible than the other methods and, therefore, not recommended.

To determine whether an Astro Alert or the Datasets feature is the right solution for your use case, consider the following guidance. 

**Astro Alerts:**

Astro alerts can be used to implement cross-deployment DAG dependencies using the DAG trigger communication channel. They are simple to implement and are the preferred method in the following situations: 
- If you need to implement a dependency trigger based on any DAG state other than success, such as a DAG failure, a task taking longer than expected, or a DAG not completing by a certain time. 
- If you need to implement a simple one-to-one cross-deployment dependency (one upstream DAG triggers one downstream DAG) and do not want to update your DAG code.
- When your DAGs do not already use the Datasets feature and when it is easy to identify the relevant dependent DAGs, which is not always the case in larger organizations. 

**Airflow Datasets:**

Datasets represent a significant evolution in the way Airflow can be used to define dependencies and, for some users, offer a more natural way of expressing pipelines than traditional DAGs. They offer more flexibility for cross-deployment dependencies than Astro alerts, are the preferred method in the following scenarios:
- You need to implement dependencies in a many-to-one pattern, such that a DAG can be made dependent on the completion of multiple other DAGs or tasks. This is not possible using Astro Alerts.
- You need to implement dependencies in a one-to-many pattern, such that multiple DAGs or tasks are triggered by one DAG or task. This is also possible using Astro Alerts, but requires a separate alert for each dependency.

**Note:** Before Airflow 2.9, Datasets were only available within a single deployment. As of Airflow 2.9, you can update a dataset with a `POST` request to the [datasets endpoint of the Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Dataset), which supports implementation across deployments.

## Astro alerts example

### Assumed knowledge

To use Astro Alerts to create cross-deployment dependencies, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](https://docs.astronomer.io/learn/dags.md).
- Creating and managing Astro deployments. See [Create a deployment](https://docs.astronomer.io/astro/create-deployment).

### Implementation

This example shows you how to create dependencies between DAGs in different Astro deployments using Astro Alerts.

#### Prerequisites

- Two [Astro Deployments](https://docs.astronomer.io/astro/create-deployment), each containing at least one DAG.

#### Process

Creating a dependency between DAGs in separate deployments is easy with an alert trigger on Astro. 

1. First, [create a deployment API token](https://docs.astronomer.io/astro/deployment-api-tokens) for the upstream deployment.
2. Navigate to [Alerts](https://docs.astronomer.io/astro/alerts) in the workspace sidebar and create a new alert.
3. Give the alert a name you'll remember, select an alert type (e.g., `DAG Success`), and then select `DAG Trigger` as the communication channel.
4. In the deployment dropdown menu for the `DAG Trigger` communication channel, select the downstream deployment.
5. In the `DAG NAME` dropdown, select the DAG to be triggered.
6. Paste your API token in the `DEPLOYMENT API TOKEN` field.
7. Run the upstream DAG and verify that the alert triggers and the downstream DAG runs as expected.

![Alert dialog](/img/guides/cross-deployment-alert-dialog.png)

## Datasets example

### Assumed knowledge

To use Airflow Datasets to create cross-deployment dependencies, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](https://docs.astronomer.io/learn/dags.md).
- [Airflow Datasets](https://docs.astronomer.io/learn/airflow-datasets.md).
- The [Airflow API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

### Implementation

This section explains how to use a listener in combination with the [Airflow API's Datasets endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Dataset) to trigger the downstream DAG in another deployment when a dataset is updated. Typical dataset implementation only works for DAGs in the same Airflow deployment, but by using the API, this pattern can be implemented across deployments.

While HttpOperator could also be used to make the API request to update the dataset, an advantage of using a listener is that the dataset will be updated and the downstream DAG will run whenever _any_ DAG updates the dataset. This avoids the need to implement an API call in every upstream DAG that updates the same dataset.
 
#### Prerequisites

- Two [Astro Deployments](https://docs.astronomer.io/astro/create-deployment).
- A [Deployment API token](https://docs.astronomer.io/astro/deployment-api-tokens), [Workspace API token](https://docs.astronomer.io/astro/workspace-api-tokens), or [Organization API token](https://docs.astronomer.io/astro/organization-api-tokens) for one of your deployments. This deployment will host your downstream DAG.
- Two [Astro projects](https://docs.astronomer.io/astro/cli/develop-project#create-an-astro-project).

#### Process

1. In the deployment you did **not** get your token from (your upstream deployment) use Variables in Astro to create an environment variable for your API token and use `API_KEY` for the key.
2. Following the guidance in [Airflow REST API](https://docs.astronomer.io/astro/airflow-api#step-2-retrieve-the-deployment-url), obtain the deployment URL for your downstream deployment and store it in an environment variable in your upstream deployment alongside the API token variable, using `DEPLOYMENT_URL` for the key.
3. In the upstream deployment, implement a listener following the guidance in the [Create Airflow listeners tutorial](https://docs.astronomer.io/learn/airflow-listeners). Use the following code in place of the `listeners_code.py` code provided there:

```
from airflow.datasets import Dataset
from airflow.listeners import hookimpl
import requests
import os

TOKEN = os.environ.get("API_KEY")
DEPLOYMENT_URL = os.environ.get("DEPLOYMENT_URL")

@hookimpl
def on_dataset_changed(dataset: Dataset):
    """Execute if a dataset is updated."""
    if dataset.uri == "file://include/bears":
        payload = {
            "dataset_uri": dataset.uri
        }
        response = requests.post(
            url=f"https://{DEPLOYMENT_URL}/api/v1/datasets/events",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json=payload
        )
        print(response.json())

```

4. Add the following DAG to your Astro project.

```
from airflow.datasets import Dataset
from airflow.decorators import dag, task
from pendulum import datetime

URI = "file://include/bears"
MY_DATASET = Dataset(URI)

@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * 0",
    catchup=False,
    doc_md=__doc__,
)
def producer_dag():
    @task(
        outlets=[MY_DATASET],
    )
    def get_bear():
        print("Update the bears dataset")

    get_bear()

producer_dag()

```

5. Deploy the project to Astro.
6. Deploy a DAG of any kind to your downstream deployment, using a `dag_id` of `consumer_dag` and scheduling it on the same dataset in the `producer_dag`.

For example:

```
from airflow.decorators import dag, task
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.datasets import Dataset

URI = "file://include/bears"

@dag(
    dag_id="consumer_dag",
    start_date=datetime(2023, 12, 1),
    schedule=[Dataset(URI)],
    catchup=False,
    doc_md=__doc__,
)
def consumer_dag():
    @task(task_id="empty")
    def nada(): EmptyOperator()

    nada()

consumer_dag()

```

After deploying both projects to their respective deployments on Astro, you should see your `consumer_dag` being triggered automatically by runs of your `producer_dag`. If the downstream DAG is not firing, verify that the upstream deployment's environment variables (the API key and deployment URL) correspond to the downstream deployment. Also, a properly functioning listener will emit an API response payload containing DAG run information related to the dataset. Check the task logs for output that looks similar to this:

```
{\'created_dagruns\': [], \'dataset_id\': 2, \'dataset_uri\': \'file://include/bears\', \'extra\': {\'from_rest_api\': True}, \'id\': 3, \'source_dag_id\': None, \'source_map_index\': -1, \'source_run_id\': None, \'source_task_id\': None, \'timestamp\': \'2024-05-07T21:52:40.295802+00:00\'}
```

## See also

- Creating [cross-DAG dependencies](https://docs.astronomer.io/learn/cross-dag-dependencies.md).
- Setting up [alerts](https://docs.astronomer.io/astro/alerts).
