---
sidebar_label: 'Work locally'
title: 'Run your Astro project locally'
id: work-locally
description: Work with your Astro project in a local environment by running Airflow and DAGs locally.
---

Running Airflow locally with the Astro CLI can be an easy way to preview and debug DAG changes quickly before deploying your code to Astro. By locally running your DAGs, you can fix issues with your DAGs without consuming infrastructure resources or waiting on code deploy processes.

- [Run Airflow locally](cli/run-airflow-locally.md)
- [Test your DAGs](cli/test-your-astro-project-locally.md)
- [Trouleshoot locally](cli/troubleshoot-locally.md)

## Sync connection details

When you set connections using the [Astro Environment Manager](create-and-link-connections.md), you can easily use them in your local environment to test your DAGs and deployment settings without having to manage access credentials in multiple environments. You can configure the Astro CLI can automatically [sync your Deployment connection credentials](cli/local-connections.md) with your local project.

Unlike importing or exporting connections and variables, using Astro Connections locally doesn't require you to manually store or manage your connection details.

- [Use Astro connections locally](cli/local-connections.md)