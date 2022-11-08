---
sidebar_label: "astro dev start"
title: "astro dev start"
id: astro-dev-start
description: Reference documentation for astro dev start.
hide_table_of_contents: true
---

Build your Astro project into a Docker image and spin up a local Docker container for each Airflow component.

This command can be used to rebuild an Astro project and run it locally. For more information, read [Build and run a project locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev start
```

## Options

| Option          | Description                   | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `-e`,`--env`         | Path to your environment variable file. Default is `.env`                                                                                             | Valid filepaths                                                  |
| `-i`, `--image-name` | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine | A valid name for a pre-built Docker image based on Astro Runtime |
| `-n`, `--no-browser` | Starts a local Airflow environment without opening a web browser for the Airflow UI      | None                                                             |
| `--no-cache`         | Do not use cache when building your Astro project into a Docker image                   | None                                                             |
| `-s`, `--settings-file` | Settings file from which to import Airflow objects. Default is `airflow_settings.yaml`. | Any valid path to an Airflow settings file                           |
| `--wait`                | Amount of time to wait for the webserver to get healthy before timing out. The default is 1 minute for most machines and 5 minutes for Apple M1 machines. | Time in minutes defined as `<integer>m` and time in seconds defined as `<integer>s` |


## Examples

```sh
$ astro dev start --env=/users/username/documents/myfile.env
```

## Related Commands

- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
