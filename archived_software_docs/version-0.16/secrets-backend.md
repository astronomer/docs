---
title: 'Configure an External Secrets Backend on Astronomer Software'
sidebar_label: 'Configure a Secrets Backend'
id: secrets-backend
description: Configure a secret backend tool on Astronomer Software to store Airflow Connections and Variables.
---

As of [Apache Airflow® 1.10.10](https://airflow.apache.org/docs/1.10.10/howto/use-alternative-secrets-backend.html), users can manage and sync Airflow Connections and Variables from a variety of external secrets backend tools, including [Hashicorp Vault](https://www.vaultproject.io/), [AWS SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html), and [GCP Secret Manager](https://cloud.google.com/secret-manager).

This guide will walk you through how to leverage Airflow's latest feature on Astronomer with specific instructions for the following tools:

- Hashicorp Vault
- AWS SSM Parameter Store
- Google Cloud Secret Manager

## Hashicorp Vault

In this section, we'll walk through how to use Vault as a secrets backend both locally and for your Airflow Deployment running on Astronomer.

### Prerequisites

To use this feature, you'll need the following:

- "Admin" access to an Airflow Deployment on Astronomer
- [The Astronomer CLI](cli-quickstart.md)
- A running Hashicorp Vault server
- [The Vault CLI](https://www.vaultproject.io/docs/install)
- Your Vault server's [Root Token](https://www.vaultproject.io/docs/concepts/tokens#root-tokens)
- Your Vault Server's URL (if you're planning on using a local server, this should be `http://127.0.0.1:8200/`)

If you do not already have a Vault server deployed but would like to test this feature, we'd recommend either:

1. Deploying a light-weight server using [this Heroku Element](https://elements.heroku.com/buttons/pallavkothari/vault)
2. Deploying a local server via the instructions in [our Apache Airflow® and Vault guide](https://www.astronomer.io/guides/airflow-and-hashicorp-vault)

### Write a Connection to Vault

To start, you'll need to write an [Apache Airflow® connection URI](https://airflow.apache.org/docs/stable/howto/connection/index.html#generating-connection-uri) to your Vault server.

To write the connection to your Vault server as a key/value pair, run:

```
vault kv put secret/connections/<your-connection> conn_uri=my-conn-type://my-login:my-password@my-host:5432
```

This methodology should apply to any secret that is expressed as a Connection URI. For an SMTP connection, for example, this would look like the following:

```
vault kv put secret/connections/smtp_default conn_uri=smtps://user:host@relay.example.com:465
```

> **Note:** We recommend setting the path to `secret/connections/<your-connection>` to keep all of your Apache Airflow® connections organized in the `connections` directory of the mount point.

#### Confirm your secret was written successfully

To confirm that the secret was written successfully for the example above, run the following:

```
vault kv gt secret/connections/<your-connection>
```

For the SMTP example anove, the output would be:

    vault kv get secret/connections/smtp_default
    ====== Metadata ======
    Key              Value
    ---              -----
    created_time     2020-03-26T14:43:50.819791Z
    deletion_time    n/a
    destroyed        false
    version          1

    ====== Data ======
    Key         Value
    ---         -----
    conn_uri    smtps://user:host@relay.example.com:465

### Set your Connection Locally

Now that you have a running Vault server with your secret injected, the next step is to configure your `Dockerfile` to use this Vault server as the default secrets backend for your local Airflow instance. Following this section, we'll set these variables on an Airflow Deployment running on Astronomer.

To set this configuration up, follow the steps below.

1. Add the following Environment Variables to the `.env` file in your project directory to be used locally:

        VAULT__ROOT_TOKEN="YOUR-ROOT-TOKEN"
        VAULT__URL="YOUR-VAULT-URL"

   This will keep your connection to the Vault server secure. Be sure to keep your `.env` in your `.gitignore` when you deploy these changes to your project if they contain sensitive credentials. We'll set these variables separately on Astronomer.

2. Add the following lines to your `Dockerfile` to instantiate those vault-specific Environment Variables and use them in the context of Airflow's `AIRFLOW__SECRETS__BACKEND` configuration:

        ENV VAULT__ROOT_TOKEN=$VAULT__ROOT_TOKEN
        ENV VAULT__URL=$VAULT__URL
        ENV AIRFLOW__SECRETS__BACKEND="airflow.contrib.secrets.hashicorp_vault.VaultBackend"
        ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"url":$VAULT__URL,"token": $VAULT__ROOT_TOKEN,"connections_path": "connections","variables_path": "variables","kv_engine_version":1}'

   This tells Airflow to look for connection information at the `secret/connections/*` path in your Vault server.

> **Note:** By default, Airflow uses `"kv_engine_version": 2`, but we've written this secret using v1. You're welcome to change this to accommodate how you write and read your secrets.

If you'd like to further customize what the interaction between Airflow and Vault server will look like, you read [the full list of available kwargs for this integration](https://airflow.apache.org/docs/stable/_api/airflow/contrib/secrets/hashicorp_vault/index.html).

### Test Your Connection

To test your connection to Vault locally, add the code below as a new DAG in your `/dags` directory. This will print your connection information to the task logs and confirm that your connection has been established successfully.

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook


def get_secrets(**kwargs):
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    print(f"Password: {conn.password}, Login: {conn.login}, URI: {conn.get_uri()}, Host: {conn.host}")

with DAG('example_secrets_dags', start_date=datetime(2020, 1, 1), schedule_interval=None) as dag:


    test_task = PythonOperator(
        task_id='test-task',
        python_callable=get_secrets,
        op_kwargs={'my_conn_id': 'smtp_default'},
 )
```

Once you've added this DAG to your project:

1. Run `$ astro dev stop` and `$astro dev start`  to rebuild your image locally
2. Trigger your new DAG (`example_secrets_dags`) via the Airflow UI at http://localhost:8080/admin/
3. Click on `test-task` > `View Logs`
4. Confirm your `smtp_default` connection information is being printed in the task logs.

![Apache Airflow® Logs for Vault](/img/software/logs.png)

This works because we set the `connections_path` in our `AIRFLOW__SECRETS__BACKEND_KWARGS` to be `connections`. You are welcome to change this path name if you'd prefer to access Variables from a different Vault directory.

> **Note:** If you've written other secrets to your Vault server's `/connections` path, you should be able to test those here as well just by changing the `my_conn_id` value in the DAG code above.

### Use Vault Secrets in your DAGs

Once you've established that your connection is working, you can leverage the `BaseHook.get_connection(kwargs['conn_id'])` method to use your connections in your own DAG code.

You can also pass the `conn_id` of your secret directly to most Airflow operators, which will take care of instantiating the connection using a pre-built hook.

### Deploy to Astronomer

Once you've confirmed that your connections are being imported correctly locally, you're ready to set your Environment Variables on Astronomer.

1. Navigate to `Deployment > Configure > Environment Variables` section of the Software UI
2. Set your `VAULT__ROOT_TOKEN` and `VAULT__URL` as you did above
3. Click `Deploy Changes` to save and publish your changes
4. Deploy to Astronomer by running `$ astro deploy`

You now should be able to see your connection information being pulled from Vault on Astronomer! If you're interested in pulling Airflow Variables, read below.

### Pulling Variables from Vault

While the above section required that you add your connection information as a `conn_uri` to Vault, you can also pull Airflow Variables from Vault. To do so, you'll need to add your variable to vault via the following syntax:

```console
vault kv put airflow/variables/hello value=world
```

This works because we set the `variables_path` in our `AIRFLOW__SECRETS__BACKEND_KWARGS` to be `variables`. You are welcome to change this path name if you'd prefer to access variables from a different Vault directory.

Now, if you print `Variables.get('hello')` in Airflow, it will print the value of that variable. In our case, that's `world`.

## AWS SSM Parameter Store

In this section, we'll walk through how to use AWS SSM Parameter Store as a secrets backend for your Airflow Deployment running on Astronomer.

For the purpose of this doc, we'll assume you already have an SSM Parameter Store instance running.

### Prerequisites

To use this feature, you'll need the following:

- "Admin" access to an Airflow Deployment on Astronomer
- The [Astronomer CLI](cli-quickstart.md)
- A running AWS SSM Parameter Store instance
- A valid AWS Access Key ID and Secret Access Key

### Add Secrets to Parameter Store

To start, ensure that you have an Airflow Connection or Variable added to Parameter Store for testing.

Those should live at `/airflow/connections` and `/airflow/variables`, respectively. If you're using a secret with a connection id of `smtp_default`, it should exist at `/airflow/connections/smtp_default`, for example.

> **Note:** The connection you add _must_ exist as a string representing an Airflow `connection_uri`. [Here is an example](https://godatadriven.com/blog/highlights-of-the-apache-airflow-1-10-10-release/) to help get you started. You can read up on generating a `connection_uri` [in the Apache Airflow® docs here](https://airflow.apache.org/docs/stable/howto/connection/index.html#generating-connection-uri).

### Set your Connection Locally

Now that you have a Connection saved, the next step is to configure your `Dockerfile` on Astronomer to use this AWS SSM Parameter Store instance server as the default secrets backend for your local Airflow instance.

To do so, follow the steps below.

1. Add the following environment variables to the `.env` file in your project directory to be used in your _local_ Airflow instance:

        AWS_ACCESS_KEY_ID="YOUR-AWS-KEY"
        AWS_SECRET_ACCESS_KEY="YOUR-AWS-SECRET-KEY"

   This will keep our connection to the SSM server secure, though make sure to keep your `.env` file in `.gitignore` when you deploy these changes to your project. We'll set these variables separately on Astronomer.

2. Add the following lines to your `Dockerfile` to instantiate those SSM-specific Environment Variables and use them in the context of Airflow's `AIRFLOW__SECRETS__BACKEND` configuration:

        ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
        ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
        ENV AIRFLOW__SECRETS__BACKEND="airflow.contrib.secrets.aws_systems_manager.SystemsManagerParameterStoreBackend"
        ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "/airflow/connections", "variables_prefix": "/airflow/variables"}'

This tells Airflow to look for connection information at the `airflow/connections/*` path in your SSM instance.

If you're interested in further customizing what the interaction between Airflow and your SSM server looks like, learn more by reading [the full list of available kwargs for this integration](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/secrets/systems_manager/index.html).

> **Note:** If you'd like to reference an AWS profile instead of connecting via Environment Variables, you can also [add the `profile` param to your kwargs](https://airflow.apache.org/docs/1.10.10/howto/use-alternative-secrets-backend.html).

### Test Your Connection

Test the connection to AWS SSM Parameter Store by calling the `get_conn_uri` method and passing it the `conn_id` of the secret you uploaded to your parameter store. If you followed our example, this would be `smtp_default`.

### Deploy to Astronomer

Once you've confirmed that your connections are being imported correctly locally, you're ready to set your Environment Variables on Astronomer.

1. Navigate to `Deployment > Configure > Environment Variables` section of our UI
2. Set your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as you did above in your `Dockerfile`
3. Click "Deploy Changes" to save and publish your changes
4. Deploy to Astronomer by running `$ astro deploy`.

You now should be able to see your connection information being pulled from AWS SSM Parameter Store on Astronomer!

## Google Cloud Secret Manager

This setup assumes that you already have a Google Cloud project with [Secret Manager configured](https://cloud.google.com/secret-manager/docs/configuring-secret-manager). To use Google Cloud Secrets Manager as your secrets backend for an Airflow Deployment on Astronomer:

1. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the appropriate permissions on Google Cloud.
2. Add the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control) role to the service account.
3. Create and download a [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) for the service account.
4. In the Software UI, set the following [environment variables](environment-variables.md) in your Airflow Deployment, making sure to paste the entire JSON key file in place of `<your-key-file>`:

    ```sh
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "gcp_keyfile_dict": <your-key-file>}'
    ```

    We recommend marking the `AIRFLOW__SECRETS__BACKEND_KWARGS` environment variable as "Secret" because it contains sensitive information about Secrets Manager.
