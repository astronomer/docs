---
sidebar_label: 'Airflow API'
title: 'Make requests to the Airflow REST API'
id: airflow-api
description: Call the Apache Airflow REST API on Astronomer Software.

---

Apache Airflow is an extensible orchestration tool that offers multiple ways to define and orchestrate data workflows. For users looking to automate actions around those workflows, Airflow exposes a [stable REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in Airflow 2 and an [experimental REST API](https://airflow.apache.org/docs/stable/rest-api-ref.html) for users running Airflow 1.10. You can use both on Astronomer.

To externally trigger DAG runs without needing to access your Airflow Deployment directly, for example, you can make an HTTP request in Python or cURL to the corresponding endpoint in the Airflow REST API that calls for that exact action.

To get started, you need a service account on Astronomer to authenticate. Read below for guidelines.

## Step 1: Create a service account on Astronomer

The first step to calling the Airflow REST API on Astronomer is to create a Deployment-level Service Account, which will assume a user role and set of permissions and output an API key that you can use to authenticate with your request.

You can use the Software UI or the Astro CLI to create a Service account.

:::info

If you just need to call the Airflow REST API once, you can create a temporary Authentication Token (_expires in 24 hours_) on Astronomer in place of a long-lasting Service account. To do so, go to: `https://app.<BASE-DOMAIN>/token` (e.g. `https://app.astronomer.yourcompany.com/token`) and skip to Step 2.

:::

### Create a service account using the Software UI

1. Log in to the Software UI.

2. Select a Deployment and then click the **Service Accounts** tab.

3. Click **New Service Account** and then complete the following fields:

   - **Name**: Enter a meaningful name for the service account.
   - **Category**: Optional. Enter an optional category name or description for the service account. Categories can help you locate and sort service accounts.
   - **Permissions**: Select the permissions for the service account. To push code to your Airflow Deployment, the service account must have Deployment Editor or Deployment Admin permissions. For more information about user permissions, see [Manage user permissions on Astronomer Software](workspace-permissions.md).

4. Click **Create Service Account**.

5. Copy and save the API key in the **API Key** field. You can store this key in an environment variable or in a secrets management tool.

6. Click **Service Accounts** to return to the Service Accounts page.

### Create a service account with the Astro CLI

To use the Astro CLI to create a Deployment-level Service Account:

1. Authenticate to the Astro CLI by running:
   ```
   astro login <BASE-DOMAIN>
   ```
   To identify your `<BASE-DOMAIN>`, run `astro cluster list` and select the domain name that corresponds to the cluster you're working in.

2. Identify your Airflow Deployment's Deployment ID. To do so, run:
   ```
   astro deployment list
   ```
   This will output the list of Airflow Deployments you have access to and their corresponding Deployment ID in the `DEPLOYMENT ID` column.

3. With that Deployment ID, run:
   ```
   astro deployment service-account create -d <deployment-id> --label <service-account-label> --role <deployment-role>
   ```
   The `<deployment-role>` must be either `editor` or `admin`.

4.  Save the API key that was generated. Depending on your use case, you might want to store this key in an Environment Variable or secret management tool.

## Step 2: Make an Airflow REST API request

With the information from Step 1, you can now execute requests against any supported endpoints in the [Airflow Rest API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) at the following base URL:

```
https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-NAME>/airflow/api/v1
```

## Example API Requests

In the following examples, replace the following values with your own:

- `<BASE-DOMAIN>`: The base domain for your organization on Astronomer Software. For example: `mycompany.astronomer.io`.
- `<DEPLOYMENT-RELEASE-NAME>`: The release name of your Deployment. For example: `galactic-stars-1234`.
- `<API-KEY>`: The API key for your Deployment Service account.
- `<DAG-ID>`: Name of your DAG (_case-sensitive_).


The example requests listed below are made with cURL and Python, but you can make requests with any standard method. In all cases, your request will have the same permissions as the role of the service account you created on Astronomer.

### Trigger DAG

To trigger a DAG, execute a POST request to the [dagRuns endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) of the Airflow REST API:

```
POST /dags/<dag-id>/dagRuns
```

This request will trigger a DAG run for your desired DAG with an `execution_date` value of `NOW()`, which is equivalent to clicking the "Play" button in the DAGs view of the Airflow UI.

#### cURL

```
curl -v -X POST https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-RELEASE-NAME>/airflow/api/v1/dags/<DAG-ID>/dagRuns \
  -H 'Authorization: <API-KEY>' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' -d '{}'
```

#### Python

```python
import requests

token = "<API-KEY>"
base_domain = "<BASE-DOMAIN>"
deployment_name = "<DEPLOYMENT-RELEASE-NAME>"
resp = requests.post(
    url=f"https://deployments.{base_domain}/{deployment_name}/airflow/api/v1/dags/example_dag/dagRuns",
    headers={"Authorization": token, "Content-Type": "application/json"},
    data='{}'
)
print(resp.json())
# {'conf': {}, 'dag_id': 'example_dag', 'dag_run_id': 'manual__2022-04-26T21:57:23.572567+00:00', 'end_date': None, 'execution_date': '2022-04-26T21:57:23.572567+00:00', 'external_trigger': True, 'logical_date': '2022-04-26T21:57:23.572567+00:00', 'start_date': None, 'state': 'queued'}
```

#### Specify execution date

To set a specific `execution_date` for your DAG, you can pass in a timestamp with the parameter's JSON value `("-d'{}')`.

The string needs to be in the following format (in UTC):

```
"YYYY-MM-DDTHH:mm:SS"
```

Where, `YYYY` represents the year, `MM` represents the month, `DD` represents the day, `HH` represents the hour, `mm` represents the minute, and `SS` represents the second of your timestamp. For example, `"2021-11-16T11:34:00"` would create a DAG run with an `execution_date` of November 16, 2021 at 11:34 AM.

Here, your request would be:

```
curl -v -X POST https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-RELEASE-NAME>/airflow/api/v1/dags/<DAG-ID>/dagRuns \
  -H 'Authorization: <API-KEY>' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' -d '{"execution_date": "2021-11-16T11:34:00"}'
```

:::tip

The `execution_date` parameter was replaced with `logical_date` in Airflow 2.2. If you run Airflow 2.2+, replace `execution_date` with `logical_date` and add a "Z" to the end of your timestamp. For example, `"logical_date": "2019-11-16T11:34:00Z"`.

For more information, see [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html?highlight=pass%20data#data-interval).

:::

### List pools

To list all Airflow pools for your Deployment, execute a GET request to the [`pools` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Pool) of the Airflow REST API:

```
GET /pools
```

#### cURL

```
curl -X GET https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-RELEASE-NAME>/airflow/api/v1/pools \
  -H 'Authorization: <API-KEY>'
```

#### Python

```python
import requests

token = "<API-KEY>"
base_domain = "<BASE-DOMAIN>"
deployment_name = "<DEPLOYMENT-RELEASE-NAME>"
resp = requests.get(
    url=f"https://deployments.{base_domain}/{deployment_name}/airflow/api/v1/pools",
    headers={"Authorization": token, "Content-Type": "application/json"},
    data='{}'
)
print(resp.json())
# {'pools': [{'name': 'default_pool', 'occupied_slots': 0, 'open_slots': 128, 'queued_slots': 0, 'running_slots': 0, 'slots': 128}], 'total_entries': 1}
```

## Notes on the Airflow 2 stable REST API

As of its momentous [2.0 release](https://www.astronomer.io/blog/introducing-airflow-2-0), the Apache Astro project now supports an official and more robust Stable REST API. Among other things, Airflow's new REST API:

- Makes for easy access by third-parties.
- Is based on the [Swagger/OpenAPI Spec](https://swagger.io/specification/).
- Implements CRUD (Create, Read, Update, Delete) operations on *all* Airflow resources.
- Includes authorization capabilities.

### Make a request

To convert a call from the Airflow experimental API, simply update the URL to use the endpoint specified in the [Airflow Stable REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

For example, requests to the [Get current configuration endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_config) are different depending on which version of Airflow you run.

```
GET /api/v1/config
```

Prior to Airflow 2, a cURL request to this endpoint would be:

```
curl -X GET \
  https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-RELEASE-NAME>/api/experimental/config \
  -H 'Authorization: <API-KEY>' \
  -H 'Cache-Control: no-cache'
```

With the stable REST API in Airflow 2, your cURL request would be:

```
curl -X GET \
  https://deployments.<BASE-DOMAIN>/<DEPLOYMENT-RELEASE-NAME>/api/v1/config \
  -H 'Authorization: <API-KEY>' \
  -H 'Cache-Control: no-cache'
  -H 'Content-Type: application/json' -d '{}'
```
