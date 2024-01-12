---
title: 'Set up AWS Secrets Manager as your secrets backend'
sidebar_label: 'AWS Secrets Manager'
id: aws-secretsmanager
---

This topic provides setup steps for configuring [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) as a secrets backend on Astro. A secrets backend is configured by declaring a set of environment variables. You cans et these environment variables in several different ways, including a Dockerfile, `.env` file for the Astronomer CLI, or through the UI. This guide shows how to extend your Dockerfile to use AWS Secrets Manager as a backend, because this method works across all Astronomer products.

For more information about Airflow and AWS connections, see [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project) with `apache-airflow-providers-amazon` version 5.1.0 or later. See [Add Python and OS-level packages](cli/develop-project.md#add-python-and-os-level-packages).
- An IAM role with the `SecretsManagerReadWrite` policy that your Astro cluster can assume. See [AWS IAM roles](https://docs.astronomer.io/astro/connect-aws?tab=AWS%20IAM%20roles#authorization-options).

## Step 1: Create directories in Secrets Manager

1. Create directories for Airflow variables and connections in AWS Secrets Manager that you want to store as secrets. You can use real or test values.

2. Store your variables in `/airflow/variables` and connections in `/airflow/connections`. For example, if you're setting a secret variable with the key `my_secret`, store it in the `/airflow/connections/` directory. If you modify the directory paths, make sure you change the values for `variables_prefix` and `connections_prefix` when you set up Paramater Store locally.

## Step 2: Set up Secrets Manager locally

In this step, you add two environment variables that define the type of Secrets backend you want to use.

- `AIRFLOW__SECRETS__BACKEND` defines the type of Secrets Backend you want to use and the [Airflow provider package](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html#storing-and-retrieving-connections) required to use it.
- `AIRFLOW_SECRETS_BACKEND_KWARGS` defines the arguments needed for Airflow to initiate with your secrets backend tool.

1. Add the following environment variables to your Astro project's Dockerfile:


```text

ENV AIRFLOW__SECRETS__BACKEND="airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend"
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables", "full_url_mode": true}'

```

In order build connections using the [URI format method](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#uri-format), `full_url_mode` must be set to `true`. Starting with Airflow 2.3.0, it is not required that `full_url_mode` be set to `false` for JSON connections, so this should be set to `true` by default.

2. (Optional) After you configure an Airflow connection to AWS, can run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

::: tip Assign an access role to Airflow

You can also [define the role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#api_assumerole) that Airflow has to read, write, and delete secrets in your secrets backend by including `role_arn` when you define backend kwargs.

```text
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables", "role_arn": "arn:aws:iam::############:role/Airflow_ParameterStoreRole"}'
```

:::

## Step 3: Update your `.env` file to store AWS access details

After defining the secrets backend and the arguments required for Airflow to use it, you need to authorize your Deployment to access it.

1. Retrieve the following access credentials that your Deployment needs to access the secrets backend from [AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).

    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `AWS_DEFAULT_REGION`

2. Add your secrets backend access credentials to your Astro project's `.env` file:

    ```text
    ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    ENV AWS_DEFAULT_REGION=$AWS_REGION
    ```

## Step 4: Deploy environment variables to Astro

1. Run the following commands to export your secrets backend configurations as environment variables to Astro.

    ```sh
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials.

  :::info

  If you delete the `.env` file, the Secrets Manager backend won't work locally.

  :::

3. Open the Airflow UI for your Deployment and create an [Amazon Web Services connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) without credentials. When you use this connection in a DAG, Airflow will automatically fall back to using the credentials in your configured environment variables.

To further customize the Airflow and AWS SSM Parameter Store integration, see the [full list of available kwargs](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/secrets/systems_manager/index.html).

## Step 4: Add Airflow Secrets to the Secrets manager

In the Secrets Manager, add connections and variables to the directories you set up in Step 1.

- When setting the secret type, choose `Other type of secret` and select the `Plaintext` option.
- If creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.
- Provide the plaintext value and clicking `Next`. Then, the AWS Secrets Manager generates the secret name.

Secret names must correspond with the `connections_prefix` and `variables_prefix` that you set in step 2. Specifically:

- If you use `"variables_prefix": "airflow/variables"`, you must set Airflow variable names as:

    ```text
    airflow/variables/<variable-key>
    ```

- Use the `<variable-key>` to retrieve that variable's value in a DAG. For example:

    ```python
    my_var = Variable.get("variable-key>")
    ```

- If you use `"connections_prefix": "airflow/connections"`, you must set Airflow connections as:

    ```text
    airflow/connections/<connection-id>
    ```

- Use the `<connection-id>` to retrieve that connection's URI in a DAG. For example:

    ```python
    conn = BaseHook.get_connection(conn_id="<connection-id>")
    ```

- Be sure to not include a leading `/` at the beginning of your variable or connection name

For more information on adding secrets to Secrets Manager, see [AWS documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_create-basic-secret.html).