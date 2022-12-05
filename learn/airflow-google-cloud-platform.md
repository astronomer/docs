# Authenticate with User Credentials for local development (Google Cloud)

It is possible to use local User credentials instead of Service Account Keys to autenticate to Google Cloud.

Using these credentials, it is also possible to configure a custom Secret Backend like Google Secret Manager for local development.

Pre-requisites:
- Install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install-sdk

Steps:
1. Acquire user credentials with Google Cloud SDK
    
    The following command is used to obtain user access credentials via a web flow. 
    
    ```
    gcloud auth application-default login
    ```

    Running the command in your terminal will provide a like and open a webpage to authenticate to your Google Cloud Account.
    Once login is complete, it will store user credentials in your local Google Cloud SDK folder. 
    This credentials file is named Application Default Credentials (ADC).
    The file is used in place of the Service Account Key file.
    
    The location of the Application Default Credentials file depends on your operating system:
    - Linux, macOS: `$HOME/.config/gcloud/application_default_credentials.json`
    - Windows: `%APPDATA%/gcloud/application_default_credentials.json`

    For more information:
    [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials#personal)
    [Google Cloud Auth Login](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login)

2. Mount your Google Cloud application_default_credentials file as a volume and attach it to Airflow:

    This step is done by overriding the CLI Docker Compose file.
    Make sure that the source path matches the file location mentionned in step 1 above.

    For Linux, MacOS:
    ```yaml
    version: "3.1"
    services:
    scheduler:
        volumes:
        - /home/<username>/.config/gcloud/application_default_credentials.json:/home/astro/.config/gcloud/application_default_credentials.json:ro
    webserver:
        volumes:
        - /home/<username>/.config/gcloud/application_default_credentials.json:/home/astro/.config/gcloud/application_default_credentials.json:ro
    ```

    For Windows:
    ```yaml
    version: "3.1"
    services:
    scheduler:
        volumes:
        - /c/Users/OlivierDaneau/AppData/Roaming/gcloud/application_default_credentials.json:/home/astro/.config/gcloud/application_default_credentials.json:ro
    webserver:
        volumes:
        - /c/Users/OlivierDaneau/AppData/Roaming/gcloud/application_default_credentials.json:/home/astro/.config/gcloud/application_default_credentials.json:ro
    ```

    For more information:
    [Override the CLI Docker Compose file](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#override-the-cli-docker-compose-file)

3. Configure the GOOGLE_APPLICATION_CREDENTIALS environment variable:

    Make sure that the path matches the file location mentioned in the Yaml override file above.
    ```
    GOOGLE_APPLICATION_CREDENTIALS=/home/astro/.config/gcloud/application_default_credentials.json
    ```

4. Optional - Configure your Custom Secret Backend
    For custom Airflow Secret Backend Only

    Follow the steps to configure an external secrets backend described here: https://docs.astronomer.io/astro/secrets-backend?tab=gcp#setup

    Make sure to configure the AIRFLOW__SECRETS__BACKEND_KWARGS environment variables as follows:
    - Remove any mention of `gcp_keyfile_dict` or `gcp_key_path`.
    - Add the Project ID key

    Example:
    
    ```
    AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<GCP PROJECT ID>"}
    ```