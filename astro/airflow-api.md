---
title: 'Make Requests to the Airflow REST API'
sidebar_label: 'Airflow REST API'
id: airflow-api
description: Make requests to the Airflow REST API with Astro Deployment API Keys.
---

## Overview

You can use Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) to automate various Airflow workflows in your Deployments.

If you're looking to externally trigger DAG runs without needing to access your Airflow Deployment directly, for example, you can make an HTTP request (in Python, cURL etc.) to the corresponding endpoint in Airflow's API.

## Prerequisites

To make an Airflow API request, you need:

- A [Deployment API key](api-keys.md).
- A Deployment on Astro.
- [cURL](https://curl.se/).

## Step 1: Retrieve an Access Token and Deployment URL

All Airflow API calls require:

- An Astro access token.
- A Deployment URL.

To retrieve an Astro access token, run the following API request with your Deployment API key ID and secret:

```sh
curl --location --request POST "https://auth.astronomer.io/oauth/token" \
        --header "content-type: application/json" \
        --data-raw "{
            \"client_id\": \"<api-key-id>\",
            \"client_secret\": \"<api-key-secret>\",
            \"audience\": \"astronomer-ee\",
            \"grant_type\": \"client_credentials\"}" | jq -r '.access_token'
```

Note that this token is valid only for 24 hours. You need to refresh this token every time you make a request to the Airflow API.

To avoid manually refreshing tokens, we recommend adding a step that retrieves a new access token to any CI/CD pipeline that calls the Airflow API. That way, your access token is automatically refreshed every time your CI/CD pipeline needs it.

:::info

If you need to call the Airflow API only once, you can retrieve a single 24-hour access token at `https://cloud.astronomer.io/token` in the Cloud UI.

:::

To retrieve your Deployment URL, open your Deployment in the Cloud UI and click **Open Airflow**. The URL for the Airflow UI is your Deployment URL. It includes the name of your Organization and a short Deployment ID. For example, your Deployment URL will look similar to `https://mycompany.astronomer.run/dhbhijp0`.

## Step 2: Make an Airflow API Request

With the information from Step 1, you can now run `GET` or `POST` requests to any supported endpoints in Airflow's [Rest API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html). For example, to retrieve a list of all DAGs in a Deployment, you can run:

```sh
curl -X GET <deployment-url>/api/v1/dags -H 'Accept: application/json' -H 'Cache-Control: no-cache' -H "Authorization: Bearer <access-token>"
```

Below, we'll walk through an example request via cURL to Airflow's "Trigger DAG" endpoint and an example request via Python to the "Get all Pools" endpoint.

## Example Requests

Use the following example API requests to begin automating your own Airflow actions. For more examples, see Airflow's [Rest API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

### Trigger a DAG

If you'd like to externally trigger a DAG run, you can start with a generic cURL command to Airflow's POST endpoint:

```
POST /airflow/api/v1/dags/<dag-id>/dag_runs
```

The command for your request should look like this:

```
curl -v -X POST
<deployment-url>/api/v1/dags/<dag-id>/dag_runs
-H 'Authorization: Bearer <access-token>’
-H ‘Cache-Control: no-cache’
-H ‘content-type: application/json’ -d ‘{}’
```

Make sure to replace the following values with your own:

- `<dag-id>`
- `<deployment-url>`
- `<access-token>`

This will trigger a DAG run for your desired DAG with an `execution_date` value of `NOW()`, which is equivalent to clicking the **Play** button in the main **DAGs** view of the Airflow UI.

#### Specify Execution Date

If you have a specific `execution_date` (i.e. start timestamp) to trigger your DAG on, you can pass that in with the data parameter's JSON value `("-d'{}')`.

The string needs to be in the following format (in UTC):

```
“YYYY-MM-DDTHH:MM:SS”
```

Where, `YYYY`: Year, `MM`: Month, `DD`: Day, `HH`: Hour, `MM`: Minute, `SS`: Second.

For example:

```
“2019-11-16T11:34:00”
```

Here, your request becomes:

```
curl -v -X POST
<deployment-url>/api/v1/dags/<dag-id>/dag_runs
-H ‘Authorization: <access-token>’
-H ‘Cache-Control: no-cache’
-H ‘content-type: application/json’ -d ‘{“execution_date”:“2019-11-16T11:34:00”}’
```

### Get All Pools

If you want to get all existing Pools from your Deployment, you can start with a generic Python command to Airflow's `GET` endpoint:

```
GET /api/v1/pools
```

Here, your request would look like this:

```python
python
import requests
token="<access-token>"
base_url="<deployment-url>"
resp = requests.get(
   url=base_url + "/api/v1/pools",
   headers={"Authorization": token},
   data={}
)
print(resp.json())
>>>>  [{'description': 'Default pool', 'id': 1, 'pool': 'default_pool', 'slots': 128}]
```
