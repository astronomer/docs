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
- (Optional) AWS IAM Credentials, both the AWS Access Key ID and AWS Access Key Secret, for an identity that has the required permissions to interact with Parameter Store from Airflow running locally. If you're using IAM roles, this access key should be for the identity that owns the IAM role.

## Step 1: Create Airflow secrets directories in Parameter Store

1. Create directories for Airflow variables and connections in Parameter Store that you want to store as secrets. For instructions, see the [AWS Systems Manager Console](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html), the [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-cli.html), or the [Tools for Windows PowerShell](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-ps.html) documentation.

Store your variables in `/airflow/variables` and connections in `/airflow/connections`. For example, if you're setting a secret variable with the key `my_secret`, store it in the `/airflow/connections/` directory. If you modify the directory paths, make sure you change the values for `variables_prefix` and `connections_prefix` when you set up Paramater Store locally in Step 2.

## Step 2: Set up Parameter Store locally

In this step, you add two environment variables that define the type of secrets backend you want Airflow to use and the configuration values to connect Airflow to that secrets backend.

- `AIRFLOW__SECRETS__BACKEND` defines the type of secrets backend you want to use and the Airflow provider package required to use it.
- `AIRFLOW_SECRETS_BACKEND_KWARGS` specifies the values needed for Airflow to connect to your secrets backend tool.

1. Add the following environment variables to your Astro project's Dockerfile:

    ```dockerfile
    ENV AIRFLOW__SECRETS__BACKEND="airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend"
    ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables"}'
    ```

    :::tip

    You can also choose to add the configuration variables to your `.env` file instead of your Dockerfile. Instead of using the variable format, `ENV <environment-variable-name>`, you just declare `<environment-variable-name>`. For example, instead of `ENV AIRFLOW_SECRETS_BACKEND`, you use `AIRFLOW_SECRETS_BACKEND`.

    :::

2. (Optional) Run a DAG locally  using `Variable.get("<your-variable-key>")` to check that your variables are accessible.

## Step 3: (Optional) Assign an access role to Airflow

If you manage permissions using [roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#api_assumerole), you can specify a role that Airflow assumes to read, write, and delete secrets in your secrets backend. Specify the role's ARN using `role_arn` in `AIRFLOW__SECRETS__BACKEND_KWARGS` as shown in the following example:

```dockerfile
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables", "role_arn": "arn:aws:iam::############:role/Airflow_ParameterStoreRole"}'
```

## Step 4: Add AWS access credentials

After defining the secrets backend and the arguments required for Airflow to use it, you need to authorize your local Deployment to access it.

1. Retrieve the following values from [AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html):

    - Access Key ID for your `AWS_ACCESS_KEY_ID`
    - The secret value for your access key `AWS_SECRET_ACCESS_KEY`
    - The [default region](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html) to use for your secrets backend for `AWS_DEFAULT_REGION`

2. Add your secrets backend access credentials to your Astro project's Dockerfile:

    ```dockerfile
    ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    ENV AWS_DEFAULT_REGION=$AWS_REGION
    ```

## Step 5: Deploy environment variables to Astro

1. Run the following commands to export your secrets backend configurations as environment variables to Astro.

    ```sh
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. Remove the environment variables from your Dockerfile or store your Dockerfile in a safe location, where you won't accidentally push to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.
