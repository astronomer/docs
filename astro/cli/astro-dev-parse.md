---
sidebar_label: "astro dev parse"
title: "astro dev parse"
id: astro-dev-parse
description: Parse the DAGs to check for errors in a local Airflow environment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

The behavior and format of this command are the same for both Astro and Software.

:::

Parse the DAGs in a locally hosted Astro project to quickly check them for errors. For more information about testing DAGs locally, read [Test your Astro project locally](cli/test-your-astro-project-locally.md).

## Usage

```sh
astro dev parse
```

## Options

| Option               | Description                                                                                                                                           | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `--build-secrets` | Run `docker build --secret` to mount a secret value to your Docker image. | `id=<your-secret-id>, src=<path-to-secret> .` See [Docker documentation](https://docs.docker.com/build/building/secrets/#secret-mounts). |
| `-e`, `--env`        | The filepath to your environment variables. (The default is `.env`)                                                                                   | Any valid filepath within your Astro project                     |
| `-i`, `--image-name` | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine | A valid name for a pre-built Docker image based on Astro Runtime |

## Examples

```sh
# Parse DAGs
astro dev parse

# Specify alternative environment variables
astro dev parse --env=myAlternativeEnvFile.env
```

## Related Commands

- [`astro dev pytest`](cli/astro-dev-pytest.md)
- [`astro dev start`](cli/astro-dev-start.md)
- [`astro deploy`](cli/astro-deploy.md)
