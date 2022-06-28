---
sidebar_label: 'Overview'
title: 'Astro CLI'
id: overview
description: Learn about every command that you can run with the Astro CLI.
---

## Run Airflow locally

The Astro CLI is the command line interface for data orchestration. It's the easiest way to get started with [Apache Airflow](https://airflow.apache.org/) and can be used with all Astronomer products.

The Astro CLI is open source and built for data practitioners everywhere. The binary is maintained in the public [Astro CLI GitHub repository](https://github.com/astronomer/astro-cli), where pull requests and GitHub issues are welcome.

## Get started

Follow [Get started](get-started.md) to install the CLI and run your first Astro project locally.

## Features

Specifically, the Astro CLI includes:

- A built-in Astro project directory that includes all the files required to run Airflow, including dedicated folders for your DAGs, packages, and unit tests.
- Commands to enhance the local development experience. Using the CLI, you can run a local Airfow environment, apply code changes, and view logs for all Airflow components.
- A set of example pytests and example DAGs that showcase important Airflow best practices and can help your team learn quickly and identify errors in your DAGs ahead of time.
- Easy and secure browser-based authentication for Astro and Astronomer Software.
- A robust set of commands to match functionality in the Cloud UI, including commands to create a Deployment and modify environment variables.
- Support for Deployment API keys, which you can use to automate commands as part of CI/CD workflows.

To stay up to date on the latest features, see [Astro CLI Release Notes](cli/release-notes.md).

## CLI reference

For a full list of available CLI commands, see the [CLI command reference](cli/reference.md).
