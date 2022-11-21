---
sidebar_label: "astro run"
title: "astro run"
id: astro-run
description: Reference documentation for astro run.
hide_table_of_contents: true
---

Compile an run a DAG with only the command line. `astro run`will run your DAGs within a Docker container bulit from your local `Dockerfile` containing your DAGs, DAG utility files, python requirments, and env vars from your `.env` file. 

This command works both with and without your local Airflow project running. For more information read [Run and Debug DAGs with Astro Run](test-and-troubleshoot-locally.md#run-and-debug-dags-with-astro-run).

## Usage

```sh
astro run <dag-id>
```

## Options

| Option          | Description                   | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `-e`,`--env`         | Path to your environment variable file. Default is `.env`                                                                                             | Valid filepaths                                                  |
| `--no-cache`         | Do not use cache when building your Astro project into a Docker image                   | None                                                             |
| `-s`, `--settings-file` | Settings file from which to import Airflow objects. Default is `airflow_settings.yaml`. | Any valid path to an Airflow settings file                           |

## Examples

```sh
$ astro run example_dag_basic --env dev.env
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro deploy`](cli/deploy.md)