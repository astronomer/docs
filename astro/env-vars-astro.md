---
sidebar_label: 'Edit environment variables'
title: 'Manage environment variables on Astro'
id: env-vars-astro
description: Learn how to manage environment variables on Astro
---

import {siteVariables} from '@site/src/versions';

On Astro, you can add, edit, update, or delete environment variables in three different ways for your Deployment:

- Your Deployment's **Variable** tab in the Cloud UI
- Your Astro project's `Dockerfile` during deploy
- Using Astro CLI
    - Your Astro project's `.env` file
    - Using Astro CLI commands `astro deployment variable create` and `astro deployment variable update`

The method you choose depends on your [specific use case](environment-variables.md#choose-the-strategy-to-manage-environment-variables). 

Use this document to understand how to use these methods to create environment variables on Astro.

## Using the Cloud UI

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Variables** tab.

3. Click **Edit Variables**.

4. Enter an environment variable key and value. For sensitive credentials that should be treated with an additional layer of security, select the **Secret** checkbox. This will permanently hide the variable's value from all users in your Workspace.

5. Click **Update Environment Variables** to save your changes. Your Airflow scheduler, webserver, and workers restart. After saving, it can take up to two minutes for new variables to be applied to your Deployment.

### Edit or delete existing values

After you set an environment variable key, only the environment variable value can be modified. While you can modify environment variables that are set as secret, however, the secret variable value is never shown. When you modify a secret environment variable, you'll be prompted to enter a new value.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Variables** tab.

3. Click **Edit Variables**. 

4. Modify the value of the variable you wish to edit.

    ![Edit value location](/img/docs/variables-edit.png)

5. Click **Update Environment Variables** to save your changes. Your Airflow scheduler, webserver, and workers restart. After saving, it can take up to two minutes for updated variables to be applied to your Deployment.

## Using your Dockerfile

If you want to store environment variables with an external version control tool, Astronomer recommends setting them in your `Dockerfile`. This file is automatically created when you first initialize an Astro project using `astro dev init`.

:::caution

Environment variables set in your `Dockerfile` are stored in plain text. For this reason, Astronomer recommends storing sensitive environment variables using the Cloud UI or a third-party secrets backend. For more information, see [Configure a secrets backend](secrets-backend.md).

:::

1. Go to your Astro project and open the `Dockerfile`.

2. To add the environment variables, declare an ENV command with the environment variable key and value. For example, the following `Dockerfile` sets two environment variables:

    <pre><code parentName="pre">
    {`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
    ENV AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=1
    ENV AIRFLOW_VAR_MY_VAR=25`}
    </code></pre>

3. After you add your environment variables, use the `astro deploy` command to apply your changes to your Deployment on Astro. To apply your changes locally, use `astro dev restart` to rebuild your image.

4. (Optional) To verify if the environment variables are applied correctly to Astro Deployment or your local Airflow environment, you can use `os.getenv("AIRFLOW_VAR_MY_VAR")` inside of Airflow DAGs and tasks.

    To view a list of all the environment variables set in your local Airflow environment, refer to the Step 4 of [Using Astro CLI in local Airflow environment](#in-your-local-airflow-environment)

To delete an environment variable from your Astro Runtime image, just remove or comment the line in your `Dockerfile` that defines it.

:::info

Environment variables set in your Dockerfile are not visible in the Cloud UI.

:::

## Using Astro CLI

You can use Astro CLI to set environment variables on Astro and your local Airflow environment. 

You can either use `.env` file to update environment variables on your local Airflow and Astro Deployment or manually add environment variables to your Deployment using Astro CLI commands `astro deployment variable create` and `astro deployment variable update`.

### In your local Airflow environment

If your environment variables contain sensitive information or credentials that you don’t want to expose in plain-text, ensure that your `.env` file is part of `.gitignore` when you deploy these changes to your code repository.

1. Go to your Astro project and open the `.env` file.

2. Use the following format to set your environment variables in the `.env` file:

    ```bash
    KEY=VALUE
    ```

    Environment variables should be in all-caps and not include spaces.

    Alternatively, you can run `astro deployment variable list --save` to copy environment variables from an existing Deployment to a file.

3. Restart your local environment using `astro dev restart`.

4. (Optional) You can run the following commands to confirm if your environment variables were applied:

    1. Run `astro dev bash --scheduler` to login to the scheduler container.
    2. Run `printenv | grep <your-env-variable>` in the container to print the environment variables and find your environment variable.
    3. Run `exit` to exit the container.

#### Using multiple .env files

The Astro CLI looks for `.env` by default, but if you want to specify multiple files, make `.env` a top-level directory and create sub-files within that folder.

A project with multiple `.env` files might look like the following:

```
my_project
├── Dockerfile
├── dags
│   └── my_dag
├── include
│   └── my_operators
├── airflow_settings.yaml
└── .env
    ├── dev.env
    └── prod.env
```

### In your Astro Deployment

To add an environment variable to your Astro Deployment, run the following command:

```bash
astro deployment variable create AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=60 ENVIRONMENT_TYPE=dev --deployment-id cl03oiq7d80402nwn7fsl3dmv
```

Alternatively, to directly load the contents of your `.env` file to your Astro Deployment use the `--load` flag:

```bash
astro deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --load .env
```

To update an existing environment variable to your Astro Deployment, use [`astro deployment variable update`](cli/astro-deployment-airflow-variable-update.md) command.

:::caution

Note that when you use `.env` file to add or update environment variables, it will overwrite all the variables in your Astro Deployment from your `.env` file. 

:::

When you use Astro CLI commands to add or update environment variabes to your Deployment, your Deployment is automatically restarted to apply the environment variables. To verify if the environment varibles were applied correctly to your Deployment, go to the **Variables** tab of your Deployment in the Cloud UI. 

You cannot delete an environment variable using the Astro CLI. You either need to use the Cloud UI or use the `.env` file to only include the required environment variables.

:::tip

To mark an environment variable as a secret using Astro CLI use the `--secret` flag.

:::

## See also

- [Set Airflow connections](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables) using environment variables.
- [Set Airflow variables](http://localhost:3000/learn/airflow-variables#using-environment-variables) using environment variables.
- [Import and export environment variables](import-export-connections-variables.md#from-environment-variables)