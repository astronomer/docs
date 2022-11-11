---
sidebar_label: "astro dev pytest"
title: "astro dev pytest"
id: astro-dev-pytest
description: Reference documentation for astro dev pytest.
hide_table_of_contents: true
---

Run unit tests for your data pipelines on Astro with `pytest`, a testing framework for Python. When you run this command, the Astro CLI creates a local Python environment that includes your DAG code, dependencies, and Astro Runtime Docker image. The CLI then runs any pytests in the `tests` directory of your Astro project and shows you the results of those tests in your terminal.

For more information on this functionality, see [Test and troubleshoot locally](test-and-troubleshoot-locally.md).

:::info

This command requires Astro Runtime version `4.1.0`+. For more information, see [Astro Runtime Release Notes](https://docs.astronomer.io/astro/runtime-release-notes#astro-runtime-410).

:::

## Usage

```sh
astro dev pytest
```

## Options

| Option               | Description                                                                                                                                           | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `<pytest-filepath>`  | The filepath to an alternative pytest file or directory. Must be within the `tests` directory                                                         | Any valid filepath within the `tests` directory                  |
| `-e`, `--env`        | The filepath to your environment variables. The default is `.env`)                                                                                    | Any valid filepath within your Astro project                     |
| `-i`, `--image-name` | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine | A valid name for a pre-built Docker image based on Astro Runtime |

## Examples

```sh
$ astro dev pytest --env=myAlternativeEnvFile.env
# Specify env file at root of Astro project
```

## Related Commands

- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev start`](cli/astro-dev-start.md)
- [`astro deploy`](cli/astro-deploy.md)
