---
sidebar_label: 'Global environment variables'
title: 'Global environment variables'
id: platform-variables
description: A list of environment variables that are set globally on Astro and should not be modified.
---

This document is a reference for all environment variables on Astronomer with different default values than open source Apache Airflow. You can override [default Runtime environment variables](#default-runtime-environment-variables), but you can't override [system environment variables](#system-environment-variables).

For information on setting your own environment variables, see [Environment variables](environment-variables.md).

## System environment variables

On Astro, certain environment variables have preset values that are required and should not be overridden by your team. The following table provides information about each global environment variable set by Astronomer.

:::warning 

The Cloud UI does not currently prevent you from setting these environment variables, but attempting to set them can result in unexpected behavior that can include access problems, missing task logs, and failed tasks.

If you need to set one of these variables for a particular use case, contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

:::


| Environment Variable                         | Description                                                                                                                     | Value                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `AIRFLOW__LOGGING__DAG_PROCESSOR_LOG_TARGET` | Routes scheduler logs to stdout                                                                                                 | `stdout`                                                   |
| `AIRFLOW__LOGGING__REMOTE_LOGGING`           | Enables remote logging                                                                                                          | `True`                                                     |
| `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER`   | Location of remote logging storage                                                                                              | `baseLogFolder`                                            |
| `AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID`       | ID of the connection that provides access to your remote logging location                                            | `<connection-name>`                                        |
| `AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS`     | Class name that specifies the logging configuration                                                                         |`astronomer.runtime.logging.logging_config`                |
| `AIRFLOW_CONN_ASTRO_S3_LOGGING`              | Connection URI for writing task logs to Astro's managed S3 bucket                                                               | `<Connection-URI>`                                         |
| `AIRFLOW__LOGGING__ENCRYPT_S3_LOGS`          | Determines whether to use server-side encryption for S3 logs                                                                    | `False`                                                    |
| `AIRFLOW__WEBSERVER__BASE_URL`               | The base URL of the Airflow UI                                                                                                  | `https://${fullIngressHostname}`                           |
| `AIRFLOW__CORE__SQL_ALCHEMY_CONN`            | The SqlAlchemy connection string for the metadata database                                                                      | `dbConnSecret`                                             |
| `AIRFLOW__WEBSERVER__UPDATE_FAB_PERMS`       | Determines whether to update FAB permissions on webserver startup                                                               | `True`                                                     |
| `AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX`       | Determines whether to enable werkzeug ProxyFix middleware for reverse proxy                                                     | `True`                                                     |
| `AIRFLOW_CONN_AIRFLOW_DB`                    | The connection ID for accessing the Airflow metadata database                                                                   | `dbConnSecret`                                             |
| `AIRFLOW__CORE__FERNET_KEY`                  | The secret key for saving connection passwords in the metadata database                                                         | `fernetKeySecret`                                          |
| `AIRFLOW__CORE__EXECUTOR`                    | The executor class that Airflow uses. Astro exclusively supports the Celery executor                                            | `executor`                                                 |
| `AIRFLOW_HOME`                               | The home directory for an Astro project                                                                                         | `usr/local/airflow`                                        |
| `AIRFLOW__KUBERNETES__NAMESPACE`             | The Kubernetes namespace where Airflow workers are created                                                                      | `namespace`                                                |
| `AIRFLOW__CORE__HOSTNAME_CALLABLE`           | Path to a callable, which resolves to the hostname                                                                              | `airflow.utils.net.get_host_ip_address`                    |
| `AIRFLOW__SCHEDULER__STATSD_ON`              | Determines whether Statsd is on                                                                                                 | `True`                                                     |
| `AIRFLOW__SCHEDULER__STATSD_HOST`            | The hostname for Statsd                                                                                                         | `statsd.Hostname`                                          |
| `AIRFLOW__SCHEDULER__STATSD_PORT`            | The port for Statsd                                                                                                             | `<statsd-port>`                                            |
| `AIRFLOW__METRICS__STATSD_ON`                | Determines whether metrics are sent to Statsd                                                                                   | `True`                                                     |
| `AIRFLOW__METRICS__STATSD_HOST`              | The hostname for sending metrics to Statsd                                                                                      | `statsd.Hostname`                                          |
| `AIRFLOW__METRICS__STATSD_PORT`              | The port for sending metrics to Statsd                                                                                          | `<statsd-metrics-port>`                                    |
| `AIRFLOW__METRICS__STATSD_PREFIX`            | The prefix for sending the metrics to Statsd                                                                                    | `airflow`                                                  |
| `AIRFLOW__WEBSERVER__COOKIE_SECURE`          | Sets a `secure` flag on server cookies                                                                                          | `True`                                                     |
| `AIRFLOW__WEBSERVER__INSTANCE_NAME`          | Shows the name of your Deployment in the Home view of the Airflow UI                                                            | `<Deployment-Name>`                                        |
| `AIRFLOW__CELERY__WORKER_CONCURRENCY`        | Determines how many tasks each Celery worker can run at any given time and is the basis of worker auto-scaling logic            | `<Max-Tasks-Per-Worker>`                                   |
| `AIRFLOW__WEBSERVER__NAVBAR_COLOR`           | The color of the main navigation bar in the Airflow UI                                                                          | `#4a4466`                                                  |
| `AIRFLOW__WEBSERVER__EXPOSE_CONFIG`          | Exposes the **Configuration** tab of the Airflow UI and hides sensitive values                                                  | `NON-SENSITIVE-ONLY`                                       |
| `AWS_SECRET_ACCESS_KEY`                      | The key secret for accessing Astro's managed S3 bucket¹                                                                         | `<s3-aws-access-key-secret>`                               |
| `INSTANCE_TYPE`                              | Provides the instance size of the node the DAG is scheduled on.                                                                 | `(v1:metadata.labels['beta.kubernetes.io/instance-type'])` |
| `OPENLINEAGE_URL`                            | The URL for your Astro lineage backend. The destination for lineage metadata sent from external systems to the OpenLineage API. | `https://astro-<your-astro-base-domain>.datakin.com`       |
| `OPENLINEAGE_API_KEY`                        | Your OpenLineage API key                                                                                                        | `<your-lineage-api-key>`                                   |


## Default Runtime environment variables

Astro Runtime images include baked-in environment variables that have different default values than on Apache Airflow. See [Astro Runtime image architecture](runtime-image-architecture.md) for a complete list of variables and values.
