---
sidebar_label: 'Manage connections and variables'
title: 'Manage Airflow connections and variables'
id: manage-connections-variables
description: "Learn about different strategies for managing Airflow connections and variables in local environments and on Astro"
---

*Airflow connections* are used for storing credentials and other information necessary for connecting to external services. *Airflow variables* are a generic way to store and retrieve arbitrary content or settings as a simple key value store within Airflow.

Use this document to select the right Airflow connection and variable management strategies for your team.

Airflow supports several different methods for managing connections and variables. Each of these strategies has benefits and limitations related to their security and ease of use. The strategies you choose should be compatible with both your local environments and Astro Deployments, allowing you to [import and export objects](import-export-connections-variables.md) between the two contexts.

For in-depth information on managing connections and variables, see [Connection Basics](https://docs.astronomer.io/learn/connections) and [Variable Basics](https://docs.astronomer.io/learn/airflow-variables).

## Requirements

- A locally hosted Astro project created with the Astro CLI. See [Create a project](cli/get-started-cli.md).
- A Deployment on Astro. See [Create a Deployment](create-deployment.md).

## Choose a connection and variable management strategy

The following table suggests possible management strategies for specific use cases.

| Scenario | Strategy |
|----------|----------|
| I'm getting started and want to quickly create Airflow objects | [Airflow UI](#airflow-ui) |
| I prefer to manage my Airflow variables in a Git repository and to upload directly to Airflow | [Airflow UI](#airflow-ui) |
| I need to keep my connections and variables stored in a centralized and secure location. | [Secrets backend](#secrets-backend) |
| I want to create Connections once and then apply them to multiple Deployments or Workspaces. | [Astro Environment Manager](#astro-cloud-ui-environment-manager) |
| I don't have a secrets backend, but I still want some security and permissions attached to Airflow objects. | [Astro Environment Manager](#astro-cloud-ui-environment-manager) or [Environment variables](#environment-variables) |

### How Airflow finds connections

Because variables and connections serve different purposes in Airflow, you might want to use a different strategy for each object type. For example, you can use a secrets backend for connections and use combination of a `json` files and the Airflow UI for variables.

If you use a mix of strategies for managing connections, it's important to understand that when Airflow searches for connections, it uses the following order:

1. Secrets Backend
2. Astro Environment Manager
3. Environment Variables
4. Airflow's metadata database (Airflow UI)

This means that Astro first checks secrets backends, then the Environment Manager, followed by environment variables, and finally checks for connections defined in the Airflow UI.

If you use the same `Connection ID` in these resources with different credentials, Airflow ignores any duplicates and applies the highest priority configuration.

:::tip
If you only want to test connections or export connections in  a JSON or URI format, use the Airflow UI to [manage your connection](https://docs.astronomer.io/learn/connections#defining-connections-in-the-airflow-ui).  You can then use the Astro CLI commands to export the connections in a URI or JSON format. See [Import and export connections and variables](import-export-connections-variables.md#from-the-airflow-ui-metadata-database).
:::

## Compare strategies

The following sections explain the benefits, limitations, and implementations of each strategy in more detail.

### Astro Cloud UI Environment Manager

Astro includes connection management system that behaves like you are using an Astro-managed secrets backend. After you create a connection in the Cloud UI, you can share it with multiple Deployments in a Workspace and override connection values on a per-Deployment basis.

#### Benefits

- It securely stores your connection configuration and authentication information on Astro, without a secrets backend.
- You can create a connection once for a Deployment and then add it to multiple Deployments.
- Authenticate connections using credentials other than what the Airflow UI supports.
- After you configure a connection, the authentication information is securely stored in an Astro-managed secrets backend.
- Control whether connections can be used in a single Deployment or shared across Deployments in a Workspace.
- Override certain fields in the connection per Deployment, so you can create a general connection and then customize its behavior.

#### Limitations

- Currently, it only works with the Celery Executor. Kubernetes Executor support is coming soon.
- If you create a connection in the Cloud UI, you also need to add its related provider package to the `requirements.txt` file in your Astro project.
- Only available with Astro Runtime 9.3.0 and greater.
- You can't see connections defined in the Cloud UI in the Airflow UI.
- You need`WORKSPACE_OPERATOR` or `WORKSPACE_OWNER` user permissions.
- You can't programmatically import connections to the Environment Manager from your local environment.

:::info

To see how you can use connections set in the Astro Cloud UI Environment Manager in a best practice branch-based Deployment set up, see the [Manage Astro connections in branch-based deploy workflows](use-cases/connections-branch-deploys.md) use case.

:::

### Airflow UI

You can create Airflow connections and variables is through the Airflow UI. This experience is the same for both local Airflow environments and Astro Deployments. Astronomer recommends this method if you're just getting started with Airflow, you want to get your DAGs running quickly, or if you want to export connections in a URI/JSON format.

#### Benefits

- The UI has features for correctly formatting and testing your connections.
- It's easy to change variables or connections to test different use cases on the fly.
- You can export and import your variables from the Airflow UI using JSON files and the Astro CLI. See [Import and export connections and variables](import-export-connections-variables.md#from-the-airflow-ui-metadata-database).
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

- Store objects in a centralized location alongside other secrets used by your organization.
- Comply with internal security postures and policies that protect your organization.
- Recover objects if your Airflow environments go down.
- Share secrets across different Airflow environments.
- Allow selective access to connections and variables by using `connections_prefix` and `variables_prefix`.
- Limit the number of open connections to your metadata database, especially if you are using your connections and variables outside of task definitions.

#### Limitations

- A third-party secrets manager is required.
- Separate configurations might be required for using a secrets backend locally and on Astro.
- You cannot use the Airflow UI to view connections and variables.
- You are responsible for ensuring that secrets are encrypted.

### Environment variables

You can use Airflow's system-level environment variables to store connections and variables. This strategy is recommended when you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables.

Airflow connections and variables are stored in the Airflow metadata database. Calling them outside of task definitions and operators requires an additional connection to the Airflow metadata database which is used every time the scheduler parses a DAG. By adding connections and variables as environment variables, you can lower the amount of open connections and improve the performance of your database and resources.

You can configure system-level environment variables both locally and on Astro. For setup steps, see:

- [Set environment variables locally](cli/develop-project.md#set-environment-variables-locally)
- [Set environment variables on Astro](manage-env-vars.md)

#### Benefits

- If you use an `.env` file for your local Airflow environment and your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables.
- You can export environment variables from a local Airflow environment to Astro using the Astro CLI. See [Import and export connections and variables](import-export-connections-variables.md#environment-variables).
- You can override Airflow variables set in the Airflow UI. See [Environment variable priority](environment-variables.md#environment-variable-priority)
- You can create your connections and variables as environment variables from the Cloud UI. See [Use environment variables](manage-env-vars.md#using-the-cloud-ui).
- Environment variables marked as **Secret** are encrypted in the Astronomer control plane. See [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-in-the-cloud-ui) for details.
- This approach limits the number of open connections to your metadata database, especially if you are using your connections and variables outside of task definitions.

#### Limitations

- You can't view connections and variables from the Airflow UI.
- You must restart your local environment using `astro dev restart` whenever you make changes to your `.env` file.
- The environment variables are defined in plain text in your `.env` file.
- Connections must be formatted as either a URI or serialized JSON.
- Environment variables are not as secure or centralized compared to a [secrets backend](secrets-backend.md).
- You cannot directly export your environment variables from the Cloud UI to a local Airflow environment. See [Import and export Airflow objects](import-export-connections-variables.md#environment-variables).

## Other strategies

While it's possible to manage Airflow connections and variables with these strategies, Astronomer doesn't recommend them at scale:

- You can use the Airflow REST API to programmatically create Airflow connections and variables for a Deployment. Airflow objects created with the API are stored in the Airflow metadata database and visible in the Airflow UI.
- For local Astro projects, you can use `airflow_settings.yaml` for defining your connections and variables. See [Configure `airflow_settings.yaml`](cli/develop-project.md#configure-airflow_settingsyaml-local-development-only) for more details.

## See also
- [Import and export Airflow objects](import-export-connections-variables.md)
- [Authenticate to cloud services with user credentials](cli/authenticate-to-clouds.md)
