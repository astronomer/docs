---
sidebar_label: "astrocloud dev run"
title: "astrocloud dev run"
id: astrocloud-dev-run
description: Reference documentation for astrocloud dev run.
---

## Description

Run [Airflow CLI commands](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) in your local Airflow environment. This command is for local development only and cannot be applied to Deployments running on Astro.

## Usage

```sh
astrocloud dev run <airflow-command>
```

## Examples

```sh
$ astrocloud dev run users create --role Admin --username admin --email <your-email-address> --firstname <your-first-name> --lastname <your-last-name> --password admin
# Create a user in your local Airflow environment using the `airflow user create` Airflow CLI command
```

## Related Commands

- [`astrocloud dev logs`](cli-reference/astrocloud-dev-logs.md)
- [`astrocloud dev ps`](cli-reference/astrocloud-dev-ps.md)
