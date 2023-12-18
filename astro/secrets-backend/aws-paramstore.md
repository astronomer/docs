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

Create directories for Airflow variables and connections in Parameter Store that you want to store as secrets.

Variables and connections should be stored in `/airflow/variables` and `/airflow/connections`, respectively. For example, if you're setting a secret variable with the key `my_secret`, it should be stored in the `/airflow/connections/` directory. If you modify the directory paths, make sure you change the values for `variables_prefix` and `connections_prefix` in Step 2.

For instructions, see the [AWS Systems Manager Console](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html), the [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-cli.html), or the [Tools for Windows PowerShell](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-ps.html) documentation.
  
## Step 2: Set up Parameter Store locally

Add the following environment variables to your Astro project's `.env` file:

```text 
AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}
```

You can now run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

## Step 3: Deploy environment variables to Astro 
  
1. Run the following commands to export your secrets backend configurations as environment variables to Astro.

    ```sh
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.