---
sidebar_label: "astro dev run"
title: "astro dev run"
id: astro-dev-run
description: Reference documentation for astro dev run.
hide_table_of_contents: true
---

Run [Airflow CLI commands](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) in your local Airflow environment. This command is for local development only and cannot be applied to Deployments running on Astro.

## Usage

```sh
astro dev run <airflow-command>
```

## Examples

```sh
$ astro dev run users create --role Admin --username admin --email <your-email-address> --firstname <your-first-name> --lastname <your-last-name> --password admin
# Create a user in your local Airflow environment using the `airflow user create` Airflow CLI command

$ astro dev run connections export - --file-format=env --serialization-format=json
# Export connections in your local Airflow environment to STDOUT in a JSON format 

$ astro dev run connections export - --file-format=env
# Export connections in your local Airflow environment to STDOUT in the default URI format
```

## Related Commands

- [`astro dev logs`](cli/astro-dev-logs.md)
- [`astro dev ps`](cli/astro-dev-ps.md)
