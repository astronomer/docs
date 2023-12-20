---
title: 'Set up AWS Secrets Manager as your secrets backend'
sidebar_label: 'AWS Secrets Manager'
id: aws-secretsmanager
---

This topic provides setup steps for configuring [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) as a secrets backend on Astro.

For more information about Airflow and AWS connections, see [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project) with `apache-airflow-providers-amazon` version 5.1.0 or later. See [Add Python and OS-level packages](cli/develop-project.md#add-python-and-os-level-packages).
- An IAM role with the `SecretsManagerReadWrite` policy that your Astro cluster can assume. See [AWS IAM roles](https://docs.astronomer.io/astro/connect-aws?tab=AWS%20IAM%20roles#authorization-options).

## Step 1: Add Airflow secrets to Secrets Manager

Create directories for Airflow variables and connections in AWS Secrets Manager that you want to store as secrets. You can use real or test values.

- When setting the secret type, choose `Other type of secret` and select the `Plaintext` option.
- If creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.
- The secret name is assigned after providing the plaintext value and clicking `Next`.

Secret names must correspond with the `connections_prefix` and `variables_prefix` set below in step 2. Specifically:

- If you use `"variables_prefix": "airflow/variables"`, you must set Airflow variable names as:

    ```text
    airflow/variables/<variable-key>
    ```

- The `<variable-key>` is how you will retrieve that variable's value in a DAG. For example:

    ```python
    my_var = Variable.get("variable-key>")
    ```

- If you use `"connections_prefix": "airflow/connections"`, you must set Airflow connections as:

    ```text
    airflow/connections/<connection-id>
    ```

- The `<connection-id>` is how you will retrieve that connection's URI in a DAG. For example:

    ```python
    conn = BaseHook.get_connection(conn_id="<connection-id>")
    ```

- Be sure to not include a leading `/` at the beginning of your variable or connection name

For more information on adding secrets to Secrets Manager, see [AWS documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_create-basic-secret.html).

## Step 2: Set up Secrets Manager locally

Add the following environment variables to your Astro project's `.env` file:

```text 
AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables"}
AWS_DEFAULT_REGION=<region>
AWS_ACCESS_KEY_ID=<Access Key> # Make sure the user has the permission to access secret manager
AWS_SECRET_ACCESS_KEY=<secret key>
```

After you configure an Airflow connection to AWS, can run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

## Step 3: Deploy environment variables to Astro

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