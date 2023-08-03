---
sidebar_label: "astro run"
title: "astro run"
id: astro-run
description: Reference documentation for astro run.
hide_table_of_contents: true
---

Trigger a single DAG run in a local Airflow environment and see task success or failure in your terminal. This command compiles your DAG and runs it in a single Airflow worker container based on your Astro project configurations.

For more information, see [Run a DAG with Astro Run](test-and-troubleshoot-locally.md#run-a-dag-with-astro-run).

## Usage

```sh
astro run <dag-id>
```

 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, %Y-%m-%d %H:%M:%S"

## Options

| Option                  | Description                                                                                                                                 | Possible Values                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `-d`, `--dag-file` | The location of your DAG file. When you specify this flag, only the specified DAG is parsed by the Astro CLI. All other DAGs in the project are ignored.| Any valid DAG file in your `dags` directory. |
| `--execution-date`            | The execution date for the DAG run.                                      | An execution date formatted as either `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS`. or `YYYY-MM-DD HH:MM:SS`.                        |
| `-e`,`--env`            | Path to an alternative environment variable file. The default is `.env` in your current Astro project.                                      | Any valid filepath.                         |
| `--no-cache`            | Build your Astro project into a Docker image without using cache.                                                                           | None.                                       |
| `-s`, `--settings-file` | An alternative settings file from which Airflow objects are imported. The default is `airflow_settings.yaml` in your current Astro project. | Any valid filepath. |

## Examples

```sh
# Run a DAG with an alternative set of environment variables
$ astro run example_dag_basic --env dev.env
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro deploy`](cli/astro-deploy.md)