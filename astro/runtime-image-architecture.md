---
sidebar_label: "Astro Runtime architecture"
title: "Astro Runtime architecture"
id: runtime-image-architecture
description: Reference documentation for Astro Runtime, a differentiated distribution of Apache Airflow.
---

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and is required by all Astronomer products. It is intended to provide organizations with improved functionality, reliability, efficiency, and performance.

Deploying Astro Runtime is a requirement if your organization is using Astro. Astro Runtime includes the following features:

- Timely support for new patch, minor, and major versions of Apache Airflow. This includes bug fixes that have not been released by the open source project but are backported to Astro Runtime and available to users earlier.
- Exclusive features to enrich the task execution experience, including smart task concurrency defaults and high availability configurations.
- The `astronomer-providers` package. This package is an open source collection of Apache Airflow providers and modules maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`. See [Astronomer Providers documentation](https://astronomer-providers.readthedocs.io/en/stable/index.html)
- The `openlineage-airflow` package. [OpenLineage](https://openlineage.io/) standardizes the definition of data lineage, the metadata that forms lineage metadata, and how data lineage metadata is collected from external systems. This package enables data lineage on Astro. See [OpenLineage and Airflow](https://docs.astronomer.io/learn/airflow-openlineage/).
- A custom logging module that ensures Airflow task logs are reliably available to the Astro data plane.
- A custom security manager that enforces user roles and permissions as defined by Astro. See [User permissions](user-permissions.md).
- A custom Airflow UI that includes links to Astronomer resources and exposes the currently running Docker image tag in the footer of all UI pages.
- A monitoring DAG that the Astronomer team uses to monitor the health of Astro Deployments.

For more information about the features that are available in Astro Runtime releases, see the [Astro Runtime release notes](runtime-release-notes.md).

## Runtime versioning

Astro Runtime versions are released regularly and use [semantic versioning](https://semver.org/). Astronomer ships major, minor, and patch releases of Astro Runtime in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions. This includes new major or minor versions of Apache Airflow, as well as API or DAG specification changes that are not backward compatible.
- **Minor** versions are released for functional changes. This includes API or DAG specification changes that are backward compatible, which might include new minor versions of `astronomer-providers` and `openlineage-airflow`.
- **Patch** versions are released for bug and security fixes that resolve unwanted behavior. This includes new patch versions of Apache Airflow, `astronomer-providers`, and `openlineage-airflow`.

Every version of Astro Runtime correlates to an Apache Airflow version. All Deployments on Astro must run only one version of Astro Runtime, but you can run different versions of Astro Runtime on different Deployments within a given cluster or Workspace. See [Create a Deployment](create-deployment.md#create-a-deployment).

For a list of supported Astro Runtime versions and more information on the Astro Runtime maintenance policy, see [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.md).

### Astro Runtime and Apache Airflow parity

<!--- Version-specific -->

This table lists Astro Runtime releases and their associated Apache Airflow versions.

| Astro Runtime | Apache Airflow version |
| ------------- | ---------------------- |
| 4             | 2.2                    |
| 5             | 2.3                    |
| 6             | 2.4                    |
| 7             | 2.5                    |
| 8             | 2.6                    |

For version compatibility information, see the [Runtime release notes](runtime-release-notes.md).

## Default environment variables

The following table lists the Airflow environment variables that have different default values on Astro Runtime. Unlike [global environment variables](platform-variables.md) set on the data plane, you can override the values of these variables for specific use cases. To edit the values of the default Airflow environment variables, see [Set environment variables on Astro](environment-variables.md).

| Environment Variable                                            | Description                                                                                                                                                                                 | Value                                                                        |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`                     | The time in seconds that Airflow waits before re-scanning the `dags` directory for new files. Note that this environment variable is set for all Deployments regardless of Runtime version. | `30`                                                                         |
| `AIRFLOW__CELERY__STALLED_TASK_TIMEOUT`                         | The maximum time in seconds that tasks running with the Celery executor can remain in a `queued` state before they are automatically rescheduled.                                           | `600`                                                                        |
| `AIRFLOW_CORE_PARALLELISM`                                      | The maximum number of task instances that can run concurrently for each scheduler in your Deployment.                                                                                       | `[number-of-running-workers-for-all-worker-queues] * [max-tasks-per-worker]` |
| `AIRFLOW__KUBERNETES_EXECUTOR__WORKER_PODS_CREATION_BATCH_SIZE` | The number of worker Pods that can be created each time the scheduler parses DAGs. This setting limits the number of tasks that can be scheduled at one time.                               | `16`                                                                         |

## Astro monitoring DAG (Hybrid only)

Astro Runtime includes a monitoring DAG that is pre-installed in the Docker image and enabled for all Deployments on Astro Hybrid. In addition to generating Deployment health and metrics functionality, this DAG allows the Astronomer team to monitor the health of your data plane by enabling real-time visibility into whether your workers are healthy and tasks are running.

The `astronomer_monitoring_dag` runs a simple bash task every 5 minutes to ensure that your Airflow scheduler and workers are functioning as expected. If the task fails twice in a row or is not scheduled within a 10-minute interval, Astronomer support receives an alert and will work with you to troubleshoot. The DAG runs and appears in the Airflow UI only on Astro Deployments. 

Because this DAG is essential to Astro's managed service, you are not charged for its task runs. For the same reasons, this DAG can't be modified or disabled through the Airflow UI. To modify when this DAG runs on a Deployment, set the following [Deployment environment variable](environment-variables.md):

- Key: `AIRFLOW_MONITORING_DAG_SCHEDULE_INTERVAL`
- Value: An alternative schedule defined as a [cron expression](https://crontab.guru/)

## Provider packages

The latest version of the Astro Runtime image has the following open source provider packages pre-installed. Providers marked with an asterisk (`*`) are installed only in Astro Runtime and not installed by default on Apache Airflow.

- Amazon [`apache-airflow-providers-amazon`](https://pypi.org/project/apache-airflow-providers-amazon/) `*`
- Astronomer Providers [`astronomer-providers`](https://pypi.org/project/astronomer-providers/) `*`
- Astro Python SDK [`astro-sdk-python`](https://pypi.org/project/astro-sdk-python/) `*`
- Celery [`apache-airflow-providers-celery`](https://pypi.org/project/apache-airflow-providers-celery/)
- Cloud Native Computing Foundation (CNCF) Kubernetes [`apache-airflow-providers-cncf-kubernetes`](https://pypi.org/project/apache-airflow-providers-cncf-kubernetes/)
- Common SQL [`apache-airflow-providers-common-sql`](https://pypi.org/project/apache-airflow-providers-common-sql/)
- Datadog [`apache-airflow-providers-datadog](https://pypi.org/project/apache-airflow-providers-datadog/) `*`
- Elasticsearch [`apache-airflow-providers-elasticsearch`](https://pypi.org/project/apache-airflow-providers-elasticsearch/) `*`
- FTP [`apache-airflow-providers-ftp`](https://pypi.org/project/apache-airflow-providers-ftp/) 
- Google [`apache-airflow-providers-google`](https://pypi.org/project/apache-airflow-providers-google/) `*`
- HTTP [`apache-airflow-providers-http`](https://pypi.org/project/apache-airflow-providers-http/)
- IMAP [`apache-airflow-providers-imap`](https://pypi.org/project/apache-airflow-providers-imap/)
- Microsoft Azure [`apache-airflow-providers-microsoft-azure`](https://pypi.org/project/apache-airflow-providers-microsoft-azure/) `*`
- OpenLineage [`openlineage-airflow`](https://pypi.org/project/openlineage-airflow/) (this package installs an Airflow plugin) `*`
- PostgreSQL (Postgres) [`apache-airflow-providers-postgres`](https://pypi.org/project/apache-airflow-providers-postgres/) `*`
- Redis [`apache-airflow-providers-redis`](https://pypi.org/project/apache-airflow-providers-redis/) `*`
- SQLite [`apache-airflow-providers-sqlite`](https://pypi.org/project/apache-airflow-providers-sqlite/)

### Provider package versioning

If an Astro Runtime release includes changes to an installed version of a provider package that is maintained by Astronomer (`astronomer-providers` or `openlineage-airflow`), the version change is documented in the [Astro Runtime release notes](runtime-release-notes.md).

To determine the version of any provider package installed in your current Astro Runtime image, run:

```
docker run --rm <runtime-image> pip freeze | grep <provider>
```

## Python versioning

| Astro Runtime | Python version |
| ------------- | -------------- |
| 4             | 3.9            |
| 5             | 3.9            |
| 6             | 3.9            |
| 7             | 3.9            |
| 8             | 3.10           |

If your data pipelines require an unsupported Python version and you're running Astro Runtime 6.0 (based on Airflow 2.4) or later, Astronomer recommends that you use the `ExternalPythonOperator`. See [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#externalpythonoperator).

If you're currently using the `KubernetesPodOperator` or the `PythonVirtualenvOperator` in your DAGs, you can continue to use them to create virtual or isolated environments that can run tasks with different versions of Python.

## Executors

In Airflow, the executor is responsible for determining how and where a task is completed.

In all local environments created with the Astro CLI, Astro Runtime runs the [Local executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html). On Astro, Astro Runtime exclusively supports the [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html). Support for the Kubernetes executor is currently in Private Preview.

Soon, Astronomer will provide a new executor with intelligent worker packing, task-level resource requests, improved logging, and Kubernetes-like task isolation.

## Distribution

Astro Runtime is distributed as a Debian-based Docker image. Runtime Docker images have the following format:

- `quay.io/astronomer/astro-runtime:<version>`
- `quay.io/astronomer/astro-runtime:<version>-base`

An Astro Runtime image must be specified in the `Dockerfile` of your Astro project. Astronomer recommends using non-`base` images, which incorporate ONBUILD commands that copy and scaffold your Astro project directory so you can more easily pass those files to the containers running each core Airflow component. A `base` Astro Runtime image is recommended for complex use cases that require additional customization, such as [installing Python packages from private sources](develop-project.md#install-python-packages-from-private-sources).

For a list of all Astro Runtime Docker images, see [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

## System distribution

The following table lists the operating systems and architectures supported by each Astro Runtime version. If you're using a Mac computer with an M1 chip, Astronomer recommends using Astro Runtime 6.0.4 or later.

| Astro Runtime | Operating System (OS)  | Architecture    |
| ------------- | ---------------------- | --------------- |
| 4             | Debian 11.3 (bullseye) | AMD64           |
| 5             | Debian 11.3 (bullseye) | AMD64           |
| 6             | Debian 11.3 (bullseye) | AMD64 and ARM64 |
| 7             | Debian 11.3 (bullseye) | AMD64 and ARM64 |
| 8             | Debian 11.3 (bullseye) | AMD64 and ARM64 |

Astro Runtime 6.0.4 and later images are multi-arch and support AMD64 and ARM64 processor architectures for local development. Docker automatically uses the correct processor architecture based on the computer you are using.

## Related documentation

- [Astro Runtime release notes](runtime-release-notes.md)
- [Upgrade Runtime](https://docs.astronomer.io/astro/upgrade-runtime)
- [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.md)
