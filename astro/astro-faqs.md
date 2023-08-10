---
sidebar_label: 'FAQs'
title: 'Astro FAQs'
id: astro-faq
---

This FAQ contains help and troubleshooting for the most common problems you might experience when getting started on Astro.

For more advanced troubleshooting topics, see the [Astronomer support portal](astro-support.md).

## Why aren't my new DAGs visible in the Airflow UI?

Make sure that no DAGs have duplicate `dag_ids`. When two DAGs use the same `dag_id`, the newest DAG won't appear in the Airflow UI and you won't receive an error message.

By default, the Airflow scheduler scans the `dags` directory of your Astro project for new files every 300 seconds (5 minutes). For this reason, it might take a few minutes for new DAGs to appear in the Airflow UI. Changes to existing DAGs appear immediately. 

To have the scheduler check for new DAGs more frequently, you can set the [`AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval) environment variable to less than 300 seconds. If you have less than 200 DAGs in a Deployment, it's safe to set `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` to `30` (30 seconds). See [Set environment variables](environment-variables.md) for how to set this on Astro.

In Astro Runtime 7.0 and later, the Airflow UI **Code** page includes a **Parsed at** value which shows when a DAG was last parsed. This value can help you determine when a DAG was last rendered in the Airflow UI. To view the **Parsed at** value in the Airflow UI, click **DAGs**, select a DAG, and then click **Code**. The **Parsed at** value appears at the top of the DAG code pane.

## Why are my DAGs running slowly?

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

## My Astro project won't load after running `astro dev start`

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

## Ports are not available for my local Airflow webserver 

By default, the Astro CLI uses port `8080` for the Airflow webserver and port `5432` for the Airflow metadata database in a local Airflow environment. If these ports are already in use on your local computer, an error message similar to the following appears:

```text
Error: error building, (re)creating or starting project containers: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 → 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use
```

To resolve a port availability error, you have the following options:

- Stop all running Docker containers and restart your local environment using `astro dev restart`.
- Change the default ports for these components. For example, you can use `astro config set webserver.port 8081` for the webserver and `astro config set postgres.port 5433` for Postgres. See [Configure CLI](cli/configure-cli.md) for all available configurations.

### Stop all running Docker containers

1. Run `docker ps` to identify the Docker containers running on your computer.
2. Copy the values in the `CONTAINER ID` column.
3. Select one of the following options:

    - Run `docker stop <container_id>` to stop a specific Docker container. Replace `<container_id>` with one of the values you copied in step 2.
    - Run `docker stop $(docker ps -q)` to stop all running Docker containers.

### Change the default port assignment

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
