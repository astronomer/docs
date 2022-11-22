---
sidebar_label: "astro run"
title: "astro run"
id: astro-run
description: Reference documentation for astro run.
hide_table_of_contents: true
---

Run a single DAG in a local Airflow environment and see task success or failure in your terminal. This command compiles any DAG file in your Astro project into a Docker container that is built from your local `Dockerfile`. It runs with the utility files, python packages, and environment variables from the `.env` file. 

This command works with or without your local Airflow environment running. The scheduler and webserver are not required. For more information, see [Run and Debug DAGs with Astro Run](test-and-troubleshoot-locally.md#run-and-debug-dags-with-astro-run).

## Usage

```sh
astro run <dag-id>
```

## Options

| Option          | Description                   | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `-e`,`--env`         | Path to your environment variable file. The default is `.env`.                                                                                             | Any valid filepath                                                  |
| `--no-cache`         | Build your Astro project into a Docker image without using cache.                  | None                                                             |
| `-s`, `--settings-file` | The settings file from which Airflow objects are imported. The default is `airflow_settings.yaml`. | Any valid path to an Airflow settings file                           |

## Examples

```sh
$ astro run example_dag_basic --env dev.env
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro deploy`](cli/deploy.md)