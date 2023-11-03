---
sidebar_label: "astro dev start"
title: "astro dev start"
id: astro-dev-start
description: Build your Astro project and start a local Airflow environment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Build your Astro project into a Docker image and spin up a local Docker container for each Airflow component.

This command can be used to build an Astro project and run it locally. For more information, see [Build and run a project locally](cli/develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev start
```

## Options

| Option          | Description                   | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `--compose-file`            | The location of a custom Docker Compose file to use for starting Airflow on Docker.                           | Any valid filepath              |
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

:::info

The following error can sometimes occur when the CLI tries to build your Astro Runtime image using Podman:

```bash
WARN[0010] SHELL is not supported for OCI image format, [/bin/bash -o pipefail -e -u -x -c] will be ignored. Must use `docker` format 
```
You can resolve this issue by exporting the `BUILDAH_FORMAT` [environment variable](astro/environment-variables.md) to Podman:

```dockerfile
export BUILDAH_FORMAT=docker
```
:::

## Related Commands

- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
