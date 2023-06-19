---
sidebar_label: 'Run your first DAG'
title: 'Create and run your first DAG on Astro'
id: 'create-first-DAG'
---

<head>
  <meta name="description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI." />
  <meta name="og:description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI." />
</head>

import {siteVariables} from '@site/src/versions';

Astro is the industry's leading managed service for Apache Airflow. The best way to understand how Astro works is to run an Apache Airflow DAG with the Astro CLI. In this quickstart, follow the steps required to deploy an example DAG to Astro and trigger a DAG run from the Astro CLI.

Specifically, you will:

- Authenticate and log in to Astro. 
- Create a Deployment. 
- Create an Astro project. 
- Deploy DAGs to Astro with the Astro CLI.
- Trigger a run of an example DAG in the Airflow UI. 

This tutorial takes about 15 minutes. If you're new to Airflow and want a more in-depth tutorial, see [Write your First DAG](https://docs.astronomer.io/learn/get-started-with-airflow).

## Prerequisites

- An Astro account. To start an Astro trial, see [Start a trial](trial.md). 
- The latest version of the [the Astro CLI](cli/overview.md). 

Astronomer recommends installing [Docker Desktop](https://docs.docker.com/get-docker/) for testing and running Airflow on your local computer, but it's not required for this tutorial. If you just want to run Airflow on your local machine, see [Get started with Airflow using the Astro CLI](cli/get-started-cli.md).

## Step 1: Create a Deployment

An Astro _Deployment_ is an instance of Apache Airflow that is powered by all core Airflow components, including a webserver, scheduler, and one or more workers. You deploy DAGs to a Deployment, and you can have one or more Deployments within a Workspace.

1. Log in to the [Cloud UI](https://cloud.astronomer.io)

2. On the **Deployments** page, click **+ Deployment**.

3. In the **Name** field, enter a name for your Deployment. You can leave the other fields at their default values. This creates a basic Deployment on a standard Astronomer-hosted cluster. You can delete the Deployment after you finish testing your example DAG runs. 

4. Click **Create Deployment**.

    A confirmation message appears indicating that the Deployment status is **Creating** until all underlying components in the Deployment are healthy. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health). Or, to learn more about how to customize your Deployment settings, see [Configure a Deployment](configure-deployment-resources).

## Step 2: Create an Astro project

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
    │   └── test_dag_integrity.py # Test that checks for basic errors in your DAGs
    ├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
    ├── packages.txt # For OS-level packages
    └── requirements.txt # For Python packages
    ```

## Step 3: Deploy example DAGs to your Astro Deployment

DAG-only deploys are an Astro feature that you can use to quickly update your Astro Deployment by only deploying the `dags` folder of your Astro project. You'll now trigger a DAG-only deploy to push your example DAGs to Astro.

1. Run the following command to authenticate to Astro on the CLI:

    ```sh
    astro login astronomer.io
    ```

    After running this command, you are prompted to open your web browser and enter your credentials to the Cloud UI. The Cloud UI then automatically authenticates you to the CLI. The next time you need to log in, you can run `astro login` without specifying a domain.

2. Run the following command to deploy your DAGs to Astro: 
   
    ```sh
    astro deploy --dags
    ```

    This command returns a list of Deployments available in your Workspace and prompts you to confirm where you want to deploy your DAG code. After you select a Deployment, the CLI parses your DAGs to ensure that they don't contain basic syntax and import errors. If your code passes the parse, the Astro CLI deploys your DAGs to Astro.

## Step 4: Trigger your DAG on Astro

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

## Step 5: View your DAG status in the Cloud UI

The Cloud UI shows you information about the health of your Deployment, including analytics and logs for your DAG runs.

Go back to your Deployment page in the Cloud UI. Because you ran your example DAG, your Deployment information page now has data about your Deployment and DAG runs. The following example shows an example of what you might find in the **Analytics** view for your Deployment.

![Summary information about your DAG runs in the Analytics tab of a Quickstart Deployment.](/img/docs/first-DAG-data.png)

## Step 6: (Optional) Delete your Deployment

To limit resource usage, you might want to delete your Deployment after you finish triggering your DAG test runs.

1. In the Cloud UI, open your Workspace, then open your Deployment.

2. Select the ellipses to see more options, then click **Delete**.

3. When prompted, confirm the deletion by typing **DELETE**.

## Next Steps

Now that you've created and run your first DAG on Astro, the next step is to add your own DAGs, build out the rest of your Astro project, and start testing real data. See:

- [Install Docker](https://www.docker.com/products/docker-desktop/) to use the full capabilities of the Astro CLI, including the ability to run Airflow locally and deploy the rest of your Astro project to Astro, including Python packages.
- [Deploy code to Astro](/astro/deploy-code).
- [Develop a project](/astro/develop-project).
