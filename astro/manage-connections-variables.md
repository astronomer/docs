---
sidebar_label: 'Manage Airflow connections and variables'
title: 'Manage Airflow connections and variables on Astro'
id: manage-connections-variables
description: "Manage Airflow Connections and Variables"
---

You can store Airflow [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) and [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) locally in Airflow or remotely on Astro using several different methods. Each of these methods has advantages and limitations related to their security, ease of use, and performance. Similarly, you can choose different strategies for testing connections and variables on your local computer and then deploying these configurations to Astro.

Use this document to understand all available options for managing variables and connections in both local Astro projects and Astro Deployments.

## Prerequisites

- A locally hosted Astro project created with the Astro CLI. See [Create a project](develop-project.md#create-an-astro-project).
- A Deployment on Astro. See [Create a Deployment](create-deployment.md).

## Choose a connection and variable management strategy

:::tip 

It is not necessary to choose the same approach for both connections and variables. Variables often determine your DAG's flow of execution and you might prefer to check them into source control. You also might want to view or edit them in the Airflow UI. For such cases, you can export your variables in a `json` file from the Airflow UI or using Astro CLI.

:::

Astronomer recommends using the [Astro CLI](cli/overview.md) to run a local Airflow environment and test your DAGs locally before deploying to Astro. Your Airflow connection and variable management strategies should be compatible with both your local testing workflows and your Astro workflows. However, you might need to use one strategy for storing variables and a different strategy for storing connections.

The following table suggests possible management strategies for specific use cases.

| Scenario | Strategy |
|----------|----------|
| I'm getting started and want to quickly create Airflow objects | Airflow UI |
| I want to test my connection and export as URI format | Airflow UI. For exporting as URI refer to [Import and export](manage-connections-variables#import-and-export-airflow-connections-and-variables) |
| I want to deploy the same variables across multiple different Airflow environments  | Environment variables or [export as json](manage-connections-variables#astro-cli) |
| I need to keep my connections and variables centralized and as secure as possible | Secrets backend |

### Storage and encryption

If you want to choose a strategy based on how Airflow connections and variables are stored, the following table shows which storage and encryption methods that each strategy uses.

| Strategy | Storage location | Visible via UI | Encrypted |
|-----------|----------------|-----|------|
| Airflow UI | Airflow metadata database | Yes | Yes. See [Fernet Key](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html#fernet) | 
| Airflow API | Airflow metadata database | Yes | Yes. See [Fernet Key](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html#fernet) |
| Environment variables | On local environments, in plain text. On Astro, in the control plane. | No | Yes, on Astro only. See [Data Protection](data-protection.md) | 
| Secrets backend | Third-party secrets backend | No | Refer to your secrets backend tool documentation. |

#### How Astro prioritizes storage locations

If you store the same variable or connection in multiple locations, Astro applies and overrides your configurations in the following order:

1. Secrets backend 
2. Environment variables
3. Metadata database (any connection or variable which is visible in the Airflow UI)

For example, if you set `AIRFLOW_VAR_MY_VARIABLE` with one value as an environment variable and you set the same variable `MY_VARIABLE` with another value in the Airflow UI, Astro uses the value set in the environment variable.

## Airflow connection and variable management strategies 

The following sections explain the benefits, limitations, and implementations of each strategy in more detail.

### Airflow UI

The quickest way to create Airflow connections and variables is through the Airflow UI. This experience is the same for both local Airflow environments and Astro Deployments. Astronomer recommends this method if you're just getting started with Airflow, you want to get your DAGs running quickly, or if you want to export connections in a URI/JSON format

#### Benefits

- The UI has features for correctly formatting and testing your connections.
- You can export your variables from the Airflow UI, as well as import them to the Airflow UI from a JSON file.
- Connections and variables are encrypted and stored in the Airflow metadata database.

#### Limitations

- You can only automatically export your Airflow variables to Astro as environment variables.
- Managing many connections or variables can become unwieldy.
- It's not the most secure option for sensitive variables.
- In a local environment, you lose your connections and variables if you delete your metadata database with `astro dev kill`.

### Secrets backend

A secrets backend is the most secure way to store connections and variables. You can access a secrets backend both locally and on Astro by configuring the appropriate credentials in your Airflow environment. Astronomer recommends this method for all critical production workflows. See the following documentation for setup steps:

- [Authenticate to clouds locally](cli/authenticate-to-clouds.md)
- [Configure a secrets backend](secrets-backend.md)

#### Benefits

- It's compatible with strict organization security standards.
- All connections and variables are centralized and standardized.
- Secrets that can be shared across different Airflow environments.
- You can configure your secrets backend to allow selective access to connections and variables based on naming convention.

#### Limitations

- A third-party secrets manager is required.
- There are separate configurations for using a secrets backend locally and on Astro.
- You cannot use the Airflow UI to view connections and variables.
- You are responsible to ensure the secrets are encrypted.

### Environment variables

You can use Airflow's system-level environment variables to store connections and variables. This strategy is recommended when you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables. You can configure system-level environment variables both locally and on Astro. For setup steps, see:

- [Set environment variables locally](develop-project.md#set-environment-variables-locally)
- [Set environment variables on Astro](environment-variables.md)

#### Benefits

- For local Airflow, if your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables in the `.env` file.
- You can export environment variables from local Airflow to Astro using the Astro CLI.
- In case you want to override variables in the Airflow UI, Airflow variables set in environment variables take precedence over Airflow UI variables.
- On Astro, you can manage your connections and variables from the Cloud UI.
- Environment variables marked as **Secret** are encrypted in the Astronomer control plane.

#### Limitations

- Connections and variables can't be viewed from the Airflow UI, but you can use them in your DAGs. 
- You must restart your local environment using `astro dev restart` whenever you make changes to your `.env` file.
- The environment variables are defined in plain text in `.env` and you can only mark them as a secret once you deploy to Astro.
- Connections must be formatted as either a URI or serialized JSON.
- Environment variables are not as secure or centralized compared to a [secrets backend](secrets-backend.md).

### Airflow API

You can use the Airflow REST API to programmatically create Airflow connections and variables for a Deployment. Airflow objects created this way are stored in the Airflow metadata database. This strategy is good for teams setting up large Deployments with many Airflow connections and variables.

For more information, see [Airflow API](airflow-api.md).

#### Benefits

- You can still manage your secrets using a centralized service like a secrets backend. 
- Programmatically update Airflow both locally and on Astro to ensure parity across environments. 
- Connections and variables are encrypted and stored in the Airflow metadata database.
- You can see your variables and connections in the Airflow UI.
- You can export variables and connections using the Airflow API.

#### Limitations

- You need an additional tool or process to keep your secrets in sync across environments.

## Import and export connections and variables

In production environments with multiple team members, you might want to export Airflow connections and variables from an Airflow environment and import them to another environment. For example, you might want to export an Airflow connection you use locally and import it to an Astro Deployment after you've tested it. 

Use the following topics to learn different strategies for exporting and importing Airflow objects based on where they are stored:

### Secrets backend

If you use a secrets backend, the method for managing connections and variables between local environments and Deployments varies based on your secrets backend and its API. You can still export the connections and variables from local, but you must rely on secret manager's API to migrate.

### Environment variables

You can easily import connections and variables stored as Environment variables in `.env` file to another local Airflow by copying the `.env` file to another Astro project. To import Airflow connections and variables to Astro, you can refer the commands defined in [Astro CLI](#using-astro-cli) to import all environment variables in your `.env` file to a Deployment on Astro.

### Airflow metadata database

You can export Airflow connections and variables stored in metadata database using the [Astro CLI](#using-astro-cli) or [Airflow API](#using-airflow-api). An Airflow connection or variable is stored in the metadata database if it's viewable in the Airflow UI under **Connections** or **Variables**. For variables, you can also use [Airflow UI](#using-airflow-ui) to import or export.

#### Using Astro CLI

Run the following command to import or export your Airflow connections and variables, and then import them to Astro as environment variables:

```bash
# export all airflow objects including connections and variables to `.env` file in URI format
astro dev object export --env-export 

# import into Astro variables and/or connections defined as environment variables in the .env file
astro deployment variable create -d <deployment_id> --load --env .env
```

You can also export only variables from your local environment and then deploy them to Astro as part of your `include` folder:

```bash
# export variables in JSON format to vars.json in your astro project's include dir
astro dev run variables export /usr/local/airflow/include/vars.json
```

You can't automatically export Airflow connections and variables from Astro and import them to a local environment if they're set as environment variables. However, you can pull down all non-secret environment variables from a Deployment using `astro deployment variable list` and then copy them into your `.env` file. Refer

#### Using Airflow API

To export connections from any Airflow environment, you can use the [List Connections API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_connections) and [Get Connection API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_connection) .

To export variables from any Airflow environment, you can use [List Variables API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_variables) and [Get Variable API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_variable).

To import connections or variables to any Airflow environment, you can use the [Create Connection API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_connection) and [Create Variable API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_variables) respectively.

#### Using Airflow UI

To export variables from a local Airflow or Astro Deployment, go to the **Admin** menu on the Airflow UI, click on **Variables** and select the variables you want to export. Then, click on **Export** option in the **Actions** dropdown. The file `variables.json` will be downloaded.

![Export Variables](/img/docs/airflow-ui-export-vars.png)

To import variables to a local Airflow or Astro Deployment from a `json` file, go to the **Admin** menu on the Airflow UI, click on **Variables** and click on **Choose file**. Select the file you want to import and then click on **Import Variables**.

![Import Variables](/img/docs/airflow-ui-import-vars.png)

Learn more about [connections](https://docs.astronomer.io/learn/connections) in Learn.