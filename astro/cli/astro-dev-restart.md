---
sidebar_label: "astro dev restart"
title: "astro dev restart"
id: astro-dev-restart
description: Restart a local Airflow environment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Stop your Airflow environment, rebuild your Astro project into a Docker image, and restart your Airflow environment with the new Docker image.

This command can be used to rebuild an Astro project and run it locally. For more information, read [Build and run a project locally](develop-project.md#build-and-run-a-project-locally).

## Usage

```sh
astro dev restart
```

## Options

| Option               | Description                                                                                                                                           | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `-e`,`--env`         | Path to your environment variable file. Default is `.env`                                                                                             | Valid filepaths                                                  |
| `-i`, `--image-name` | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine | A valid name for a pre-built Docker image based on Astro Runtime |


## Examples

```sh
$ astro dev restart --env=/users/username/documents/myfile.env
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro dev kill`](cli/astro-dev-kill.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev logs`](cli/astro-dev-logs.md)
