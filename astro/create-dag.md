---
sidebar_label: 'Run your first DAG on Astro'
title: 'Create and run your first DAG on Astro.'
id: 'create-first-DAG'
---

<head>
  <meta name="description" content="Learn how to deploy and run a DAG in an Astro project with the Astro command-line interface (CLI). You need an Astro project to run Airflow pipelines on Astro." />
  <meta name="og:description" content="Learn how to deploy and run a DAG in an Astro project with the Astro command-line interface (CLI). You need an Astro project to run Airflow pipelines on Astro." />
</head>

import {siteVariables} from '@site/src/versions';

## Prerequisites

- [The Astro CLI](cli/install-cli.md)
- [Docker](https://www.docker.com/products/docker-desktop)
- A [Workspace](manage-workspaces.md)
- An Astronomer account

## Step 1: Create an Astro project

1. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

2. Open the directory:

    ```sh
    cd <your-astro-project-name>
    ```

3. Run the following Astro CLI command to initialize an Astro project in the directory:

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

    This set of files will build into a Docker image that you can both run on your local machine and deploy to Astro.

### Astro Runtime

Your `Dockerfile` includes a reference to Astro Runtime. Packaged into a Debian-based Docker image, Astro Runtime extends the Apache Airflow open source project to provide you with differentiated functionality that centers around reliability, efficiency, and performance. For more information on what's included in Runtime and how it's versioned, see [Runtime versioning](runtime-version-lifecycle-policy.md).

By default, the Docker image in your Dockerfile is:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
`}</code></pre>

## Step 2: Build your project locally

To confirm that you successfully initialized an Astro project, run the following command from your project directory:

```sh
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators)

If your project builds successfully, the Airflow UI automatically opens in your default webserver at `https://localhost:8080/`.

When you create an Astro project, the Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database by default. If these ports are already in use on your local computer, an error message might appear. To resolve this error message, see [Test and troubleshoot locally](test-and-troubleshoot-locally.md#ports-are-not-available).

:::tip

Use the `astro run <dag-id>` command to run and debug a DAG from the command line without starting a local Airflow environment. This is an alternative to testing your entire Astro project with the Airflow webserver and scheduler. See [Run and Debug DAGs with Astro Run](test-and-troubleshoot-locally.md#run-and-debug-dags-with-astro-run).

:::

## Step 3: Locally access the Airflow UI

Once your project is running, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password.

:::info

It might take a few minutes for the Airflow UI to be available. As you wait for the webserver container to start up, you may need to refresh your browser.

:::

After logging in, you should see the DAGs from your `dags` directory in the Airflow UI.

![Example DAG in the Airflow UI](/img/docs/sample-dag.png)

## Step 4: Authenticate to Astro

Run the following command to authenticate to Astro:

```sh
astro login
```

After running this command, you are prompted to open your web browser and log in to the Cloud UI. Once you complete this login, you are automatically authenticated to the CLI.

:::tip

If you have [Deployment API key](api-keys.md) credentials set as OS-level environment variables on your local machine, you can deploy directly to Astro without needing to manually authenticate. This setup is required for automating code deploys with [CI/CD](ci-cd.md).

:::

## Step 5: Access the Astro Cloud UI

## Step 5: Deploy your code

When you start a code deploy to Astro, the status of the Deployment is **DEPLOYING** until it is determined that the underlying Airflow components are running the latest version of your code. During this time, you can hover over the status indicator to determine whether your entire Astro project or only DAGs were deployed .

When the deploy completes, the **Docker Image** and **DAG Bundle Version** fields in the Cloud UI are updated depending on the type of deploy you completed. 

- The **Docker Image** field displays a unique identifier generated by a Continuous Integration (CI) tool or a timestamp generated by the Astro CLI after you complete an image deploy. 
- The **DAG Bundle Version** field displays a unique timestamp generated by the Astro CLI after you complete an image deploy or a DAG-only deploy. If you do not have DAG-only deploys enabled, the DAG bundle version field isn't populated.

To confirm a deploy was successful, verify that the running versions of your Docker image and DAG bundle have been updated.

1. In the Cloud UI, select a Workspace and then select a Deployment.
2. Review the information in the **Docker Image** and **DAG bundle version** fields to determine the Deployment code version.

## Step 6: Access the Airflow UI on the Cloud

Steps to go to the Airflow UI through Astro

## Step 7: Trigger your DAG on Astro

A **DAG run** is an instance of a DAG running on a specific date. Let's trigger a run of the `example-dag-basic` DAG that was generated with your Astro project.

To provide a basic demonstration of an ETL pipeline, this DAG creates an example JSON string, calculates a value based on the string, and prints the results of the calculation to the Airflow logs.

1. Before you can run any DAG in Airflow, you have to unpause it. To unpause `example-dag-basic`, click the slider button next to its name. Once you unpause it, the DAG starts to run on the schedule defined in its code.

    ![Pause DAG slider in the Airflow UI](/img/docs/tutorial-unpause-dag.png)

2. While all DAGs can run on a schedule defined in their code, you can manually trigger a DAG run at any time from the Airflow UI. Manually trigger `example-dag-basic` by clicking the play button under the **Actions** column. During development, running DAGs on demand can help you identify and resolve issues.

After you press **Play**, the **Runs** and **Recent Tasks** sections for the DAG start to populate with data.

![DAG running in the Airflow UI](/img/docs/tutorial-run-dag.png)

These circles represent different [states](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) that your DAG and task runs can be in. However, these are only high-level summaries of your runs that won't make much sense until you learn more about how Airflow works. To get a better picture of how your DAG is running, let's explore some other views in Airflow.