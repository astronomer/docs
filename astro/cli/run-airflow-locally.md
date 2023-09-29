---
sidebar_label: 'Run Airflow locally'
title: 'Run your Astro project in a local Airflow environment'
id: run-airflow-locally
description: Run commands in your local Airflow environment to troubleshoot running DAGs and tasks.
---

Running Airflow locally with the Astro CLI can be an easy way to preview and debug DAG changes quickly before deploying your code to Astro. By locally running your DAGs, you can fix issues with your DAGs without consuming infrastructure resources or waiting on code deploy processes.

This document explains how to use the Astro CLI to start a local Airflow environment on your computer and interact with your Astro project. To learn more about unit testing for your DAGs or testing project dependencies when changing Python or Astro Runtime versions, see [Test your project locally](test-your-astro-project-locally.md).


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

## Troubleshoot KubernetesPodOperator issues

View local Kubernetes logs to troubleshoot issues with Pods that are created by the KubernetesPodOPerator. See [Test and Troubleshoot the KubernetesPodOperator Locally](https://docs.astronomer.io/learn/kubepod-operator#run-the-kubernetespodoperator-locally).

## Hard reset your local environment

In most cases, [restarting your local project](cli/develop-project.md#restart-your-local-environment) is sufficient for testing and making changes to your project. However, it is sometimes necessary to kill your Docker containers and metadata database for testing purposes. To do so, run the following command:

```sh
astro dev kill
```

This command forces your running containers to stop and deletes all data associated with your local Postgres metadata database, including Airflow connections, logs, and task history.

## Troubleshoot dependency errors

When dependency errors occur, the error message that is returned often doesn't contain enough information to help you resolve the error. To retrieve additional error information, you can review individual operating system or python package dependencies inside your local Docker containers.

For example, if your `packages.txt` file contains several packages and you receive build errors after running `astro dev start`, you can enter the container and install the packages manually to review additional information about the errors.

1. Open your Astro project `packages.txt` file and remove the references to the packages that are returning error messages.

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

5. Open your Astro project `packages.txt` file and add the package references you removed in Step 1 individually until you find the package that is the source of the error.

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

## Common issues 

Use the following topics to resolve common issues with running an Astro project in a local environment.

### Why aren't my new DAGs visible in the Airflow UI?

Make sure that no DAGs have duplicate `dag_ids`. When two DAGs use the same `dag_id`, the newest DAG won't appear in the Airflow UI and you won't receive an error message.

By default, the Airflow scheduler scans the `dags` directory of your Astro project for new files every 300 seconds (5 minutes). For this reason, it might take a few minutes for new DAGs to appear in the Airflow UI. Changes to existing DAGs appear immediately. 

To have the scheduler check for new DAGs more frequently, you can set the [`AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval) environment variable to less than 300 seconds. If you have less than 200 DAGs in a Deployment, it's safe to set `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` to `30` (30 seconds). See [Set environment variables](environment-variables.md) for how to set this on Astro.

In Astro Runtime 7.0 and later, the Airflow UI **Code** page includes a **Parsed at** value which shows when a DAG was last parsed. This value can help you determine when a DAG was last rendered in the Airflow UI. To view the **Parsed at** value in the Airflow UI, click **DAGs**, select a DAG, and then click **Code**. The **Parsed at** value appears at the top of the DAG code pane.

### Why are my DAGs running slowly?

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

If you are using Podman, you can run `podman machine set --cpus 4 --memory 4096`. See [Podman commands reference](https://docs.podman.io/en/latest/markdown/podman-machine-set.1.html) for more details.

:::

### My Astro project won't load after running `astro dev start`

If you're running the Astro CLI on a Mac computer that's built with the Apple M1 chip, your Astro project might take more than 5 mins to start after running `astro dev start`. This is a current limitation of Astro Runtime and the Astro CLI.

If your project won't load, it might also be because your webserver or scheduler is unhealthy. In this case, you might need to debug your containers.

1. After running `astro dev start`, retrieve a list of running containers by running `astro dev ps`.
2. If the webserver and scheduler containers exist but are unhealthy, check their logs by running:

    ```sh
    $ astro dev logs --webserver
    $ astro dev logs --scheduler
    ```
3. (Optional) Run the following command to prune all unused Docker objects including volumes and free disk space:

    ```bash
    docker system prune --volumes
    ```

    See [`docker system prune`](https://docs.docker.com/config/pruning/#prune-everything) for more information about pruning.
These logs should help you understand why your webserver or scheduler is unhealthy. Possible reasons why these containers might be unhealthy include:

- Not enough Docker resources.
- A failed Airflow or Astro Runtime version upgrade.
- Misconfigured Dockerfile or Docker override file.
- Misconfigured Airflow settings including `packages.txt` or `requirements.txt`.

### Ports are not available for my local Airflow webserver 

By default, the Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database in a local Airflow environment. If these ports are already in use on your local computer, an error message similar to the following appears:

```text
Error: error building, (re)creating or starting project containers: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 → 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use
```

To resolve a port availability error, you have the following options:

- Stop all running Docker containers and restart your local environment using `astro dev restart`.
- Change the default ports for these components. For example, you can use `astro config set webserver.port 8081` for the webserver and `astro config set postgres.port 5433` for Postgres. See [Configure CLI](cli/configure-cli.md) for all available configurations.

#### Stop all running Docker containers

1. Run `docker ps` to identify the Docker containers running on your computer.
2. Copy the values in the `CONTAINER ID` column.
3. Select one of the following options:

    - Run `docker stop <container_id>` to stop a specific Docker container. Replace `<container_id>` with one of the values you copied in step 2.
    - Run `docker stop $(docker ps -q)` to stop all running Docker containers.

#### Change the default port assignment

If port 8080 or 5432 are in use on your machine by other services, the Airflow webserver and metadata database won't be able to start. To run these components on different ports, run the following commands in your Astro project:

```bash
astro config set webserver.port <available-port>
astro config set postgres.port <available-port>
```

For example, to use 8081 for your webserver port and 5435 for your database port, you would run the following commands:

```bash
astro config set webserver.port 8081
astro config set postgres.port 5435
```
