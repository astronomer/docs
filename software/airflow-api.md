---
sidebar_label: 'Airflow API'
title: 'Make Requests to the Airflow REST API'
id: airflow-api
description: Call the Apache Airflow REST API on Astronomer Software.

---

## Overview

Apache Airflow is an extensible orchestration tool that offers multiple ways to define and orchestrate data workflows. For users looking to automate actions around those workflows, Airflow exposes a [stable REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in Airflow 2, and an ["experimental" REST API](https://airflow.apache.org/docs/stable/rest-api-ref.html) for users running Airflow 1.10. You can use both on Astronomer.

To externally trigger DAG runs without needing to access your Airflow Deployment directly, for example, you can make an HTTP request in Python or cURL to the corresponding endpoint in the Airflow REST API that calls for that exact action.

To get started, you need a Service Account on Astronomer to authenticate. Read below for guidelines.

## Step 1: Create a Service Account on Astronomer

The first step to calling the Airflow REST API on Astronomer is to create a Deployment-level Service Account, which will assume a user role and set of permissions and output an API Key that you can use to authenticate with your request.

You can create a Service Account via either the Software UI or the Astronomer CLI.

:::info

If you just need to call the Airflow REST API once, you can create a temporary Authentication Token (_expires in 24 hours_) on Astronomer in place of a long-lasting Service Account. To do so, simply navigate to: `https://<your-base-domain>/token` and skip to Step 2.

:::

### Create a Service Account via the Software UI

To create a Service Account via the Software UI:

1. Log in to the Software UI.
2. Go to **Deployment** > **Service Accounts**.
   ![New Service Account](https://assets2.astronomer.io/main/docs/ci-cd/ci-cd-new-service-account.png)
3. Give your Service Account a **Name**, **User Role**, and **Category** (_Optional_).
   > **Note:** In order for a Service Account to have permission to push code to your Airflow Deployment, it must have either the Editor or Admin role. For more information on Workspace roles, refer to [Roles and Permissions](workspace-permissions.md).

   ![Name Service Account](https://assets2.astronomer.io/main/docs/ci-cd/ci-cd-name-service-account.png)
4. Save the API Key that was generated. Depending on your use case, you may want to store this key in an Environment Variable or secret management tool of choice.

   ![Service Account](https://assets2.astronomer.io/main/docs/ci-cd/ci-cd-api-key.png)

### Create a Service Account via the Astronomer CLI

To create a Deployment-level Service Account via the Astronomer CLI:

1. Authenticate to the Astronomer CLI by running:
   ```
   astro auth login <your-base-domain>
   ```
2. Identify your Airflow Deployment's Deployment ID. To do so, run:
   ```
   astro deployment list
   ```
   This will output the list of Airflow Deployments you have access to and their corresponding Deployment ID.
3. With that Deployment ID, run:
   ```
   astro deployment service-account create -d <deployment-id> --label <service-account-label> --role <deployment-role>
   ```
4.  Save the API Key that was generated. Depending on your use case, you might want to store this key in an Environment Variable or secret management tool of choice.

## Step 2: Make an Airflow REST API Request

Now that you've created a Service Account, you're free to generate both `GET` or `POST` requests to any supported endpoints in Airflow's [Rest API Reference](https://airflow.apache.org/docs/stable/rest-api-ref.html) via the following base URL:

```
https://<your-base-domain>/<deployment-release-name>
```

In the examples below, we'll refer to this URL as the `AIRFLOW-DOMAIN`, where you'll replace `<your-base-domain>` (e.g. `mycompany.astronomer.io`) and `<deployment-release-name>` (e.g. `galactic-stars-1234`) with your own.

You can make requests via the method of your choosing. Below, we'll walk through an example request via cURL to Airflow's "Trigger DAG" endpoint and an example request via Python to the "Get all Pools" endpoint. In all cases, your request will have the same permissions as the role of the Service Account you created on Astronomer.

### Trigger DAG

To trigger a DAG, run a simple cURL command that makes a POST request to the [dagRuns endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) of the Airflow REST API:

```
POST /dags/<dag-id>/dagRuns
```

The command for your request should look like this:

```
curl -v -X POST
https://<AIRFLOW-DOMAIN>/api/v1/dags/<DAG-ID>/dagRuns
-H 'Authorization: <API-Key> '
-H 'Cache-Control: no-cache'
-H 'content-type: application/json' -d '{}'
```

To run this, replace the following placeholder values:

- `<AIRFLOW-DOMAIN>`: Use `https://<your-base-domain>/<deployment-release-name>`
- `<DAG-ID>`: Name of your DAG (_case-sensitive_)
- `<API-Key>`: API Key from your Service Account

This will trigger a DAG run for your desired DAG with a `execution_date` value of `NOW()`, which is equivalent to clicking the "Play" button in the main "DAGs" view of the Airflow UI.

#### Specify Execution Date

To set a specific `execution_date` for your DAG, you can pass in a timestamp with the parameter's JSON value `("-d'{}')`.

The string needs to be in the following format (in UTC):

```
"YYYY-MM-DDTHH:MM:SS"
```

Where, `YYYY`: Year, `MM`: Month, `DD`: Day, `HH`: Hour, `MM`: Minute, `SS`: Second.

For example:

```
"2019-11-16T11:34:00"
```

Here, your request becomes:

```
curl -v -X POST
https://<AIRFLOW_DOMAIN>/api/v1/dags/<DAG-ID>/dagRuns
-H 'Authorization: <API-Key>'
-H 'Cache-Control: no-cache'
-H 'content-type: application/json' -d '{"execution_date":"2019-11-16T11:34:00"}'
```

:::info

The `execution_date` parameter was replaced with `logical_date` in Airflow 2.2+. If you run Astronomer Certified 2.2+, replace `execution_date` with `logical_date`. For more information, see [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html?highlight=pass%20data#data-interval).

:::

### List Pools

To list all Airflow pools for your Deployment, you can run a simple command that makes a GET request to the [`pools` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/Pool) of the Airflow REST API:

```
GET /pools
```

Here, your request would look like this:

```python
python
import requests
token="<API-Key>"
base_url="https://<your-base-domain/"
resp = requests.get(
   url=base_url + "<deployment-release-name>/api/v1/pools",
   headers={"Authorization": token},
   data={}
)
print(resp.json())
>>>>  [{'description': 'Default pool', 'id': 1, 'pool': 'default_pool', 'slots': 128}]
```

To run this, replace the following placeholder values:

- `<your-base-domain>`: Your Astronomer Software base domain
- `<API-Key>`: API Key from your Service Account
- `<deployment-release-name>`: Your Airflow Deployment Release Name

## Airflow 2.0 Stable REST API

### What's new

As of its momentous [2.0 release](https://www.astronomer.io/blog/introducing-airflow-2-0), the Apache Airflow project now supports an official and more robust Stable REST API. Among other things, Airflow's new REST API:

* Makes for easy access by third-parties.
* Is based on the [Swagger/OpenAPI Spec](https://swagger.io/specification/).
* Implements CRUD (Create, Update, Delete) operations on *all* Airflow resources.
* Includes authorization capabilities.

:::tip

To get started with Airflow 2.0 locally, read [Get Started with Apache Airflow 2.0](https://www.astronomer.io/guides/get-started-airflow-2). To upgrade an Airflow Deployment on Astronomer to 2.0, make sure you've first upgraded to both Astronomer Software v0.23 and Airflow 1.10.15. For questions, reach out to [Astronomer Support](https://support.astronomer.io).

:::

### Make a Request

To convert a call from Airflow's experimental API, simply update the URL to use the endpoint specified in Airflow's [Stable REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

For example, take Airflow's "Get Current Configuration" endpoint:

```
GET /api/v1/config
```

Here, your cURL request would look like the following:

```
curl -X GET \
https://<AIRFLOW-DOMAIN>/api/v1/config \
-H 'Authorization: <API-Key>' \
-H 'Cache-Control: no-cache'
```

To run this, update the following placeholder values:

- `<AIRFLOW-DOMAIN>`: Use `https://<your-base-domain>/<deployment-release-name>`
- `<API-Key>`: API Key from your Service Account
