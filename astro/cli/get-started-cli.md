---
sidebar_label: 'Quickstart'
title: 'Get started with Airflow using the Astro CLI'
id: get-started-cli
description: Create an Airflow project and run it locally on your computer in just a few minutes. 
---

One of the Astro CLI's main features is its ability to run Airflow on your local machine. After you install the Astro CLI and Docker Desktop, follow this quickstart to build an Airflow project and run it in a local Airflow environment using just a few commands. At the end of the tutorial, you'll have all of the files and components you need to develop and test Airflow DAGs locally.

## Prerequisites

- The [Astro CLI](install-cli.md)
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

## Step 1: Create an Astro project

An _Astro project_ contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. All new Astro projects contain two example DAGs. This set of files builds a Docker image that you can both run on your local machine with Airflow and deploy to Astro.

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

## Step 2: Run Airflow locally

Running your project locally allows you to test your DAGs before you deploy them to a production environment. While this step is not required for deploying and running your code on Astro, Astronomer recommends always using the Astro CLI to test locally before deploying.

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

The Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database by default. If these ports are already in use on your local computer, an error message might appear. To resolve this error message, see [Run Airflow locally](cli/run-airflow-locally.md#ports-are-not-available-for-my-local-airflow-webserver).

:::

## Step 3: Develop locally with the CLI

Now that you have a locally running project, you can start to develop your Astro project by adding DAGs, dependencies, environment variables, and more. See [Develop your project](develop-project.md) for more details on how to modify all aspects of your Astro project. 

Most changes you make, including updates to your DAG code, are applied automatically to your running environment and don't require rebuilding your project. However, you must rebuild your project and restart your environment to apply changes from any of the following files in your Astro project:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To restart your local Airflow environment, run:

```sh
astro dev restart
```

This command rebuilds your image and restarts the Docker containers running on your local machine with the new image. Alternatively, you can run `astro dev stop` to stop your Docker containers without restarting your environment, then run `astro dev start` when you want to restart.

## Next Steps

After you have finished Getting Started with the CLI, you can configure your CLI to locally debug your Airflow environment, authenticate to cloud services to test your DAGs with data stored on the cloud, or you can learn more about developing DAGs with Astro.

- [Configure the CLI](configure-cli.md)
- [Authenticate to cloud services](authenticate-to-clouds.md)
- [Build and run a project locally](cli/develop-project.md#build-and-run-a-project-locally)
