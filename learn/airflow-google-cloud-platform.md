---
title: "Add GCP user credentials to a local Apache Airflow environment"
sidebar_label: "Authenticate to GCP locally"
description: "Learn how to connect to a hosted environment on Google Cloud Platform (GCP) from Apache Airflow. Use GCP credentials to access secrets backends and more from a locally running Airflow environment."
id: airflow-google-cloud-platform
---

For initial testing and DAG development, running Airflow with local test data and publicly accessible APIs is often enough. Once you start expanding your Airflow use within your organization, you might need to develop and test DAGs locally with data from your organization's cloud. For example, you might need to test your DAGs using environment variables stored in a secrets backend like Google Cloud Secret Manager.

You could create access keys for each user developing locally, but service account keys are difficult to track and manage especially on larger teams. Instead, Astronomer recommends exporting credentials for your own GCP account and securely adding these credentials to Airflow. This way, you know which permissions Airflow has without needing to configure a separate access key. 

## Prerequisites 

- A user account on GCP with access to GCP cloud resources
- The [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview)
- Optional. Access to a secrets backend hosted on GCP, such as GCP Secret Manager
  
## Step 1:  Retrieve GCP user credentials locally

Run the following command to obtain your user credentials locally:

```sh
gcloud auth application-default login
```

The SDK provides a link to a webpage where you can log in to your Google Cloud account. After you complete your login, the SDK stores your user credentials in a file name named `application_default_credentials.json`.

The location of this file depends on your operating system:

- Linux: `$HOME/.config/gcloud/application_default_credentials.json`
- Mac: `/Users/<username>/.config/gcloud/application_default_credentials.json`
- Windows: `%APPDATA%/gcloud/application_default_credentials.json`

## Step 2: Configure your Astro project

The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential files, you'll mount them as a volume in Docker.

1. Run the following commands to create an Astro project:

    ```sh
    $ mkdir gcp-airflow && cd gcp-airflow
    $ astro dev init
    ```

2. Add a file named `docker-compose.override.yml` to your project with the following configuration: 
   
3. Mount your Google Cloud application_default_credentials file as a volume and attach it to Airflow:

<Tabs
    defaultValue="mac"
    groupId= "step-2-configure-your-astro-project"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Linux', value: 'linux'},
        {label: 'Windows', value: 'windows'},
    ]}>
<TabItem value="mac">

```yaml
version: "3.1"
services:
    scheduler:
        volumes:
        - /Users/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    webserver:
        volumes:
        - /Users/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    triggerer:
        volumes:
        - /Users/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
```

</TabItem>
<TabItem value="linux">

```yaml
version: "3.1"
services:
    scheduler:
        volumes:
        - /home/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    webserver:
        volumes:
        - /home/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    triggerer:
        volumes:
        - /home/<username>/.config/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
```

</TabItem>
<TabItem value="windows">

```yaml
version: "3.1"
services:
    scheduler:
        volumes:
        - /c/Users/<username>/AppData/Roaming/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    webserver:
        volumes:
        - /c/Users/<username>/AppData/Roaming/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
    triggerer:
        volumes:
        - /c/Users/<username>/AppData/Roaming/gcloud/application_default_credentials.json:/usr/local/airflow/gcloud/application_default_credentials.json:ro
```

</TabItem>
</Tabs>

3. In your Astro project's `.env` file, add the following environment variable. Ensure that this volume path is the same as the one your configured in `docker-compose.override.yml`.
    
    ```text
    GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcloud/application_default_credentials.json
    ```

When you run Airflow locally, all GCP connections without defined credentials now automatically fall back to your user credentials when connecting to GCP.

## Step 3: Test your credentials with a secrets backend (Optional)

Now that Airflow has access to your user credentials, you can use them to connect to GCP services. Use the following example setup to test your credentials by pulling a variable from GCP Secret Manager. 

1. Create a secret for an Airflow variable or connection in GCP Secret Manager. You can do this using the Google Cloud Console or the gcloud CLI. All Airflow variables and connection keys must be prefixed with the following strings respectively:

    - `airflow-variables-`
    - `airflow-connections-`

    When setting the secret type, choose `Other type of secret` and select the `Plaintext` option. If you're creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.

2. Add the following environment variables to your Astro project `.env` file:

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables"}
    ```

3. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

4. Access the Airflow UI at `localhost:8080` and create an Airflow GCP connection named `gcp_standard` with no credentials. See [Connections](connections.md).

   When you use this connection in your DAG, it will fall back to using your configured user credentials. 

5. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve a value from `airflow/variables` and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.operators.python import PythonOperator
    from datetime import datetime
    
    def print_var():
        my_var = Variable.get("<your-variable-key>")
        print(f'My variable is: {my_var}')
    
        conn = BaseHook.get_connection(conn_id="gcp_standard")
        print(conn.get_uri())
    
    with DAG(
        dag_id='example_secrets_dag',
        start_date=datetime(2022, 1, 1),
        schedule=None
    ):
    
        test_task = PythonOperator(
            task_id='test-task',
            python_callable=print_var
        )
    ```

6. In the Airflow UI, unpause your DAG and click **Play** to trigger a DAG run. 
7. View logs for your DAG run. If the connection was successful, the value of your secret appears in your logs. See [Airflow logging](https://docs.astronomer.io/learn/logging).
