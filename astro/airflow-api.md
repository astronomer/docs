---
title: 'Make requests to the Airflow REST API'
sidebar_label: 'Airflow REST API'
id: airflow-api
---

<head>
  <meta name="description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
  <meta name="og:description" content="Learn how to make requests to the Airflow REST API and how you can use the Airflow REST API to automate Airflow workflows in your Deployments. Common examples of API requests are provided." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

You can use the Airflow [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) to automate Airflow workflows in your Deployments on Astro. For example, you can externally trigger a DAG run without accessing your Deployment directly by making an HTTP request in Python or cURL to the [dagRuns endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) in the Airflow REST API.

To test Airflow API calls in a local Airflow environment running with the Astro CLI, see [Troubleshoot your local Airflow environment](cli/run-airflow-locally.md).

:::info

Updates to the Airflow REST API are released in new Airflow versions and new releases don’t have a separate release cycle or versioning scheme. To take advantage of specific Airflow REST API functionality, you might need to upgrade Astro Runtime. See [Upgrade Runtime](upgrade-runtime.md) and the [Airflow release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

:::

## Prerequisites

- A Deployment on Astro.
- A [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- [cURL](https://curl.se/) or, if using Python, the [Requests library](https://docs.python-requests.org/en/latest/index.html).
- The [Astro CLI](cli/overview.md).

## Step 1: Retrieve your access token

<Tabs groupId="step-1-retrieve-your-access-token">

<TabItem value="workspace" label="Workspace token (Recommended)">

Follow the steps in [Create a Workspace API token](workspace-api-tokens.md#create-a-workspace-api-token) to create your token. Make sure to save the token on creation in order to use it later in this setup.

</TabItem>

<TabItem value="organization" label="Organization token">

Follow the steps in [Create a Orgaization API token](organization-api-tokens.md#create-an-organization-api-token) to create your token. Make sure to save the token on creation in order to use it later in this setup.

</TabItem>

<TabItem value="deployment" label="Deployment API key">

:::warning

Deployment API keys will soon be deprecated in favor of [Deployment API tokens](deployment-api-tokens.md). You can continue to use existing Deployment API keys for now, but you will have to complete a one-time migration to Deployment API tokens in the future.

:::

To retrieve an access token using [cURL](https://curl.se/), run the following API request with your Deployment API key ID and secret:

```bash
curl --location --request POST "https://auth.astronomer.io/oauth/token" \
        --header "content-type: application/json" \
        --data-raw '{
            "client_id": "<api-key-id>",
            "client_secret": "<api-key-secret>",
            "audience": "astronomer-ee",
            "grant_type": "client_credentials"}'
```

To retrieve an Astro access token using Python, use the [`requests`](https://docs.python-requests.org/en/latest/index.html) library to make your API request:

```python
def get_api_token() -> str:
  r = requests.post(
      "https://auth.astronomer.io/oauth/token",
      json={
          "client_id": "<api-key-id>",
          "client_secret": "<api-key-secret>",
          "audience": "astronomer-ee",
          "grant_type": "client_credentials"
      }
  )
  r.raise_for_status()
  return r.json()
```

</TabItem>
</Tabs>

## Step 2: Retrieve the Deployment URL

Run the following command to retrieve a Deployment URL:

```bash
astro deployment inspect -n <deployment-name> -k metadata.webserver_url
```

The Deployment URL is used to access your Astro Deployment's Airflow UI. It includes the name of your Organization and first 7 letters of your Deployment ID. 

For example, the Deployment URL for an Organization named `mycompany` with the Deployment ID `dhbhijp0vt68400dj40tmc8virf` is `mycompany.astronomer.run/dhbhijp0`.

## Step 3: Make an Airflow API request

You can execute requests against any endpoint that is listed in the [Airflow REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

To make a request based on Airflow documentation, make sure to:

- Use the Astro access token from Step 1 for authentication.
- Replace `airflow.apache.org` with your Deployment URL from Step 1.

## Example API Requests

The following are common examples of Airflow REST API requests that you can run against a Deployment on Astro.

### List DAGs

To retrieve a list of all DAGs in a Deployment, you can run a `GET` request to the [`dags` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags)

#### cURL

```sh
curl -X GET https://<your-deployment-url>/api/v1/dags \
   -H 'Cache-Control: no-cache' \
   -H 'Authorization: Bearer <your-access-token>'
```

#### Python

```python
import requests
token = "<your-access-token>"
deployment_url = "<your-deployment-url>"
response = requests.get(
   url=f"https://{deployment_url}/api/v1/dags",
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
curl -v -X POST https://<your-deployment-url>/api/v1/dags/<your-dag-id>/dagRuns \
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
    url=f"https://{deployment_url}/api/v1/dags/{dag_id}/dagRuns",
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
curl -X PATCH https://<your-deployment-url>/api/v1/dags/<your-dag-id> \
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
    url=f"https://{deployment_url}/api/v1/dags/{dag_id}",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data='{"is_paused": true}'
)
print(response.json())
# Prints data about the DAG with id <dag-id>
```
### Trigger DAG runs across Deployments

You can use the Airflow REST API to make a request in one Deployment that triggers a DAG run in a different Deployment. This is sometimes necessary when you have interdependent workflows across multiple Deployments. On Astro, you can do this for any Deployment in any Workspace or cluster. 

This topic has guidelines on how to trigger a DAG run, but you can modify the example DAG provided to trigger any request that's supported in the Airflow REST API.

1. Create a [Deployment API token](deployment-api-tokens.md) for the Deployment that contains the DAG you want to trigger.


2. In the Deployment that contains the triggering DAG, create an [Airflow HTTP connection](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html) with the following values: 

    - **Connection Id**: `http_conn`
    - **Connection Type**: HTTP
    - **Host**: `<your-deployment-url>`
    - **Schema**: `https`
    - **Extras**:
      
    ```json
    {
        "Content-Type": "application/json",
        "Authorization": "Bearer <your-deployment-api-token>"
    }
    ```

    See [Manage connections in Apache Airflow](https://docs.astronomer.io/learn/connections).

  :::info

  If the `HTTP` connection type is not available, double check that the [HTTP provider](https://registry.astronomer.io/providers/apache-airflow-providers-http/versions/latest) is installed in your Airflow environment. If it's not, add `apache-airflow-providers-http` to the `requirements.txt` file of our Astro project and redeploy it to Astro. 

  :::


3. In your triggering DAG, add the following task. It uses the [SimpleHttpOperator](https://registry.astronomer.io/providers/apache-airflow-providers-http/versions/latest/modules/SimpleHttpOperator) to make a request to the `dagRuns` endpoint of the Deployment that contains the DAG to trigger.

    ```python
    from datetime import datetime
    from airflow import DAG
    from airflow.providers.http.operators.http import SimpleHttpOperator

    with DAG(dag_id="triggering_dag", schedule=None, start_date=datetime(2023, 1, 1)):
        SimpleHttpOperator(
            task_id="trigger_external_dag",
            log_response=True,
            method="POST",
                # Change this to the DAG_ID of the DAG you are triggering
            endpoint=f"api/v1/dags/<triggered_dag>/dagRuns",
            http_conn_id="http_conn",
            data={
                "logical_date": "{{ logical_date }}",
                
                # if you want to add parameters:
                # params: '{"foo": "bar"}'
            }
        )
    ```
