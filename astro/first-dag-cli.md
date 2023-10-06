---
sidebar_label: 'With Astro CLI'
title: 'Run your first DAG with the Astro CLI'
id: 'first-dag-cli'
---

<head>
  <meta name="description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI." />
  <meta name="og:description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Astro is the industry's leading managed service for Apache Airflow. To quickly learn how Astro works, follow the steps in this quickstart to create an Airflow environment and run your first DAG with the Astro CLI.

Specifically, you will:

- Install the CLI.
- Authenticate and log in to Astro. 
- Create a Deployment. 
- Create an Astro project. 
- Deploy DAGs to Astro with the Astro CLI.
- Trigger a run of an example DAG in the Airflow UI. 

This tutorial takes about 15 minutes. If you're new to Airflow and want a more in-depth tutorial, see [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).

If you want to deploy your first DAG without installing any software to your local machine, see [Run your first DAG with GitHub Actions](first-dag-github-actions.md).

## Prerequisites

- An Astro account. To start an Astro trial and create your free trial account, see [Start a trial](trial.md).

:::info

If you're on your organization's network and can't access Astro, make a request to allowlist the following domains on your network:

- `https://cloud.astronomer.io/`
- `https://api.astronomer.io/`
- `https://images.astronomer.cloud/`
- `https://auth.astronomer.io/`
- `https://updates.astronomer.io/`
- `https://install.astronomer.io/`
- `https://astro-<your-org>.datakin.com/`
- `https://<your-org>.astronomer.run/`

:::

## Step 1: Install the Astro CLI

<Tabs
    defaultValue="mac"
    groupId= "install-the-astro-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows with winget', value: 'windowswithwinget'},
        {label: 'Linux', value: 'linux'},
    ]}>

<TabItem value="mac">

:::tip

If you're encountering problems with installing the CLI or don't want to install software locally, see [Run your first DAG with GitHub Actions](first-dag-github-actions.md).

:::

Use [Homebrew](https://brew.sh/) to install the latest version of the [the Astro CLI](cli/overview.md).

```sh
brew install astro
```

</TabItem>

<TabItem value="windowswithwinget">

:::tip

If you're encountering problems with installing the CLI or don't want to install software locally, see [Run your first DAG with GitHub Actions](first-dag-github-actions.md).

:::

The winget command line tool is supported on Windows 10 1709 (build 16299) or later, and is bundled with Windows 11 and modern versions of Windows 10 by default as the App Installer. If you don't have winget, you can [Install the CLI on Windows manually](/cli/install-cli.md#install-the-astro-cli) instead.

1. Make sure you have the following:

    - Microsoft Hyper-V enabled. See [How to Enable Hyper-V On Windows](https://www.wintips.org/how-to-enable-hyper-v-on-windows-10-11-home/).
    - The latest version of the Windows [App Installer](https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1?hl=en-ca&gl=ca).
    - Windows 10 1709 (build 16299) or later or Windows 11.

2. Open Windows PowerShell as an administrator and then run the following command:

    ```sh
    winget install -e --id Astronomer.Astro
    ```

3. Run the following command to access the location of the CLI executable:

    ```sh
    $env:path.split(";")
    ```
    
    From the text that appears, copy the path for the Astro CLI executable. It should be similar to `C:\Users\myname\AppData\Local\Microsoft\WinGet\Packages\Astronomer.Astro_Microsoft.Winget.Source_8wekyb3d8bbwe`. 

4. Paste the path into File Explorer or open the file path in terminal, then rename the Astro executable to `astro.exe`.

</TabItem>

<TabItem value="linux">

:::tip

If you're encountering problems with installing the CLI or don't want to install software locally, see [Run your first DAG with GitHub Actions](first-dag-github-actions.md).

:::

Run the following command to install the latest version of the Astro CLI directly to `PATH`:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

</TabItem>

</Tabs>

## Step 2: Create a Deployment

An Astro _Deployment_ is an instance of Apache Airflow that is powered by all core Airflow components, including a webserver, scheduler, and one or more workers. You deploy DAGs to a Deployment, and you can have one or more Deployments within a Workspace.

1. Log in to the [Cloud UI](https://cloud.astronomer.io).

2. On the **Deployments** page, click **+ Deployment**.

3. In the **Name** field, enter a name for your Deployment. You can leave the other fields at their default values. This creates a basic Deployment on a standard Astronomer-hosted cluster. You can delete the Deployment after you finish testing your example DAG runs. 

4. Click **Create Deployment**.

    A confirmation message appears indicating that the Deployment status is **Creating** until all underlying components in the Deployment are healthy. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health). Or, to learn more about how to customize your Deployment settings, see [Deployment settings](deployment-settings.md).

## Step 3: Create an Astro project

An _Astro project_ contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. All new Astro projects contain two example DAGs. In this tutorial, you'll be deploying these example DAGs to your Deployment on Astro.

1. Open your terminal or IDE.

2. Create a new folder for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

3. Open the folder:

    ```sh
    cd <your-astro-project-name>
    ```

4. Run the following Astro CLI command to initialize an Astro project in the folder:

    ```sh
    astro dev init
    ```

    The command generates the following files in your folder:

    ```
    .
    ├── .env # Local environment variables
    ├── dags # Where your DAGs go
    │   ├── example-dag-basic.py # Example DAG that showcases a simple ETL data pipeline
    │   └── example-dag-advanced.py # Example DAG that showcases more advanced Airflow features, such as the TaskFlow API
    ├── Dockerfile # For the Astro Runtime Docker image, environment variables, and overrides
    ├── include # For any other files you'd like to include
    ├── plugins # For any custom or community Airflow plugins
    │   └── example-plugin.py
    ├── tests # For any DAG unit test files to be run with pytest
    │   └── test_dag_example.py # Example test that checks for basic errors in your DAGs
    ├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
    ├── packages.txt # For OS-level packages
    └── requirements.txt # For Python packages
    ```

## Step 4: Deploy example DAGs to your Astro Deployment

DAG-only deploys are an Astro feature that you can use to quickly update your Astro Deployment by only deploying the `dags` folder of your Astro project. You'll now trigger a DAG-only deploy to push your example DAGs to Astro.

1. Run the following command to authenticate to Astro on the CLI:

    ```sh
    astro login astronomer.io
    ```

    After running this command, you are prompted to open your web browser and enter your credentials to the Cloud UI. The Cloud UI then automatically authenticates you to the CLI. The next time you log in, you can run `astro login` without specifying a domain. If you run into issues logging in, check to make sure that you have the latest version of the Astro CLI. See [Upgrade the CLI](cli/install-cli.md#upgrade-the-cli).

2. Run the following command to deploy your DAGs to Astro: 
   
    ```sh
    astro deploy --dags
    ```

    This command returns a list of Deployments available in your Workspace and prompts you to confirm where you want to deploy your DAG code. After you select a Deployment, the CLI parses your DAGs to ensure that they don't contain basic syntax and import errors. If your code passes the parse, the Astro CLI deploys your DAGs to Astro. If you run into issues deploying your DAGs, check to make sure that you have the latest version of the Astro CLI. See [Upgrade the CLI](cli/install-cli.md#upgrade-the-cli).

## Step 5: Trigger your DAG on Astro

Newly-deployed DAGs are paused by default and will not start running automatically. To run one of the example DAGs in your Astro project according to its schedule, you must unpause it from the Airflow UI hosted on your Deployment.

1. In the Deployment page of the Cloud UI, click the **Open Airflow** button.

2. In the main DAGs view of the Airflow UI, click the slider button next to `example-dag-basic` to unpause it. If you hover over the DAG, it says `DAG is Active`. When you do this, the DAG starts to run on the schedule that is defined in its code.

    ![Pause DAG slider in the Airflow UI](/img/docs/tutorial-unpause-dag.png)

3. Manually trigger a DAG run of `example-dag-basic` by clicking the play button in the **Actions** column. When you develop DAGs on Astro, triggering a DAG run instead of waiting for the DAG schedule can help you quickly identify and resolve issues.

    After you press **Play**, the **Runs** and **Recent Tasks** sections for the DAG start to populate with data.

    ![DAG running in the Airflow UI](/img/docs/tutorial-run-dag.png)

    These circles represent different [states](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) that your DAG and task runs can be in. 

4. Click on the name of the DAG, **example-dag-basic**, to open the **Grid** view for the DAG. To see if your DAG ran successfully, the most recent entry in the grid should have green squares for all of your tasks.

5. Pause your DAG by clicking the slider button next to `example-dag-basic`. This prevents your example DAG from running automatically and consuming your Deployment resources.

## Step 6: View your DAG status in the Cloud UI

The Cloud UI shows you information about the health of your Deployment, including analytics and logs for your DAG runs.

Go back to your Deployment page in the Cloud UI. Because you ran your example DAG, your Deployment information page now has data about your Deployment and DAG runs. The following example shows an example of what you might find in the **Overview** page for your Deployment.

![Summary information about your DAG runs in the Analytics tab of a Quickstart Deployment.](/img/docs/first-DAG-data.png)

When you're done exploring, you can delete your Deployment from the **More Options** menu on your **Deployments** page.

## Next Steps

Now that you've created and run your first DAG on Astro, the next step is to add your own DAGs, build out the rest of your Astro project, and start testing real data. See:

- [Develop a project](cli/develop-project.md).
- [Install Docker](https://www.docker.com/products/docker-desktop/) to use the full capabilities of the Astro CLI, such as the ability to run Airflow locally and deploy the rest of your Astro project to Astro, including Python packages.
- [Write your First DAG](https://docs.astronomer.io/learn/get-started-with-airflow).
- [Deploy code to Astro](deploy-code.md).
