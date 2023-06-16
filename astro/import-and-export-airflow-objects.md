---
sidebar_label: 'Import and export Airflow objects'
title: 'Import and export Airflow objects'
id: import-export-airflow-objects
description: "Learn how to import and export Airflow objects from/to Astro and local Airflow"
---

Airflow objects include connections, variables and pools. There are different strategies that you can choose to store your Airflow objects as explained in [Manage connections and variables](manage-connections-variables.md). With multiple teams using the same data stack, you might want to export Airflow connections and variables from an Airflow environment and import them to another environment. *For example*, you can export an Airflow connection that you use locally and import to an Astro Deployment after you've tested it. 

Based on your management strategy, the storage location for your Airflow objects will vary and hence the methods to import and export will vary as well. [Astro CLI](https://docs.astronomer.io/astro/cli/overview) can be used to export/import your Airflow objects from/to your local Airflow or Astro Deployment for all management strategies except Secrets Backend. 

Use this document to understand these methods and also how to use simple Astro CLI commands to import or export.

## Import and export Airflow objects

The following sections describe different methods for exporting and importing Airflow objects based on the management strategies.

### Airflow UI

When you use Airflow UI to store your Airflow connections and variables, they are stored in Airflow's metadata database. Airflow UI allows you to create, edit and delete these. For variables, Airflow UI additionally provides the option to bulk import and export.

To export variables from a local Airflow environment or Astro Deployment, go to **Admin** in the Airflow UI, click **Variables** and select the variables you want to export. Then, click **Export** in the **Actions** dropdown menu. This exports a file named `variables.json` to your local computer.

![Export Variables](/img/docs/airflow-ui-export-vars.png)

To import variables to a local Airflow environment or Astro Deployment from a `json` file, go to **Admin** in the Airflow UI, click **Variables**, then and click **Choose file**. Select the file you want to import and then click **Import Variables**.

![Import Variables](/img/docs/airflow-ui-import-vars.png)

You cannot bulk import or export Connections from the Airflow UI due to security reasons. See [Connections](https://docs.astronomer.io/learn/connections) for more information about creating and editing connections in the Airflow UI.

### Secrets backend

If you use a secrets backend, it's API determines how you manage connections and variables between local environments and Deployments. Refer to your secrets backend provider's documentation to learn how to manage resources using API calls:

- Google secret manager's [Python SDK](https://cloud.google.com/secret-manager/docs/reference/libraries#client-libraries-install-python) and [REST API](https://cloud.google.com/secret-manager/docs/reference/rest) reference.
- AWS secret manager's [Python SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html) and [other SDKs](https://docs.aws.amazon.com/secretsmanager/latest/apireference/Welcome.html).
- Azure key vault's [SDK and API](https://learn.microsoft.com/en-us/azure/key-vault/general/developers-guide#apis-and-sdks-for-key-vault-management) reference.
- Hashicorp Vault's [Python SDK](https://developer.hashicorp.com/vault/docs/get-started/developer-qs#step-2-install-a-client-library)

To get started with secrets backend on Astro, see [configure secrets backend](secrets-backend).

### Environment variables

If you use `.env` file to manage your connections and variables as environment variables, you can copy the file to another local Airflow Astro project. The `.env` file is for local development only and is not automatically deployed to your Deployment when you use `astro deploy` command. But you can use Astro CLI commands to export your connections and variables to an `.env` file and import to an Astro Deployment as shown below. All the connections and variables stored in the Airflow metadata database will be exported as environment variables.

```bash
# export all airflow objects including connections and variables to `.env` file in URI format
astro dev object export --env-export 

# import into Astro all airflow objects defined as environment variables in the .env file
astro deployment variable create -d <deployment_id> --load --env .env
```

You can't automatically export connections and variables defined as environment varianles in your Astro Deployment either via Cloud UI or Dockerfile. However, you can pull down these using Astro CLI from a Deployment with secret values redacted. For example:

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
