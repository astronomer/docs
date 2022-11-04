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
| `-n`, `--no-browser` | Starts Airflow without opening a browser for the Airflow UI      | None                                                             |
| `--no-cache`         | Do not use cache when building container image                   | None                                                             |
| `-s`, `--settings-file` | Settings file to import airflow objects from (default "airflow_settings.yaml") | airflow settings file                           |
| `--wait`                | Duration to wait for webserver to get healthy. The default is 5 minutes on M1 architecture and 1 minute for everything else. Use --wait 2m to wait for 2 minutes. (default 1m0s) | time in seconds |


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
