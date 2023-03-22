---
sidebar_label: 'Manage Airflow connections and variables'
title: 'Manage Airflow connections and variables on Astro'
id: airflow-connections-variables
description: "Manage Airflow Connections and Variables"
---

You can store Airflow [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) and [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) on Astro using several different methods. Each of these methods has advantages and limitations related to their security, ease of use, and performance. Similarly, there are a few strategies for testing connections and variables on your local computer and deploying these configurations to Astro.

Use this document to understand all available options for managing variables and connections in both local Astro projects and Astro Deployments. 

To set system-level environment variables to [change Airflow configuration settings](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html), see [Set environment variables](environment-variables.md). To learn more about Airflow variables and connections, see [Manage connections in Apache Airflow](https://docs.astronomer.io/learn/connections)** and [Variables in Apache Airflow: The Guide](https://marclamberti.com/blog/variables-with-apache-airflow/).

## Prerequisites

- A locally hosted Astro project. See [Create a project](create-project.md).
- A Deployment. See [Create a Deployment](create-deployment.md).

## Choose a strategy for managing connections and variables locally

Use the [Astro CLI](https://docs.astronomer.io/astro/cli/overview) to run a local Airflow environment and test your DAGs before Deploying to Astro. As part of your environment, you can configure connections and variables to use for testing.

Regardless of the strategy you choose, keep in mind the following:

- To minimize complexity, try to use only one management strategy per project.
- Your strategy for managing connections and variables locally should be compatible with your management strategy on Astro. For example, if you use a secrets backend on Astro, you might want to use test data from the same secrets backend to test your DAGs locally. Read the following topics to learn more about each available strategy for local development. 

### Manage connections and variables locally in the Airflow UI

The easiest and most accessible way to create Airflow connections and variables locally is through the Airflow UI. This process is identical to managing connections and variables in Apache Airflow.

The benefits of this strategy are:

- The UI helps you correctly format your connections and variables.
- To get started, you only need an Astro project and the Astro CLI. 

The limitations of this strategy are:

- You can only automatically export your variables to Astro as environment variables
- Managing many connections or variables this way can become unwieldy.
- It's not the most secure option for sensitive variables. 
- You'll lose your connections and variables if you delete your metadata database with `astro dev kill`.

To create Airflow connections and variables in the Airflow UI:

1. Run the following command to start your local Airflow environment:

    ```sh
    astro dev start
    ```

2. Access the Airflow UI at `localhost:8080`.
3. Create your connections and variables. See:

    - [Managing Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html)
    - [Create a Connection in the UI](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui)

Airflow connections and variables configured in the Airflow UI are stored in your local environment's metadata database. You can view all connections and variables set this way in the Airflow UI under **Admin** > **Connections** and **Admin** > **Variables**. 

#### Deploy to Astro

To export connections and variables from the Airflow UI to a Deployment on Astro, run:

```sh
astro dev object export --env-export
astro deployment variable create --deployment-name="My Deployment" --load --env .env
```

These commands format your connections and variables as system environment variables, then push the variables to Astro. Connections are formatted as [URIs](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#uri-format).

### Manage connections and variables locally as environment variables

You can use Airflow's system-level environment variables to store connections and variables for use by your DAGs. To do this locally, add each environment variable on its own line in your Astro project `.env` file. When you start your Airflow environment, the Astro CLI builds these variables into your Docker image and makes them available to your Airflow components. However, your connections and variables are not available to view in the Airflow UI. 

The benefits of managing Airflow connections and variables in your `.env` file are: 

- If your local metadata database is corrupted or accidentally deleted, you still have access to all of your connections and variables. 
- You can export the file to an Astro Deployment using the Astro CLI.
- You can manage connections and variables as code, allowing you to move and copy connections and variables between Deployments.

The limitations of this method are:

- Connections can't be viewed or managed from the Airflow UI.
- You have to restart your local Airflow environment whenever you make changes to your `.env` file. 
- You can't store your variables as secrets until you deploy to Astro.
- Connections are more difficult to format as URIs and JSON.

#### Set Airflow variables as local environment variables

To define an Airflow variable as an environment variable, use the following format:

```text
AIRFLOW_VAR_<VAR_NAME>='<VALUE>'
```

To retrieve the value of an Airflow variable in a DAG, use `os.getenv('AIRFLOW_VAR_<VAR_NAME>','<default-value>')`. This method is reduces the number of Airflow metadata database requests. However, it's less secure. Astronomer does not recommend using `os.getenv` with secret values because calling these values with the function can print them to your logs. Replace `<default_value>` with a default value to use if Airflow can't find the environment variable. Typically, this is the value you defined for the environment variable in the Cloud UI.

#### Set Airflow connections as local environment variables

To define an Airflow connection as an environment variable in Runtime 4.2 and earlier, add the connection as a [URI](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#uri-format) to your `.env` file in the following format:

```text
AIRFLOW_CONN_<CONN_ID>='<connection-uri>'
```

In Astro Runtime version 5.0 and later, you can also use JSON format to store connections. See [JSON format example](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#json-format-example). When using the JSON format in environment variables, the JSON object must be defined in a single, unbroken line. 

To use a connection in your DAG, you specify the connection ID like you normally would for a connection set in the Airflow UI.

:::tip

If you prefer to format your Airflow connections in the Airflow UI but you want to store them as environment variables, run the following command to export all connections  from the metadata database to your `.env` file:

```sh
astro dev object export --connections --env-export
```

:::

#### Deploy to Astro

To push your environment variables to a Deployment, run:

```sh
astro deployment variable create --deployment-name="My Deployment" --load --env .env
```

After running this command, open the Cloud UI and mark any environment variables storing secret values as **Secret**. See [Environment variables](environment-variables.md).

### Manage Airflow connections and variables locally using `airflow_settings.yaml`

You can use the Astro CLI to manage local Airflow connections and variables with an [`airflow_settings.yaml` file](https://docs.astronomer.io/astro/develop-project#configure-airflow_settingsyaml-local-development-only). The CLI automatically adds all Airflow connections, variables, and pools listed in this file to your local metadata database. 

The benefits of using `airflow_settings.yaml` are:

- You can copy a single configuration file into multiple projects.
- If your local metadata database gets corrupted or accidentally deleted, you will still have access to your connections and variables. 
- You can have multiple files for different groups of objects. For example, you can use a file called `airflow_settings_dev.yaml` to test DAGs with resources specific to testing.
- You can apply changes from the file without restarting your local Airflow environment. 

The limitations of this method are:

- You can't directly export your configurations to Astro.
- This file does not work on deployed Airflow environments.
- You have to manage your connections and variables as YAML.

:::tip

If you prefer to format your Airflow connections and variables in the Airflow UI but you want to store them in `airflow_settings.yaml`, run the following command to export all connections from the metadata database to your `airflow_settings.yaml` file as connection URIs:

```sh
astro dev object export --variables --connections --settings-file
```

:::

#### Create Airflow connections and variables using `airflow_settings.yaml`

See [Configure `airflow_settings.yaml` (local development only)](https://docs.astronomer.io/astro/develop-project#configure-airflow_settingsyaml-local-development-only).

#### Deploy to Astro

To export connections and variables from the Airflow UI to a Deployment on Astro, run:

```sh
astro dev object export --env-export
astro deployment variable create --deployment-name="My Deployment" --load --env .env
```

### Manage Airflow connections and variables using a secrets backend

Using a secrets backend is the most secure way to access connections and variables on Airflow. The benefits of this method are:

- It's compatible with strict organization security standards.

The limitations of this method are:

- It's complicated to set up.
- There are different recommended methods for running a secrets backend locally and running one on Astro.

#### Create Airflow connections and variables in a secrets backend

See [Configure a secrets backend](https://docs.astronomer.io/astro/secrets-backend) for steps to create Airflow environment variables on each of the most popular secrets backend services on Astro. 

To authenticate to your secrets backend locally, Astronomer recommends using your user credentials so that you don't have to request an API token for testing purposes. See [Authenticate to clouds locally with user credentials](https://docs.astronomer.io/astro/cli/authenticate-to-clouds).

#### Deploy to Astro

See [Configure a secrets backend](https://docs.astronomer.io/astro/secrets-backend) for steps to configure each of the most popular secrets backend services on Astro.  

## Choose a strategy for managing connections and variables on Astro

You can manage connections and variables on Astro similarly to how you manage them locally. However, some features available on your local deployments may not be available on Astronomer.

Regardless of the strategy you choose, keep in mind the following:

- To minimize complexity, try to use only one management strategy per Deployment.
- Your strategy for managing connections and variables locally should be compatible with your management strategy locally. For example, if you use a secrets backend on Astro, you might want to use test data from the same secrets backend to test your DAGs locally. Read the following topics to learn more about each available strategy for local development. 

### Manage connections and variables in the Airflow UI for your Deployment

Similarly to in your local environment, you can create connections and variables in the Airflow UI on your Deployment. This strategy is good if you're just getting started with Airflow or you're the only person with access to your Deployment.

The limitations of this strategy are:

- Any Workspace Admin can view your connections and variables. 
- Managing many connections or variables this way can become unwieldy.
- It's not the most secure option for sensitive variables. 
- You can't pull your variables down into a local project. 

To create Airflow connections and variables in the Airflow UI for your Deployment:

1. In the Cloud UI, select a Workspace, then select a Deployment.
2. Click **Open Airflow**. 
3. Create your connections and variables. See:

    - [Managing Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html)
    - [Create a Connection in the UI](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui)

### Store connections and variables as environment variables

You can use Astro [environment variables](environment-variables.md) to store Airflow connections and variables. This strategy is good if you don't have a secrets backend, but you still want to take advantage of security and RBAC features to limit access to connections and variables.

The benefits of managing Airflow connections and variables in your `.env` file are: 

- You can pull environment variables down to your local computer using the Astro CLI, making it easy to import Airflow resources from Astro.
- Your secret values are encrypted on the Astronomer control plane.

The limitations of this method are:

- Connections can't be viewed or managed from the Airflow UI.
- Connections are more difficult to format as URIs or JSON.
- It's not as secure or centralized as a secrets backend.

#### Set Airflow connections as Astro environment variables

Create an Astro environment variable to store your connection. See [Set environment variables in the Cloud UI](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-in-the-cloud-ui).

In Astro Runtime version 4.2 and earlier, use the Airflow [connection URI format](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#uri-format) to store connections as environment variables. The naming convention for Airflow environment variable connections is:

- Key: `AIRFLOW_CONN_<CONN_ID>` 
- Value: `<connection-uri>`

In Astro Runtime version 5.0 and later, you can also use JSON format to store connections. See [JSON format example](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#json-format-example). When using the JSON format in environment variables, the JSON object must be defined in a single, unbroken line. 

#### Set Airflow variables as Astro environment variables

Create an Astro environment variable to store your Airflow variable. See [Set environment variables in the Cloud UI](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-in-the-cloud-ui).

The environment variable naming convention for Airflow variables is:

- Key: `AIRFLOW_VAR_<VAR_NAME>` 
- Value: `<value>`

#### Import environment variables to a local project

If you are storing your connections and variables in Astro environment variables, run the following command to pull the keys and non-secret values of your environment variables to a local `.env` file:

```bash
astro deployment variable list --deployment-name "<deployment name>" --save --env <env-file-location>
```

This command does not pull connections or variables that were set in the Airflow UI, nor does it pull down any environment variable values stored as secrets. 

### Manage connections and variables in a secrets backend

If your team uses a secrets backend, Astronomer recommends storing Airflow connections and variables as environment variables in your secrets backend. The benefits of this method are:

- It's compatible with strict organization security standards.
- You can centralize secrets management for larger teams. 

The limitations of this method are:

- You have to manage an external tool on top of Airflow and Astro.
- Connections are more difficult to format as URIs or JSON.
- There are different recommended methods for running a secrets backend locally and running one on Astro.

See [Configure a secrets backend](secrets-backend.md) for setup steps. 

### Create connections and variables using the Airflow API

You can use the Airflow REST API to programmatically create Airflow connections and variables on a Deployment. 

Airflow objects created this way are stored in the Airflow metadata database on your Deployment data plane. This strategy is good for teams setting up large Deployments with many Airflow connections and variables. You can also use the API to export Airflow objects, but the API response will omit secret values from an export.

See [Airflow REST API](airflow-api.md) for setup steps. See the [Airflow API documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_connection) for examples of connection and variable creation API requests.
