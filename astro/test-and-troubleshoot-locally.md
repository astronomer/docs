---
sidebar_label: 'Test and troubleshoot locally'
title: 'Test and troubleshoot locally'
id: test-and-troubleshoot-locally
---

<head>
  <meta name="description" content="Learn how to test and troubleshoot DAGs in a local Apache Airflow environment with the Astro command-line interface (CLI)." />
  <meta name="og:description" content="Learn how to test and troubleshoot DAGs in a local Apache Airflow environment with the Astro command-line interface (CLI)." />
</head>

As you develop data pipelines on Astro, Astronomer recommends running and testing your DAGs locally before deploying your project to a Deployment on Astro. This document provides information about testing and troubleshooting DAGs in a local Apache Airflow environment with the Astro CLI.

For information about creating an Astro project, see [Create an Astro project](develop-project.md#create-an-astro-project). For information about adding DAGs to your Astro project and applying changes, see [Develop a project](develop-project.md).

## Run a DAG with `astro run`

Use the `astro run` command to run a DAG from the command line. When you run the command, the CLI compiles your DAG and runs it in a single Airflow worker container based on your Astro project configurations, including your `Dockerfile`, DAG utility files, Python requirements, and environment variables. You can review task logs and whether a task succeeded or failed in your terminal without opening the Airflow UI. You can only run one DAG at a time. Running DAGs without a scheduler or webserver can help reduce the time required to develop and test data pipelines.

To run a DAG located within your local `/dags` directory run:

```sh
astro run <dag-id>
```

All the tasks in your DAG run sequentially. Any errors produced by your code while parsing or running your DAG appear in the command line. For more information about this command, see the [CLI command reference](cli/astro-run.md).

## Test DAGs with the Astro CLI

To enhance the development experience for data pipelines, Astro enables users to run DAG unit tests with two different Astro CLI commands:

- `astro dev parse`
- `astro dev pytest`

### Parse DAGs

To quickly parse your DAGs, you can run:

```sh
astro dev parse
```

This command parses your DAGs to ensure that they don't contain any basic syntax or import errors and that they can successfully render in the Airflow UI.

The command `astro dev parse` is a more convenient but less customizable version of `astro dev pytest`. If you don't have any specific test files that you want to run on your DAGs, Astronomer recommends using `astro dev parse` as your primary testing tool. For more information about this command, see the [CLI command reference](cli/astro-dev-parse.md).

### Run tests with pytest

To perform unit tests on your Astro project, you can run:

```sh
astro dev pytest
```

This command runs all tests in your project's `tests` directory with [pytest](https://docs.pytest.org/en/7.0.x/index.html#), a testing framework for Python. With pytest, you can test custom Python code and operators locally without having to start a local Airflow environment.

By default, the `tests` directory in your Astro project includes a default DAG integrity test called `test_dag_integrity.py`. This test checks that:

- All Airflow tasks have required arguments.
- DAG IDs are unique across the Astro project.
- DAGs have no cycles.
- There are no general import or syntax errors.

`astro dev pytest` runs this default test alongside any other custom tests that you add to the `tests` directory. For more information about this command, see the [CLI command reference](cli/astro-dev-pytest.md).

## View Airflow logs

You can use the Astro CLI to view logs for Airflow tasks and components from your local Airflow environment. This is useful if you want to troubleshoot a specific task instance, or if your environment suddenly stops working after a code change.

See [View logs](view-logs.md).

## Run Airflow CLI commands

To run [Apache Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) commands locally, run the following:

```sh
astro dev run <airflow-cli-command>
```

For example, the Airflow CLI command for listing connections is `airflow connections list`. To run this command with the Astro CLI, you would run `astro dev run connections list` instead.

Running `astro dev run` with the Astro CLI is the equivalent of running `docker exec` in local containers and then running an Airflow CLI command within those containers.

:::tip

You can only use `astro dev run` in a local Airflow environment. To automate Airflow actions on Astro, you can use the [Airflow REST API](airflow-api.md). For example, you can make a request to the [`dagRuns` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) to trigger a DAG run programmatically, which is equivalent to running `airflow dags trigger` in the Airflow CLI.

:::

## Make requests to the Airflow REST API locally

Make requests to the [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) in a local Airflow environment with HTTP basic access authentication. This can be useful for testing and troubleshooting API calls before executing them in a Deployment on Astro.

To make local requests with cURL or Python, you only need the username and password for your local user. Both of these values are `admin` by default. They are the same credentials that are listed when you run `astro dev start` with the Astro CLI and required by the Airflow UI in a local environment.

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

View local Kubernetes logs to troubleshoot issues with Pods that are created by the operator. See [Test and Troubleshoot the KubernetesPodOperator Locally](https://docs.astronomer.io/learn/kubepod-operator#run-the-kubernetespodoperator-locally).

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

## Override the CLI Docker Compose file

The Astro CLI uses a default set of [Docker Compose](https://docs.docker.com/compose/) configurations to define and run local Airflow components. For advanced testing cases, you might need to override these default configurations. For example:

- Adding extra containers to mimic services that your Airflow environment needs to interact with locally, such as an SFTP server.
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

## Troubleshoot common issues

Use the information provided here to resolve common issues with running an Astro project in a local environment.

### New DAGs aren't visible in the Airflow UI

Make sure that no DAGs have duplicate `dag_ids`. When two DAGs use the same `dag_id`, the newest DAG won't appear in the Airflow UI and you won't receive an error message.

By default, the Airflow scheduler scans the `dags` directory of your Astro project for new files every 300 seconds (5 minutes). For this reason, it might take a few minutes for new DAGs to appear in the Airflow UI. Changes to existing DAGs appear immediately. 

To have the scheduler check for new DAGs more frequently, you can set the [`AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval) environment variable to less than 300 seconds. If you have less than 200 DAGs in a Deployment, it's safe to set `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` to `30` (30 seconds). See [Environment variables](environment-variables.md).

In Astro Runtime 7.0 and later, the Airflow UI **Code** page includes a **Parsed at** value which shows when a DAG was last parsed. This value can help you determine when a DAG was last rendered in the Airflow UI. To view the **Parsed at** value in the Airflow UI, click **DAGs**, select a DAG, and then click **Code**. The **Parsed at** value appears at the top of the DAG code pane.

### DAGs are running slowly

If your Astro project contains many DAGs or tasks, then you might experience performance issues in your local Airflow environment.

To improve the performance of your environment, you can:

 - Adjust CPU and memory resource allocation in your Docker configuration. Be aware that increasing Docker resource allocation might decrease the performance of your computer.
 - Modify Airflow-level environment variables, including concurrency and parallelism. See [Scaling out Airflow](https://docs.astronomer.io/learn/airflow-scaling-workers).

Generating DAGs dynamically can also decrease the performance of your local Airflow environment, though it's a common authoring pattern for advanced use cases. For more information, see [Dynamically Generating DAGs in Airflow](https://docs.astronomer.io/learn/dynamically-generating-dags/). If your DAGs continue to run slowly and you can't scale Docker or Airflow any further, Astronomer recommends pushing your project to a Deployment on Astro that's dedicated to testing.

:::tip

If you don't have enough Docker resources allocated to your local Airflow environment, you might see tasks fail and exit with this error:

   ```
   Task exited with return code Negsignal.SIGKILL
   ```

If you see this error, increase the CPU and memory allocated to Docker. If you're using Docker Desktop, you can do this by opening Docker Desktop and going to **Preferences** > **Resources** > **Advanced**. See [Change Docker Desktop preferences on Mac](https://docs.docker.com/desktop/settings/mac/).

:::

### Astro project won't load after `astro dev start`

If you're running the Astro CLI on a Mac computer that's built with the Apple M1 chip, your Astro project might take more than 5 mins to start after running `astro dev start`. This is a current limitation of Astro Runtime and the Astro CLI.

If your project won't load, it might also be because your webserver or scheduler is unhealthy. In this case, you might need to debug your containers.

1. After running `astro dev start`, retrieve a list of running containers by running `astro dev ps`.
2. If the webserver and scheduler containers exist but are unhealthy, check their logs by running:

    ```sh
    $ astro dev logs --webserver
    $ astro dev logs --scheduler
    ```
3. Optional. Run the following command to prune volumes and free disk space:

    ```sh
    docker system prune --volumes
    ```

These logs should help you understand why your webserver or scheduler is unhealthy. Possible reasons why these containers might be unhealthy include:

- Not enough Docker resources.
- A failed Airflow or Astro Runtime version upgrade.
- Misconfigured Dockerfile or Docker override file.
- Misconfigured Airflow settings.

### Ports are not available

By default, the Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database in a local Airflow environment. If these ports are already in use on your local computer, an error message similar to the following appears:

```text
Error: error building, (re)creating or starting project containers: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 → 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use
```

To resolve a port availability error, you have the following options:

- Stop all running Docker containers and restart your local environment.
- Change the default ports for these components.

#### Stop all running Docker containers

1. Run `docker ps` to identify the Docker containers running on your computer.
2. Copy the values in the `CONTAINER ID` column.
3. Select one of the following options:

    - Run `docker stop <container_id>` to stop a specific Docker container. Replace `<container_id>` with one of the values you copied in step 2.
    - Run `docker stop $(docker ps -q)` to stop all running Docker containers.

#### Change the default port assignment

If port 8080 or 5432 are in use on your machine by other services, the Airflow webserver and metadata database won't be able to start. To run these components on different ports, run the following commands in your Astro project:

```sh
astro config set webserver.port <available-port>
astro config set postgres.port <available-port>
```

For example, to use 8081 for your webserver port and 5435 for your database port, you would run the following commands:

```sh
astro config set webserver.port 8081
astro config set postgres.port 5435
```
