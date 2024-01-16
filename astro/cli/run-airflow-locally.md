---
sidebar_label: 'Work with a local Airflow environment'
title: 'Run your Astro project in a local Airflow environment with the CLI'
id: run-airflow-locally
description: Run commands in your local Airflow environment.
---

Running Airflow locally with the Astro CLI can be an easy way to preview and debug DAG changes quickly before deploying your code to Astro. By locally running your DAGs, you can fix issues with your DAGs without consuming infrastructure resources or waiting on code deploy processes.

This document explains how to use the Astro CLI to start a local Airflow environment on your computer and interact with your Astro project. To learn more about unit testing for your DAGs or testing project dependencies when changing Python or Astro Runtime versions, see [Test your project locally](test-your-astro-project-locally.md).

You can find common issues and resolutions in the [troubleshoot a local environment](troubleshoot-locally.md) section.

## Start a local Airflow environment

To begin running your project in a local Airflow environment, run:

```bash
astro dev start
```

This command builds your project and spins up 4 containers on your machine, each for a different Airflow component. After the command completes, you can access your project's Airflow UI at `https://localhost:8080/`.

## Restart a local Airflow environment

Restarting your Airflow environment rebuilds your image and restarts the Docker containers running on your local machine with the new image. Restart your environment to apply changes from specific files in your project, or to troubleshoot issues that occur when your project is running.

To restart your local Airflow environment, run:

```sh
astro dev restart
```

Alternatively, you can run `astro dev stop` to stop your Docker containers without restarting your environment, then run `astro dev start` when you want to restart.

## Stop a local Airflow environment

Run the following command to pause all Docker containers and stop running your local Airflow environment.

```sh
astro dev stop
```

Unlike [`astro dev kill`](#hard-reset-your-airflow-environment), this command does not prune mounted volumes and delete data associated with your local Postgres database. If you run this command, Airflow connections and task history will be preserved.

Use this command when you're finished testing Airflow and you want to stop running its components locally.

## View Airflow component logs

You can use the Astro CLI to view logs for your local Airflow environment's webserver, scheduler, and triggerer. This is useful if you want to troubleshoot a specific task instance, or if your local environment does not run properly after a code change.

To view component logs in a local Airflow environment, run:

```sh
astro dev logs
```

See the [Astro CLI reference guide](cli/astro-dev-logs.md) for more details and options.

## Apply changes to a running project

If you update DAG code for an Astro project that's currently running locally, the Astro CLI automatically applies your changes to your environment. However, to update other files, you must restart your environment to apply your changes.

Specifically, you must restart your environment to apply changes for any of the following files:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To restart your local Airflow environment, run:

```sh
astro dev restart
```

## Run Airflow CLI commands

To run [Apache Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) commands locally, run the following:

```sh
astro dev run <airflow-cli-command>
```

For example, the Airflow CLI command for listing connections is `airflow connections list`. To run this command with the Astro CLI, you would run `astro dev run connections list` instead.

`astro dev run` is the equivalent of running `docker exec` in local containers and then running an Airflow CLI command within those containers.

:::info

You can only use `astro dev run` in a local Airflow environment. To automate Airflow actions on Astro, you can use the [Airflow REST API](airflow-api.md). For example, you can make a request to the [`dagRuns` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) to trigger a DAG run programmatically, which is equivalent to running `astro dev run dags trigger` in the Astro CLI.

:::

## Make requests to the Airflow REST API locally

Make requests to the [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in a local Airflow environment with HTTP basic access authentication. This can be useful for testing and troubleshooting API calls before executing them in a Deployment on Astro.

To make local requests with cURL or Python, you only need the username and password for your local user. Both of these values are `admin` by default. They are the same credentials for logging into the Airflow UI, and they're listed when you run `astro dev start`.

To make requests to the Airflow REST API in a Deployment on Astro, see [Airflow API](airflow-api.md).

### cURL

```bash
curl -X GET localhost:8080/api/v1/<endpoint> --user "admin:admin"
```

### Python

```python
import requests

response = requests.get(
   url="http://localhost:8080/api/v1/<endpoint>",
   auth=("admin", "admin")
)
```

## Hard reset your local environment

In most cases, [restarting your local project](cli/develop-project.md#restart-your-local-environment) is sufficient for testing and making changes to your project. However, it is sometimes necessary to kill your Docker containers and metadata database for testing purposes. To do so, run the following command:

```sh
astro dev kill
```

This command forces your running containers to stop and deletes all data associated with your local Postgres metadata database, including Airflow connections, logs, and task history.

## Override the Astro CLI Docker Compose file

The Astro CLI uses a default set of [Docker Compose](https://docs.docker.com/compose/) configurations to define and run local Airflow components. For advanced testing cases, you might need to override these default configurations. For example, you might need to:

- Add extra containers to mimic services that your Airflow environment needs to interact with locally, such as an SFTP server.
- Change the volumes mounted to any of your local containers.

:::info

The Astro CLI does not support overrides to environment variables that are required globally. For the list of environment variables that Astro enforces, see [Global environment variables](platform-variables.md). To learn more about environment variables, read [Environment variables](environment-variables.md).

:::

1. Reference the Astro CLI's default [Docker Compose file](https://github.com/astronomer/astro-cli/blob/main/airflow/include/composeyml.yml) (`composeyml.yml`) and determine one or more configurations to override.
2. Add a `docker-compose.override.yml` file at the top level of your Astro project.
3. Specify your new configuration values in `docker-compose.override.yml` file using the same format as in `composeyml.yml`.

For example, to add another volume mount for a directory named `custom_dependencies`, add the following to your `docker-compose.override.yml` file:

```yaml
version: "3.1"
services:
  scheduler:
    volumes:
      - /home/astronomer_project/custom_dependencies:/usr/local/airflow/custom_dependencies:ro
```

Make sure to specify `version: "3.1"` and follow the format of the source code file linked above.

Run the following command to see the override file in your scheduler container:

```sh
astro dev bash --scheduler "ls -al"
```
