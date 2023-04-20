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

- Create an Astro project. 
- Authenticate and log in to Astro. 
- Create a Deployment. 
- Deploy your project to Astro with the Astro CLI.
- Trigger a run of an example DAG in the Airflow UI. 

## Prerequisites

- The [Astro CLI](cli/install-cli.md)
- An Astronomer account
- An Astro Organization and [Workspace](manage-workspaces.md)
- An Astro [cluster](create-cluster.md)

If you're the first person on your team to try Astro, see [Start your Astro trial](astro/trial.md). If your team has an existing Organization on Astro that you are not a member of, see [Add a user to an Organization](astro/add-user#add-a-user-to-an-organization).

## Step 1: Create an Astro project

An _Astro project_ contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. All new Astro projects contain two example DAGs.

1. Open your terminal or IDE

2. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

3. Open the directory:

    ```sh
    cd <your-astro-project-name>
    ```

4. Run the following Astro CLI command to initialize an Astro project in the directory:

    ```sh
    astro dev init
    ```

    This command generates the following files in the directory:

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

    This set of files builds a Docker image that you can both run on your local machine and deploy to Astro.

## Step 2: Build your project locally

Building your project locally allows you to test your DAGs and confirm that your example Astro project builds correctly before you run it remotely in Astro. While this step is not required for deploying and running your code on Astro, Astronomer recommends always using the Astro CLI to test locally before deploying.

1. To start running your project in a local Airflow environment, run the following command from your project directory:

    ```sh
    astro dev start
    ```

    This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

    - **Postgres:** Airflow's metadata database
    - **Webserver:** The Airflow component responsible for rendering the Airflow UI
    - **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
    - **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators)

2. After your project builds successfully, open the Airflow UI in your web browser at `https://localhost:8080/`.

3. Find your DAGs in the`dags` directory in the Airflow UI. 

    In this directory, you can find several example DAGs including `example-dag-basic` DAG, which was generated with your Astro project. To provide a basic demonstration of an ETL pipeline, this DAG creates an example JSON string, calculates a value based on the string, and prints the results of the calculation to the Airflow logs.

    ![Example DAG in the Airflow UI](/img/docs/sample-dag.png)

:::info

The Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database by default. If these ports are already in use on your local computer, an error message might appear. To resolve this error message, see [Test and troubleshoot locally](test-and-troubleshoot-locally.md#ports-are-not-available).

:::

## Step 3: Log in to Astro CLI and Cloud UI

While you run your DAGs locally, you don't need to log in with the CLI or Cloud UI. But to run your DAGs on the Cloud UI, you need to authenticate with both the Astro CLI and Cloud UI.

1. Run the following command to authenticate to Astro on the CLI:

    ```sh
    astro login
    ```

    After running this command, you are prompted to open your web browser and enter your credentials to the Cloud UI. Then, you are automatically authenticated to the CLI.

2. Go to `https://cloud.astronomer.io`, and select one of the available options to access the Cloud UI.

## Step 4: Create a Deployment

An Astro _Deployment_ is an Astro Runtime environment that is powered by the core components of Apache Airflow, including the Airflow webserver, scheduler, and one or more workers. You can have one or more Deployments within a _Workspace_, which is a collection of users that have access to the same Deployments.

When you create a Deployment on Astro, infrastructure is created in your cluster that runs your DAGs with all core Apache Airflow components.

1. In the Cloud UI, select a **Workspace**.

2. On the **Deployments** page, click **Deployment**.

3. Complete the following fields:

    - **Name**: Enter a name for your Deployment.
    - **Cluster**: Select the Astro cluster in which you want to create this Deployment.
  
    You can leave the other fields at their default values. This creates a basic Deployment that you can delete after you finish testing your example DAG runs. 

4. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment status is **Creating** until all underlying components in your Astro cluster are healthy. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health). Or, to learn more about how to customize your Deployment settings, see [Configure a Deployment](configure-deployment-resources).

## Step 5: Deploy your Astro project to your Astro Deployment

To deploy your Astro project, run:

```sh
astro deploy
```

This command returns a list of Deployments available in your Workspace and prompts you to pick one.

After you select a Deployment, the CLI parses your DAGs to ensure that they don't contain basic syntax and import errors. If your code passes the parse, the Astro CLI builds all files in your Astro project directory into a new Docker image and then pushes the image to your Deployment on Astro. 

## Step 6: Trigger your DAG on Astro

When you deploy your Astro project, all example DAGs will initially be paused and will not start running automatically. To run one of these example DAGs according to its schedule, you have to unpause it from the Airflow UI.

1. In the Deployment page of the Cloud UI, click the **Open Airflow** button.

2. In the main DAGs view of the Airflow UI, click the slider button next to `example-dag-basic` to unpause it. If you hover over the DAG, it says `DAG is Active`. When you do this, the DAG starts to run on the schedule that is defined in its code.

    ![Pause DAG slider in the Airflow UI](/img/docs/tutorial-unpause-dag.png)

3. Manually trigger a DAG run of `example-dag-basic` by clicking the play button in the **Actions** column. When you develop DAGs on Astro, triggering a DAG run instead of waiting for the DAG schedule can help you quickly identify and resolve issues.

    After you press **Play**, the **Runs** and **Recent Tasks** sections for the DAG start to populate with data.

    ![DAG running in the Airflow UI](/img/docs/tutorial-run-dag.png)

    These circles represent different [states](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) that your DAG and task runs can be in. 

4. Click on the name of the DAG, **example-dag-basic**, to open the **Grid** view for the DAG. To see if your DAG ran successfully, the most recent entry in the grid should have green squares for all of your tasks.

5. Pause your DAG by clicking the slider button next to `example-dag-basic`. This prevents your example DAG from running automatically and consuming your Deployment resources.

## Step 7: View your DAG status in the Cloud UI

Your Airflow UI view allows you to examine your DAGs in detail, while the Cloud UI shows you information about the health of your Deployment including analytics and logs of your DAG runs.

Go back to your Deployment page in the Cloud UI. Because you ran your example DAG, your Deployment information page now has data about your Deployment and DAG runs. The following example shows an example of what you might find in the **Analytics** view for your Deployment.

![Summary information about your DAG runs in the Analytics tab of a Quickstart Deployment.](/img/docs/first-DAG-data.png)

## Step 8: (Optional) Delete your Deployment

To limit resource usage, you might want to delete your Deployment after you finish triggering your DAG test runs.

1. In the Cloud UI, open your Workspace, then open your Deployment.

2. Select the ellipses to see more options, then click **Delete**.

3. When prompted, confirm the deletion by typing **DELETE**.

## Next Steps

Now that you've created and run your first DAG on Astro, you can learn more about working with Astro, Airflow, and DAGs.

- [Develop a project](/astro/develop-project)
- [Learn how to write your own DAGs](https://docs.astronomer.io/learn/category/dags)
- [Deploy code to Astro](/astro/deploy-code)
- [Set up CI/CD](/astro/set-up-ci-cd)
