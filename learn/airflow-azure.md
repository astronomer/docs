# Authenticate with User Credentials for local development (Azure)

It is possible to use local User credentials instead of Service Account Keys to authenticate to Azure.

Using these credentials, it is also possible to configure a custom Secret Backend like Azure Key Vault for local development.

Pre-requisites:
- Install the Azure CLI locally (Mac & Linux): https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
- (Windows) Install Windows Subsystem Linux: https://learn.microsoft.com/en-us/windows/wsl/install

**IMPORTANT NOTES**
- There is an open issue with DefaultAzureCredential forcing the installation Azure CLI inside Astro Runtime. [You can read more about it here](https://github.com/Azure/azure-sdk-for-net/issues/19167#issuecomment-1127081646)
- Starting from Azure CLI v2.30.0, credentials generated from a Windows installed Azure CLI are now saved in an encrypted file; the credentials cannot be accessed from the Astronomer Runtime Docker containers. Workarounds are described below. [See here for more details.](https://learn.microsoft.com/en-us/cli/azure/msal-based-azure-cli)


Steps:
1. Acquire user credentials with Azure CLI
    
    The following command is used to obtain user access credentials via a web flow. 
    
    ```
    az login
    ```

    Running the command in your terminal will provide a link and open a webpage to authenticate to your Azure Account.
    Once login is complete, it will store user credentials in your local Azure config folder.
    The developer account credentials are used in place of the credentials associated with the Registrated Application (Service Principal) in Azure AD.
    
    The location of the Azure configuration folder depends on your operating system:
    - Linux, macOS: `$HOME/.azure/`
    - Windows: `%USERPROFILE%/.azure/`

    It is possible to define the AZURE_CONFIG_DIR environment variable to use a different folder.

    For more information:
    [CLI configuration files](https://learn.microsoft.com/en-us/cli/azure/azure-cli-configuration#cli-configuration-file)
    [Azure Login](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli)

2. Mount your Azure configuration folder as a volume and attach it to Airflow:

    This step is done by overriding the CLI Docker Compose file.
    Make sure that the source path matches the file location mentioned in step 1 above.

    For Linux, MacOS:
    ```yaml
    version: "3.1"
    services:
      scheduler:
        volumes:
          - /home/<username>/.azure:/home/astro/.azure
      webserver:
        volumes:
          - /home/<username>/.azure:/home/astro/.azure
      triggerer:
        volumes:
          - /home/<username>/.azure:/home/astro/.azure    
    ```
    For more information:
    [Override the CLI Docker Compose file](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#override-the-cli-docker-compose-file)

    For Windows:

    As mentioned in the important notes above, Windows-based Azure CLI credentials cannot be used with Astronomer Runtime.
    
    You can use Azure CLI with Windows Subsystem Linux (WSL) by following the steps for Linux above.
    If you have installed Azure CLI both in Windows and in WSL, make sure that the `~/.azure` folder does not point to the Windows folder. Redefine the `AZURE_CONFIG_DIR` environment variable if needed.

3. Install Azure CLI inside Astronomer Runtime by updating the Dockerfile as follows:

    ```dockerfile
    FROM quay.io/astronomer/astro-runtime:6.0.4
    USER root
    RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
    USER ASTRO
    ```

4. Configure the AZURE_CONFIG_DIR environment variable:

    Make sure that the path matches the file location mentioned in the Yaml override file above.
    ```
    AZURE_CONFIG_DIR=/home/astro/.azure
    ```

5. Optional - Configure your Custom Secret Backend
    For custom Airflow Secret Backend Only

    Follow the steps to configure an external secrets backend described here: https://docs.astronomer.io/astro/secrets-backend?tab=azure#setup

    Make sure to configure the AIRFLOW__SECRETS__BACKEND_KWARGS environment variables as follows:
    - Do not define `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` or `AZURE_CLIENT_SECRET`.

    Example:
    
    ```
    AZURE_CONFIG_DIR=/home/astro/.azure
    AIRFLOW__SECRETS__BACKEND=airflow.providers.microsoft.azure.secrets.azure_key_vault.AzureKeyVaultBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "<your-vault-url>"}
    ```