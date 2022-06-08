---
sidebar_label: 'Astro Runtime Architecture'
title: 'Astro Image Architecture'
id: runtime-image-architecture
description: Reference documentation for Astro Runtime, Astronomer Software's Docker image for Apache Airflow.
---

Astro Runtime is a Debian-based, production-ready distribution of Apache Airflow. The Astro Runtime image is intended to provide organizations improved functionality, reliability, efficiency, and performance.

Astro Runtime Docker images are hosted on the Astronomer Docker registry and enable Airflow on Astro. All Astro projects require that you specify an Astro Runtime image in your Dockerfile, and all Deployments on Astro must run only one version of Astro Runtime. Every version of Astro Runtime correlates to one version of Apache Airflow. Depending on the needs of your organization, you can run different versions of Astro Runtime on different Deployments within a given Workspace or Cluster.

## Astro Runtime Advantages

If your organization is using Software version 0.29 or later, you can use Astro Runtime images in your Software Deployments. Astro Runtime images include the following features that are not available in Astronomer Certified images:

- The `astronomer-providers` package, which includes a set of deferrable operators created and maintained by Astronomer.
- Airflow UI improvements. For example, showing the Deployment Docker image tag in the footer of all UI pages.
- Exclusive features such as new Airflow components and improvements to the DAG development experience.

For more information about the features that are available in Astro Runtime releases, see the [Astro Runtime Release Notes](https://docs.astronomer.io/astro/runtime-release-notes).

## Runtime Versioning

Astro Runtime versions are released regularly and use [Semantic Versioning](https://semver.org/). Astronomer ships major, minor, and patch releases of Astro Runtime in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions. This includes API or DAG specification changes that are not backwards-compatible.
- **Minor** versions are released for functional changes. This includes API or DAG specification changes that are backwards-compatible.
- **Patch** versions are released for bug and security fixes that resolve unwanted behavior. 

An **LTS** qualifier identifies Long Term Support versions of Astro Runtime.  

To install or upgrade Astro Runtime, see [Upgrade Runtime](https://docs.astronomer.io/astro/upgrade-runtime).

## Distribution

Astro Runtime is distributed as a Debian-based Docker image. The Docker image is functionally identical to open source Apache Airflow. However, Astro Runtime includes performance and stability improvements, including critical bug fixes and security patches.

The Astro Runtime Docker image incorporates additional functionality that makes it easier for organizations to get started with Airflow implementations. This includes:

- A robust testing suite that includes performance benchmarking and end-to-end functionality and upgrade testing.
- A built-in directory of sample DAGs that fully utilize Airflow functionality.
- A collection of pre-installed Airflow provider packages.
- Compatibility with the Astronomer Platform.

The Dockerfiles for all supported Astro Runtime images are located in the [Astronomer `astro-runtime` GitHub repository](https://github.com/astronomer/astro-runtime).

## Executors

Executors are used to schedule, monitor, and execute tasks. Only a single executor can be configured at a time. 

Astro Runtime supports the [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html).

## Provider Packages

This table lists the provider packages and version information for each provider package that is included with Astro Runtime.

| Astro Runtime | [amazon](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) |[azure](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html) | [celery](https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/index.html) | [cncf.kubernetes](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html) | [elasticsearch](https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/index.html) | [ftp](https://airflow.apache.org/docs/apache-airflow-providers-ftp/stable/index.html) | [google](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html) |   [http](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/index.html) |[imap](https://airflow.apache.org/docs/apache-airflow-providers-imap/stable/index.html) | [mysql](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/index.html) | [postgres](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html) | [redis](https://airflow.apache.org/docs/apache-airflow-providers-redis/stable/index.html) | [slack](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/index.html) | [sqlite](https://airflow.apache.org/docs/apache-airflow-providers-sqlite/stable/index.html) | [ssh](https://airflow.apache.org/docs/apache-airflow-providers-ssh/stable/index.html) |
| -------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
|**3.0.x**|1.0.0|1.1.0|1.0.0|1.0.1|1.0.4|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|
|**4.0.x**|1.3.0|1.3.0|1.0.1|1.2.0|1.0.4|1.0.1|2.2.0|1.1.1|1.0.1|1.1.0|1.0.1|1.0.1|3.0.0|1.0.2|1.3.0|
|**4.1.x**|1.4.0|2.0.0|1.0.1|1!1.2.1|1.0.4|1.1.0|3.0.0|2.0.0|1.0.1|1.1.0|1.0.2|1.0.1|3.0.0|1.0.2|1.3.0|
|**4.2.x**|1!2.0.0|1!3.0.0|1!2.0.0|1!2.0.0|1!2.0.1|1!2.0.0|1!4.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!4.0.0|1!2.0.0|1!2.0.0|
|**5.0.x**|1!2.1.0|1!3.1.0|1!2.0.0|1!2.0.2|1!2.0.2|1!2.0.0|1!5.0.0|1!2.0.0|1!2.0.0|1!2.1.0|1!2.0.0|1!2.0.0|1!4.0.0|1!2.0.0|1!2.1.0|

## Python Packages

This table lists the Python packages supported by Astro Runtime.

| Astro Runtime                                   | Python Package                                                                | 
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **3.0.x**                                       |                                                                               |
| **4.0.x**                                       |                                                                               | 
| **4.1.x**                                       |                                                                               |
| **4.2.x**                                       |                                                                               | 
| **5.0.x**                                       |                                                                               | 

## Astro Runtime and Apache Airflow Parity

This table lists Astro Runtime releases and their associated Apache Airflow versions.

| Astro Runtime                                   | Apache Airflow Version                                                                | 
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **3.0.x**                                       |                                                                               |
| **4.0.x**                                       |                                                                               | 
| **4.1.x**                                       |                                                                               |
| **4.2.x**                                       |                                                                               | 
| **5.0.x**                                       | **2.3**                                                                        | 

## System Dependencies

The following are the operating system (OS) level dependencies for running basic Astro Runtime system processes:

- Debian 11.3 or later (bullseye). See [Installing Debian 11.3](https://www.debian.org/releases/bullseye/debian-installer/).