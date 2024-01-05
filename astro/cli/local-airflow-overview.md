---
sidebar_label: 'Overview'
title: 'Local Airflow overview'
id: local-airflow-overview
description: Work with your Astro project in a local environment by running Airflow and DAGs locally.
---

Running Airflow locally with the Astro CLI lets you preview and debug DAG changes before deploying to production. In a local Airflow environment, you can fix issues with your DAGs without consuming infrastructure resources or waiting on code deploy processes. 

To run Airflow locally, the Astro CLI creates and runs containers for core Airflow components. It uses Docker by default to orchestrate these containers, but you can also use [Podman](cli/configure-cli.md#run-the-astro-cli-using-podman). All tasks run locally in the scheduler container using the [local executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local.html).

See the following documentation to get started:

- [Run Airflow locally](cli/run-airflow-locally.md)
- [Test your DAGs](cli/test-your-astro-project-locally.md)
- [Trouleshoot locally](cli/troubleshoot-locally.md)

## Sync connection details

When you set connections using the [Astro Environment Manager](create-and-link-connections.md), you can easily use them in your local environment to test your DAGs and deployment settings without having to manage access credentials in multiple environments. You can configure the Astro CLI can automatically [sync your Deployment connection credentials](cli/local-connections.md) with your local project.

Unlike importing or exporting connections and variables, using Astro Connections locally doesn't require you to manually store or manage your connection details.

- [Use Astro connections locally](cli/local-connections.md)