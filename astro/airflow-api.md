---
title: 'Make requests to the Airflow REST API'
sidebar_label: 'Airflow REST API'
id: airflow-api
---

<head>
  <meta name="description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
  <meta name="og:description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
</head>

This guide explains how to make requests to Airflow's REST API for your Deployments.

You can use Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) to automate various Airflow workflows in your Deployments. For example, you can externally trigger a DAG run without accessing your Deployment directly by making an HTTP request in Python or cURL to the [corresponding endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) in the Airflow REST API.


To test Airflow API calls in a local Airflow environment running with the Astro CLI, see [Test and Troubleshoot Locally](test-and-troubleshoot-locally.md#make-requests-to-the-airflow-rest-api).

## Prerequisites

- A [Deployment API key](api-keys.md).
- A Deployment on Astro.
- [cURL](https://curl.se/).

## Step 1: Retrieve an access token and Deployment URL

Calling the Airflow REST API for a Deployment requires:

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

Note that this token is only valid for 24 hours. If you need to call the Airflow API only once, you can retrieve a single 24-hour access token at `https://cloud.astronomer.io/token` in the Cloud UI.

If you have an automated [CI/CD process](ci-cd.md) configured, we recommend including logic to generate a fresh access token. If you add a step to your CI/CD pipeline that automatically generates an API access token, for example, you can avoid having to generate the token manually.

:::

To retrieve your Deployment URL, open your Deployment in the Cloud UI and click **Open Airflow**. The Deployment URL is the URL for the Airflow UI homepage up until `/home`. It includes the name of your Organization and a short Deployment ID. For example, a Deployment with an ID `dhbhijp0` that is part of an Organization called `mycompany` would have a Deployment URL of `https://mycompany.astronomer.run/dhbhijp0`.

## Step 2: Make an Airflow API request

You can now execute requests against any endpoint that is listed in the [Airflow Rest API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).
To make a request based on Airflow documentation, make sure to:

- Replace `https://airflow.apache.org` with your Deployment URL
- Use the Astro access token for authentication

## Example API Requests

The following topic contains common examples of API requests that you can run against a Deployment.

### List DAGs

To retrieve a list of all DAGs in a Deployment, you can run a `GET` request to the [`dags` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags)

#### cURL

```sh
curl -X GET <deployment-url>/api/v1/dags \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <your-access-token>'
```

#### Python

```python
import requests
token = "<your-access-token>"
deployment_url = "<your-deployment-url>"
response = requests.get(
   url=f"{deployment_url}/api/v1/dags",
   headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
# Prints data about all DAGs in your Deployment
```

### Trigger a DAG run

You can trigger a DAG run by executing a `POST` request to Airflow's [`dagRuns` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run).

This will trigger a DAG run for the DAG you specify with a `logical_date` value of `NOW()`, which is equivalent to clicking the **Play** button in the main **DAGs** view of the Airflow UI.

#### cURL

```sh
curl -X POST <your-deployment-url>/api/v1/dags/<your-dag-id>/dagRuns \
   -H 'Content-Type: application/json' \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <your-access-token>' \
   -d '{}'
```

#### Python

```python
import requests
token = "<your-access-token>"
deployment_url = "<your-deployment-url>"
dag_id = "<your-dag-id>"
response = requests.post(
    url=f"{deployment_url}/api/v1/dags/{dag_id}/dagRuns",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{}'
)
print(response.json())
# Prints metadata of the DAG run that was just triggered
```

### Trigger a DAG run by date

You can also specify a `logical_date` at the time in which you wish to trigger the DAG run by passing the `logical_date` with the desired timestamp with the request's `data` field. The timestamp string is expressed in UTC and must be specified in the format `"YYYY-MM-DDTHH:MM:SSZ"`, where:

- `YYYY` represents the year.
- `MM` represents the month.
- `DD` represents the day.
- `HH` represents the hour.
- `MM` represents the minute.
- `SS` represents the second.
- `Z` stands for "Zulu" time, which represents UTC.

#### cURL

```sh
curl -v -X POST <your-deployment-url>/api/v1/dags/<your-dag-id>/dagRuns \
   -H 'Authorization: Bearer <your-access-token>' \
   -H 'Cache-Control: no-cache' \
   -H 'content-type: application/json' \
   -d '{"logical_date":"2021-11-16T11:34:00Z"}'
```

#### Python

Using Python:
```python
import requests
token = "<your-access-token>"
deployment_url = "<your-deployment-url>"
dag_id = "<your-dag-id>"
response = requests.post(
    url=f"{deployment_url}/api/v1/dags/{dag_id}/dagRuns",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{"logical_date": "2021-11-16T11:34:01Z"}'
)
print(response.json())
# Prints metadata of the DAG run that was just triggered
```

### Pause a DAG

You can pause a given DAG by executing a `PATCH` command against the [`dag` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag).

#### cURL

```sh
curl -X PATCH <your-deployment-url>/api/v1/dags/<your-dag-id> \
   -H 'Content-Type: application/json' \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <your-access-token>' \
   -d '{"is_paused": true}'
```

#### Python

```python
import requests
token = "<your-access-token>"
deployment_url = "<your-deployment-url>"
dag_id = "<your-dag-id>"
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
