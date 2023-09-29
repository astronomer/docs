---
sidebar_label: 'Environment variables'
title: 'Set environment variables on Astro'
id: environment-variables
---

<head>
  <meta name="description" content="Learn how you can set environment variables on Astro to specify Airflow configurations and custom logic that better meet the requirements of your organization." />
  <meta name="og:description" content="Learn how you can set environment variables on Astro to specify Airflow configurations and custom logic that better meet the requirements of your organization." />
</head>

import {siteVariables} from '@site/src/versions';

An environment variable on Astro is a key-value configuration that is applied to a specific Deployment. You can use environment variables to set Airflow configurations and custom values for Deployments on Astro. For example, you can use environment variables to:

- Identify a production Deployment versus a development Deployment that allows you to apply conditional logic in your DAG code.
- Store [Airflow connections and variables](environment-variables.md#add-airflow-connections-and-variables-using-environment-variables).
- Set some [core Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html).
- Set up an SMTP service to receive [Airflow alerts](airflow-email-notifications.md) by email.
- Integrate with Datadog or other third-party tooling to [export Deployment metrics](deployment-metrics.md#export-airflow-metrics-to-datadog).
- Set [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html?), such as default timezone and maximum active runs per DAG.

You can use environment variables to configure the same keys and values that you would configure as [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/index.html). However, the variables that you configure in Astro are exposed as environment variables and managed differently than Airflow variables. For more information, see [How environment variables are stored on Astro](#how-environment-variables-are-stored-on-astro).

Some environment variables on Astro are set globally and cannot be overridden for individual Deployments. For more information on these environment variables, see [Global environment variables](platform-variables.md).

## Set environment variables in the Cloud UI

:::cli

If you prefer to work with the Astro CLI, you can create and update environment variables using the `astro deployment variable create` and `astro deployment variable update` commands. See [CLI command reference](cli/astro-deployment-variable-create.md).

:::

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Variables** tab.

3. Click **Edit Variables**.

4. Enter an environment variable key and value. For sensitive credentials that should be treated with an additional layer of security, select the **Secret** checkbox. This will permanently hide the variable's value from all users in your Workspace.

5. Click **Add**.

6. Click **Save Variables** to save your changes. Your Airflow scheduler, webserver, and workers restart. After saving, it can take up to two minutes for new variables to be applied to your Deployment.

### Edit existing values

After you set an environment variable key, only the environment variable value can be modified. You can modify environment variables that are set as secret. However, the variable value is never shown. When you modify a secret environment variable, you'll be prompted to enter a new value.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Variables** tab.

3. Click **Edit Variables**.

4. Click **Edit value** next to the value you want to edit.

    ![Edit value location](/img/docs/variable-pencil.png)

5. Modify the variable's value, then click **Done editing**.

    ![Done editing location](/img/docs/variable-checkmark.png)

6. Click **Save Variables** to save your changes. Your Airflow scheduler, webserver, and workers restart. After saving, it can take up to two minutes for updated variables to be applied to your Deployment.

### How environment variables are stored on Astro

Non-secret environment variables set in the Cloud UI are stored in a Hashicorp Vault secrets manager hosted in Astro control plane. These environment variables are available to your Astro Deployment’s Kubernetes namespace as a Kubernetes secret.

To use these environment variables in an Astro Deployment:
- In a regular PythonOperator or Python code, you can use `os.environ` method.
- If you can’t use Python or are using a pre-defined code that expects specific keys for environment variables, you need to mount the secret environment variables using BaseOperator’s `executor_config` by providing a `pod_override`. See [Use secret environment variables in worker Pods](kubernetes-executor.md#use-secret-environment-variables-in-worker-pods).
- If you need to use these secret environment variables in a KubernetesPodOperator, see [Use secret environment variables with KubernetesPodOperator](kubernetespodoperator.md#use-secret-environment-variables-with-the-kubernetespodoperator).

:::caution

Environment variables marked as secret are stored securely by Astronomer and are not shown in the Cloud UI. However, it's possible for a user in your organization to create or configure a DAG that exposes secret values in Airflow task logs. Airflow task logs are visible to all Workspace users in the Airflow UI and accessible in your Astro cluster's storage.

To avoid exposing secret values in task logs, instruct users to not log environment variables in DAG code.

:::

## Set environment variables in your Dockerfile

If you want to store environment variables using an external version control tool, Astronomer recommends setting them in your `Dockerfile`. This file is automatically created when you first initialize an Astro project using `astro dev init`.

Environment variables added to a `Dockerfile` are mounted at build time and can be referenced in any other build process that follows `astro deploy` or `astro dev start`. Environment variables applied in the Cloud UI only become available once the Docker build process is completed.

:::caution

Environment variables set in your `Dockerfile` are stored in plain text. For this reason, Astronomer recommends storing sensitive environment variables using the Cloud UI or a third party secrets backend. For more information, see [Configure a secrets backend](secrets-backend.md).

:::

To add environment variables, declare an ENV command with the environment variable key and value. For example, the following `Dockerfile` sets two environment variables:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
ENV AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=1
ENV AIRFLOW_VAR_MY_VAR=25`}</code></pre>

After you add your environment variables, use one of the following options to deploy your changes:

- Run `astro dev restart` to rebuild your image and apply your changes locally.
- Run `astro deploy` to apply your changes to your Deployment on Astro.

## Environment variable priority

On Astro, environment variables are applied and overridden in the following order:

- Cloud UI
- [.env (local development only)](develop-project.md#set-environment-variables-locally)
- Dockerfile

For example, if you set `AIRFLOW__CORE__PARALLELISM` with one value in the Cloud UI and you set the same environment variable with another value in your `Dockerfile`, the value set in the Cloud UI takes precedence.

## Add Airflow connections and variables using environment variables

If you regularly use [Airflow connections](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html) and [variables](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html), Astronomer recommends storing and fetching them with environment variables instead of adding them to the Airflow UI.

Airflow connections and variables are stored in the Airflow metadata database. Calling them outside of task definitions and operators requires an additional connection to the Airflow metadata database which is used every time the scheduler parses a DAG.

By adding connections and variables as environment variables, you can lower the amount of open connections and improve the performance of your database and resources.

### Airflow connections

In Astro Runtime version 4.2 and earlier, use the Airflow [connection URI format](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#uri-format) to store connections as environment variables. The naming convention for Airflow environment variable connections is:

- Key: `AIRFLOW_CONN_<CONN_ID>` 
- Value: `<connection-uri>`

For example, consider the following Airflow connection:

- Connection ID: `MY_PROD_DB`
- Connection URI: `my-conn-type://login:password@host:5432/schema`

To store this connection as an environment variable, you create an environment variable with the key `AIRFLOW_CONN_MY_PROD_DB` and the value `my-conn-type://login:password@host:5432/schema`.

In Astro Runtime version 5.0 and later, you can also use JSON format to store connections. See [JSON format example](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#json-format-example). When using the JSON format in environment variables, the JSON object must be defined in a single, unbroken line. 

:::info

Airflow connections set with environment variables do not appear in the Airflow UI. They can only be seen and updated in the Cloud UI or your Dockerfile. 

:::

### Airflow variables

Use environment variables to store values you would normally store as [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/index.html). This gives you better control and security of custom values. To fetch a Deployment environment variable value from a DAG, you must format the variable key as `AIRFLOW_VAR_<VAR_NAME>`.

For example, consider the following Airflow variable:

- Variable name: `My_Var`
- Value: `2`

To store this Airflow variable as an environment variable, you create an environment variable with the key `AIRFLOW_VAR_MY_VAR` and the value `2`.

You can then use the following Python functions in the top level of your DAG code to fetch the variable value:

- `Variable.get('<VAR_NAME>')`: This method is more secure for fetching secret values. However, this method can affect performance because it makes a request to the Airflow metadata database every time your DAGs are parsed, which can occur every 30 seconds. See [DAG writing best practices](https://docs.astronomer.io/learn/dag-best-practices#avoid-top-level-code-in-your-dag-file) for more information about avoiding repeated requests in top level code.
- `os.getenv('AIRFLOW_VAR_<VAR_NAME>','<default-value>')`: This method is faster because it reduces the number of Airflow metadata database requests. However, it's less secure. Astronomer does not recommend using `os.getenv` with secret values because calling these values with the function can print them to your logs. 

    Replace `<default_value>` with a default value to use if Airflow can't find the environment variable. Typically, this is the value you defined for the environment variable in the Cloud UI. 

## Set Airflow configurations using environment variables

:::caution

Some Airflow configurations should not be overridden because Astro already uses them. See [Global environment variables](platform-variables.md) for a list of all non-configurable environment variables.

:::

You can use Astro environment variables to set Airflow environment variables. 

For example, to set `AIRFLOW__CORE__PARALLELISM` in your Deployment, you would configure the following environment variable:

- **Key**: `AIRFLOW__CORE__PARALLELISM`
- **Value**: `64`

See the [ Airflow Configurations Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) for a list of all possible configurations.

