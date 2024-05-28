---
sidebar_label: 'Use Airflow connections from Astro'
title: 'Use Airflow connections hosted on Astro in a local environment'
id: local-connections
description: Use DAGs locally with Airflow connections that you created in the Astro Environment Manager.
---

When you create Airflow connections for a Deployment on Astro with the [Environment Manager](create-and-link-connections.md), you can also use them to test DAGs locally. This is the easiest way to share connection details between a Deployment on Astro and your local Airflow environment.

Using connections from the Astro Environment Manager in a local Airflow environment means that instead of creating a connection twice or manually importing connection details, you can configure the Astro CLI to use any connections that are already configured for a particular Deployment or Workspace. The CLI then adds your connection details directly to your local Airflow metadata database, so you don't need to manage a `.env` file, secrets backend, or `airflow_settings.yaml` file to keep connection information consistent between your local environment and your Deployments on Astro.

To use connections from the Environment Manager locally, start a local project using `astro dev start`, and then specify either the Workspace or Deployment that you want to import connections from. When you start your project with these settings, the Astro CLI fetches the necessary connections from Astro. Then, after the local Airflow containers start, the Astro CLI populates the metadata database with the connections. This ensures that the connections are encrypted in the metadata database and not easily accessible by an end user.

Connection details in the Astro Environment Manager are not visible from the Airflow UI when you run your project locally. Instead, they are synced using the Astro CLI for the Workspace and Deployment that you want to work with.

### Prerequisites

- The latest version of the [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli)
- Either a Workspace or Deployment with at least one connection [configured through the Astro Environment Manager in the Astro UI](create-and-link-connections.md)
- A local [Astro Project](https://www.astronomer.io/docs/astro/cli/develop-project#create-an-astro-project)
- Astro Runtime 9.3.0 or greater
- `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER` user permissions
- An internet connection

### Setup

1. Enable local development access to connections created in the Astro UI.

    ```zsh
    # -g sets this config globally
    astro config set -g disable_env_objects false
    ```

2. Log in to Astro.

    ```zsh
    astro login <domain name>
    ```

3. Retrieve the ID of either the Workspace or Deployment that you want to import connections from.

    ```zsh
    # Retrieve Workspace IDs
    astro workspace list
    # Retrieve Deployment IDs
    astro deployment list
    ```

4. Start your project locally specifying the Deployment or Workspace ID from Step 3.

    - **Using connections linked to all Deployments in a Workspace**
    ```zsh
    astro dev start --workspace-id [workspace-id]
    ```

    - **Using Deployment-level connections**
    ```zsh
    astro dev start --deployment-id [deployment-id]
    ```

    :::info

    If you see the error `Error: showSecrets on organization with id is not allowed`, your [Organization Owner](user-permissions.md#organization-roles) needs to enable **Environment Secrets Fetching** in the **Organization Settings** on the Astro UI before you can use your connections locally. See [Configure environment secrets fetching for the Astro Environment Manager](organization-settings.md#configure-environment-secrets-fetching-for-the-astro-environment-manager).

    :::

Congratulations! You set up your local Airflow environment with the Astro CLI to use connections created in the Astro Environment Manager. Now, you can run and test DAGs locally that automatically use these connections without any additional setup.