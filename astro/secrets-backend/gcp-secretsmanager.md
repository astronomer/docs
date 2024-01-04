---
title: 'Set up Google Cloud Secret Manager as your secrets backend'
sidebar_label: 'Google Cloud Secret Manager'
id: gcp-secretsmanager
---

This topic provides setup steps for configuring [Google Cloud Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) as a secrets backend on Astro.

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project).
- [Cloud SDK](https://cloud.google.com/sdk/gcloud).
- A Google Cloud environment with [Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) configured.
- A [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control) role on Google Cloud.
- (Optional) A [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) for the service account. This is required to provide access to a secrets backend from a local machine, or when you're not using Workload Identity.

## Step 1: Create an Airflow variable or connection in Google Cloud Secret Manager

To start, create an Airflow variable or connection in Google Cloud Secret Manager that you want to store as a secret. You can use the Cloud Console or the gcloud CLI.

Secrets must be formatted such that:
- Airflow variables are set as `airflow-variables-<variable-key>`.
- Airflow connections are set as `airflow-connections-<connection-id>`.

For example, to add an Airflow variable with a key `my-secret-variable`, you run the following gcloud CLI command:

```sh
gcloud secrets create airflow-variables-<my-secret-variable> \
    --replication-policy="automatic"
```

For more information on creating secrets in Google Cloud Secret Manager, read the [Google Cloud documentation](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#create).

## Step 2: Set up GCP Secret Manager locally

1. Copy the complete JSON service account key for the service account that you want to use to access Secret Manager. 
2. Add the following environment variables to your Astro project's `.env` file, replacing `<your-service-account-key>` with the key you copied in Step 1:

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "gcp_keyfile_dict": "<your-service-account-key>"}
    ```

3. (Optional) Run `Variable.get("<your-variable-key>")` to run a DAG locally and confirm that your variables are accessible.

## Step 3: Configure Secret Manager on Astro using Workload Identity (Recommended)

1. Set up Workload Identity for your Airflow Deployment. See [Connect Astro to GCP data sources](connect-gcp.md?tab=Workload%20Identity#authorization-options).

2. Run the following commands to set the secrets backend for your Astro Deployment:

    ```text
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<your-secret-manager-project-id>"}
    ```

3. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.

To ensure the security of secrets, the `.env` variable is only available in your local environment and not in the Cloud UI . See [Set Environment Variables Locally](cli/develop-project.md#set-environment-variables-locally).

## Step 4: Configure Secret Manager on Astro using a service account JSON key file

1. Set up the Secret Manager locally. See [Set up GCP Secret Manager locally](#set-up-gcp-secret-manager-locally).

2. Run the following command to set the `SECRET_VAR_SERVICE_ACCOUNT` environment variable on your Astro Deployment: 
 
    ```sh
    astro deployment variable create --deployment-id <your-deployment-id> SECRET_VAR_SERVICE_ACCOUNT="<your-service-account-key>" --secret
    ```

3. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.