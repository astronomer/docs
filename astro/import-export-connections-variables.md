---
sidebar_label: 'Import and export connections and variables'
title: 'Import and export connections and variables'
id: import-export-connections-variables
description: "Learn how to import and export Airflow objects between Airflow environments"
---

After you create connections and variables in an Airflow environment, you might want to move export and import them between environments for any of the following reasons:

- You are launching a production Airflow environment on Astro based on a locally running Airflow environment.
- You need to replicate a production Airflow environment on your local machine.
- Your team is migrating old Airflow environments to a new location.

Use this document to learn how to export and import environment variables based on different connection and variable [storage and management strategies](manage-connections-variables.md). 

Based on your management strategy, the storage location for your Airflow objects will vary and hence the methods to import and export will vary as well. [Astro CLI](https://docs.astronomer.io/astro/cli/overview) can be used to export/import your Airflow objects from/to your local Airflow or Astro Deployment for all management strategies except Secrets Backend. 

Use this document to understand these methods and also how to use simple Astro CLI commands to import or export.

## From the Airflow UI/ metadata database

When you use the Airflow UI to store your Airflow connections and variables, they are stored in Airflow's metadata database. If your variables are stored in Airflow's metadata database, you can use the Airflow UI to import and export them in bulk.

To export variables from a local Airflow environment or Astro Deployment, go to **Admin** in the Airflow UI, click **Variables** and select the variables you want to export. Then, click **Export** in the **Actions** dropdown menu. This exports a file named `variables.json` to your local computer.

![Export Variables](/img/docs/airflow-ui-export-vars.png)

To import variables to a local Airflow environment or Astro Deployment from a `json` file, go to **Admin** in the Airflow UI, click **Variables**, then and click **Choose file**. Select the file you want to import and then click **Import Variables**.

![Import Variables](/img/docs/airflow-ui-import-vars.png)

For security reasons, you can't bulk import or export connections from the Airflow UI.

## From a secrets backend

If you use a secrets backend to store connections and variables, you need to use your secrets backend's API to manage connections and variables between environments. Note that this is necessary only in rare circumstances, when:

- You want to migrate your secrets backend to a different account.
- You want to use your secrets as a reference for another Deployment and then customize it. Astronomer recommends maintaining separate `development` and `production` secrets backend.
- You want to migrate to a different cloud provider.

Refer to your secrets backend provider's documentation to learn how to manage resources using API calls:

- Google secret manager's [Python SDK](https://cloud.google.com/secret-manager/docs/reference/libraries#client-libraries-install-python) and [REST API](https://cloud.google.com/secret-manager/docs/reference/rest) reference.
- AWS secret manager's [Python SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html) and [other SDKs](https://docs.aws.amazon.com/secretsmanager/latest/apireference/Welcome.html).
- Azure key vault's [SDK and API](https://learn.microsoft.com/en-us/azure/key-vault/general/developers-guide#apis-and-sdks-for-key-vault-management) reference.
- Hashicorp Vault's [Python SDK](https://developer.hashicorp.com/vault/docs/get-started/developer-qs#step-2-install-a-client-library)

To set up a secrets backend on Astro, see [configure secrets backend](secrets-backend).

## From environment variables

If you use an `.env` file to manage your connections and variables as environment variables in a local Astro project, you can import your Airflow objects to another local Airflow Astro project by copying the `.env` file into the destination project. 

The `.env` file is not pushed to your Deployment when you run `astro deploy`. However, you can use Astro CLI commands to import the contents of your `.env` file to an Astro Deployment using `astro deployment` commands. 

If your connections and variables are stored in a local Airflow metadata database, you can also export these to a `.env` file and then import them to an Astro Deployment as environment variables.

```bash
# export all airflow objects including connections and variables to `.env` file in URI format
astro dev object export --env-export 

# import into Astro all airflow objects defined as environment variables in the .env file
astro deployment variable create -d <deployment_id> --load --env .env
```

If your connections and variables are defined as environment variables on an Astro Deployment, you can export them to a local Airflow environment using the Astro CLI. Note that when you run the following command, environment variables with secret values will have those values redacted.

```bash
# export the variables from your Deployment and append to `.env` file
astro deployment variable list --deployment-id <deployment-id> --save
```
See [Use environment variables on Astro](environment-variables.md#add-airflow-connections-and-variables-using-environment-variables) and refer to [`astro deployment variable create`](cli/astro-deployment-variable-create.md#examples) for more examples.

### Airflow REST API

You can use [Airflow REST API with Astro](airflow-api.md) to setup import and export workflow for your connections and variables and easily replicate your Deployment settings.

To export connections from any Airflow environment, you can use the [List Connections API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_connections) and [Get Connection API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_connection).

To export variables from any Airflow environment, you can use [List Variables API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_variables) and [Get Variable API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_variable).

To import connections or variables to any Airflow environment, you can use the [Create Connection API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_connection) and [Create Variable API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_variables) respectively.

See 
