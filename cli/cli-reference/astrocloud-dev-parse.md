---
sidebar_label: "astrocloud dev parse"
title: "astrocloud dev parse"
id: astrocloud-dev-parse
description: Reference documentation for astrocloud dev parse.
---

## Description

Parse the DAGs in a locally hosted Astro project to quickly check them for errors. For more information about testing DAGs locally, read [Run Tests with the Astro CLI](test-and-troubleshoot-locally.md#run-tests-with-the-astro-cli).

## Usage

```sh
astrocloud dev parse
```

## Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-e`, `--env`       | The filepath to your environment variables. (The default is `.env`)                            | Any valid filepath within your Astro project    |

## Examples

```sh
# Parse DAGs
astrocloud dev parse

# Specify alternative environment variables
astrocloud dev parse --env=myAlternativeEnvFile.env
```

## Related Commands

- [`astrocloud dev pytest`](cli-reference/astrocloud-dev-pytest.md)
- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud deploy`](cli-reference/astrocloud-deploy.md)
