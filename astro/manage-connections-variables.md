---
sidebar_label: 'Manage connections and variables'
title: 'Manage Airflow connections and variables'
id: manage-connections-variables
description: "Learn about different strategies for managing Airflow connections and variables in local environments and on Astro"
---

*Airflow connections* are used for storing credentials and other information necessary for connecting to external services. *Airflow variables* are a generic way to store and retrieve arbitrary content or settings as a simple key value store within Airflow.

Use this document to select the right Airflow connection and variable management strategies for your team.

Airflow supports several different methods for managing connections and variables. Each of these strategies has benefits and limitations related to their security and ease of use. The strategies you choose should be compatible with both your local environments and Astro Deployments, allowing you to [import and export objects](import-export-connections-variables.md) between the two contexts.

For in-depth information on creating and managing connections, see [Connection Basics](https://docs.astronomer.io/learn/connections).

## Prerequisites

- A locally hosted Astro project created with the Astro CLI. See [Create a project](develop-project.md#create-an-astro-project).
- A Deployment on Astro. See [Create a Deployment](create-deployment.md).

## Choose a connection and variable management strategy

The following table suggests possible management strategies for specific use cases.

| Scenario | Strategy |
|----------|----------|
| I'm getting started and want to quickly create Airflow objects | [Airflow UI](#airflow-ui) |
| I prefer to manage my Airflow variables in a Git repository and to upload directly to Airflow | [Airflow UI](#airflow-ui) |
| I need to keep my connections and variables stored in a centralized and secure location. | [Secrets backend](#secrets-backend) |
| I don't have a secrets backend, but I still want some security and permissions attached to Airflow objects. | [Environment variables](#environment-variables) |

Because variables and connections serve different purposes in Airflow, you might want to use a different strategy for each object type. For example, you can use a secrets backend for connections and use combination of a `json` files and the Airflow UI for variables.

:::tip
If you only want to test connections or export connections in  a JSON or URI format, use the Airflow UI to [manage your connection](https://docs.astronomer.io/learn/connections#defining-connections-in-the-airflow-ui).  You can then use the Astro CLI commands to export the connections in a URI or JSON format. See [Import and export connections and variables](import-export-connections-variables.md#from-the-airflow-ui-metadata-database).
:::

## Compare connection and variable management strategies 

The following sections explain the benefits, limitations, and implementations of each strategy in more detail.

### Airflow UI

The quickest way to create Airflow connections and variables is through the Airflow UI. This experience is the same for both local Airflow environments and Astro Deployments. Astronomer recommends this method if you're just getting started with Airflow, you want to get your DAGs running quickly, or if you want to export connections in a URI/JSON format.

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

You can use Airflow's system-level environment variables to store connections and variables. This strategy is recommended when you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables. You can configure system-level environment variables both locally and on Astro. For setup steps, see:

- [Set environment variables locally](develop-project.md#set-environment-variables-locally)
- [Set environment variables on Astro](environment-variables.md#add-airflow-connections-and-variables-using-environment-variables)

#### Benefits

- If you use an `.env` file for your local Airflow environment and your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables.
- You can export environment variables from a local Airflow environment to Astro using the Astro CLI. See [Import and export connections and variables](import-export-connections-variables.md#environment-variables).
- You can override Airflow variables set in the Airflow UI. See [Environment variable priority](environment-variables.md#environment-variable-priority)
- You can create your connections and variables as environment variables from the Cloud UI. See [Use environment variables](environment-variables.md#set-environment-variables-in-the-cloud-ui). 
- Environment variables marked as **Secret** are encrypted in the Astronomer control plane. See [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-on-astro) for details.
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

- You can use the Airflow REST API to programmatically create Airflow connections and variables for a Deployment. Airflow objects created with the API are stored in the Airflow metadata database and hence visible on the Airflow UI.
- For local Astro projects, you can use `airflow_settings.yaml` for defining your connections and variables. See [Configure `airflow_settings.yaml`](develop-project.md#configure-airflow_settingsyaml-local-development-only) for more details.

## See also
- [Import and export Airflow objects](import-export-connections-variables.md)
- [Authenticate to cloud services with user credentials](cli/authenticate-to-clouds.md)