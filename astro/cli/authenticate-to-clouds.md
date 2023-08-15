---
title: "Authenticate to cloud services with user credentials"
sidebar_label: "Authenticate to cloud services"
description: "Configure the Astro CLI to use locally stored user credentials as the default for all connections to your cloud."
id: authenticate-to-clouds
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

When you develop Apache Airflow DAGs locally with the Astro CLI, testing with local data is the easiest way to get started. For more complex data pipelines, you might need to test DAGs locally with data that's stored in your organization's cloud, such as secret values in a secrets backend service.

To access data on the cloud while developing locally with the Astro CLI, export your cloud account user credentials to a secure configuration file and mount that file in the Docker containers running your local Airflow environment. After you configure this file, you can connect to your cloud without needing to configure additional credentials in Airflow connections. Airflow inherits all permissions from your cloud account and uses them to access your cloud.

## Setup

<Tabs
    defaultValue="aws"
    groupId= "prerequisites"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

#### Prerequisites

- A user account on AWS with access to AWS cloud resources.
- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- The [Astro CLI](astro/cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project).
    
#### Retrieve AWS user credentials locally

Run the following command to obtain your user credentials locally:
    
```
aws configure
```    

This command prompts you for your Access Key Id, Secret Access Key, Region, and output format. If you log into AWS using single sign-on (SSO), run `aws configure sso` instead.

The AWS CLI then stores your credentials in two separate files:
    
- `.aws/config`
- `.aws/credentials`

The location of these files depends on your operating system:

- Linux: `/home/<username>/.aws`
- Mac: `/Users/<username>/.aws`
- Windows: `%UserProfile%/.aws`

#### Configure your Astro project

The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential files, you'll mount the `.aws` folder as a volume in Docker.

1. In your Astro project, create a file named `docker-compose.override.yml` with the following configuration: 
    
    <Tabs
        defaultValue="mac"
        groupId= "configure-your-astro-project"
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
            - /Users/<username>/.aws:/home/astro/.aws:ro
        webserver:
            volumes:
            - /Users/<username>/.aws:/home/astro/.aws:ro
        triggerer:
            volumes:
            - /Users/<username>/.aws:/home/astro/.aws:ro
    ```
    
    </TabItem>
    <TabItem value="linux">
    
    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /home/<username>/.aws:/usr/local/airflow/.aws:ro
        webserver:
            volumes:
            - /home/<username>/.aws:/usr/local/airflow/.aws:ro
        triggerer:
            volumes:
            - /home/<username>/.aws:/usr/local/airflow/.aws:ro
    ```
    
    </TabItem>
    <TabItem value="windows">
    
    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /c/Users/<username>/.aws:/usr/local/airflow/.aws:ro
        webserver:
            volumes:
            - /c/Users/<username>/.aws:/usr/local/airflow/.aws:ro
        triggerer:
            volumes:
            - /c/Users/<username>/.aws:/usr/local/airflow/.aws:ro
    ```

    </TabItem>
    </Tabs>

:::info

Depending on your Docker configurations, you might have to make your `.aws` folder accessible to Docker. To do this, open **Preferences** in Docker Desktop and go to **Resources** -> **File Sharing**. Add the full path of your `.aws` folder to the list of shared folders.

:::

2. In your Astro project's `.env` file, add the following environment variables. Make sure that the volume path is the same as the one you configured in the `docker-compose.override.yml`.

    ```text
    AWS_CONFIG_FILE=/usr/local/airflow/.aws/config
    AWS_SHARED_CREDENTIALS_FILE=/usr/local/airflow/.aws/credentials
    ```

When you run Airflow locally, all AWS connections without defined credentials automatically fall back to your user credentials when connecting to AWS. Airflow applies and overrides user credentials for AWS connections in the following order:

- Mounted user credentials in the `~/.aws/config` file.
- Configurations in `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token`.
- An explicit username & password provided in the connection.

For example, if you completed the configuration in this document and then created a new AWS connection with its own username and password, Airflow would use those credentials instead of the credentials in `~/.aws/config`.

</TabItem>
<TabItem value="gcp">

#### Prerequisites 

- A user account on GCP with access to GCP cloud resources.
- The [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk).
- The [Astro CLI](astro/cli/overview.md).
- An [Astro project](develop-project.md#create-an-astro-project).
- Optional. Access to a secrets backend hosted on GCP, such as GCP Secret Manager.

#### Retrieve GCP user credentials locally

Run the following command to obtain your user credentials locally:

```sh
gcloud auth application-default login
```

The SDK provides a link to a webpage where you can log in to your Google Cloud account. After you complete your login, the SDK stores your user credentials in a file named `application_default_credentials.json`.

The location of this file depends on your operating system:

- Linux: `$HOME/.config/gcloud/application_default_credentials.json`
- Mac: `/Users/<username>/.config/gcloud/application_default_credentials.json`
- Windows: `%APPDATA%/gcloud/application_default_credentials.json`

#### Configure your Astro project

The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential file, mount it as a Docker volume.

1. In your Astro project, create a file named `docker-compose.override.yml` to your project with the following configuration: 
       
    <Tabs
        defaultValue="mac"
        groupId= "configure-your-astro-project"
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
    
2. In your Astro project's `.env` file, add the following environment variable. Ensure that this volume path is the same as the one you configured in `docker-compose.override.yml`.

    
    ```text
    GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcloud/application_default_credentials.json
    ```

When you run Airflow locally, all GCP connections without defined credentials automatically fall back to your user credentials when connecting to GCP. Airflow applies and overrides user credentials for GCP connections in the following order:

- Mounted user credentials in the `/~/gcloud/` folder
- Configurations in `gcp_keyfile_dict`
- An explicit username & password provided in the connection

For example, if you completed the configuration in this document and then created a new GCP connection with its own username and password, Airflow would use those credentials instead of the credentials in `~/gcloud/application_default_credentials.json`.

</TabItem>
<TabItem value="azure">

#### Prerequisites

- A user account on Azure with access to Azure cloud resources.
- The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
- The [Astro CLI](astro/cli/overview.md).
- [An Astro project](develop-project.md#create-an-astro-project)
- If you're using Windows, [Windows Subsystem Linux](https://learn.microsoft.com/en-us/windows/wsl/install).

#### Retrieve Azure user credentials locally
    
Run the following command to obtain your user credentials locally:
      
```sh
az login
```

The CLI provides you with a link to a webpage where you authenticate to your Azure account. Once you complete the login, the CLI stores your user credentials in your local Azure configuration folder. The developer account credentials are used in place of the credentials associated with the Registered Application (Service Principal) in Azure AD.
    
The default location of the Azure configuration folder depends on your operating system:

- Linux: `$HOME/.azure/`
- Mac: `/Users/<username>/.azure`
- Windows: `%USERPROFILE%/.azure/`

#### Configure your Astro project

The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential files, mount the `.azure` folder as a volume in Docker.

1. In your Astro project, create a file named `docker-compose.override.yml` with the following configuration: 

    <Tabs
        defaultValue="mac"
        groupId= "configure-your-airflow-project"
        values={[
            {label: 'Mac', value: 'mac'},
            {label: 'Windows and Linux', value: 'windowslinux'},
        ]}>
    <TabItem value="mac">
    
    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /Users/<username>/.azure:/usr/local/airflow/.azure:ro
        webserver:
            volumes:
            - /Users/<username>/.azure:/usr/local/airflow/.azure:ro
        triggerer:
            volumes:
            - /Users/<username>/.azure:/usr/local/airflow/.azure:ro
    ```
    
    </TabItem>
    <TabItem value="windowslinux">
    
    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /home/<username>/.azure:/usr/local/airflow/.azure
        webserver:
            volumes:
            - /home/<username>/.azure:/usr/local/airflow/.azure
        triggerer:
            volumes:
            - /home/<username>/.azure:/usr/local/airflow/.azure
    
    ```
    
    :::info 
    
    In Azure CLI versions 2.30.0 and later on Windows systems, credentials generated by the CLI are saved in an encrypted file and cannot be accessed from Astro Runtime Docker containers. See [MSAL-based Azure CLI](https://learn.microsoft.com/en-us/cli/azure/msal-based-azure-cli).
        
    To work around this limitation on a Windows computer, use Windows Subsystem Linux (WSL) when completing this setup.
      
    If you installed the Azure CLI both in Windows and WSL, make sure that the `~/.azure` file path in your volume points to the configuration file for the Azure CLI installed in WSL.
    
    :::
    
    </TabItem>
    </Tabs>    

2. Add the following lines after the `FROM` line in your `Dockerfile` to install the Azure CLI inside your Astro Runtime image:

    ```dockerfile
    # FROM ...
    USER root
    RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
    USER ASTRO
    ```

:::info

If you're using an Apple M1 Mac, you must use the`linux/amd64` distribution of Astro Runtime. Replace the first line in the `Dockerfile` of your Astro project with `FROM --platform=linux/amd64 quay.io/astronomer/astro-runtime:<version>`. 

:::

3. Add the following environment variable to your `.env` file. Make sure the file path is the same volume location you configured in `docker-compose.override.yml`
   
    ```text
    AZURE_CONFIG_DIR=/usr/local/airflow/.azure
    ```

When you run Airflow locally, all Azure connections without defined credentials automatically fall back to your user credentials when connecting to Azure. Airflow applies and overrides user credentials for Azure connections in the following order:

- Mounted user credentials in `/~/.azure`.
- Configurations in `azure_client_id`, `azure_tenant_id`, and `azure_client_secret`.
- An explicit username & password provided in the connection.

For example, if you completed the configuration in this document and then created a new Azure connection with its own username and password, Airflow would use those credentials instead of the credentials in `~/.azure/config`.

</TabItem>
</Tabs>

## Test your credentials with a secrets backend

Now that Airflow has access to your user credentials, you can use them to connect to your cloud services. Use the following example setup to test your credentials by pulling values from different secrets backends. 


<Tabs
    defaultValue="aws"
    groupId= "optional-test-your-credentials-with-a-secrets-backend"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

1. Create a secret for an Airflow variable or connection in AWS Secrets Manager. All Airflow variables and connection keys must be prefixed with the following strings respectively:

    - `airflow/variables/<my_variable_name>`
    - `airflow/connections/<my_connection_id>`
    
    For example when adding the secret variable `my_secret_var` you will need to give the secret the name `airflow/variables/my_secret_var`.

    When setting the secret type, choose `Other type of secret` and select the `Plaintext` option. If you're creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.

2. Add the following environment variables to your Astro project `.env` file. For additional configuration options, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html). Make sure to specify your `region_name`.

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables", "region_name": "<your-aws-region>"}
    ```

3. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

4. Access the Airflow UI at `localhost:8080` and create an Airflow AWS connection named `aws_standard` with no credentials. See [Connections](https://docs.astronomer.io/learn/connections).

   When you use this connection in your DAG, it will fall back to using your configured user credentials. 

5. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve `<my_variable_name>` and `<my_connection_id> from the secrets backend and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.decorators import task
    from datetime import datetime

    with DAG(
        'example_secrets_dag',
        start_date=datetime(2022, 1, 1),
        schedule=None
    ):

        @task
        def print_var():
            my_var = Variable.get("<my_variable_name>")
            print(f"My secret variable is: {my_var}") # secrets will be masked in the logs!

            conn = BaseHook.get_connection(conn_id="<my_connection_id>")
            print(f"My secret connection is: {conn.get_uri()}") # secrets will be masked in the logs!
            
        print_var()
    ```

6. In the Airflow UI, unpause your DAG and click **Play** to trigger a DAG run. 
7. View logs for your DAG run. If the connection was successful, your masked secrets appear in your logs. See [Airflow logging](https://docs.astronomer.io/learn/logging).

</TabItem>
<TabItem value="gcp">

1. Create a secret for an Airflow variable or connection in GCP Secret Manager. You can do this using the Google Cloud Console or the gcloud CLI. All Airflow variables and connection keys must be prefixed with the following strings respectively:

    - `airflow-variables-<my_variable_name>`
    - `airflow-connections-<my_connection_name>`
    
     For example when adding the secret variable `my_secret_var` you will need to give the secret the name `airflow-variables-my_secret_var`.

2. Add the following environment variables to your Astro project `.env` file. For additional configuration options, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/secrets-backends/google-cloud-secret-manager-backend.html). Make sure to specify your `project_id`. 

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<my-project-id>"}
    ```

3. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

4. Access the Airflow UI at `localhost:8080` and create an Airflow GCP connection named `gcp_standard` with no credentials. See [Connections](https://docs.astronomer.io/learn/connections).

   When you use this connection in your DAG, it will fall back to using your configured user credentials. 

5. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve `<my_variable_name>` and `<my_connection_id>` from the secrets backend and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.decorators import task
    from datetime import datetime

    with DAG(
        'example_secrets_dag',
        start_date=datetime(2022, 1, 1),
        schedule=None
    ):

        @task
        def print_var():
            my_var = Variable.get("<my_variable_name>")
            print(f"My secret variable is: {my_var}")

            conn = BaseHook.get_connection(conn_id="<my_connection_name>")
            print(f"My secret connection is: {conn.get_uri()}")

        print_var()
    ```

6. In the Airflow UI, unpause your DAG and click **Play** to trigger a DAG run. 
7. View logs for your DAG run. If the connection was successful, your masked secrets appear in your logs. See [Airflow logging](https://docs.astronomer.io/learn/logging). 

</TabItem>

<TabItem value="azure">

1. Create a secret for an Airflow variable or connection in Azure Key Vault. All Airflow variables and connection keys must be prefixed with the following strings respectively:

    - `airflow-variables-<my_variable_name>`
    - `airflow-connections-<my_connection_name>`
    
    For example, to use a secret named `mysecretvar` in your DAG, you must name the secret `airflow-variables-mysecretvar`.

    You will need to store your connection in [URI format](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables). 

2. In your Astro project, add the following line to Astro project `requirements.txt` file:

    ```text
    apache-airflow-providers-microsoft-azure
    ```

3. Add the following environment variables to your Astro project `.env` file. For additional configuration options, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/secrets-backends/azure-key-vault.html). Make sure to specify your `vault_url`. 
  
    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.microsoft.azure.secrets.key_vault.AzureKeyVaultBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "<your-vault-url>"}
    ```

    By default, this setup requires that you prefix any secret names in Key Vault with `airflow-connections` or `airflow-variables`. If you don't want to use prefixes in your Key Vault secret names, set the values for `"connections_prefix"` and `"variables_prefix"` to `""` within `AIRFLOW__SECRETS__BACKEND_KWARGS`. The `vault_url` can be found on the overview page of your Key vault under `Vault URI`.

4. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

5. Access the Airflow UI at `localhost:8080` and create an Airflow Azure connection named `azure_standard` with no credentials. See [Connections](https://docs.astronomer.io/learn/connections).

   When you use this connection in your DAG, it will fall back to using your configured user credentials. 

6. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve a value from `airflow/variables` and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.decorators import task
    from datetime import datetime

    with DAG(
        'example_secrets_dag',
        start_date=datetime(2022, 1, 1),
        schedule=None
    ):

        @task
        def print_var():
            my_var = Variable.get("mysecretvar")
            print(f"My secret variable is: {my_var}")

            conn = BaseHook.get_connection(conn_id="mysecretconnection")
            print(f"My secret connection is: {conn.get_uri()}")

        print_var()
    ```

7. In the Airflow UI, unpause your DAG and click **Play** to trigger a DAG run. 
8. View logs for your DAG run. If the connection was successful, your masked secrets appear in your logs. See [Airflow logging](https://docs.astronomer.io/learn/logging).

</TabItem>
</Tabs>

![Secrets in logs](/img/docs/secret_logs.png)
