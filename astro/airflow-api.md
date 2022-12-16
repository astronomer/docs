---
title: 'Make requests to the Airflow REST API'
sidebar_label: 'Airflow REST API'
id: airflow-api
---

<head>
  <meta name="description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
  <meta name="og:description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
</head>

You can use the Airflow [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) to automate Airflow workflows in your Deployments on Astro. For example, you can externally trigger a DAG run without accessing your Deployment directly by making an HTTP request in Python or cURL to the [dagRuns endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) in the Airflow REST API.

To test Airflow API calls in a local Airflow environment running with the Astro CLI, see [Test and Troubleshoot Locally](test-and-troubleshoot-locally.md#make-requests-to-the-airflow-rest-api).

:::info

Updates to the Airflow REST API are released in new Airflow versions and new releases don’t have a separate release cycle or versioning scheme. To take advantage of specific Airflow REST API functionality, you might need to upgrade Astro Runtime. See [Upgrade Runtime](upgrade-runtime.md) and the [Airflow release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

:::

## Prerequisites

- A Deployment on Astro.
- A [Deployment API key](api-keys.md).
- [cURL](https://curl.se/).

## Step 1: Retrieve an access token and Deployment URL

Calling the Airflow REST API for a Deployment requires:

- An Astro access token.
- A Deployment URL.

### Retrieve an access token

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

If you've configured a [CI/CD process](ci-cd.md) and you want to avoid generating an access token manually, Astronomer recommends that you automate the API request to generate a new access token.

:::

### Retrieve the Deployment URL

<PremiumBadge />

The Deployment URL includes the name of your Organization and a short Deployment ID. For example, a Deployment with an ID `dhbhijp0` that is part of an Organization called `mycompany` would have a Deployment URL of `https://mycompany.astronomer.run/dhbhijp0`.

1. In the Cloud UI, select a Workspace and then a Deployment.
2. Click **Open Airflow**.
3. When the Airflow UI opens in your browser, copy the URL up to `/home`.

## Step 2: Make an Airflow API request

You can execute requests against any endpoint that is listed in the [Airflow REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

To make a request based on Airflow documentation, make sure to:

- Use the Astro access token from Step 1 for authentication.
- Replace `https://airflow.apache.org` with your Deployment URL from Step 1.

## Example API Requests

The following are common examples of Airflow REST API requests that you can run against a Deployment on Astro.

### List DAGs

To retrieve a list of all DAGs in a Deployment, you can run a `GET` request to the [`dags` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags)

#### cURL

```sh
curl -X GET <your-deployment-url>/api/v1/dags \
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
   -d '{"logical_date":"2022-11-16T11:34:00Z"}'
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

You can pause a DAG by executing a `PATCH` command against the [`dag` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag).

Replace `<your-dag-id>` with your own value.

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
## Trigger DAG runs across Deployments

You can use the Airflow REST API to make a request in one Deployment that triggers a DAG run in a different Deployment. This is sometimes necessary when you have interdependent workflows across multiple Deployments. On Astro, you can do this for any Deployment in any Workspace or cluster. 

This topic has guidelines on how to trigger a DAG run, but you can modify the example DAG provided to trigger any request that's supported in the Airflow REST API.

1. On the target Deployment, create an API key ID and API key secret. See [Create an API key](api-keys.md#create-an-api-key).

2. On the triggering Deployment, set the API key ID and API key secret from the target Deployment as `KEY_ID` and `KEY_SECRET` environment variables in the Cloud UI. Make `KEY_SECRET` secret. See [Set environment variables on Astro](environment-variables.md).

3. In your DAG, write a task called `get-token` that uses your Deployment API key ID and secret to make a request to the Astronomer API that retrieves the access token that's required for authentication to the Airflow API. In another task called `trigger_external_dag`, use the access token to make a request to the `dagRuns` endpoint of the Airflow REST API. Make sure to replace `<target-deployment-url>` with your own value. For example:

    ````python
    import requests
    from datetime import datetime
    import os
    from airflow.decorators import dag, task
    KEY_ID = os.environ.get("KEY_ID")
    KEY_SECRET = os.environ.get("KEY_SECRET")
    AIRFLOW_URL = "<target-deployment-url>"
    @dag(schedule="@daily",
        start_date=datetime(2022, 1, 1),
        catchup=False)
    def triggering_dag():
        @task
        def get_token():
            response = requests.post("https://auth.astronomer.io/oauth/token",
                                    json={"audience": "astronomer-ee",
                                        "grant_type": "client_credentials",
                                        "client_id": {KEY_ID},
                                        "client_secret": {KEY_SECRET})
            return response.json()["access_token"]
        @task
        def trigger_external_dag(token):
            dag_id = "target"
            response = requests.post(
                url=f"{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                data='{"logical_date": "' + datetime.utcnow().isoformat().split(".")[0] + 'Z"}'
            )
            print(response.json())
        trigger_external_dag(get_token())
    a = triggering_dag()
    ```