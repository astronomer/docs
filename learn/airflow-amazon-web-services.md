# Authenticate with User Credentials for local development (AWS)

It is possible to use local User credentials instead of Service Account Keys to authenticate to AWS.

Using these credentials, it is also possible to configure a custom Secret Backend like AWS Secrets Manager for local development.

Pre-requisites:
- Install the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Steps:
1. Acquire user credentials with AWS CLI
    
    The following command is used to obtain user access credentials via AWS Access Key ID and AWS Secret Access Key.
    ```
    aws configure
    ```    

    The following command is used to obtain user access credentials via SSO.
    ```
    aws configure sso
    ```

    Running the command in your terminal will prompt you for four pieces of information: 
      - Access key ID, 
      - Secret access key, 
      - AWS Region, 
      - Output format
    Once login is complete, it will store user credentials in your local AWS config folder.
    
    The location of the AWS configuration folder depends on your operating system:
    - Linux, macOS: `/home/<username>/.aws`
    - Windows: `%UserProfile%/.aws`

    Two files will be saved at this location: `config` and `credentials`.

    For more information:
    [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
    [Configuration and credentials file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
    [Configuring the AWS CLI to use AWS IAM Identity Center (Single Sign-On)](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)

2. Mount your AWS configuration folder as a volume and attach it to Airflow:

    This step is done by overriding the CLI Docker Compose file.
    Make sure that the source path matches the file location mentioned in step 1 above.
    For the AWS configuration to be accessible to Airflow, you may beed to grand permission to read the config and credentials files. 
    Airflow also needs access to read and write to the cache folder.

    For Linux, MacOS:
    ```yaml
    version: "3.1"
    services:
    scheduler:
        volumes:
        - /home/odaneau/.aws:/home/astro/.aws:ro
    webserver:
        volumes:
        - /home/odaneau/.aws:/home/astro/.aws:ro
    triggerer:
        volumes:
        - /home/odaneau/.aws:/home/astro/.aws:ro
    ```

    For Windows:
    ```yaml
    version: "3.1"
    services:
    scheduler:
        volumes:
        - /c/Users/<username>/.aws:/home/astro/.aws:ro
    webserver:
        volumes:
        - /c/Users/<username>/.aws:/home/astro/.aws:ro
    ```

    For more information:
    [Override the CLI Docker Compose file](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#override-the-cli-docker-compose-file)

3. Configure the AWS_CONFIG_FILE and AWS_SHARED_CREDENTIALS_FILE environment variables:

    Make sure that the path matches the file location mentioned in the Yaml override file above.
    ```
    AWS_CONFIG_FILE=/home/astro/.aws/config
    AWS_SHARED_CREDENTIALS_FILE=/home/astro/.aws/credentials
    ```

4. Optional - Configure your Custom Secret Backend
    For custom Airflow Secret Backend Only

    Follow the steps to configure an external secrets backend described here: https://docs.astronomer.io/astro/secrets-backend?tab=gcp#setup

    Make sure to configure the AIRFLOW__SECRETS__BACKEND_KWARGS environment variables as follows:
    - Remove any mention of `role_arn`.

    Example:
    
    ```
    AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables", "region_name": "us-west-2"}
    ```