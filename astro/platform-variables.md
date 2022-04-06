---
sidebar_label: 'Global Environment Variables'
title: 'Global Environment Variables'
id: platform-variables
description: A list of environment variables that are set globally on Astro and cannot be modified.
---

## Overview

As part of the Astro architecture, certain environment variables have preset values that cannot be overridden by your organization. This reference page contains information about each global environment variable set by Astronomer.

## Global Environment Variables

|Environment Variable | Description | Value |
|---------------------|-------|------------|
| `AIRFLOW__LOGGING__REMOTE_LOGGING`| Enables remote logging | `True` |
| `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER`| Location of remote logging storage | `baseLogFolder`|
| `AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID` | Airflow connection ID to access remote logging storage   | `astro_s3_logging` |
| `AIRFLOW_CONN_ASTRO_S3_LOGGING` | Connection URI for writing task logs to Astro's managed S3 bucket | `<Connection URI>`|
| `AIRFLOW__LOGGING__ENCRYPT_S3_LOGS` | Determines whether to use server-side encryption for S3 logs | `False` |
| `AIRFLOW__WEBSERVER__BASE_URL` | The base URL of the Airflow UI  | `https://${fullIngressHostname}`|
|`AIRFLOW__CORE__SQL_ALCHEMY_CONN`| The SqlAlchemy connection string for the metadata DB | `dbConnSecret` |
|`AIRFLOW__WEBSERVER__UPDATE_FAB_PERMS`| Determines whether to update FAB permissions on Webserver startup | `True`|
| `AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX` | Determines whether to enable werkzeug ProxyFix middleware for reverse proxy | `True` |
| `AIRFLOW_CONN_AIRFLOW_DB` | The connection ID for accessing the Airflow metadata DB  | `dbConnSecret` |
| `AIRFLOW__CORE__FERNET_KEY` |The secret key for saving connection passwords in the metadata DB | `fernetKeySecret` |
| `AIRFLOW__CORE__EXECUTOR`  | The executor class that Airflow uses. Astro exclusively supports the Celery Executor | `executor` |
| `AIRFLOW_HOME`  | The home directory for an Airflow project | `usr/local/airflow` |
| `AIRFLOW__KUBERNETES__NAMESPACE`| The Kubernetes namespace where Airflow Workers are created | `namespace` |
| `AIRFLOW__CORE__HOSTNAME_CALLABLE` | Path to a callable, which resolves to the hostname | `airflow.utils.net.get_host_ip_address`|
| `AIRFLOW__SCHEDULER__STATSD_ON` | Determines whether Statsd is on | `True` |
| `AIRFLOW__SCHEDULER__STATSD_HOST` |The hostname for Statsd | `statsd.Hostname`|
| `AIRFLOW__SCHEDULER__STATSD_PORT` | The port for Statsd | `strconv.FormatInt(int64(statsd.IngestPort), baseTen)` |
| `AIRFLOW__METRICS__STATSD_ON` | Determines whether metrics are sent to Statsd | `True` |
| `AIRFLOW__METRICS__STATSD_HOST` | The hostname for sending metrics to Statsd | `statsd.Hostname`|
| `AIRFLOW__METRICS__STATSD_PORT` | The port for sending metrics to Statsd | `strconv.FormatInt(int64(statsd.IngestPort), baseTen)` |
| `AIRFLOW__WEBSERVER__COOKIE_SECURE` | Sets a `secure` flag on server cookies | `True` |
| `AIRFLOW__WEBSERVER__INSTANCE_NAME` | Shows the name of your Deployment in the Home view of the Airflow UI | `<Deployment-Name>` |
| `AIRFLOW__CELERY__WORKER_CONCURRENCY` | Determines how many tasks each Celery worker can run at any given time and is the basis of worker auto-scaling logic | `16` |
