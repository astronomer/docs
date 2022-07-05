---
sidebar_label: "astro dev parse"
title: "astro dev parse"
id: astro-dev-parse
description: Reference documentation for astro dev parse.
---

Parse the DAGs in a locally hosted Astro project to quickly check them for errors. For more information about testing DAGs locally, read [Run Tests with the Astro CLI](test-and-troubleshoot-locally.md#run-tests-with-the-astro-cli).

## Usage

```sh
astro dev parse
```

## Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-e`, `--env`       | The filepath to your environment variables. (The default is `.env`)                            | Any valid filepath within your Astro project    |

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
