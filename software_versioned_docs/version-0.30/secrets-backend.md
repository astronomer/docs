---
title: 'Configure an external secrets backend on Astronomer Software'
sidebar_label: 'Configure a secrets backend'
id: secrets-backend
description: Configure a secrets backend on Astronomer Software to store Airflow variables and connections in a centralized place.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Apache Airflow [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) and [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#) often contain sensitive information about your external systems that should be kept [secret](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/secrets/index.html) in a secure, centralized location that complies with your organization's security requirements. While secret values of Airflow variables and connections are encrypted in the Airflow metadata database of every Deployment, Astronomer recommends integrating with a secrets backend tool.

## Secrets backend tool integration benefits

Integrating a secrets backend tool with Astronomer Software allows you to:

- Store Airflow variables and connections in a centralized location alongside secrets from other tools and systems used by your organization, including Kubernetes secrets, SSL certificates, and more.
- Comply with internal security postures and policies that protect your organization.
- Recover in the case of an incident.
- Automatically pull Airflow variables and connections that are already stored in your secrets backend when you create a new Deployment instead of having to set them manually in the Airflow UI.

Astronomer Software integrates with the following secrets backend tools:

- Hashicorp Vault
- AWS Systems Manager Parameter Store
- Google Cloud Secret Manager
- Azure Key Vault

Secrets backend integrations are configured individually with each Astronomer Software Deployment.

:::info

If you enable a secrets backend on Astronomer Software, you can continue to define Airflow variables and connections either [as environment variables](environment-variables.md#add-airflow-connections-and-variables-via-environment-variables) or in the Airflow UI as needed. If you define variables and connections in the Airflow UI, they are stored as encrypted values in the Airflow metadata database.

Airflow checks for the value of an Airflow variable or connection in the following order:

1. Secrets backend
2. Environment variable
3. The Airflow UI

:::

:::tip

Setting Airflow connections with secrets requires knowledge of how to generate Airflow connection URIs. If you plan to store Airflow connections on your secrets backend, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#connection-uri-format) for guidance on how to generate a connection URI.

:::

## Setup

<Tabs
    defaultValue="hashicorp"
    values={[
        {label: 'Hashicorp Vault', value: 'hashicorp'},
        {label: 'AWS Parameter Store', value: 'paramstore'},
        {label: 'Google Cloud Secret Manager', value: 'gcp'},
        {label: 'Azure Key Vault', value: 'azure'},
    ]}>
<TabItem value="hashicorp">

In this section, you'll learn how to use [Hashicorp Vault](https://www.vaultproject.io/) as a secrets backend for both local development and on Astronomer Software. To do this, you will:

- Create an AppRole in Vault which grants Astronomer minimal required permissions.
- Write a test Airflow variable or connection as a secret to your Vault server.
- Configure your Astro project to pull the secret from Vault.
- Test the backend in a local environment.
- Deploy your changes to Astronomer Software.

#### Prerequisites

- A [Deployment](configure-deployment.md) on Astronomer.
- [The Astro CLI](install-cli.md).
- A [Hashicorp Vault server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started).
- An Astro project initialized with `astro dev init`.
- [The Vault CLI](https://www.vaultproject.io/docs/install).
- Your Vault Server's URL. If you're using a local server, this should be `http://127.0.0.1:8200/`.

If you do not already have a Vault server deployed but would like to test this feature, Astronomer recommends that you either:

- Sign up for a Vault trial on [Hashicorp Cloud Platform (HCP)](https://cloud.hashicorp.com/products/vault) or
- Deploy a local Vault server. See [Starting the server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started) in Hashicorp documentation. 

#### Step 1: Create a Policy and AppRole in Vault

To use Vault as a secrets backend, Astronomer recommends configuring a Vault AppRole with a policy that grants only the minimum necessary permissions for Astronomer Software. To do this:

1. [Create a Vault policy](https://www.vaultproject.io/docs/concepts/policies) with the following permissions:

    ```hcl
    path "secret/data/variables/*" {
      capabilities = ["read", "list"]
    }

    path "secret/data/connections/*" {
      capabilities = ["read", "list"]
    }
    ```

2. [Create a Vault AppRole](https://www.vaultproject.io/docs/auth/approle) and attach the policy you just created to it.
3. Retrieve the `role-id` and `secret-id` for your AppRole by running the following commands:

    ```sh
    vault read auth/approle/role/<your-approle>/role-id
    vault write -f auth/approle/role/<your-approle>/secret-id
    ```

    Save these values for Step 3.

#### Step 2: Write an Airflow variable or connection to Vault

To test whether your Vault server is set up properly, create a test Airflow variable or connection to store as a secret.

To store an Airflow variable in Vault as a secret, run the following Vault CLI command with your own values:

```sh
vault kv put secret/variables/<your-variable-key> value=<your-variable-value>
```

To store a connection in Vault as a secret, run the following Vault CLI command with your own values:

```sh
vault kv put secret/connections/<your-connection-id> conn_uri=<connection-type>://<connection-login>:<connection-password>@<connection-host>:5432
```

To confirm that your secret was written to Vault successfully, run:

```sh
# For variables
$ vault kv get secret/variables/<your-variable-key>
# For connections
$ vault kv get secret/connections/<your-connection-id>
```

#### Step 3: Set up Vault locally

In your Astro project, add the [Hashicorp Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-hashicorp/stable/index.html) to your project by adding the following to your `requirements.txt` file:

```
apache-airflow-providers-hashicorp
```

Then, add the following environment variables to your `Dockerfile`:

```docker
# Make sure to replace `<your-approle-id>` and `<your-approle-secret>` with your own values.
ENV AIRFLOW__SECRETS__BACKEND=airflow.providers.hashicorp.secrets.vault.VaultBackend
ENV AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_path": "connections", "variables_path": "variables", "config_path": null, "url": "http://host.docker.internal:8200", "auth_type": "approle", "role_id":"<your-approle-id>", "secret_id":"<your-approle-secret>"}
```

This tells Airflow to look for variable and connection information at the `secret/variables/*` and `secret/connections/*` paths in your Vault server. In the next step, you'll test this configuration in a local Airflow environment.

:::danger

If you want to deploy your project to a hosted Git repository before deploying to Astronomer Software, be sure to save `<your-approle-id>` and `<your-approle-secret>` securely. Astronomer recommends adding them to your project's [`.env` file](customize-image.md#add-environment-variables-locally) and specifying this file in `.gitignore`.

When you deploy to Astronomer Software in Step 4, you can set these values as secrets in the Software UI.

:::

:::info
By default, Airflow uses `"kv_engine_version": 2`, but this secret was written using v1. You can change this to accommodate how you write and read your secrets.
:::

For more information on the Airflow provider for Hashicorp Vault and how to further customize your integration, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-hashicorp/stable/_api/airflow/providers/hashicorp/hooks/vault/index.html).

#### Step 4: Run an example DAG to test Vault locally

To test Vault, write a simple DAG which calls your test secret and add this DAG to your project's `dags` directory. For example, you can use the following DAG to print the value of a variable to your task logs:

```python
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_var():
    my_var = Variable.get("<your-variable-key>")
    print(f'My variable is: {my_var}')

with DAG('example_secrets_dags', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:

  test_task = PythonOperator(
      task_id='test-task',
      python_callable=print_var,
)
```

Once you've added this DAG to your project:

1. Run `astro dev restart` to push your changes to your local Airflow environment.
2. In the Airflow UI (`http://localhost:8080/admin/`), trigger your new DAG.
3. Click on `test-task` > **View Logs**.  If you ran the example DAG above, you should see the contents of your secret in the task logs:

    ```text
    {logging_mixin.py:109} INFO - My variable is: my-test-variable
    ```

Once you confirm that the setup was successful, you can delete this example DAG.

#### Step 5: Deploy on Astronomer Software

Once you've confirmed that the integration with Vault works locally, you can complete a similar set up with a Deployment on Astronomer Software.

1. In the Software UI, add the same environment variables found in your `Dockerfile` to your Deployment [environment variables](environment-variables.md). Specify `AIRFLOW__SECRETS__BACKEND_KWARGS` as **secret** to ensure that your Vault credentials are stored securely.
2. In your Astro project, delete the environment variables from your `Dockerfile`.
3. [Deploy your changes](deploy-cli.md) to Astronomer Software.

Now, any Airflow variable or connection that you write to your Vault server can be successfully accessed and pulled by any DAG in your Deployment on Astronomer Software.

</TabItem>

<TabItem value="paramstore">

In this section, you'll learn how to use [AWS Systems Manager (SSM) Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) as a secrets backend on Astronomer Software.

#### Prerequisites

- A [Deployment](configure-deployment.md).
- The [Astro CLI](install-cli.md).
- An Astro project initialized with `astro dev init`.
- Access to AWS SSM Parameter Store.
- A valid AWS Access Key ID and Secret Access Key.

#### Step 1: Write an Airflow variable or connection to AWS Parameter Store

To start, add an Airflow variable or connection as a secret to Parameter Store for testing. For instructions, see the AWS documentation on how to do so using the [AWS Systems Manager Console](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-create-console.html), the [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-cli.html), or [Tools for Windows PowerShell](https://docs.aws.amazon.com/systems-manager/latest/userguide/param-create-ps.html).

Variables and connections should live at `/airflow/variables` and `/airflow/connections`, respectively. For example, if you're setting a secret variable with the key `my_secret`, it should exist at `/airflow/connections/my_secret`.

#### Step 2: Set up AWS Parameter Store locally

To test AWS Parameter Store locally, configure it as a secrets backend in your Astro project.

First, install the [Airflow provider for Amazon](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) by adding the following to your project's `requirements.txt` file:

```
apache-airflow-providers-amazon
```

Then, add the following environment variables to your project's `Dockerfile`:

```docker
# Make sure to replace `<your-aws-key>` and `<your-aws-secret-key>` with your own values.
ENV AWS_ACCESS_KEY_ID="<your-aws-key>"
ENV AWS_SECRET_ACCESS_KEY="<your-aws-secret-key>"
ENV AWS_DEFAULT_REGION="<your-aws-region>"
ENV AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.systems_manager.SystemsManagerParameterStoreBackend
ENV AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables"}
```

In the next step, you'll test that this configuration is valid locally.

:::danger

If you want to deploy your project to a hosted Git repository before deploying to Astronomer Software, be sure to save `<your-aws-key>` and `<your-aws-secret-key>` in a secure manner. When you deploy to Astronomer Software, use the Software UI to set these values as secrets.

:::

:::tip

If you'd like to reference an AWS profile, you can also add the `profile` param to `ENV AIRFLOW__SECRETS__BACKEND_KWARGS`.

To further customize the integration between Airflow and AWS SSM Parameter Store, reference Airflow documentation with the [full list of available kwargs](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/secrets/systems_manager/index.html).

:::

#### Step 3: Run an example DAG to test AWS Parameter Store locally

To test Parameter Store, write a simple DAG which calls your secret and add this DAG to your Astro project's `dags` directory.

For example, you can use the following DAG to print the value of an Airflow variable to your task logs:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook

def print_var():
    my_var = Variable.get("<your-variable-key>")
    print(f'My variable is: {my_var}')

with DAG('example_secrets_dags', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:

  test_task = PythonOperator(
      task_id='test-task',
      python_callable=print_var,
)
```

You can do the same for any Airflow connection.

To test your changes:

1. Run `astro dev restart` to push your changes to your local Airflow environment.
2. In the Airflow UI (`http://localhost:8080/admin/`), trigger your new DAG.
3. Click on `test-task` > **View Logs**. If you ran the example DAG above, you should see the contents of your secret in the task logs:

    ```text
    {logging_mixin.py:109} INFO - My variable is: my-test-variable
    ```

#### Step 4: Deploy to Astronomer Software

Once you've confirmed that the integration with AWS SSM Parameter Store works locally, you can complete a similar set up with a Deployment on Astronomer Software.

1. In the Software UI, add the same environment variables found in your `Dockerfile` to your Deployment [environment variables](environment-variables.md). Specify both `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as **secret** ensure that your credentials are stored securely.
2. In your Astro project, delete the environment variables from your `Dockerfile`.
3. [Deploy your changes](deploy-cli.md) to Astronomer Software.

Now, any Airflow variable or connection that you write to AWS SSM Parameter Store can be automatically pulled by any DAG in your Deployment on Astronomer Software.

</TabItem>

<TabItem value="gcp">

In this section, you'll learn how to use [Google Cloud Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) as a secrets backend on Astronomer Software.

#### Prerequisites

- A [Deployment](configure-deployment.md).
- The [Astro CLI](install-cli.md).
- An Astro project initialized with `astro dev init`.
- [Cloud SDK](https://cloud.google.com/sdk/gcloud).
- A Google Cloud environment with [Secret Manager](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) configured.
- A [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control) role on Google Cloud.
- A [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) for the service account.

#### Step 1: Write an Airflow variable or connection to Google Cloud Secret Manager

To start, add an Airflow variable or connection as a secret to Google Cloud Secret Manager. You can do so in the Cloud Console or the gcloud CLI.

Secrets must be formatted such that:
- Airflow variables are set as `airflow-variables-<variable-key>`.
- Airflow connections are set as `airflow-connections-<connection-id>`.

For example, to add an Airflow variable with a key `my-secret-variable`, you would run the following gcloud CLI command:

```sh
gcloud secrets create airflow-variables-<my-secret-variable> \
    --replication-policy="automatic"
```

For more information on creating secrets in Google Cloud Secret Manager, see the [Google Cloud documentation](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#create).

#### Step 2: Set up Secret Manager locally

To test Google Secret Manager locally, configure it as a secrets backend in your Astro project.

First, install the [Airflow provider for Google](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html) by adding the following to your project's `requirements.txt` file:

```
apache-airflow-providers-google
```

Then, add the following environment variables to your project's Dockerfile:

```docker
ENV AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
ENV AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "gcp_keyfile_dict": <your-key-file>}
```

Make sure to paste your entire JSON service account key in place of `<your-key-file>`. In the next step, you'll test that this configuration is valid locally.

:::danger

If you want to deploy your project to a hosted Git repository before deploying to Astronomer, be sure to save `<your-key-file>` securely. Astronomer recommends adding it to your project's [`.env` file](customize-image.md#add-environment-variables-locally) and specifying this file in `.gitignore`. When you deploy to Astronomer, you should set these values as secrets in the Software UI.

:::

#### Step 3: Run an example DAG to test Secret Manager locally

To test Secret Manager, [create a secret](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#create) containing either an Airflow variable or connection for testing.

Once you create a test secret, write a simple DAG which calls the secret and add this DAG to your project's `dags` directory. For example, you can use the following DAG to print the value of a variable to your task logs:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook

def print_var():
    my_var = Variable.get("<your-variable-key>")
    print(f'My variable is: {my_var}')

with DAG('example_secrets_dags', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:

  test_task = PythonOperator(

      task_id='test-task',
      python_callable=print_var,
)
```

To test your changes:

1. Run `astro dev stop` followed by `astro dev start` to push your changes to your local Airflow environment.
2. In the Airflow UI (`http://localhost:8080/admin/`), trigger your new DAG.
3. Click on `test-task` > **View Logs**. If you ran the example DAG above, you should see the contents of your secret in the task logs:

    ```text
    {logging_mixin.py:109} INFO - My variable is: my-test-variable
    ```

Once you confirm that the setup was successful, you can delete this DAG.

#### Step 4: Deploy to Astronomer Software

Once you've confirmed that the integration with Google Cloud Secret Manager works locally, you can complete a similar set up with a Deployment on Astronomer Software.

1. In the Software UI, add the same environment variables found in your `Dockerfile` to your Deployment [environment variables](environment-variables.md). Specify both `AIRFLOW__SECRETS__BACKEND` and `AIRFLOW__SECRETS__BACKEND_KWARGS` as **Secret** to ensure that your credentials are stored securely.
2. In your Astro project, delete the environment variables from your `Dockerfile`.
3. [Deploy your changes](deploy-cli.md) to Astronomer Software.

You now should be able to see your secret information being pulled from Secret Manager on Astronomer. From here, you can store any Airflow variables or connections as secrets on Secret Manager and use them in your project.

</TabItem>

<TabItem value="azure">

In this section, you'll learn how to use [Azure Key Vault](https://cloud.google.com/secret-manager/docs/configuring-secret-manager) as a secrets backend on Astronomer Software.

#### Prerequisites

- A [Deployment](configure-deployment.md).
- The [Astro CLI](install-cli.md).
- An Astro project initialized with `astro dev init`.
- An existing Azure Key Vault linked to a resource group.
- Your Key Vault URL. To find this, go to your Key Vault overview page > **Vault URI**.

If you do not already have Key Vault configured, see the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal).

#### Step 1: Register Astronomer as an app on Azure

Follow the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to register a new application for Astronomer.

At a minimum, you need to add a [secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) that Astronomer can use to authenticate to Key Vault.

Note the value of the application's client ID and secret for Step 3.

#### Step 2: Create an access policy

Follow the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a new access policy for the application that you just registered. The settings you need to configure for your policy are:

- **Configure from template**: Select `Key, Secret, & Certificate Management`.
- **Select principal**: Select the name of the application that you registered in Step 1.

#### Step 3: Set up Key Vault locally

In your Astro project, add the following line to your `requirements.txt` file:

```text
apache-airflow-providers-microsoft-azure
```

In your `Dockerfile`, add the following environment variables with your own values:

```docker
ENV AZURE_CLIENT_ID="<your-client-id>" # Found on App Registration page > 'Application (Client) ID'
ENV AZURE_TENANT_ID="<your-tenant-id>" # Found on App Registration page > 'Directory (tenant) ID'
ENV AZURE_CLIENT_SECRET="<your-client-secret>" # Found on App Registration Page > Certificates and Secrets > Client Secrets > 'Value'
ENV AIRFLOW__SECRETS__BACKEND=airflow.providers.microsoft.azure.secrets.azure_key_vault.AzureKeyVaultBackend
ENV AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "<your-vault-url>"}
```

This tells Airflow to look for variable information at the `airflow-variables-*` path in Azure Key Vault and connection information at the `airflow-connections-*` path. In the next step, you'll run an example DAG to test this configuration locally.

:::tip
By default, this setup requires that you prefix any secret names in Key Vault with `airflow-connections` or `airflow-variables`. If you don't want to use prefixes in your Key Vault secret names, set the values for `sep`, `"connections_prefix"`, and `"variables_prefix"` to `""` within `AIRFLOW__SECRETS__BACKEND_KWARGS`.

:::danger

If you want to deploy your project to a hosted Git repository before deploying to Astronomer, be sure to save `<your-client-id>`, `<your-tenant-id>`, and `<your-client-secret>`  in a secure manner. When you deploy to Astronomer, you should set these values as secrets with the Software UI.

:::

#### Step 4: Test Key Vault locally

To test your Key Vault setup on Astronomer locally, [create a new secret](https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal#add-a-secret-to-key-vault) in Key Vault containing either a variable or a connection.

Once you create a test secret, write a simple DAG which calls the secret and add this DAG to your project's `dags` directory. For example, you can use the following DAG to print the value of a variable to your task logs:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook

def print_var():
    my_var = Variable.get("<your-variable-key>")
    print(f'My variable is: {my_var}')

with DAG('example_secrets_dags', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:

  test_task = PythonOperator(
      task_id='test-task',
      python_callable=print_var,
)
```

To test your changes:

1. Run `astro dev stop` followed by `astro dev start` to push your changes to your local Airflow environment.
2. In the Airflow UI (`http://localhost:8080/admin/`), trigger your new DAG.
3. Click on `test-task` > **View Logs**. If you ran the example DAG above, you should see the contents of your secret in the task logs:

    ```text
    {logging_mixin.py:109} INFO - My variable is: my-test-variable
    ```

Once you confirm that the setup was successful, you can delete this DAG.

#### Step 5: Push changes to Astronomer

Once you've confirmed that your secrets are being imported correctly to your local environment, you're ready to configure the same feature in a Deployment on Astronomer Software.

1. In the Software UI, add the same environment variables found in your `Dockerfile` to your Deployment [environment variables](environment-variables.md). Specify the `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` variables as **Secret** to ensure that your credentials are stored securely.
2. In your Astro project, delete the environment variables from your `Dockerfile`.
3. [Deploy your changes](deploy-cli.md) to Astronomer Software.

From here, you can store any Airflow variables or connections as secrets on Key Vault and use them in your project.

</TabItem>

</Tabs>
