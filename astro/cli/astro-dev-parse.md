---
sidebar_label: "astro dev parse"
title: "astro dev parse"
id: astro-dev-parse
description: Reference documentation for astro dev parse.
hide_table_of_contents: true
---

Parse the DAGs in a locally hosted Astro project to quickly check them for errors. For more information about testing DAGs locally, read [Test your Astro project locally](cli/test-your-astro-project-locally.md#run-tests-with-the-astro-cli).

## Usage

```sh
astro dev parse
```

## Options

| Option               | Description                                                                                                                                           | Possible Values                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
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
