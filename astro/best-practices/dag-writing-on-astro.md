---
title: 'DAG writing on Astro'
sidebar_label: 'DAG writing on Astro'
id: dag-writing-on-astro
---

You can run any valid Airflow DAG on Astro. 

That said, following best practices and taking full advantage of Astro features will help you:

- Write DAGs more efficiently.
- Improve your development workflow.
- Better organize your deployment and DAGs. 
- Optimize resource usage and task execution efficiency.

This guide describes best practices for taking advantage of Astro features when writing DAGs. While this focuses on writing Airflow DAGs for Astro, all [general Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) are also recommended.

:::info New to Airflow?

If you are new to Airflow, Astronomer suggests starting with the following resources:

- Hands-on tutorial: [Get started with Apache Airflow](https://docs.astronomer.io/learn/get-started-with-airflow).
- Astronomer Academy: [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).
- Webinar: [Airflow 101: How to get started writing data pipelines with Apache Airflow](https://www.astronomer.io/events/webinars/airflow-101-how-to-get-started-writing-data-pipelines-with-apache-airflow-video/).

:::

## Feature overview

In this guide, you'll learn about a number of Astro and Airflow features for optimizing your DAGs for Astro:

- [Astro Cloud IDE](https://docs.astronomer.io/astro/cloud-ide). A low-code, notebook-inspired IDE for writing and testing pipelines on Astro.
- [Astro CLI](overview.md). An OSS tool for developing DAGs and deploying projects tailor-made for Astro.
- [Worker queues](configure-worker-queues.mdx). A feature of Astro that enables resource optimization beyond what is possible using OSS Airflow.
- [Astro Cloud UI Environment Manager](manage-connections-variables.md). A tool for managing connections across multiple deployments locally and on Astro.
- [Astro alerts](alerts.md). No-code alerting on Astro configurable for various trigger types and communication channels.

## Best practice guidance

The guidance in this section is split into two categories: writing DAG code for Astro and managing DAG code on Astro.

### Writing DAG code for Astro

Astro users have options when it comes to developing DAGs: the Astro Cloud IDE or the Astro CLI. The Astro Cloud IDE is a low-code, cloud-based solution that does not require installing any software. It is recommended for new Airflow users or those who cannot install the Astro CLI or its prerequisites. The Astro CLI is recommended for those who want to develop code locally in a containerized setup using their preferred IDE. It is especially useful for those migrating existing DAGs to Astro.

#### Use the Astro Cloud IDE for secure, low-code development in the cloud

One of the highest barriers to using Airflow is writing boilerplate code for basic actions such as creating dependencies, passing data between tasks, and connecting to external services. If your team prefers a low-code option, the Cloud IDE conveniently enables you to set up these actions with the Astro UI and create pipelines by writing a minimal amount of Python or SQL code rather than entire DAGs.

To get the most out of the Astro Cloud IDE:

- Connect a Git repository for deployment of your pipelines using the [Astro GitHub integration](https://www.astronomer.io/docs/astro/deploy-github-integration). Deployment using the Astro CLI is also supported, but the GitHub integration offers advantages such as easy enforcement of software development best practices without custom CI/CD scripts, faster iteration on DAG code for teams, and greater visibility into the status and logs of individual deploys. For detailed guidance on deploying Cloud IDE pipelines, see [Deploy a project from the Cloud IDE to Astro](https://www.astronomer.io/docs/astro/cloud-ide/deploy-project).
- Make sure to [export](https://www.astronomer.io/docs/astro/cloud-ide/deploy-project#export-your-pipelines-to-a-local-astro-project) and test locally any DAGs employing async operators and sensors prior to deployment. Although supported, async operators and task sensors cannot currently be tested in the Cloud IDE.

Learn more and get started by following the guidance in [Cloud IDE](https://www.astronomer.io/docs/astro/cloud-ide).

#### Use the Astro CLI for local development

When writing DAGs intended for Astro Deployments, use the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) for containerized local development. The Astro CLI is an open-source interface you can use to:

- Test Airflow DAGs locally.
- Deploy code to Astro.
- Automate key actions as part of a CI/CD process. 

To get the most out of the Astro CLI: 

- Use the `dags` directory to store your DAGs. If you have multiple DAGs, you can use subdirectories to keep your environment organized.
- Modularize your code and store all supporting classes, files and functions in the `include` directory.
- Store all your [tests](#follow-devops-best-practices) in the `tests` directory.

:::tip

If you are unable to install the Astro CLI on your local machine, due to company policy or for other reasons, you can use it in GitHub Codespaces by forking the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

:::

Learn more and get started by following the guidance in [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).

### Managing DAG code on Astro

Compared to open-source Airflow, Astro offers a distinct feature set for optimizing your Airflow pipelines. Some of these features impact individual DAGs, and you should consider them not only when writing new DAG code but also when migrating DAGs to Astro. You don't need to make changes to existing DAGs when you migrate them, but by implementing some small changes you can get access to an upgraded experience when it comes to managing connections, defining and storing environment variables, allocating resources, and implementing alerts.

Making use of the following features can require DAG code changes or adding Airflow configuration environment variables in Astro instead of Airflow. Astronomer recommends considering these features during DAG development to streamline the development process and make use of everything Astro has to offer.

- **[Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables)** for managing connections. This allows you to define connections once and use them in multiple deployments (with or without overrides for individual fields), as well as in your local development environment. Connections in the Environment Manager are stored in the Astronomer managed secrets backend. Using the Environment Manager requires adding the relevant Airflow provider packages to your Astro project and adding configuring the connection in the Astro UI.
- **[Deployment environment variables in the Astro UI](environment-variables.md)** for storing environment variables. Common uses of environment variables include adding tokens or URLs required by your DAGs, integrating with third-party tooling to export metrics, customizing core settings of Airflow or Airflow Providers, and storing Airflow connections and variables. A number of approaches are supported. For example, you can mark variables as secret for storage in the Astronomer managed secrets backend. You can store [Airflow variables](https://docs.astronomer.io/learn/airflow-variables), which are Airflow native key-value pairs, as environment variables as well by using the format `AIRFLOW_VAR_MYVARIABLENAME`. You can also manage environment variables using your Astro project Dockerfile and, locally, your project `.env` file. Astro project modification and additional configuration in Astro may be required depending on the strategy chosen.
- **[Worker queues](https://docs.astronomer.io/astro/configure-worker-queues)** for optimizing task execution efficiency. Worker queues allow you to define sets of workers with specific resources that execute tasks in parallel. You can assign tasks to specific worker queues to optimize resource usage. This feature is an improvement over OSS Airflow pools, which only manage concurrency and not resources. You can use both worker queues and pools in combination. Config in Astro and DAG code modification are required to use this feature.
- **[Astro Alerts](alerts.md)** for setting up alerts for your DAGs. Astro alerts add another level of observability to Airflow's notification systems. For example, you can configure an alert to notify you in Slack when a DAG run completes or fails. Unlike Airflow callbacks and SLAs, Astro alerts require no changes to DAG code. For more information, see [When to use Airflow or Astro alerts for your pipelines on Astro](airflow-vs-astro-alerts.md). Config in the Astro UI required.

## See also

- Webinar: [Best practices for managing Airflow across teams](https://www.astronomer.io/events/webinars/best-practices-for-managing-airflow-across-teams-video/).
- Webinar: [DAG writing for data engineers and data scientists](https://www.astronomer.io/events/webinars/dag-writing-for-data-engineers-and-data-scientists-video/).
- OSS Learn guide: [DAG writing best practices in Apache Airflow](https://docs.astronomer.io/learn/dag-best-practices).
