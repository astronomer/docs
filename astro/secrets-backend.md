---
title: 'Configure an external secrets backend on Astro'
sidebar_label: 'Configure a secrets backend'
id: secrets-backend
---

<head>
  <meta name="description" content="Learn how you can configure a secrets backend on Astro to store Airflow variables and connections in a secure, centralized location that complies with your organization's security requirements." />
  <meta name="og:description" content="Learn how you can configure a secrets backend on Astro to store Airflow variables and connections in a secure, centralized location that complies with your organization's security requirements." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Apache Airflow [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) and [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#) often contain sensitive information about your external systems that should be kept [secret](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/secrets/index.html) in a secure, centralized location that complies with your organization's security requirements.

While secret values of Airflow variables and connections are encrypted in the Airflow metadata database of every Deployment, Astronomer recommends integrating with a secrets backend tool. This guide explains how to configure connections to various secrets backend tools on Astro.

:::tip

If you only need a local connection to your cloud for testing purposes, consider mounting your user credentials to a local Airflow environment. While this implementation is not recommended for deployed environments, it lets you quickly test pipelines with data hosted in your cloud. See [Authenticate to cloud services](cli/authenticate-to-clouds.md).

:::

## Benefits

Integrating a secrets backend tool with Astro allows you to:

- Store Airflow variables and connections in a centralized location alongside secrets from other tools and systems used by your organization, including Kubernetes secrets, SSL certificates, and more.
- Comply with internal security postures and policies that protect your organization.
- Recover in the case of an incident.
- Automatically pull Airflow variables and connections that are already stored in your secrets backend when you create a new Deployment instead of having to set them manually in the Airflow UI.

Astro integrates with the following secrets backend tools:

- Hashicorp Vault
- AWS Systems Manager Parameter Store
- AWS Secrets Manager
- Google Cloud Secret Manager
- Azure Key Vault

Secrets backend integrations are configured individually with each Astro Deployment.

:::info

If you enable a secrets backend on Astro, you can continue to define Airflow variables and connections either [as environment variables](environment-variables.md) or in the Airflow UI. If you set Airflow variables and connections in the Airflow UI, they are stored as encrypted values in the Airflow metadata database.

Airflow checks for the value of an Airflow variable or connection in the following order:

1. Secrets backend
2. Environment variable
3. The Airflow UI

:::

Using secrets to set Airflow connections requires knowledge of how to generate Airflow connection URIs. If you plan to store Airflow connections on your secrets backend, see [URI format](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#connection-uri-format) for guidance on how to generate a connection URI.

## Setup

<Tabs
    defaultValue="secretsmanager"
    groupId= "setup"
    values={[
        {label: 'AWS Secrets Manager', value: 'secretsmanager'},
        {label: 'Hashicorp Vault', value: 'hashicorp'},
        {label: 'Google Cloud Secret Manager', value: 'gcp'},
        {label: 'Azure Key Vault', value: 'azure'},
        {label: 'AWS Parameter Store', value: 'paramstore'},
    ]}>
    
<TabItem value="secretsmanager">

This topic provides setup steps for configuring [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) as a secrets backend on Astro.

For more information about Airflow and AWS connections, see [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).

#### Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project) with `apache-airflow-providers-amazon` version 5.1.0 or later. See [Add Python and OS-level packages](develop-project.md#add-python-and-os-level-packages).
- An IAM role with the `SecretsManagerReadWrite` policy that your Astro cluster can assume. See [AWS IAM roles](https://docs.astronomer.io/astro/connect-aws?tab=AWS%20IAM%20roles#authorization-options).

#### Add Airflow secrets to Secrets Manager

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

#### Set up Secrets Manager locally

Add the following environment variables to your Astro project's `.env` file:

```text 
AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables"}
AWS_DEFAULT_REGION=<region>
AWS_ACCESS_KEY_ID=<Access Key> # Make sure the user has the permission to access secret manager
AWS_SECRET_ACCESS_KEY=<secret key>
```

After you configure an Airflow connection to AWS, can run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

#### Deploy environment variables to Astro

1. Run the following commands to export your secrets backend configurations as environment variables to Astro.

    ```sh
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
  
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. Optional. Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials. 

  :::info
    
  If you delete the `.env` file, the Secrets Manager backend won't work locally.

  :::

3. Open the Airflow UI for your Deployment and create an [Amazon Web Services connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) without credentials. When you use this connection in a DAG, Airflow will automatically fall back to using the credentials in your configured environment variables. 
 
To further customize the Airflow and AWS SSM Parameter Store integration, see the [full list of available kwargs](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/secrets/systems_manager/index.html).

</TabItem>
    
<TabItem value="hashicorp">

This topic provides steps for using [Hashicorp Vault](https://www.vaultproject.io/) as a secrets backend for both local development and on Astro. To do this, you will:

- Create an AppRole in Vault which grants Astro minimal required permissions.
- Write a test Airflow variable or connection as a secret to your Vault server.
- Configure your Astro project to pull the secret from Vault.
- Test the backend in a local environment.
- Deploy your changes to Astro.

#### Prerequisites

- A [Deployment](create-deployment.md) on Astro.
- [The Astro CLI](cli/overview.md).
- A local or hosted Vault server. See [Starting the Server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started) or [Create a Vault Cluster on HCP](https://developer.hashicorp.com/vault/tutorials/cloud/get-started-vault).
- An [Astro project](develop-project.md#create-an-astro-project).
- [The Vault CLI](https://www.vaultproject.io/docs/install).
- Your Vault Server's URL. If you're using a local server, this should be `http://127.0.0.1:8200/`.

If you do not already have a Vault server deployed but would like to test this feature, Astronomer recommends that you either:

- Sign up for a Vault trial on [Hashicorp Cloud Platform (HCP)](https://cloud.hashicorp.com/products/vault) or
- Deploy a local Vault server. See [Starting the server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started) in Hashicorp documentation. 

#### Create a Policy and AppRole in Vault

To use Vault as a secrets backend, Astronomer recommends configuring a Vault AppRole with a policy that grants only the minimum necessary permissions for Astro. To do this:

1. Run the following command to [create a Vault policy](https://www.vaultproject.io/docs/concepts/policies) that Astro can use to access a Vault server:

    ```hcl
    vault auth enable approle
    vault policy write astro_policy - <<EOF
    path "secret/*" {
      capabilities = ["create", "read", "update", "patch", "delete", "list"]
    }
    EOF
    ```

2. Run the following command to [create a Vault AppRole](https://www.vaultproject.io/docs/auth/approle):

    ```hcl
    vault auth enable approle
    vault write auth/approle/role/astro_role \
        role_id=astro_role \
        secret_id_ttl=0 \
        secret_id_num_uses=0 \
        token_num_uses=0 \
        token_ttl=24h \
        token_max_ttl=24h \
        token_policies=astro_policy
    ```

3. Run the following command to retrieve the `secret-id` for your AppRole:

    ```bash
    vault write -f auth/approle/role/<your-approle>/secret-id
    ```

    Save this value. You'll use this later to complete the setup.
  
#### Create an Airflow variable or connection in Vault

To start, create an Airflow variable or connection in Vault that you want to store as a secret. It can be either a real or test value. You will use this secret to test your backend's functionality.

You can use an existing mount point or create a new one to store your Airflow connections and variables. For example, to create a new mount point called `airflow`, run the following Vault CLI command:

```bash
vault secrets enable -path=airflow -version=2 kv
```

To store an Airflow variable in Vault as a secret at the path `variables`, run the following Vault CLI command with your own values:

```bash
vault kv put -mount=airflow variables/<your-variable-name> value=<your-value-value>
```

To store an Airflow connection in Vault as a secret at the path `connections`, first format the connection as a URI. Then, run the following Vault CLI command with your own values:

```bash
vault kv put -mount=airflow connections/<your-connection-name> conn_uri=<connection-type>://<connection-login>:<connection-password>@<connection-host>:<connection-port>
```

To format existing connections in URI format, see [Import and export connections](import-export-connections-variables.md#using-the-astro-cli-local-environments-only).

:::caution

Do not use custom key names for your secrets. Airflow requires the key name `value` for all Airflow variables and the key name `conn_uri` for all Airflow connections as shown in the previous commands.

:::

To confirm that your secret was written to Vault successfully, run:

```bash
# For variables
$ vault kv get -mount=airflow variables/<your-variable-name>

# For connections
$ vault kv get -mount=airflow connections/<your-connection-name>
```

#### Set up Vault locally

In your Astro project, add the [Hashicorp Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-hashicorp/stable/index.html) to your project by adding the following to your `requirements.txt` file:

```bash
apache-airflow-providers-hashicorp
```

Then, add the following environment variables to your `.env` file:

```bash
AIRFLOW__SECRETS__BACKEND=airflow.providers.hashicorp.secrets.vault.VaultBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_path": "connections", "variables_path": "variables",  "mount_point": "airflow", "url": "http://host.docker.internal:8200", "auth_type": "approle", "role_id":"astro_role", "secret_id":"<your-approle-secret>"}
```

:::info 

If you run Vault on Hashicorp Cloud Platform (HCP):
 
- Replace `http://host.docker.internal:8200` with `https://<your-cluster>.hashicorp.cloud:8200`.
- Add `"namespace": "admin"` as an argument after `url`.

:::

This tells Airflow to look for variable and connection information at the `airflow/variables/*` and `airflow/connections/*` paths in your Vault server. You can now run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

For more information on the Airflow provider for Hashicorp Vault and how to further customize your integration, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-hashicorp/stable/_api/airflow/providers/hashicorp/hooks/vault/index.html).

#### Deploy to Astro  
  
1. Run the following commands to export your environment variables to Astro:   
 
    ```bash
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.hashicorp.secrets.vault.VaultBackend
  
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_path": "connections", "variables_path": "variables", "mount_point": "airflow", "url": "<your-hashicorpvault-url>", "auth_type": "approle", "role_id":"astro_role", "secret_id":"<your-approle-secret>"}' --secret
    ```
  
2. Run the following command to push your updated `requirements.txt` file to Astro:
  
    ```bash
    astro deploy --deployment-id <your-deployment-id> 
    ```

3. Optional. Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.
  
Now, any Airflow variable or connection that you write to your Vault server can be successfully accessed and pulled by any DAG in your Deployment on Astro.

</TabItem>

<TabItem value="paramstore">

In this section, you'll learn how to use [AWS Systems Manager (SSM) Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) as a secrets backend on Astro.

#### Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project) with version 5.1.0+ of `apache-airflow-providers-amazon`. See [Add Python and OS-level packages](develop-project.md#add-python-and-os-level-packages).
- An IAM role with access to the [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html) that your Astro cluster can assume. See [AWS IAM roles](connect-aws.md#AWS-IAM-roles).

#### Create Airflow secrets directories in Parameter Store

Create directories for Airflow variables and connections in Parameter Store that you want to store as secrets.

Variables and connections should be stored in `/airflow/variables` and `/airflow/connections`, respectively. For example, if you're setting a secret variable with the key `my_secret`, it should be stored in the `/airflow/connections/` directory. If you modify the directory paths, make sure you change the values for `variables_prefix` and `connections_prefix` in Step 2.

For instructions, see the [AWS Systems Manager Console](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html), the [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-cli.html), or the [Tools for Windows PowerShell](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-ps.html) documentation.
  
#### Set up Parameter Store locally

Add the following environment variables to your Astro project's `.env` file:

```text 
AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}
```

You can now run a DAG locally to check that your variables are accessible using `Variable.get("<your-variable-key>")`.

#### Deploy environment variables to Astro 
  
1. Run the following commands to export your secrets backend configurations as environment variables to Astro.

    ```sh
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables",  "role_arn": "<your-role-arn>", "region_name": "<your-region>"}' --secret
    ```

2. Optional. Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.

</TabItem>

<TabItem value="gcp">

This topic provides setup steps for configuring [Google Cloud Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) as a secrets backend on Astro.

#### Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project).
- [Cloud SDK](https://cloud.google.com/sdk/gcloud).
- A Google Cloud environment with [Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) configured.
- A [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control) role on Google Cloud.
- Optional: A [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) for the service account. This is required to provide access to a secrets backend from a local machine, or when you're not using Workload Identity.

#### Create an Airflow variable or connection in Google Cloud Secret Manager

To start, create an Airflow variable or connection in Google Cloud Secret Manager that you want to store as a secret. You can use the Cloud Console or the gcloud CLI.

Secrets must be formatted such that:
- Airflow variables are set as `airflow-variables-<variable-key>`.
- Airflow connections are set as `airflow-connections-<connection-id>`.

For example, to add an Airflow variable with a key `my-secret-variable`, you would run the following gcloud CLI command:

```sh
gcloud secrets create airflow-variables-<my-secret-variable> \
    --replication-policy="automatic"
```

For more information on creating secrets in Google Cloud Secret Manager, read the [Google Cloud documentation](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#create).

#### Set up GCP Secret Manager locally

1. Copy the complete JSON service account key for the service account that will be used to access Secret Manager. 
2. Add the following environment variables to your Astro project's `.env` file, replacing `<your-service-account-key>` with the key you copied in step 1:

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "gcp_keyfile_dict": "<your-service-account-key>"}
    ```

3. Optional. Run `Variable.get("<your-variable-key>")` to run a DAG locally and confirm that your variables are accessible.

#### Configure Secret Manager on Astro using Workload Identity (Recommended)

1. Set up Workload Identity for your Airflow Deployment. See [Connect Astro to GCP data sources](connect-gcp.md?tab=Workload%20Identity#authorization-options).

2. Run the following commands to set the secrets backend for your Astro Deployment:

    ```text
    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend

    $ astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<your-secret-manager-project-id>"}
    ```

3. Optional. Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.

To ensure the security of secrets, the `.env` variable is only available in your local environment and not in the Cloud UI . See [Set Environment Variables Locally](https://docs.astronomer.io/astro/develop-project#set-environment-variables-locally).

#### Configure Secret Manager on Astro using a service account JSON key file

1. Set up the Secret Manager locally. See [Set up GCP Secret Manager locally](#set-up-gcp-secret-manager-locally).

2. Run the following command to set the `SECRET_VAR_SERVICE_ACCOUNT` environment variable on your Astro Deployment: 
 
    ```sh
    astro deployment variable create --deployment-id <your-deployment-id> SECRET_VAR_SERVICE_ACCOUNT="<your-service-account-key>" --secret
    ```

3. Optional. Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.

</TabItem>

<TabItem value="azure">

This topic provides setup steps for configuring [Azure Key Vault](https://azure.microsoft.com/en-gb/services/key-vault/#getting-started) as a secrets backend on Astro.

#### Prerequisites

- A [Deployment](create-deployment.md).
- The [Astro CLI](cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project).
- An existing Azure Key Vault linked to a resource group.
- Your Key Vault URL. To find this, go to your Key Vault overview page > **Vault URI**.

If you do not already have Key Vault configured, read [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal).

#### Register Astro as an app on Azure

Follow the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to register a new application for Astro.

At a minimum, you need to add a [secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) that Astro can use to authenticate to Key Vault.

Note the value of the application's client ID and secret for Step 3.

#### Create an access policy

Follow the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a new access policy for the application that you just registered. The settings you need to configure for your policy are:

- **Configure from template**: Select `Key, Secret, & Certificate Management`.
- **Select principal**: Select the name of the application that you registered in Step 1.

#### Set up Key Vault locally

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

#### Deploy to Astro

1. Run the following commands to export your environment variables to Astro.
 
    ```sh
    astro deployment variable create --deployment-id <your-deployment-id> --load --env .env
    ```
    
    In the Cloud UI, mark `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET`, and `AIRFLOW__SECRETS__BACKEND_KWARGS` as **Secret**. See [Set environment variables in the Cloud UI](environment-variables.md#set-environment-variables-in-the-cloud-ui).
  
2. Run the following command to push your updated `requirements.txt` file to Astro:
  
    ```sh
    astro deploy --deployment-id <your-deployment-id> 
    ```
    
3. Optional. Remove the environment variables from your `.env` file, or store your `.env` file so that your credentials are hidden, for example with GitHub secrets.

</TabItem>

</Tabs>
