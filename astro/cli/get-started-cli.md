---
sidebar_label: 'Get started with the CLI'
title: 'Get started with Airflow using the Astro CLI'
id: get-started-cli
---

After you install the Astro CLI and Docker Desktop, you can use the following CLI commands to quickly build and run your Airflow projects locally. 

## Prerequisites

- The [Astro CLI](install-cli.md)
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

## Step 1: Create an Astro project with `astro dev init`

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

## Step 2: Run Airflow locally using `astro dev start`

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

## Step 3: Developing locally with the CLI

The `astro dev` command options include a number of other useful actions that you can use while developing locally. 

### `astro dev restart`

You must restart your environment to apply changes from any of the following files in your Astro project:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To restart your local Airflow environment, run:

```sh
astro dev restart
```

This command rebuilds your image and restarts the Docker containers running on your local machine with the new image. Alternatively, you can run `astro dev stop` to stop your Docker containers without restarting your environment, then run `astro dev start` when you want to restart.

### `astro dev stop`

Run the following to pause all Docker containers running your local Airflow environment. 

```sh
astro dev stop
```

Unlike `astro dev kill`, this command does not prune mounted volumes and delete data associated with your local Postgres database. If you run this command, Airflow connections and task history will be preserved.

This command can be used regularly with `astro dev start` and `astro dev restart` during local development.

### `astro dev kill`

When you want to force-stop all four Docker containers for your local Airflow environment, use the following command. 

```sh
astro dev kill
```

`astro dev kill` also deletes all data associated with your local `Postgres` database which includes Airflow connections, logs, and task history.

## Next Steps

After you have finished Getting Started with the CLI, you can configure your CLI to locally debug your Airflow environment, authenticate to cloud services to test your DAGs with data stored on the cloud, or you can learn more about developing DAGs with Astro.

- [Configure the CLI](configure-cli.md)
- [Authenticate to cloud services](authenticate-to-cloud.md)
- [Build and run a project locally](develop-project.md#build-and-run-a-project-locally)




