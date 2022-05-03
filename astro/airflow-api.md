---
title: 'Make Requests to the Airflow REST API'
sidebar_label: 'Airflow REST API'
id: airflow-api
description: Make requests to the Airflow REST API with Astro Deployment API Keys.
---

## Overview

You can use Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) to automate various Airflow workflows in your Deployments.

For example, if you're looking to externally trigger DAG runs without accessing your Airflow Deployment directly, you can make an HTTP request (in Python, cURL etc.) to the [corresponding endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) in Airflow's API.

## Prerequisites

To make an Airflow API request, you need:

- A [Deployment API key](api-keys.md).
- A Deployment on Astro.
- [cURL](https://curl.se/).

## Step 1: Retrieve an Access Token and Deployment URL

All calls to your Deployment's Airflow API require:

- An Astro access token.
- A Deployment URL.

To retrieve an Astro access token, run the following API request with your Deployment API key ID and secret:

```sh
curl --location --request POST "https://auth.astronomer.io/oauth/token" \
        --header "content-type: application/json" \
        --data-raw '{
            "client_id": "<api-key-id>",
            "client_secret": "<api-key-secret>",
            "audience": "astronomer-ee",
            "grant_type": "client_credentials"}'
```

:::info

Note that this token is only valid for 24 hours.

If you need to call the Airflow API only once, you can retrieve a single 24-hour access token at `https://cloud.astronomer.io/token` in the Cloud UI.

In automated processes (such as a [CI/CD pipeline](https://docs.astronomer.io/astro/ci-cd)), we recommend including logic to generate a fresh access token. For example, adding a step in in a CI/CD pipeline that automatically generates an API access token would remove the need to generate that token manually every 24 hours.

:::

To retrieve your Deployment URL, open your Deployment in the Cloud UI and click **Open Airflow**. The URL for the Airflow UI is your Deployment URL minus `/home`. It includes the name of your Organization and a short Deployment ID. For a Deployment with an ID `dhbhijp0` that is part of an Organization called `mycompany`, for example, the Deployment URL would be: `https://mycompany.astronomer.run/dhbhijp0`.

## Step 2: Make an Airflow API Request

With the information from Step 1, you can now execute requests against any supported endpoints in Airflow's [Rest API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

For all requests, replace `<access-token>` and `<deployment-url>` with the values obtained in Step 1, and replace `<dag-id>` with your own DAG ID where applicable.

For example, to retrieve a list of all DAGs in a Deployment, you can run a `GET` request to the [`dags` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags)

Using cURL:

```sh
curl -X GET <deployment-url>/api/v1/dags \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <access-token>'
```

Using Python:
```python
import requests
token = "<access-token>"
deployment_url = "<deployment-url>"
response = requests.get(
   url=f"{deployment_url}/api/v1/dags",
   headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
# Prints data about all DAGs in your Deployment
```

Let's walk through another example. Below, we'll trigger a DAG Run by executing a `POST` request to Airflow's [`dagRuns` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run).

Using cURL:
```sh
curl -X POST <deployment-url>/api/v1/dags/<dag-id>/dagRuns \
   -H 'Content-Type: application/json' \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <access-token>' \
   -d '{}'
```

Using Python:
```python
import requests
token = "<access-token>"
deployment_url = "<deployment-url>"
dag_id = "<dag-id>"
response = requests.post(
    url=f"{deployment_url}/api/v1/dags/{dag_id}/dagRuns",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{}'
)
print(response.json())
# Prints metadata of the DAG Run that was just triggered
```

This will trigger a DAG run for the DAG you specify with a `logical_date` value of `NOW()`, which is equivalent to clicking the **Play** button in the main **DAGs** view of the Airflow UI.

You can also specify a `logical_date` at the time in which you wish to trigger the DAG run by passing the `logical_date` with the desired timestamp with the request's `data` field. The timestamp string is expressed in UTC and must be specified in the format `"YYYY-MM-DDTHH:MM:SSZ"` where, `YYYY` represents the year, `MM` represents the month, `DD` represents the day, `HH` represents the hour, `MM` represents the minute, and `SS` represents the second, and `Z` stands for "Zulu" time, which represents UTC. For example:

Using cURL:
```sh
curl -v -X POST <deployment-url>/api/v1/dags/<dag-id>/dagRuns \
   -H 'Authorization: Bearer <access-token>' \
   -H 'Cache-Control: no-cache' \
   -H 'content-type: application/json' \
   -d '{"logical_date":"2021-11-16T11:34:00Z"}'
```

Using Python:
```python
import requests
token = "<access-token>"
deployment_url = "<deployment-url>"
dag_id = "<dag-id>"
response = requests.post(
    url=f"{deployment_url}/api/v1/dags/{dag_id}/dagRuns",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{"logical_date": "2021-11-16T11:34:01Z"}'
)
print(response.json())
# Prints metadata of the DAG Run that was just triggered
```

As a final example, we'll demonstrate pausing a given DAG by executing a `PATCH` command against the [`dag` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag).

Using cURL:
```sh
curl -X PATCH <deployment-url>/api/v1/dags/<dag-id> \
   -H 'Content-Type: application/json' \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <access-token>' \
   -d '{"is_paused": true}'
```

Using Python:
```python
import requests
token = "<access-token>"
deployment_url = "<deployment-url>"
dag_id = "<dag-id>"
response = requests.patch(
    url=f"{deployment_url}/api/v1/dags/{dag_id}",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{"is_paused": true}'
)
print(response.json())
# Prints data about the DAG with id <dag-id>
```
