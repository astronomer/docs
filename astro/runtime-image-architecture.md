---
sidebar_label: 'Astro Runtime Architecture'
title: 'Astro Runtime Architecture'
id: runtime-image-architecture
description: Reference documentation for Astro Runtime, a differentiated distribution of Apache Airflow.
---

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and required by all Astronomer products. It is intended to provide organizations improved functionality, reliability, efficiency, and performance.

## Differences between Astro Runtime and Apache Airflow

If your organization is using Astro, deploying Astro Runtime is required and central to the value of our product. Astro Runtime includes the following features:

- Timely support for new patch, minor, and major versions of Apache Airflow. This includes bug fixes that have not been released by the open source project but are backported to Astro Runtime and available to users earlier.
- Exclusive features to enrich the task execution experience, including smart task concurrency defaults and high availability configurations.
- The `astronomer-providers` package. This package is an open source collection of Apache Airflow providers and modules maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`. See [Astronomer deferrable operators](deferrable-operators.md#astronomer-deferrable-operators).
- The `openlineage-airflow` package. [OpenLineage](https://openlineage.io/) standardizes the definition of data lineage, the metadata that forms lineage data, and how data lineage data is collected from external systems. This package enables data lineage on Astro. See [OpenLineage and Airflow](https://docs.astronomer.io/astro/data-lineage-concepts#openlineage-and-airflow).
- A custom logging module that ensures Airflow task logs are reliably available to the Astro data plane and Astronomer Software.
- A custom security manager that enforces user roles and permissions as defined by Astro and Astronomer Software. See [User permissions](user-permissions.md).
- A custom Airflow UI that includes links to Astronomer resources and exposes the currently running Docker image tag in the footer of all UI pages.

For more information about the features that are available in Astro Runtime releases, see the [Astro Runtime release notes](https://docs.astronomer.io/astro/runtime-release-notes). To install or upgrade Astro Runtime, see [Upgrade Runtime](https://docs.astronomer.io/astro/upgrade-runtime).

## Runtime versioning

Astro Runtime versions are released regularly and use [semantic versioning](https://semver.org/). Astronomer ships major, minor, and patch releases of Astro Runtime in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions. This includes new major or minor versions of Apache Airflow as well as API or DAG specification changes that are not backwards-compatible.
- **Minor** versions are released for functional changes. This includes new patch versions of Apache Airflow as well as API or DAG specification changes that are backwards-compatible.
- **Patch** versions are released for bug and security fixes that resolve unwanted behavior. This includes new patch versions of `astronomer-providers` and `openlineage-airflow`.

An **LTS** qualifier identifies Long Term Support versions of Astro Runtime.  

To install or upgrade Astro Runtime, see [Upgrade Runtime](https://docs.astronomer.io/astro/upgrade-runtime).

## Distribution

Astro Runtime is distributed as a Debian-based Docker image. Runtime Docker images have the following format:

- `quay.io/astronomer/astro-runtime:<version>`
- `quay.io/astronomer/astro-runtime:<version>-base`

An Astro Runtime image must be specified in the `Dockerfile` of your Astro project. Astronomer recommends using non-`base` images, which incorporate ONBUILD commands that copy and scaffold your Astro project directory so you can more easily pass those files to the containers running each core Airflow component. A `base` Astro Runtime image is recommended for complex use cases that require additional customization, such as [installing Python packages from private sources](develop-project.md#install-python-packages-from-private-sources).

For a list of all Astro Runtime Docker images, see [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

The Dockerfiles for all supported Astro Runtime images are located in the [Astronomer `astro-runtime` GitHub repository](https://github.com/astronomer/astro-runtime).

## Executors

In Airflow, the executor is responsible for determining how and where a task is completed. On Astronomer Software, Astro Runtime supports the following executors:

- [Local Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html)
- [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html)
- [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html)

Soon, Astronomer will provide a new executor with intelligent worker packing, task-level resource requests, improved logging, and Kubernetes-like task isolation.

## Provider packages

All Astro Runtime images have the following open source provider packages pre-installed:

- Amazon [`apache-airflow-providers-amazon`](https://pypi.org/project/apache-airflow-providers-amazon/)
- Elasticsearch [`apache-airflow-providers-elasticsearch`](https://pypi.org/project/apache-airflow-providers-elasticsearch/)
- Celery [`apache-airflow-providers-celery`](https://pypi.org/project/apache-airflow-providers-celery/)
- Google [`apache-airflow-providers-google`](https://pypi.org/project/apache-airflow-providers-google/)
- Password [`apache-airflow-password`](https://pypi.org/project/apache-airflow/)
- Cloud Native Computing Foundation (CNCF) Kubernetes [`apache-airflow-cncf.kubernetes`](https://pypi.org/project/apache-airflow-providers-cncf-kubernetes/)
- PostgreSQL (Postgres) [`apache-airflow-providers-postgres`](https://pypi.org/project/apache-airflow-providers-postgres/)
- Redis [`apache-airflow-providers-redis`](https://pypi.org/project/apache-airflow-providers-redis/)
- StatsD [`apache-airflow-statsd`](https://pypi.org/project/statsd/)
- Virtualenv [`apache-airflow-virtualenv`](https://pypi.org/project/virtualenv/)
- OpenLineage with Airflow [`openlineage-airflow`](https://pypi.org/project/openlineage-airflow/)
- Astronomer Providers [`astronomer-providers`](https://pypi.org/project/astronomer-providers/)

### Provider package versioning

If an Astro Runtime release includes changes to an installed version of a provider package that is maintained by Astronomer (`astronomer-providers` or `openlineage-airflow`), the version change is documented in the [Astro Runtime Release Notes](/astro/runtime-release-notes.md).

To determine the version of a provider package installed in your current Astro Runtime image, run:

```
docker run --rm {image} pip freeze | grep apache-airflow-provider
```

## Python versioning

Astro Runtime supports Python 3.9. This is the only version of Python that Astro Runtime supports. If your data pipelines require an unsupported Python version, Astronomer recommends that you use the KuberentesPodOperator. See [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md).

## Astro Runtime and Apache Airflow parity

This table lists Astro Runtime releases and their associated Apache Airflow versions.

| Astro Runtime                                   | Apache Airflow Version                                                                | 
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| 3.0.x                                       |       2.1.1                                                                       |
| 4.0.x                                       |       2.2.0                                                                    | 
| 4.1.x                                       |       2.2.4                                                                    |
| 4.2.x                                       |       2.2.4                                                                      | 
| 5.0.x                                       |       2.3.0                                                                        | 

## System distribution

Astro Runtime images are based on Debian 11.3 (bullseye).