---
sidebar_label: 'Test and troubleshoot locally'
title: 'Test and troubleshoot locally'
id: test-and-troubleshoot-locally
description: A guide to running an Astro project locally and diagnosing common problems.
---

As you develop data pipelines on Astro, we strongly recommend running and testing your DAGs locally before deploying your project to a Deployment on Astro. This document provides information about testing and troubleshooting DAGs in a local Apache Airflow environment with the Astro CLI.

## Run a project locally

Whenever you want to test your code, the first step is always to start a local Airflow environment. To run your project in a local Airflow environment, follow the steps in [Build and run a project](develop-project.md#build-and-run-a-project-locally).

## Test DAGs with the Astro CLI

To enhance the testing experience for data pipelines, Astro enables users to run DAG unit tests with two different Astro CLI commands:

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

You can use the Astro CLI to view logs for Airflow tasks and components from your local Airflow environment. This is useful if you want to troubleshoot a specific task instance, or if your environment suddenly stops working after a code change. See [View logs](view-logs.md).

## Run Airflow CLI commands

To run [Apache Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) commands locally, run the following:

```sh
astro dev run <airflow-cli-command>
```

For example, the Airflow CLI command for listing connections is `airflow connections list`. To run this command with the Astro CLI, you would run `astro dev run connections list` instead.

In practice, running `astro dev run` is the equivalent of running `docker exec` in local containers and then running an Airflow CLI command within those containers.

:::tip

You can only use `astro dev run` in a local Airflow environment. To automate Airflow actions on Astro, you can use the [Airflow REST API](airflow-api.md). For example, you can make a request to the [`dagRuns` endpoint](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) to trigger a DAG run programmatically, which is equivalent to running `airflow dags trigger` in the Airflow CLI.

:::

## Troubleshoot KubernetesPodOperator issues

View local Kubernetes logs to troubleshoot issues with Pods that are created by the operator. See [Test and Troubleshoot the KubernetesPodOperator Locally](kubepodoperator-local.md#step-4-view-kubernetes-logs).

## Hard reset your local environment

In most cases, [restarting your local project](develop-project.md#restart-your-local-environment) is sufficient for testing and making changes to your project. However, it is sometimes necessary to kill your Docker containers and metadata database for testing purposes. To do so, run the following command:

```sh
astro dev kill
```

This command forces your running containers to stop and deletes all data associated with your local Postgres metadata database, including Airflow connections, logs, and task history.

## Troubleshoot common issues

Use the information provided here to resolve common issues with running an Astro project in a local environment.

### New DAGs aren't visible in the Airflow UI

By default, the Airflow scheduler scans the DAGs directory for new files every 300 seconds (5 minutes). For this reason, it might take a few minutes for DAGs to appear in the Airflow UI.

To have the scheduler check for DAGs more frequently, you can set the `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` environment variable to less than 300 seconds. This setting is dependent on the amount of CPU that is allocated to the scheduler. The greater the CPU allocation, the faster the scheduler can parse your DAGs.

### DAGs are running slowly

If your Astro project contains many DAGs or tasks, then you might experience performance issues in your local Airflow environment.

To improve the performance of your environment, you can:

 - Adjust CPU and memory resource allocation in your Docker resources configuration. Be aware that increasing Docker resource allocation might decrease the performance of your computer.
- Modify Airflow-level environment variables to improve the performance of your local environment, including concurrency and parallelism. See  [Scaling out Airflow](https://www.astronomer.io/guides/airflow-scaling-workers).

If your DAGs continue to run slowly and you can't scale Docker or Airflow any further, Astronomer recommends pushing your project to a Deployment on Astro that's dedicated to testing.

### Astro project won't load after `astro dev start`

If your Astro project fails to run in an Airflow environment more than 5 minutes after running `astro dev start`, it might be because your webserver or scheduler is unhealthy. In this case, you might need to debug your containers. To do so:

1. After running `astro dev start`, retrieve a list of running containers by running `astro dev ps`.
2. If the webserver and scheduler containers exist but are unhealthy, check their logs by running:

    ```sh
    $ astro dev logs --webserver
    $ astro dev logs --scheduler
    ```

These logs should help you understand why your webserver or scheduler is unhealthy. Possible reasons why these containers might be unhealthy include:

- Not enough Docker resources.
- Broken Postgres database.
- DAG code errors.
- Misconfigured Dockerfile or Docker override file.
- Misconfigured Airflow settings.
