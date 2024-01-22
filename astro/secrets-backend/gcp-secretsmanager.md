---
title: 'Set up Google Cloud Secret Manager as your secrets backend'
sidebar_label: 'Google Cloud Secret Manager'
id: gcp-secretsmanager
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This topic provides setup steps for configuring [Google Cloud Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) as a secrets backend on Astro.

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project).
- [Cloud SDK](https://cloud.google.com/sdk/gcloud).
- Enable the [Google Cloud Secret Manager API](https://cloud.google.com/secret-manager/docs/configuring-secret-manager)
- A Google Cloud environment with [Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) configured.
- A [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control) role on Google Cloud.
- A [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) for the service account. This is required to provide access to a secrets backend from a local machine, or when you're not using Workload Identity.

## Step 1: Create an Airflow variable or connection in Google Cloud Secret Manager

1. Create an Airflow variable or connection in Google Cloud Secret Manager that you want to store as a secret. You can use the Cloud Console or the gcloud CLI.

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
2. Add the following environment variables to your Astro project's `.env` file, replacing `<variable-key>` with the key you copied in Step 1:

    ```text
    ENV AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend

    ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "gcp_keyfile_dict": <variable-key>}'
    ```

3. (Optional) Run `Variable.get("<your-variable-key>")` to run a DAG locally and confirm that your variables are accessible.

## Step 3: Deploy your environment variables to Astro

<Tabs
    defaultValue="workload-identity"
    values={[
        {label: 'Use Workload Identity', value: 'workload-identity'},
        {label: 'Service account JSON key file', value: 'json-key'},
    ]}>
<TabItem value="workload-identity">

#### Using Workload Identity (Recommended)

1. Set up Workload Identity for your Airflow Deployment. See [Connect Astro to GCP data sources](connect-gcp.md?tab=Workload%20Identity#authorization-options).

2. Run the following commands to set the secrets backend for your Astro Deployment:

    ```text
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<your-secret-manager-project-id>"}
    ```

3. Run the following command to push your updated `requirements.txt` file to Astro:

    ```sh
    astro deploy --deployment-id <your-deployment-id>
    ```
4. (Optional) Remove the environment variables from your `.env` file, or store your `.env` file so that your credentials are hidden, for example with GitHub secrets.

</TabItem>
<TabItem value="json-key">

#### Using a service account JSON key file

1. Run the following command to set the `SECRET_VAR_SERVICE_ACCOUNT` environment variable on your Astro Deployment:

    ```sh
    astro deployment variable create --deployment-id <your-deployment-id> SECRET_VAR_SERVICE_ACCOUNT="<your-service-account-key>" --secret
    ```

2. In the Cloud UI, mark `AIRFLOW__SECRETS__BACKEND_KWARGS` as **Secret**. See [Set environment variables in the Cloud UI](environment-variables.md#set-environment-variables-in-the-cloud-ui).

3. Run the following command to push your updated `requirements.txt` file to Astro:

    ```sh
    astro deploy --deployment-id <your-deployment-id>
    ```

4. (Optional) Remove the environment variables from your `.env` file, or store your `.env` file so that your credentials are hidden, for example with GitHub secrets.

</TabItem>
</Tabs>