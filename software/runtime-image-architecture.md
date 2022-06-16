---
sidebar_label: 'Astro Runtime Architecture'
title: 'Astro Runtime Architecture'
id: runtime-image-architecture
description: Reference documentation for Astro Runtime, a differentiated distribution of Apache Airflow.
---

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and required by all Astronomer products. It is intended to provide organizations improved functionality, reliability, efficiency, and performance.

If your organization is using Software version 0.29 or later, you can deploy Astro Runtime images. Astro Runtime includes the following features:

- The `astronomer-providers` package. This package is an open source collection of Apache Airflow providers and modules that is maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.
- Airflow UI improvements. For example, showing the Deployment Docker image tag in the footer of all UI pages.
- Exclusive features such as new Airflow components and improvements to the DAG development experience.

For more information about the features that are available in Astro Runtime releases, see the [Astro Runtime Release Notes](/astro/runtime-release-notes).

If you're curious about the differences between Astro Runtime and Astronomer Certified, see [Differences Between Astronomer Runtime and Astronomer Certified](image-architecture.md#differences-between-astronomer-runtime-and-astronomer-certified)

## Runtime Versioning

Astro Runtime versions are released regularly and use [Semantic Versioning](https://semver.org/). Astronomer ships major, minor, and patch releases of Astro Runtime in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions. This includes API or DAG specification changes that are not backwards-compatible.
- **Minor** versions are released for functional changes. This includes API or DAG specification changes that are backwards-compatible.
- **Patch** versions are released for bug and security fixes that resolve unwanted behavior. 

An **LTS** qualifier identifies Long Term Support versions of Astro Runtime.  

To install or upgrade Astro Runtime, see [Upgrade Runtime](https://docs.astronomer.io/astro/upgrade-runtime).

## Distribution

Astro Runtime is distributed as a Debian-based Docker image. The Docker image is functionally identical to open source Apache Airflow. However, Astro Runtime includes performance and stability improvements, including critical bug fixes and security patches.

Runtime Docker images have the following format:

- `quay.io/astronomer/astro-runtime:<version>`
- `quay.io/astronomer/astro-runtime:<version>-base`

Astronomer recommends using non-`base` images in your project's `Dockerfile`. These images incorporate Docker ONBUILD commands to copy and scaffold your Astro project directory so you can more easily pass those files to the containers running each core Airflow component. A `base` Astro Runtime image is recommended for complex use cases that require additional customization.

Astro Runtime Docker images are hosted on the Astronomer Docker registry and enable Airflow on Astro. All Astro projects require that you specify an Astro Runtime image in your Dockerfile, and all Deployments on Astro must run only one version of Astro Runtime. Every version of Astro Runtime correlates to an Apache Airflow version. You can run different versions of Astro Runtime on different Deployments within a given Workspace or Cluster.

The Astro Runtime Docker image incorporates additional functionality that makes it easier for organizations to get started with Airflow implementations. This includes:

- A robust testing suite that includes performance benchmarking and end-to-end functionality and upgrade testing.
- A built-in directory of sample DAGs that fully utilize Airflow functionality.
- A collection of pre-installed Airflow provider packages.
- Compatibility with the Astronomer Platform.

The Dockerfiles for all supported Astro Runtime images are located in the [Astronomer `astro-runtime` GitHub repository](https://github.com/astronomer/astro-runtime).

## Executors

Executors are the mechanism used to run task instances. Astro Runtime supports the [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html).

Soon, Astronomer will provide a new executor with intelligent worker packing, task-level resource requests, improved logging, and Kubernetes-like task isolation.

## Provider Packages

When you install the Astro Runtime image, the supported Apache Airflow open-source software (OSS) provider packages are included. The following are the provider packages Astro Runtime supports:

- Amazon
- Elasticsearch
- Celery
- Google
- Password
- Cloud Native Computing Foundation (CNCF) Kubernetes
- PostgreSQL (Postgres)
- Redis
- StatsD
- Virtualenv
- OpenLineage with Airflow
- astronomer-providers

To determine the supported provider package version for a specific Astronomer Software release, see the release notes. Run the following command to determine the provider package versions that are supported by your current Astro Runtime image:

```
docker run --rm {image} pip freeze | grep apache-airflow-provider
```
OpenLineage with Airflow standardizes the definition of data lineage, the metadata that forms lineage data, and how data lineage data is collected from external systems. OpenLineage with Airflow is intended to make it easier for organizations to integrate their lineage tools with Apache Airflow. See [OpenLineage and Airflow](https://docs.astronomer.io/astro/data-lineage-concepts#openlineage-and-airflow).

The `astronomer-providers` package is a collection of Apache Airflow OSS providers and modules. The package is installed on Astro Runtime by default and is maintained by Astronomer. The package includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`. See [Deferrable Operators](https://docs.astronomer.io/astro/deferrable-operators). To access the source code for this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

## Python Packages

This table lists the Python packages supported by Astro Runtime. You can't modify the Python versions.

| Astro Runtime                                   | Python Package                                                                | 
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **3.0.x**                                       |      **3.9.6**                                                                        |
| **4.0.x**                                       |      **3.9.7**                                                                         | 
| **4.1.x**                                       |      **3.9.7**                                                                      |
| **4.2.x**                                       |      **3.9.7**                                                                     | 
| **5.0.x**                                       |      **3.9.7**                                                                  | 

## Astro Runtime and Apache Airflow Parity

This table lists Astro Runtime releases and their associated Apache Airflow versions.

| Astro Runtime                                   | Apache Airflow Version                                                                | 
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **3.0.x**                                       |       **2.1.1**                                                                       |
| **4.0.x**                                       |       **2.2.0**                                                                    | 
| **4.1.x**                                       |       **2.2.4**                                                                    |
| **4.2.x**                                       |       **2.2.4**                                                                      | 
| **5.0.x**                                       |       **2.3.0**                                                                        | 

## System Dependencies

The following are the operating system (OS) level dependencies for running basic Astro Runtime system processes:

- Debian 11.3 or later (bullseye). See [Installing Debian 11.3](https://www.debian.org/releases/bullseye/debian-installer/).