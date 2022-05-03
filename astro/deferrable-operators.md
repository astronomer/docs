---
sidebar_label: "Deferrable Operators"
title: "Deferrable Operators"
id: deferrable-operators
description: Run deferrable operators on Astro for improved performance and cost savings.
---

## Overview

This guide explains how deferrable operators work and how to implement them in your DAGs.

[Apache Airflow 2.2](https://airflow.apache.org/blog/airflow-2.2.0/) introduced [**deferrable operators**](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html), a powerful type of Airflow operator that's optimized for lower resource costs and improved performance. In Airflow, it's common to use [sensors](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html) and some [operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html) to configure tasks that wait for some external condition to be met before executing or triggering another task. While tasks using standard operators and sensors take up a worker slot when checking if an external condition has been met, deferrable operators suspend themselves during that process. This releases the worker to take on other tasks.

Deferrable operators rely on a new Airflow component called the Triggerer. The Triggerer is highly available and built into all Deployments on Astro, which means that you can use deferrable operators in your DAGs with no additional configuration. To ensure that you can test your DAGs locally, the Triggerer is also built into the Astro CLI local development experience.

Deferrable operators enable two primary benefits:

- Reduced resource consumption. Depending on your resources and workload, deferrable operators can lower the number of workers needed to run tasks during periods of high concurrency. Less workers can lower your infrastructure cost per Deployment.
- Resiliency against restarts. When you push code to a Deployment on Astro, the Triggerer process that deferrable operators rely on is gracefully restarted and does not fail.

In general, we recommend using deferrable versions of operators or sensors that typically spend a long time waiting for a condition to be met. This includes the `S3Sensor`, the `HTTPSensor`, the `DatabricksSubmitRunOperator`, and more.

### How It Works

Airflow 2.2 introduces two new concepts to support deferrable operators: the Trigger and the Triggerer.

A **Trigger** is a small, asynchronous Python function that quickly and continuously evaluates a given condition. Because of its design, thousands of Triggers can be run at once in a single process. In order for an operator to be deferrable, it must have its own Trigger code that determines when and how operator tasks are deferred.

The **Triggerer** is responsible for running Triggers and signaling tasks to resume when their conditions have been met. Like the Scheduler, it is designed to be highly-available. If a machine running Triggers shuts down unexpectedly, Triggers can be recovered and moved to another machine also running a Triggerer.

The process for running a task using a deferrable operator is as follows:

1. The task is picked up by a worker, which executes an initial piece of code that initializes the task. During this time, the task is in a "running" state and takes up a worker slot.
2. The task defines a Trigger and defers the function of checking on some condition to the Triggerer. Because all of the deferring work happens in the Triggerer, the task instance can now enter a "deferred" state. This frees the worker slot to take on other tasks.
3. The Triggerer runs the task's Trigger periodically to check whether the condition has been met.
4. Once the Trigger condition succeeds, the task is again queued by the Scheduler. This time, when the task is picked up by a worker, it begins to complete its main function.

For more information on how deferrable operators work and how to use them, read our [Airflow Guide for Deferrable Operators](https://www.astronomer.io/guides/deferrable-operators) or the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html).

## Prerequisites

To use deferrable operators both in a local Airflow environment and on Astro, you must have:

- An [Astro project](create-project.md) running [Astro Runtime 4.2.0+](runtime-release-notes.md#astro-runtime-420).
- The [Astro CLI v1.1.0+](https://docs.astronomer.io/astro/cli-release-notes#v110) installed.

All versions of Astro Runtime 4.2.0+ support the Triggerer and have the `astronomer-providers` package installed. For more information, read [Astro Runtime Release Notes](runtime-release-notes.md) or [Upgrade Astro Runtime](upgrade-runtime.md).

## Using Deferrable Operators

To use a deferrable version of an existing operator in your DAG, you only need to replace the import statement for the existing operator.

For example, Airflow's `TimeSensorAsync` is a replacement of the non-deferrable `TimeSensor` ([source](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/time_sensor/index.html?highlight=timesensor#module-contents)). To use `TimeSensorAsync`, remove your existing `import` and replace it with the following:

```python
# Remove this import:
# from airflow.operators.sensors import TimeSensor
# Replace with:
from airflow.sensors.time_sensor import TimeSensorAsync as TimeSensor
```

Some additional notes about using deferrable operators:

- If you want to replace non-deferrable operators in an existing project with deferrable operators, we recommend importing the deferrable operator class as its non-deferrable class name. If you don't include this part of the import statement, you need to replace all instances of non-deferrable operators in your DAGs. In the above example, that would require replacing all instances of `TimeSensor` with `TimeSensorAsync`.
- Currently, not all operators have a deferrable version. There are a few open source deferrable operators, plus additional operators designed and maintained by Astronomer.
- If you're interested in the deferrable version of an operator that is not generally available, you can write your own and contribute these to the open source project. If you need help with writing a custom deferrable operator, reach out to [Astronomer support](https://support.astronomer.io).
- There are some use cases where it can be more appropriate to use a traditional sensor instead of a deferrable operator. For example, if your task needs to wait only a few seconds for a condition to be met, we recommend using a Sensor in [`reschedule` mode](https://github.com/apache/airflow/blob/1.10.2/airflow/sensors/base_sensor_operator.py#L46-L56) to avoid unnecessary resource overhead.

## Astronomer's Deferrable Operators

In addition to the deferrable operators that are published by the Apache Airflow open source project, Astronomer maintains [`astronomer-providers`](https://github.com/astronomer/astronomer-providers), an open source collection of deferrable operators bundled as a provider package. This package is installed on Astro Runtime by default and includes deferrable versions of popular operators such as the `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

The following table contains information about each operator that's available in the package, including their import path and an example DAG. For more information about each operator in the package, see the [CHANGELOG in `astronomer-providers`](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#100-2022-03-01).

| Operator/ Sensor Class                     | Import Path                                                                                                 | Example DAG                                                                                                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RedshiftSQLOperatorAsync`                 | `from astronomer.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperatorAsync`               | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_sql.py)                |
| `RedshiftPauseClusterOperatorAsync`        | `from astronomer.providers.amazon.aws.operators.redshift_cluster import RedshiftPauseClusterOperatorAsync`  | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `RedshiftResumeClusterOperatorAsync`       | `from astronomer.providers.amazon.aws.operators.redshift_cluster import RedshiftResumeClusterOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `RedshiftClusterSensorAsync`               | `from astronomer.providers.amazon.aws.sensors.redshift_cluster import RedshiftClusterSensorAsync`           | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `S3KeySensorAsync`                         | `from astronomer.providers.amazon.aws.sensors.s3 import S3KeySensorAsync`                                   | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_s3.py)                          |
| `KubernetesPodOperatorAsync`               | `from astronomer.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperatorAsync`      | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_s3.py)                          |
| `ExternalTaskSensorAsync`                  | `from astronomer.providers.core.sensors.external_task import ExternalTaskSensorAsync`                       | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/core/example_dags/example_external_task.py)                     |
| `FileSensorAsync`                          | `from astronomer.providers.core.sensors.filesystem import FileSensorAsync`                                  | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/core/example_dags/example_file_sensor.py)                       |
| `DatabricksRunNowOperatorAsync`            | `from astronomer.providers.databricks.operators.databricks import DatabricksRunNowOperatorAsync`            | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/databricks/example_dags/example_databricks.py)                  |
| `DatabricksSubmitRunOperatorAsync`         | `from astronomer.providers.databricks.operators.databricks import DatabricksSubmitRunOperatorAsync`         | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/databricks/example_dags/example_databricks.py)                  |
| `BigQueryCheckOperatorAsync`               | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryCheckOperatorAsync`               | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py)          |
| `BigQueryGetDataOperatorAsync`             | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryGetDataOperatorAsync`             | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py)          |
| `BigQueryInsertJobOperatorAsync`           | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperatorAsync`           | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py)          |
| `BigQueryIntervalCheckOperatorAsync`       | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryIntervalCheckOperatorAsync`       | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py)          |
| `BigQueryTableExistenceSensorAsync`        | `from astronomer.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensorAsync`          | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/google/cloud/example_dags/example_bigquery_sensors.py)           |
| `BigQueryValueCheckOperatorAsync`          | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryValueCheckOperatorAsync`          | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py)          |
| `GCSObjectExistenceSensorAsync`            | `from astronomer.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensorAsync`                   | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_gcs.py)                       |
| `GCSObjectsWithPrefixExistenceSensorAsync` | `from astronomer.providers.google.cloud.sensors.gcs import GCSObjectsWithPrefixExistenceSensorAsync`        | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/google/cloud/example_dags/example_gcs.py)                        |
| `GCSObjectUpdateSensorAsync`               | `from astronomer.providers.google.cloud.sensors.gcs import GCSObjectUpdateSensorAsync`                      | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/google/cloud/example_dags/example_gcs.py)                        |
| `GCSUploadSessionCompleteSensorAsync`      | `from astronomer.providers.google.cloud.sensors.gcs import GCSUploadSessionCompleteSensorAsync`            | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/google/cloud/example_dags/example_gcs.py)                        |
| `HttpSensorAsync`                          | `from astronomer.providers.http.sensors.http import HttpSensorAsync`                                        | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/http/example_dags/example_http.py)                              |
| `SnowflakeOperatorAsync`                   | `from astronomer.providers.snowflake.operators.snowflake import SnowflakeOperatorAsync`                     | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/snowflake/example_dags/example_snowflake.py)                    |
| `S3KeySizeSensorAsync`                     | `from astronomer.providers.amazon.aws.sensors.s3 import S3KeySizeSensorAsync`                               | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/amazon/aws/example_dags/example_s3.py)                           |
| `S3KeysUnchangedSensorAsync`               | `from astronomer.providers.amazon.aws.sensors.s3 import S3KeysUnchangedSensorAsync`                         | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/amazon/aws/example_dags/example_s3.py)                           |
| `S3PrefixSensorAsync`                      | `from astronomer.providers.amazon.aws.sensors.s3 import S3PrefixSensorAsync`                                | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/main/astronomer/providers/amazon/aws/example_dags/example_s3.py)                           |
