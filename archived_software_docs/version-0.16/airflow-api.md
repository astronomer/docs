---
sidebar_label: 'Airflow API'
title: 'Make Requests to the Airflow API'
id: airflow-api
description: Call the Apache Airflow REST API on Astronomer Software.

---

## Overview

Apache Airflow® is an extensible orchestration tool that offers multiple ways to define and orchestrate data workflows. For users looking to automate actions around those workflows, Airflow exposes a [stable REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in Airflow 2.0, and an ["experimental" REST API](https://airflow.apache.org/docs/stable/rest-api-ref.html) for users running Airflow 1.10. You're free to leverage both on Astronomer.

If you're looking to externally trigger DAG runs without needing to access your Airflow Deployment directly, for example, you can make an HTTP request (in Python, cURL etc.) to the corresponding endpoint in Airflow's API that calls for that exact action.

To get started, you'll need a Service Account on Astronomer to authenticate. Read below for guidelines.

## Step 1: Create a Service Account on Astronomer

The first step to calling the Airflow API on Astronomer is to create a Deployment-level Service Account, which will assume a user role and set of permissions and output an API Key that you can use to authenticate with your request.

You can create a Service Account via either the Software UI or the Astronomer CLI.

> **Note:** If you just need to call the Apache Airflow® API once, you can create a temporary Authentication Token (_expires in 24 hours_) on Astronomer in place of a long-lasting Service Account. To do so, simply navigate to: `https://<your-base-domain>/token` and skip to Step 2.

### Create a Service Account via the Software UI

To create a Service Account via the Software UI:

1. Log in to the Software UI.
2. Go to **Deployment** > **Service Accounts**.
   ![New Service Account](/img/software/ci-cd-new-service-account.png)
3. Give your Service Account a **Name**, **User Role**, and **Category** (_Optional_).
   > **Note:** In order for a Service Account to have permission to push code to your Airflow Deployment, it must have either the Editor or Admin role. For more information on Workspace roles, refer to [Roles and Permissions](workspace-permissions.md).

   ![Name Service Account](/img/software/ci-cd-name-service-account.png)
4. Save the API Key that was generated. Depending on your use case, you may want to store this key in an Environment Variable or secret management tool of choice.

   ![Service Account](/img/software/ci-cd-api-key.png)

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

## Step 2: Make an Apache Airflow® API Request

Now that you've created a Service Account, you're free to generate both `GET` or `POST` requests to any supported endpoints in Airflow's [Rest API Reference](https://airflow.apache.org/docs/stable/rest-api-ref.html) via the following base URL:

```
https://<your-base-domain>/<deployment-release-name>
```

In the examples below, we'll refer to this URL as the `AIRFLOW-DOMAIN`, where you'll replace `<your-base-domain>` (e.g. `mycompany.astronomer.io`) and `<deployment-release-name>` (e.g. `galactic-stars-1234`) with your own.

You can make requests via the method of your choosing. Below, we'll walk through an example request via cURL to Airflow's "Trigger DAG" endpoint and an example request via Python to the "Get all Pools" endpoint.

### Trigger DAG

If you'd like to externally trigger a DAG run, you can start with a generic cURL command to Airflow's POST endpoint:

```
POST /airflow/api/experimental/dags/<DAG_ID>/dag_runs
```

The command for your request should look like this:

```
curl -v -X POST
https://<AIRFLOW-DOMAIN>/airflow/api/experimental/dags/<DAG-ID>/dag_runs
-H 'Authorization: <API-Key> '
-H 'Cache-Control: no-cache'
-H 'content-type: application/json' -d '{}'
```

To run this, replace the following placeholder values:

- `<AIRFLOW-DOMAIN>`: Use `https://<your-base-domain>/<deployment-release-name>`
- `<DAG-ID>`: Name of your DAG (_case-sensitive_)
- `<API-Key>`: API Key from your Service Account

This will trigger a DAG run for your desired DAG with an `execution_date` value of `NOW()`, which is equivalent to clicking the "Play" button in the main "DAGs" view of the Airflow UI.

> **Note:** Your request will have the same permissions as the role of the Service Account you created on Astronomer.

#### Specify Execution Date

If you'd like to choose a specific `execution_date` (i.e. start timestamp) to trigger your DAG on, you can pass that in with the data parameter's JSON value `("-d'{}')`.

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
https://<AIRFLOW_DOMAIN>/api/experimental/dags/customer_health_score/dag_runs
-H 'Authorization: <API-Key>'
-H 'Cache-Control: no-cache'
-H 'content-type: application/json' -d '{"execution_date":"2019-11-16T11:34:00"}'
```

### Get all Pools

If you'd like to get all existing Pools from your Airflow Deployment, you can start with a generic Python command to Airflow's `GET` endpoint:

```
GET /api/experimental/pools
```

Here, your request would look like this:

```python
python
import requests
token="<API-Key>"
base_url="https://<your-base-domain/"
resp = requests.get(
   url=base_url + "<deployment-release-name>/airflow/api/experimental/pools",
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
