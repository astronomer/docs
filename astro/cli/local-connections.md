---
sidebar_label: 'Use Airflow connections from Astro'
title: 'Work locally with Airflow connections hosted on Astro'
id: local-connections
description: Use connections created in the Astro Environment Manager locally.
---

You can share Airflow connections created through the [Astro Environment Manager](create-and-link-connections.md) with local Airflow projects. These connections are not visible from the Airflow UI when you run your project locally, instead, they are synced from the Astro Environment Manager using the Astro CLI for the Workspace and Deployment that you want to work with.

This means that instead of [importing connection details](import-export-connections-variables.md#using-the-astro-cli-local-environments-only) from Astro to your local Airflow metadatabase, you can configure your CLI to retrieve connection details from the Environment Manager using the Astro API. The CLI then adds your connection details directly to your local Airflow metadata database, so you don't need to manage a `.env` file, secrets backend, or `airflow_settings.yaml` file to keep connection information consistent between your local and cloud-based Deployments.

To use connections from the Environment Manager locally, start a local project using `astro dev start`, and then specify either the Workspace or Deployment that you want to import connections from. When you start your project with these settings, the Astro CLI fetches the necessary connections from Astro. Then, after the local Airflow containers start, the Astro CLI populates the metadata database with the connections. This ensures that the connections are encrypted in the metadata database and not easily accessible by an end user.

### Prerequisites

- The latest version of the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
- Either a Workspace or Deployment with at least one connection [configured through the Cloud UI](create-and-link-connections.md)
- A local [Astro Project](https://docs.astronomer.io/astro/cli/develop-project#create-an-astro-project)
- Astro Runtime 9.3.0 or greater
- `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR`, or `WORKSPACE_OWNER` user permissions
- An internet connection

### Setup

1. Enable local development access to connections created in the Cloud UI.

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

4. Start your project locally.

    - **Using connections linked to all Deployments in a Workspace**
    ```zsh
    astro dev start --workspace-id [workspace-id]
    ```

    - **Using Deployment-level connections**
    ```zsh
    astro dev start --deployment-id [deployment-id]
    ```

    :::info

    If you see the error `Error: showSecrets on organization with id is not allowed`, your [Organization Owner](user-permissions.md#organization-roles) needs to enable **Environment Secrets Fetching** in the **Organization Settings** on the Cloud UI before you can use your connections locally. See [Configure environment secrets fetching for the Astro Environment Manager](organization-settings.md#configure-environment-secrets-fetching-for-the-astro-environment-manager).

    :::

Congratulations! You set up your Astro CLI to retrieve connections from the environment manager to use when working locally. Now you can run DAGs locally that use connections set in the Astro Environment manager.