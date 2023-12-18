---
title: 'Set up Azure Key Vault as your secrets backend'
sidebar_label: 'Azure Key Vault'
id: azure-key-vault
---

This topic provides setup steps for configuring [Azure Key Vault](https://azure.microsoft.com/en-gb/services/key-vault/#getting-started) as a secrets backend on Astro.

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](cli/develop-project.md#create-an-astro-project).
- An existing Azure Key Vault linked to a resource group.
- Your Key Vault URL. To find this, go to your Key Vault overview page > **Vault URI**.

If you do not already have Key Vault configured, read [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal).

## Step 1: Register Astro as an app on Azure

Follow the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to register a new application for Astro.

At a minimum, you need to add a [secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) that Astro can use to authenticate to Key Vault.

Note the value of the application's client ID and secret for Step 3.

## Step 2: Create an access policy

Follow the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a new access policy for the application that you just registered. The settings you need to configure for your policy are:

- **Configure from template**: Select `Key, Secret, & Certificate Management`.
- **Select principal**: Select the name of the application that you registered in Step 1.

## Step 3: Set up Key Vault locally

In your Astro project, add the following line to your `requirements.txt` file:

```text
apache-airflow-providers-microsoft-azure
```

Add the following environment variables to your `.env` file: 
  
```text
AZURE_CLIENT_ID="<your-client-id>" # Found on App Registration page > 'Application (Client) ID'
AZURE_TENANT_ID="<your-tenant-id>" # Found on App Registration page > 'Directory (tenant) ID'
AZURE_CLIENT_SECRET="<your-client-secret>" # Found on App Registration Page > Certificates and Secrets > Client Secrets > 'Value'
AIRFLOW__SECRETS__BACKEND=airflow.providers.microsoft.azure.secrets.key_vault.AzureKeyVaultBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "<your-vault-url>"}
```

This tells Airflow to look for variable information at the `airflow/variables/*` path in Azure Key Vault and connection information at the `airflow/connections/*` path. You can now run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

By default, this setup requires that you prefix any secret names in Key Vault with `airflow-connections` or `airflow-variables`. If you don't want to use prefixes in your Key Vault secret names, set the values for `sep`, `"connections_prefix"`, and `"variables_prefix"` to `""` within `AIRFLOW__SECRETS__BACKEND_KWARGS`.

## Step 4: Deploy to Astro

1. Run the following commands to export your environment variables to Astro.
 
    ```sh
    astro deployment variable create --deployment-id <your-deployment-id> --load --env .env
    ```
    
    In the Cloud UI, mark `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET`, and `AIRFLOW__SECRETS__BACKEND_KWARGS` as **Secret**. See [Set environment variables in the Cloud UI](environment-variables.md#set-environment-variables-in-the-cloud-ui).
  
2. Run the following command to push your updated `requirements.txt` file to Astro:
  
    ```sh
    astro deploy --deployment-id <your-deployment-id> 
    ```
    
3. (Optional) Remove the environment variables from your `.env` file, or store your `.env` file so that your credentials are hidden, for example with GitHub secrets.