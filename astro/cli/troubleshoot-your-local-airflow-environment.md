---
sidebar_label: 'Troubleshoot your Airflow environment'
title: 'Troubleshoot your Airflow environment'
id: troubleshoot-local-airflow-environment
description: Run commands in your local Airflow environment to troubleshoot running DAGs and tasks.
---

Some issues with a local Astro project can be solved only after running your local Airflow environment with `astro dev start`. For example, one of your DAGs might cause an error in your Airflow scheduler, which you can only know by triggering the task and checking your scheduler logs.

This document explains how to use Astro CLI commands to interact with a locally running Airflow environment and troubleshoot issues. Astronomer recommends troubleshooting after after successfully testing your Astro project.

## View Airflow component logs

You can use the Astro CLI to view logs for your local Airflow environment's webserver, scheduler, and triggerer. This is useful if you want to troubleshoot a specific task instance, or if your environment suddenly stops working after a code change.

To view component logs in a local Airflow environment, run:

```sh
astro dev logs
```

See the [Astro CLI reference guide](cli/astro-dev-logs.md) for more details and options.

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

```sh
curl -X GET localhost:8080/api/v1/<endpoint> --user "admin:admin"
```

### Python

```python
import requests

response = requests.get(
   url="localhost:8080/api/v1/<endpoint>",
   auth=("admin", "admin")
)
```

## Troubleshoot KubernetesPodOperator issues

View local Kubernetes logs to troubleshoot issues with Pods that are created by the KubernetesPodOPerator. See [Test and Troubleshoot the KubernetesPodOperator Locally](https://docs.astronomer.io/learn/kubepod-operator#run-the-kubernetespodoperator-locally).

## Hard reset your local environment

In most cases, [restarting your local project](develop-project.md#restart-your-local-environment) is sufficient for testing and making changes to your project. However, it is sometimes necessary to kill your Docker containers and metadata database for testing purposes. To do so, run the following command:

```sh
astro dev kill
```

This command forces your running containers to stop and deletes all data associated with your local Postgres metadata database, including Airflow connections, logs, and task history.

## Troubleshoot dependency errors

When dependency errors occur, the error message that is returned often doesn't contain enough information to help you resolve the error. To retrieve additional error information, you can review individual operating system or python package dependencies inside your local Docker containers.

For example, if your `packages.txt` file contains the `openjdk-8-jdk`, `gcc`, `g++`, or `libsas12-dev` packages and you receive build errors after running `astro dev start`, you can enter the container and install the packages manually to review additional information about the errors.

1. Open the `requirements.txt` and `packages.txt` files for your project and remove the references to the packages that are returning error messages.

2. Run the following command to build your Astro project into a Docker image and start a local Docker container for each Airflow component:

    ```sh
    astro dev start
    ```

3. Run the following command to open a bash terminal in your scheduler container:

    ```sh
    astro dev bash --scheduler
    ```

4. In the bash terminal for your container, run the following command to install a package and review any error messages that are returned:

    ```bash
    apt-get install <package-name>
    ```
    For example, to install the GNU Compiler Collection (GCC) compiler, you would run:

    ```bash
    apt-get install gcc
    ```

5. Open the `requirements.txt` and `packages.txt` files for your project and add the package references you removed in step 1 one by one until you find the package that is the source of the error.

## Override the Astro CLI Docker Compose file

The Astro CLI uses a default set of [Docker Compose](https://docs.docker.com/compose/) configurations to define and run local Airflow components. For advanced testing cases, you might need to override these default configurations. For example, you might need to:

- Add extra containers to mimic services that your Airflow environment needs to interact with locally, such as an SFTP server.
- Change the volumes mounted to any of your local containers.

:::info

The Astro CLI does not support overrides to environment variables that are required globally. For the list of environment variables that Astro enforces, see [Global environment variables](platform-variables.md). To learn more about environment variables, read [Environment variables](environment-variables.md).

:::

1. Reference the Astro CLI's default [Docker Compose file](https://github.com/astronomer/astro-cli/blob/main/airflow/include/composeyml.yml) (`composeyml.yml`) and determine one or more configurations to override.
2. Add a `docker-compose.override.yml` file to your Astro project.
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

To see your override file live in your local Airflow environment, run the following command to see the file in your scheduler container:

```sh
astro dev bash --scheduler "ls -al"
```