---
sidebar_label: 'Manage connections and variables'
title: 'Manage Airflow connections and variables'
id: manage-connections-variables
description: "Learn about different strategies for managing Airflow connections and variables in local environments and on Astro"
---

*Airflow connections* are used for storing credentials and other information necessary for connecting to external services whereas *Airflow variables* are a generic way to store and retrieve arbitrary content or settings as a simple key value store within Airflow.

To store Airflow connections and variables in local Airflow or Astro, you can choose from different management strategies based on your usecase. Each of these strategies have benefits and limitations related to their security and ease of use. The strategy you choose should ideally be compatible with both your local environment and Astro Deployment for seamless integration. However, based on security requirements, permissions or your use-case, you might need to use one strategy for local and another for Astro Deployment.

Astro allows you to seamlessly integrate [secrets backend](secrets-backend.md) of your choice, which is recommended as the most secure and centralized management strategy. We also recommend using [Astro CLI](cli/overview.md) to run a local Airflow environment and test your DAGs locally before deploying to production. If it is not possible to run local Airflow, you can easily create dev ephemeral Deployments to test on Astro using [CI/CD](set-up-ci-cd.md#create-a-cicd-pipeline) and [Deployments-as-code](manage-deployments-as-code.md#create-a-deployment-from-a-template-file).

For in-depth information on creating and managing connections see [Connection Basics](https://docs.astronomer.io/learn/connections).

## Prerequisites

- A locally hosted Astro project created with the Astro CLI. See [Create a project](develop-project.md#create-an-astro-project).
- A Deployment on Astro. See [Create a Deployment](create-deployment.md).

## Choose a connection and variable management strategy

:::tip
If you just want to test your connection and export in JSON or URI format, use Airflow UI to [create your connection](https://docs.astronomer.io/learn/connections#defining-connections-in-the-airflow-ui) and Astro CLI commands [`astro dev object export`](https://docs.astronomer.io/astro/cli/astro-dev-object-export) or [`astro dev run`](https://docs.astronomer.io/astro/cli/astro-dev-run) to export.
:::

The following table suggests possible management strategies for specific use cases.

| Scenario | Strategy |
|----------|----------|
| I'm getting started and want to quickly create Airflow objects | [Airflow UI](https://docs.astronomer.io/learn/connections#defining-connections-in-the-airflow-ui) |
| I keep my variables in version control system and want to directly upload to Airflow | [Airflow UI](https://docs.astronomer.io/learn/connections#defining-connections-in-the-airflow-ui) |
| I need to keep my connections and variables centralized and as secure as possible | [Secrets backend](secrets-backend.md#benefits) |
| I don't have a secrets backend and want to reduce the calls to metadata db to improve performance or override existing connections defined in Airflow UI | [Environment variables](environment-variables.md) |


Because variables and connections serve different purpose in Airflow, you might want to choose a different strategy for each. For example, you can choose secrets backend for connections and use combination of a `json` file and Airflow UI for variables. See [variable basics](https://docs.astronomer.io/learn/) for in-depth information.

## Compare connection and variable management strategies 

The following sections explain the benefits, limitations, and implementations of each strategy in more detail.

### Airflow UI

The quickest way to create Airflow connections and variables is through the Airflow UI. This experience is the same for both local Airflow environments and Astro Deployments. Astronomer recommends this method if you're just getting started with Airflow, you want to get your DAGs running quickly, or if you want to export connections in a URI/JSON format.

#### Benefits

- The UI has features for correctly formatting and testing your connections.
- Easy to change variables or connections to test different usecases on-the-fly.
- You can export your variables from the Airflow UI to a JSON file and import them to the Airflow UI from a JSON file.
- Connections and variables are encrypted and stored in the Airflow metadata database.

#### Limitations

- You cannot export or import connections from the UI for security reasons.
- Managing many connections or variables can become unwieldy.
- In a local environment, you lose your connections and variables if you delete your metadata database with `astro dev kill`.

### Secrets backend

A secrets backend is the most secure way to store connections and variables. You can access a secrets backend both locally and on Astro by configuring the appropriate credentials in your Airflow environment. Astronomer recommends this method for all staging and production deployments. See the following documentation for setup steps:

- [Authenticate to clouds locally](cli/authenticate-to-clouds.md)
- [Configure a secrets backend](secrets-backend.md)

#### Benefits

- A centralized location alongside other secrets from other tools and systems used by your organization.
- Comply with internal security postures and policies that protect your organization.
- Recover in the case of an incident.
- Secrets can be shared across different Airflow environments, allowing you to integrate with your new Deployment instead of having to set them manually in the Airflow UI.
- You can configure your secrets backend to allow selective access to connections and variables by using `connections_prefix` or `variables_prefix`. 

#### Limitations

- A third-party secrets manager is required.
- Separate configurations might be required for using a secrets backend locally and on Astro.
- You cannot use the Airflow UI to view connections and variables.
- You are responsible to ensure the secrets are encrypted.

### Environment variables

You can use Airflow's system-level environment variables to store connections and variables. This strategy is recommended when you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables. You can configure system-level environment variables both locally and on Astro. For setup steps, see:

- [Set environment variables locally](develop-project.md#set-environment-variables-locally)
- [Set environment variables on Astro](environment-variables.md#add-airflow-connections-and-variables-using-environment-variables)

#### Benefits

- If you user `.env` file for local Airflow and your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables.
- You can export environment variables from local Airflow to Astro using the Astro CLI. See [import and export Airflow objects](import-export-airflow-objects#environment-variables).
- In case you want to override variables in the Airflow UI, Airflow variables set in environment variables take precedence over Airflow UI variables. See [Environment variable priority](environment-variables.md#environment-variable-priority)
- On Astro, you can create your connections and variables as environment variables from the Cloud UI. See [use environment variables](environment-variables.md#set-environment-variables-in-the-cloud-ui) for more details. 
- Environment variables marked as **Secret** are encrypted in the Astronomer control plane. See [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-on-astro) for details.
- Limits open connections to your metadata database, especially if you are using your connections and variables outside of task definitions.

#### Limitations

- You can't view connections and variables from the Airflow UI. 
- You must restart your local environment using `astro dev restart` whenever you make changes to your `.env` file.
- The environment variables are defined in plain text in `.env` file.
- Connections must be formatted as either a URI or serialized JSON.
- Environment variables are not as secure or centralized compared to a [secrets backend](secrets-backend.md).
- You cannot directly export your environment variables from Astro Cloud UI. See [import and export Airflow objects](import-export-airflow-objects#environment-variables).

## Other strategies

- You can use Airflow REST API to programmatically create Airflow connections and variables for a Deployment. Airflow objects created with the API are stored in the Airflow metadata database and hence visible on the Airflow UI. This helps you to programmatically update Airflow both locally and on Astro to ensure parity across environments.
- For local Astro projects, you can also use `airflow_settings.yaml` for defining your connections and variables. See [Configure `airflow_settings.yaml`](develop-project.md#configure-airflow_settingsyaml-local-development-only) for more details.

## Read next
- [Import and export Airflow objects](import-export-airflow-objects)