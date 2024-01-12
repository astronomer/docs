---
title: 'Set up AWS Systems Manager (SSM) Parameter Store'
sidebar_label: 'AWS Systems Manager (SSM) Parameter Store'
id: aws-paramstore
---

In this section, you'll learn how to use [AWS Systems Manager (SSM) Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) as a secrets backend on Astro.

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project) with version 5.1.0+ of `apache-airflow-providers-amazon`. See [Add Python and OS-level packages](cli/develop-project.md#add-python-and-os-level-packages).
- An IAM role with access to the [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html) that your Astro cluster can assume. See [AWS IAM roles](connect-aws.md#AWS-IAM-roles).

## Step 1: Create Airflow secrets directories in Parameter Store

1. Create directories for Airflow variables and connections in Parameter Store that you want to store as secrets. For instructions, see the [AWS Systems Manager Console](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html), the [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-cli.html), or the [Tools for Windows PowerShell](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-ps.html) documentation.

Store your variables in `/airflow/variables` and connections in `/airflow/connections`. For example, if you're setting a secret variable with the key `my_secret`, store it in the `/airflow/connections/` directory. If you modify the directory paths, make sure you change the values for `variables_prefix` and `connections_prefix` when you set up Paramater Store locally in Step 2.

## Step 2: Set up Parameter Store locally

In this step, you add two environment variables that define the type of Secrets backend you want to use.

- `AIRFLOW__SECRETS__BACKEND` defines the type of Secrets Backend you want to use and the Airflow provider package required to use it.
- `AIRFLOW_SECRETS_BACKEND_KWARGS` defines the arguments needed for Airflow to initiate with your secrets backend tool.

1. Add the following environment variables to your Astro project's `.env` file:

    ```text
    ENV AIRFLOW__SECRETS__BACKEND="airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend"
    ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables"}'
    ```

2. (Optional) Run a DAG locally  using `Variable.get("<your-variable-key>")` to check that your variables are accessible.

::: tip Assign an access role to Airflow

You can [define the role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#api_assumerole) that Airflow has to read, write, and delete secrets in your secrets backend by including `role_arn` when you define backend kwargs.

```text
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables", "role_arn": "arn:aws:iam::############:role/Airflow_ParameterStoreRole"}'
```

:::

## Step 3: Add AWS access credentials

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
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location, where you won't accidentally push to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.
