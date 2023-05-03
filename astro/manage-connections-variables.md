---
sidebar_label: 'Manage Airflow connections and variables'
title: 'Manage Airflow connections and variables on Astro'
id: manage-connections-variables
description: "Manage Airflow Connections and Variables"
---

You can store Airflow [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) and [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) on local Airflow or Astro using several different methods. Each of these methods has advantages and limitations related to their security, ease of use, and performance. Similarly, there are a few strategies for testing connections and variables on your local computer and deploying these configurations to Astro.


Use this document to understand all available options for managing variables and connections in both local Astro projects and Astro Deployments.

## Prerequisites

- A locally hosted Astro project using Astro CLI. See [Create a project](develop-project.md#create-an-astro-project).
- A Deployment on Astro. See [Create a Deployment](create-deployment.md).
## Choose a variable and connection management strategy

:::tip 

It is not necessary to choose the same approach for both connections and variables. Many a times, variables decide the flow of execution of your DAG and you might prefer to check them in to source control. You also might want to view or edit them via Airflow UI. For such cases, you can export your variables in a `json` file from Airflow UI, or use [`airflow_settings.yaml`](manage-connections-variables#local-only-airflow_settingsyaml), or [Airflow API]((manage-connections-variables#airflow-api)).

:::

Astronomer recommends using the [Astro CLI](cli/overview.md) to run a local Airflow environment and test your DAGs locally before deploying to Astro. Your Airflow connection and variable management strategy to be compatible with both your local testing workflows as well as your Astro workflows. Therefore, to minimize complexity, try using only one type of strategy for both local and deployed Airflow environments. 

The following table suggests some possible management strategies for specific use cases.

| Scenario | Strategy |
| I'm just getting started and want to quickly create Airflow objects | Airflow UI |
| I want to deploy the same connections and variables across multiple different Airflow environments  | `airflow_settings.yaml` or environment variables |
| I need to keep my connections and variables as secure as possible | Environment variables or secrets backend |



### Airflow UI


The easiest and most accessible way to create Airflow connections and variables locally is through the Airflow UI. This experience is similar across all different flavours of Airflow. This is also the first step for creating, testing and generating the URI/JSON format for a new connection.

**Benefits**

- The UI has features for correctly formatting and testing your connections.
- You can export your variables from the Airflow UI, as well as import them to the Airflow UI from a json file.
- Connections and variables are encrypted and stored in the Airflow metadata database.

**Limitations**

- You can only automatically export your Airflow variables to Astro as environment variables.
- Managing many connections or variables can become unwieldy.
- It's not the most secure option for sensitive variables.
- In a local environment, you'll lose your connections and variables if you delete your metadata database with `astro dev kill`.

### Secrets backend

:::tip IMPORTANT

Astronomer recommends this approach for Astro and local Airflow.

:::

A secrets backend is the most secure and recommended way to access connections and variables on Airflow. To unit test your DAGs locally, you can choose to use to skip this but it is advisable to integrate with a Secrets backend before you deploy to production. See how you can configure a secrets backend [locally](cli/authenticate-to-clouds) and on [Astro](secrets-backend). 

**Benefits**

- It's compatible with strict organization security standards.
- Centralized and Secure Storage for Secrets
- Easy access and management of secrets that can be shared across different Airflow environments
- Configure secrets backend to allow selective access based on naming convention

**Limitations**

- Third-party secrets manager is required
- Ways to access secrets manager locally and from Astro differ, hence first-time setup is complicated.
- You cannot use Airflow UI to view connections and variables.
- You are responsible to ensure the secrets are encrypted

### Environment Variables

:::tip IMPORTANT

Astronomer recommends this for local Airflow only

:::

You can use Airflow's system-level environment variables to store connections and variables. This strategy is good if you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables. Generally, this strategy is used for local Airflow and the connections are prefixed using `AIRFLOW_CONN_` and variables using `AIRFLOW_VAR_` .

**Benefits**

- For local Airflow, if your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables in the `.env` file.
- You can export environment variables from local Airflow using the Astro CLI.
- In case you want to override, variables set using Environment Variables take precedence over variables defined in the Airflow UI.
- For Astro Deployment, you can edit/manage your connections and variables from the Cloud UI.
- Environment variables marked as secret are encrypted in the Astronomer control plane.

**Limitations**

- Connections and Variables ***can't be*** viewed from the Airflow UI, but you can use them in your DAGs. Connections will also not be visible using `airflow connections list`
- For local Airflow, you have to restart your local environment using `astro dev restart` whenever you make changes to your `.env` file.
- The environment variables are defined in plain text in `.env` and you can only mark them as a secret once you deploy to Astro.
- Connections are more difficult to format as URIs and JSON.
- It's not secure or centralized as a secrets backend.

### Airflow API

You can use the Airflow REST API to programmatically create Airflow connections and variables on a Deployment. Airflow objects created this way are stored in the Airflow metadata database. This strategy is good for teams setting up large Deployments with many Airflow connections and variables.

**Benefits**

- Manage secrets at a central point and programmatically load in Airflow using API
- Allow to have a secure as well as consistent environment for local and Astro
- Connections and variables are encrypted and stored in the Airflow metadata database
- Ability to see connections and variables from the UI
- Ability to export connections and variables using API

**Limitations**

- Dependency on a separate process to keep the secrets in sync.
- Ability to Airflow users to override
- Secret values are omitted or redacted from the response when exporting connections/variables

### Local only `airflow_settings.yaml`

You can use the Astro CLI to manage local Airflow connections and variables with an [`airflow_settings.yaml`](manage-connections-variables#local-only-airflow_settingsyaml) file. The CLI automatically adds all Airflow connections, variables, and pools listed in this file to your local metadata database.

**Benefits**

- For local Airflow, if your local metadata database gets corrupted or accidentally deleted, you will still have access to your connections and variables.
- You can have multiple files for different groups of objects. For example, you can use a file called `airflow_settings_dev.yaml` to test DAGs with resources specific to dev.
- You can apply changes from the file without restarting your local Airflow environment.
- Ability to see connections and variables from the UI
- Ability to export connections and variables using API
- Connections and variables are encrypted and stored in the Airflow metadata database

**Limitations**

- You can't directly export your configurations to Astro because this file does not work on Astro deployments Airflow environments. It requires a two-step process of export and import using Astro CLI
- You have to manage your connections and variables as YAML.
- It’s not secure or centralized as a secrets backend

## Deploy to Astro

To deploy to Astro from local Airflow, user might need to export the connections and variables from local and import into Astro deployment. Import or export will depend on where the connections and variables are stored. There are three possible storage locations for the strategies discussed above and how to access the connections and variables from them:

| Strategy | Storage location | Visible via UI | Encrypted |
|-----------|----------------|-----|------|
| Airflow UI | Airflow metadata database | Yes | Yes. See [Fernet Key](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html#fernet) | 
| Airflow API | Airflow metadata database | Yes | Yes. See [Fernet Key](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html#fernet) |
| `airflow_settings.yaml` | Airflow metadata database | Yes | Yes. See [Fernet Key](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html#fernet) |
| Environment variables | System-level environment | No | Yes, on Astro only. See [Data Protection](data-protection.md) | 
| Secrets backend | Third-party cloud secret manager | No | Refer to your [secret manager](secrets-backend.md) |

### Import/Export


#### Secrets backend

If you use a secrets backend, the method for managing connections and variables between local environments and Deployments will vary based on your secrets backend, security policy, and naming conventions. 

#### Environment variables

- Import of connections and variables from the `.env` file is not possible either in local or Astro.
- You can export both connections and variables from local to `.env` file in URI format. See [examples](manage-connections-variables#how-to-use-astro-cli-to-export-from-local)

### How to use Astro CLI to export from local

- **YAML**

```bash
# export connections in YAML format to conns.yaml in your astro project's include dir
astro dev run connections export --file-format=yaml /usr/local/airflow/include/conns.yaml
```

- *JSON*

```bash
# export connections in JSON format to conns.json in your astro project's include dir
astro dev run connections export --file-format=json /usr/local/airflow/include/conns.json

# print the connections in the default JSON format to STDOUT
astro dev run connections export - --file-format=env --serialization-format=json

# export variables in JSON format to vars.json in your astro project's include dir
astro dev run variables export /usr/local/airflow/include/vars.json
```

- URI
```bash
# export all environment variables to .env file. It includes connections and variables stored as environment variables.
astro dev object export --env-export 

# export all connection environment variables to .env file.
astro dev object export --env-export --connections

# export all airflow variables stored as environment variables to .env file.
astro dev object export --env-export --variables

# print the connections in the default URI format to STDOUT.
astro dev run connections export - --file-format=env
```

### How to use Astro CLI to import into Astro/Local

- **Astro**

```bash
# import into Astro variables and/or connections defined as environment variables in the .env file
astro deployment variable create -d <deployment_id> --load --env .env
```

- **Local**
```bash
# import connections into local Airflow from a json or yaml file 
astro dev run connections import </path/to/your/file>

# import variables into local Airflow from a json file 
astro dev run connections import </path/to/your/file>

# import variables into local Airflow from a yaml file 
astro dev object import --settingsfile="myairflowobjects.yaml"
```