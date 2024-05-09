---
title: "Cross-deployment dependencies"
sidebar_label: "Cross-deployment dependencies"
description: "How to implement dependencies between your Airflow deployments."
id: cross-deployment-dependencies
---

import CodeBlock from '@theme/CodeBlock';

[Cross-DAG dependencies](https://docs.astronomer.io/learn/cross-dag-dependencies.md) serve a common use case: configuring a DAG to run when a separate DAG or a task in another DAG completes or updates a dataset. But what about situations in which a dataset or DAG you monitor exists in a separate deployment? For example, you might want to make a task dependent on a dataset update in a DAG that is owned by a different team and located in a separate deployment. Astro also supports the orchestration of tasks using this kind of relationship, which is referred to as a *cross-deployment dependency*.  

This guide uses the following terms to describe cross-deployment dependencies:

- **Upstream deployment**: A deployment where a DAG must reach a specified state before a DAG in another deployment can run.
- **Downstream deployment**: A deployment in which a DAG cannot run until a DAG in an upstream deployment reaches a specified state.

Cross-deployment dependencies require special implementation because methods such as TriggerDagRunOperator and ExternalTaskSensor are only designed for DAGs in the same deployment. On Astro, there are two recommended methods available for implementing cross-deployment dependencies: Astro Alerts and Airflow Datasets.

## Feature overview

In this guide, you'll learn when to use the following Astro and Airflow features to create dependencies across Astro deployments. Astro supports cross-deployment dependencies in any Workspace or cluster.

- [Astro Alerts](https://docs.astronomer.io/astro/alerts). Recommended for most Astro use cases as no code modification is required.
- [Airflow Datasets](https://docs.astronomer.io/learn/airflow-datasets.md). Can be used to trigger a DAG after a task in another DAG updates a dataset.

## Best practice guidance

Astro Alerts and Airflow Datasets are the best methods for implementing cross-deployment dependencies. The `dagRuns` endpoint of the Airflow API can also be used for this purpose, but it is less flexible than the other methods and not recommended.

To determine whether an Astro Alert or the Datasets feature is the right solution for your use case, consider the following guidance. 

**Astro Alerts:**

You can use Astro alerts to implement cross-deployment DAG dependencies using the DAG trigger communication channel. They are simple to implement and are the preferred method in the following situations: 
- If you need to implement a dependency trigger based on any DAG state other than success, such as a DAG failure, a task taking longer than expected, or a DAG not completing by a certain time. 
- If you need to implement a simple one-to-one cross-deployment dependency (one upstream DAG triggers one downstream DAG) and do not want to update your DAG code.
- When your DAGs do not already use the Datasets feature and when it is easy to identify the relevant dependent DAGs, which is not always the case in larger organizations. 

**Airflow Datasets:**

Datasets represent a significant evolution in the way Airflow can be used to define dependencies and, for some, offer a more natural way of expressing pipelines than traditional DAGs. Datasets offer more flexibility for cross-deployment dependencies than Astro alerts, are the preferred method in the following scenarios:
- You need to implement dependencies in a many-to-one pattern, so you can make a DAG dependent on the completion of multiple other DAGs or tasks. This is not possible using Astro Alerts.
- You need to implement dependencies in a one-to-many pattern, so one DAG or task triggers multiple DAGs or tasks. While this is also possible using Astro Alerts, it requires a separate alert for each dependency.

:::tip

Before Airflow 2.9, Datasets were only available within a single deployment. As of Airflow 2.9, you can update a dataset with a `POST` request to the [datasets endpoint of the Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Dataset), which supports implementation across deployments.

:::

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

Create a dependency between DAGs in separate deployments with an alert trigger on Astro. 

1. First, [create a Deployment API token](https://docs.astronomer.io/astro/deployment-api-tokens) for the upstream Deployment.
2. Click [**Alerts**](https://docs.astronomer.io/astro/alerts) in the Workspace menu, and create a new alert.
3. Enter an **Alert name** that you'll remember, select the **Alert type** (like **DAG Success**), and then select **DAG Trigger** as the **Communication Channel**.
4. In the **Deployment** menu for the **DAG Trigger** communication channel, select the downstream deployment from the list.
5. In the **DAG NAME** menu, select the DAG you want to trigger.
6. Paste your API token in the **DEPLOYMENT API TOKEN** field.
7. Run the upstream DAG, verify that the alert triggers, and confirm the downstream DAG runs as expected.

![Alert dialog](/img/guides/cross-deployment-alert-dialog.png)

## Datasets example

### Assumed knowledge

To use Airflow Datasets to create cross-deployment dependencies, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](https://docs.astronomer.io/learn/dags.md).
- [Airflow Datasets](https://docs.astronomer.io/learn/airflow-datasets.md).
- The [Airflow API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

### Implementation

This section explains how to use a listener in combination with the [Airflow API's Datasets endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Dataset) to trigger the downstream DAG in another deployment when a dataset is updated. Typical dataset implementation only works for DAGs in the same Airflow deployment, but by using the Airflow API, this pattern can be implemented across deployments.

While you can also use the HttpOperator to make the API request to update the dataset, an advantage of using a listener is that the dataset is updated and the downstream DAG runs whenever _any_ DAG updates the dataset. This means you don't need to implement an API call in every upstream DAG that updates the same dataset.
 
#### Prerequisites

- Two [Astro Deployments](https://docs.astronomer.io/astro/create-deployment).
- A [Deployment API token](https://docs.astronomer.io/astro/deployment-api-tokens), [Workspace API token](https://docs.astronomer.io/astro/workspace-api-tokens), or [Organization API token](https://docs.astronomer.io/astro/organization-api-tokens) for one of your deployments. This deployment will host your downstream DAG.
- Two [Astro projects](https://docs.astronomer.io/astro/cli/develop-project#create-an-astro-project).

#### Process

1. In your upstream Deployment, which is the Deployment for which you did **not** create an API Token, use **Variables** in the Astro UI to create an environment variable for your API token, and use `API_TOKEN` for the key.
2. For your downstream Deployment, follow the guidance in [Airflow REST API](https://docs.astronomer.io/astro/airflow-api#step-2-retrieve-the-deployment-url) to obtain the Deployment URL for your downstream Deployment. 
3. In your upstream Deployment, use Variables in the Astro UI to create an environment variable where you can store your downstream Deployment URL, using `DEPLOYMENT_URL` for the key.
4. In the upstream Deployment, implement a listener following the guidance in the [Create Airflow listeners tutorial](https://docs.astronomer.io/learn/airflow-listeners). Use the following code in place of the `listeners_code.py` code provided there:

```python
from airflow.datasets import Dataset
from airflow.listeners import hookimpl
import requests
import os

TOKEN = os.environ.get("API_TOKEN")
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

```python
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
6. Deploy a DAG of any kind to your downstream Deployment. In this DAG, use a `dag_id` of `consumer_dag` and schedule it on the same dataset in the `producer_dag`.

For example:

```python
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

After deploying both projects to their respective deployments on Astro, you should see your `consumer_dag` being triggered automatically by runs of your `producer_dag`. If the downstream DAG is not firing, verify that the upstream deployment's environment variables (the API token and deployment URL) correspond to the downstream deployment. Also, a properly functioning listener will emit an API response payload containing DAG run information related to the dataset. Check the task logs for output that looks similar to this:

```
{\'created_dagruns\': [], \'dataset_id\': 2, \'dataset_uri\': \'file://include/bears\', \'extra\': {\'from_rest_api\': True}, \'id\': 3, \'source_dag_id\': None, \'source_map_index\': -1, \'source_run_id\': None, \'source_task_id\': None, \'timestamp\': \'2024-05-07T21:52:40.295802+00:00\'}
```

## See also

- Creating [cross-DAG dependencies](https://docs.astronomer.io/learn/cross-dag-dependencies.md).
- Setting up [alerts](https://docs.astronomer.io/astro/alerts).
