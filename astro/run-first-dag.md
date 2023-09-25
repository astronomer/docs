---
sidebar_label: "Run your first DAG"
title: "Choose how to run your first DAG on Astro"
id: "run-first-DAG"
---

<head>
  <meta name="description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI or through GitHub Actions." />
  <meta name="og:description" content="Learn how to run your first Apache Airflow DAG on Astro with the Astro CLI or through GitHub Actions." />
</head>

Astro is the industry's leading managed service for Apache Airflow.

You can quickly learn how Astro works by running an Apache Airflow DAG with either [the Astro CLI](first-DAG-CLI.md) or by using [GitHub Actions](first-DAG-github-actions.md).

Either tutorial takes about 15 minutes. They each showcase different paths available for DAG development, CI/CD workflows, and code deployment options. You'll learn how to:

- Authenticate and log in to Astro.
- Create a Deployment.
- Deploy DAGs to Astro with the Astro CLI.
- Trigger a run of an example DAG in the Airflow UI.

If you're new to Airflow and want a more in-depth tutorial, see [Write your First DAG](https://docs.astronomer.io/learn/get-started-with-airflow).

## Compare your options

| ----------------------------------- | Astro CLI                                           | GitHub Actions                                                                 |
| ----------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Local software installs required    | Yes, you need to install the Astro CLI.             | No, you do not need to install anything.                                       |
| Explore how to develop locally      | Yes, the Astro CLI creates a local Airflow project. | No, GitHub Actions follows remote deployment workflows.                        |
| Try a CI/CD workflow                | No, this uses DAG only deploys.                     | Yes, you can use GitHub Actions for automated DAG deploys in a CI/CD pipeline. |

## Next Steps

- [Run your first DAG with GitHub Actions](first-DAG-github-actions.md)
- [Run your first DAG with the Astro CLI](first-dag-cli.md)
- [Install the CLI](astro/cli/install-cli.md)
