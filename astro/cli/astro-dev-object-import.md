---
sidebar_label: "astro dev object import"
title: "astro dev object import"
id: astro-dev-object-import
description: Import Airflow objects from configuration file to local Airflow.
---

Import Airflow variables, connections, and pools from a configuration file to a locally running Airflow environment. 

## Usage 

After starting your local Airflow environment with `astro dev start`, run:

```sh
astro dev object import
```

By default, the command imports all variables, connections, and pools from `airflow_settings.yaml` to your project. You do not need to restart your environment for these changes to take effect. 

## Options

| Option              | Description                                                                                                        | Possible Values             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| `-c`,`--connections` | Import connections from a given local file | ``|                                                                      
| `-p`,`--pools`            | Import pools from a given local file | ``                 |
| `-s`,`--settings-file`            | Location of the file from which to import Airflow objects. The default file path is `~/.airflow_settings.yaml`.                                 | Any valid filepath              |
| `-v`,`--variables`            | Import variables from a given local file | ``                 |


## Examples 

```sh
astro dev object import --pools 
# Imports pools from `airflow_settings.yaml` to a locally running Airflow environment

astro dev object import --settingsfile="myairflowobjects.yaml"
# Imports all Airflow objects from `myairflowobjects.yaml` to a locally running Airflow environment
```

## Related commands 

- [`astro dev object export`](cli/astro-dev-object-export.md)
- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)