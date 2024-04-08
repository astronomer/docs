---
sidebar_label: 'Overview'
title: 'Write and run DAGs on Astro'
id: dags-overview
description: Learn about how developing DAGs to run on Astro is different from other platforms.
---

Astro includes several features that enhance the Airflow development experience, from DAG creation to testing. Use this documentation to learn about all of the key differences between development on Astro and other platforms. 

## Project structure

To develop and run DAGs on Astronomer products, they must belong to an Astro project. An _Astro project_ contains all files required to run your DAGs both locally and on Astronomer. In addition to DAG files, an Astro project includes dependencies, your Astro Runtime version, and any other files your workers need access to when you run tasks.

See [Create an Astro project](cli/get-started-cli.md) to learn more about how to create and run Astro projects.

## Apache Airflow/ Astro Runtime versioning

Each Astro project uses a specific version of Astro Runtime, which is Astronomer's version of Apache Airflow that includes additional observability and performance features. As you continue to develop within an Astro project, you'll need to upgrade your Astro Runtime version to take advantage of new Astro and Apache Airflow features and fixes. 

Your Astro Runtime version is defined in your Astro project Dockerfile. Unlike Apache Airflow, upgrading Astro Runtime does not require manually migrating your metadata database. To upgrade your version of Airflow, you change the Astro Runtime version listed in your project Dockerfile and rebuild your project. See [Upgrade Astro Runtime](upgrade-runtime.md).

Your Dockerfile is also where you can define additional runtime arguments that trigger whenever your project builds. You can use these arguments to mount resources, such as API tokens, to your Airflow environment without including the specific resources in your project files. See [Customize your Dockerfile](cli/customize-dockerfile.md) for more details.

## Testing environments

You can run your DAGs in several different environments across the Astro ecosystem. Each has its own purpose in the development lifecycle. 

- **Local Airflow environment**: You can run DAGs on your local machine using the Astro CLI. This development method is most useful if you need to quickly iterate and test changes, such as when fixing a bug, or you're just getting started with Airflow. Testing locally is free, open source, and does not require an internet connection.
- **Deployment**: When you deploy your DAGs to Astro, they run on a managed Deployment. Use Deployments to run production code, or create a development Deployment to test changes over a longer period of time than you could in a local Airflow environment. To test code on a Deployment, you must have an [Astro account](log-in-to-astro.md), and an administrator on your team must grant you access to the Deployment. For more information about how to structure Deployments for specific development workflows, see [Connections and branch-based deploys](best-practices/connections-branch-deploys.md).

### Unit tests

Whether you're building your project locally or deploying to Astro, you can run unit tests with the Astro CLI to ensure that your code meets basic standards before you run your DAGs. See [Test your DAGs](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally) for more information.

## DAG feature integrations

Astro includes several features that enhance existing Airflow features and integrate them with the Astro UI. 

- On Astro, the Astro UI renders [Airflow tags](https://airflow.apache.org/docs/apache-airflow/stable/howto/add-dag-tags.html) defined in your DAGs. Use tags to filter DAGs across all Deployments from a single screen.
- The [Astro Environment Manager](manage-connections-variables.md) allows you to manage Airflow connections directly from the Astro UI. Unlike with connections defined in the Airflow UI, you can apply connections from the Environment Manager across multiple Deployments and Workspaces, as well as in a local Airflow environment. 
- Astro has built-in infrastructure to run the KubernetesPodOperator and Kubernetes executor, such as default Pod limits and requests. Resource limits and requests are set by default on Astro Deployments, meaning that tasks running in Kubernetes Pods never request more resources than expected. See [Run the Kubernetes executor](kubernetes-executor.md) and [Run the KubernetesPodOperator](kubernetespodoperator.md) for more specific instructions and examples. 

## DAG observability

In local Airflow environments, you can use the Airflow UI to check your DAG runs, task logs, and component logs just as you would in any other Airflow environment.

On Astro, in addition to the Airflow UI, you have access to the **DAGs** page. From here, you can manage DAG and task runs for any Deployment in your Workspace. See [View logs](view-logs.md) [Manage DAG runs](manage-dags.md) for more information.

Astro includes additional features for alerting on specific DAG status, such as Astro alerts. There are some circumstances where Astronomer recommends configuring Astro alerts instead of Airflow SLAs or failure notifications. See [When to use Airflow or Astro alerts for your pipelines on Astro](best-practices/airflow-vs-astro-alerts.md).

## Astro open source packages

Although they are not built into Astro, Astronomer's open source packages are recommended to simplify your Airflow pipelines.

### Orchestrate dbt Core projects using Cosmos

[Cosmos](https://www.astronomer.io/cosmos/) is Astronomer's open source tool for orchestrating dbt Core projects from a DAG. It gives you more visibility into every step of your dbt project and lets you use Airflow's data awareness features with your dbt models. See the [Cosmos documentation](https://astronomer.github.io/astronomer-cosmos/) for more information.

### Simplify data transformations using the Astro SDK

The Astro SDK is a set of functions that you can use to templatize DAGs and simplify SQL queries to a number of popular databases such as Snowflake, Redshift, and Postgres. The SDK abstracts boilerplate code for passing data between tasks so that you don't have to consider the format of your data as you move it between different systems. See the [Astro SDK getting started tutorial](https://docs.astronomer.io/learn/astro-python-sdk) for more information.