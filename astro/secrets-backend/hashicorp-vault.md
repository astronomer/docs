---
title: 'Set up Hashicorp Vault as your secrets backend'
sidebar_label: 'Hashicorp Vault'
id: hashicorp-vault
---

This topic provides steps for using [Hashicorp Vault](https://www.vaultproject.io/) as a secrets backend for both local development and on Astro. 

To do this, you will:
- Create an AppRole in Vault which grants Astro minimal required permissions.
- Write a test Airflow variable or connection as a secret to your Vault server.
- Configure your Astro project to pull the secret from Vault.
- Test the backend in a local environment.
- Deploy your changes to Astro.

If you use a different secrets backend tool or want to learn the general approach on how to integrate one, see [Configure a Secrets Backend](secrets-backend.md).

## Prerequisites

- A [Deployment](create-deployment.md) on Astro.
- [The Astro CLI](cli/overview.md).
- A local or hosted Vault server. See [Starting the Server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started) or [Create a Vault Cluster on HCP](https://developer.hashicorp.com/vault/tutorials/cloud/get-started-vault).
- An [Astro project](cli/get-started-cli.md#step-1-create-an-astro-project).
- [The Vault CLI](https://www.vaultproject.io/docs/install).
- Your Vault Server's URL. If you're using a local server, this should be `http://127.0.0.1:8200/`.

If you do not already have a Vault server deployed but would like to test this feature, Astronomer recommends that you either:

- Sign up for a Vault trial on [Hashicorp Cloud Platform (HCP)](https://cloud.hashicorp.com/products/vault) or
- Deploy a local Vault server. See [Starting the server](https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server?in=vault/getting-started) in Hashicorp documentation. 

## Step 1: Create a Policy and AppRole in Vault

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
  
## Step 2: Create an Airflow variable or connection in Vault

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

:::warning

Do not use custom key names for your secrets. Airflow requires the key name `value` for all Airflow variables and the key name `conn_uri` for all Airflow connections as shown in the previous commands.

:::

To confirm that your secret was written to Vault successfully, run:

```bash
# For variables
$ vault kv get -mount=airflow variables/<your-variable-name>

# For connections
$ vault kv get -mount=airflow connections/<your-connection-name>
```

## Step 3: Set up Vault locally

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

## Step 4: Deploy to Astro  
  
1. Run the following commands to export your environment variables to Astro:   
 
    ```bash
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND=airflow.providers.hashicorp.secrets.vault.VaultBackend
  
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_path": "connections", "variables_path": "variables", "mount_point": "airflow", "url": "<your-hashicorpvault-url>", "auth_type": "approle", "role_id":"astro_role", "secret_id":"<your-approle-secret>"}' --secret
    ```
  
2. Run the following command to push your updated `requirements.txt` file to Astro:
  
    ```bash
    astro deploy --deployment-id <your-deployment-id> 
    ```

3. (Optional) Remove the environment variables from your `.env` file or store your `.env` file in a safe location to protect your credentials in `AIRFLOW__SECRETS__BACKEND_KWARGS`.
  
Now, any Airflow variable or connection that you write to your Vault server can be successfully accessed and pulled by any DAG in your Deployment on Astro.