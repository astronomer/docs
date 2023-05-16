---
sidebar_label: "astro dev object export"
title: "astro dev object export"
id: astro-dev-object-export
description: Reference documentation for astro dev object export
---

Export Airflow variables, connections, and pools from a locally running environment to a local file and format of your choice. By default, the command exports all Airflow objects to the `airflow_settings.yaml` file in your Astro project.

## Usage 

After starting your local Airflow environment with `astro dev start`, run:

```sh
astro dev object export
```

By default, the command exports all variables, connections, and pools as YAML configurations to `airflow_settings.yaml`.

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `--compose` | Export the Compose file used to start Airflow locally.                                                                          |                |
| `--compose-file`            | The location to export the Compose file used to start Airflow locally. (default `compose.yaml`)                                 | Any valid filepath              |
| `-c`,`--connections` | Export connections to a given local file | ``|
| `-e`,`--env`            | Location of the file to export Airflow objects to as Astro environment variables. Use this option only with `--env-export`. The default file path is `env`.                                                                          | Any valid filepath                 |
| `-n`,`--env-export`            | Export Airflow objects as Astro environment variables.                                                                                  | ``                 |
| `-p`,`--pools`            | Export pools to a given local file | ``                 |
| `-s`,`--settings-file`            | Location of the file to export Airflow objects to as YAML configuration. The default file path is `airflow_settings.yaml`.                                 | Any valid filepath              |
| `-v`,`--variables`            | Export variables to a given local file | ``                 |

## Examples 

```sh
astro dev object export --pools 
# Exports only pools from the local Airflow environment to `airflow_settings.yaml`

astro dev object export --env-export --env="myairflowenv.env"
# Exports all Airflow objects from the local Airflow environment as 
# Astro variables to a file in the project named `myairflowenv.env`
```

## Related commands 

- [`astro dev object import`](cli/astro-dev-object-import.md)
- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)