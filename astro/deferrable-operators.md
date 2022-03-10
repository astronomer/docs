---
sidebar_label: "Deferrable Operators"
title: "Deferrable Operators"
id: deferrable-operators
description: Run deferrable operators on Astro for improved performance and cost savings.
---

## Overview

This guide explains how deferrable operators work and how to implement them in your DAGs.

[Apache Airflow 2.2](https://airflow.apache.org/blog/airflow-2.2.0/) introduced [**deferrable operators**](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html), a powerful type of Airflow operator that promises lower resource costs and improved performance.

In Airflow, it's common to use [sensors](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html) and some [operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html) to configure tasks that wait for some external condition to be met before executing or triggering another task. While tasks using standard operators and sensors take up a Worker slot when checking if an external condition has been met, deferrable operators, suspend themselves during that process. This releases the Worker to take on other tasks. Using the deferrable versions of operators or sensors that typically spend a long time waiting for a condition to be met, such as the `S3Sensor`, the `HTTPSensor`, or the `DatabricksSubmitRunOperator`, can result in significant per-task cost savings and performance improvements.

Deferrable operators rely on an Airflow component called the Triggerer. The Triggerer is highly available and entirely managed on Astro, meaning that you can start using deferrable operators in your DAGs as long as you're running Astro Runtime 4.0+.

### How It Works

Airflow 2.2 introduces two new concepts to support deferrable operators: the Trigger and the Triggerer.

A **Trigger** is a small, asynchronous Python function that quickly and continuously evaluates a given condition. Because of its design, thousands of Triggers can be run at once in a single process. In order for an operator to be deferrable, it must have its own Trigger code that determines when and how operator tasks are deferred.

The **Triggerer** is responsible for running Triggers and signaling tasks to resume when their conditions have been met. Like the Scheduler, it is designed to be highly-available. If a machine running Triggers shuts down unexpectedly, Triggers can be recovered and moved to another machine also running a Triggerer.

The process for running a task using a deferrable operator is as follows:

1. The task is picked up by a Worker, which executes an initial piece of code that initializes the task. During this time, the task is in a "running" state and takes up a Worker slot.
2. The task defines a Trigger and defers the function of checking on some condition to the Triggerer. Because all of the deferring work happens in the Triggerer, the task instance can now enter a "deferred" state. This frees the Worker slot to take on other tasks.
3. The Triggerer runs the task's Trigger periodically to check whether the condition has been met.
4. Once the Trigger condition succeeds, the task is again queued by the Scheduler. This time, when the task is picked up by a Worker, it begins to complete its main function.

For implementation details on deferrable operators, read the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html).

## Prerequisites

To use Deferrable operators, you must have an [Astro project](create-project.md) running [Astro Runtime 4.2.0+](runtime-release-notes.md#astro-runtime-420). For more information on upgrading your Deployment's Runtime version, read [Upgrade Runtime](upgrade-runtime.md).

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

Astronomer maintains [`astronomer-providers`](https://github.com/astronomer/astronomer-providers), which is an open source collection of deferrable operators bundled as a provider package. This package is installed on Astronomer Runtime by default and includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

The following table contains information about each operator that's available in the package, including their import path and an example DAG. For more information about each available operator in the package, see the [CHANGELOG in `astronomer-providers`](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#100-2022-03-01).

| Operator/ Sensor Class     | Import Path                                                                                   | Example DAG                                                                                                                                       |
| -------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RedshiftSQLOperatorAsync` | `from astronomer.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_sql.py) |
| `RedshiftPauseClusterOperatorAsync` | `from astronomer.providers.amazon.aws.operators.redshift_cluster import RedshiftPauseClusterOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `RedshiftResumeClusterOperatorAsync` | `from astronomer.providers.amazon.aws.operators.redshift_cluster import RedshiftResumeClusterOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `RedshiftClusterSensorAsync` | `from astronomer.providers.amazon.aws.sensors.redshift_cluster import RedshiftClusterSensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_redshift_cluster_management.py) |
| `S3KeySensorAsync` | `from astronomer.providers.amazon.aws.sensors.s3 import S3KeySensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_s3.py) |
| `KubernetesPodOperatorAsync` | `from astronomer_operators.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/amazon/aws/example_dags/example_s3.py) |
| `ExternalTaskSensorAsync` | `from astronomer_operators.core.sensors.external_task import ExternalTaskSensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/core/example_dags/example_external_task.py) |
| `FileSensorAsync` | `from astronomer_operators.core.sensors.filesystem import FileSensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/core/example_dags/example_file_sensor.py) |
| `DatabricksRunNowOperatorAsync` | `from astronomer.providers.databricks.operators.databricks import DatabricksRunNowOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/databricks/example_dags/example_databricks.py) |
| `DatabricksSubmitRunOperatorAsync` | `from astronomer.providers.databricks.operators.databricks import DatabricksSubmitRunOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/databricks/example_dags/example_databricks.py) |
| `BigQueryCheckOperatorAsync` | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryCheckOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py) |
| `BigQueryGetDataOperatorAsync` | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryGetDataOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py) |
| `BigQueryInsertJobOperatorAsync` | `from astronomer.providers.google.cloud.operators.bigquery import  BigQueryInsertJobOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py) |
| `BigQueryIntervalCheckOperatorAsync` | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryIntervalCheckOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py) |
| `BigQueryValueCheckOperatorAsync` | `from astronomer.providers.google.cloud.operators.bigquery import BigQueryValueCheckOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_bigquery_queries.py) |
| `GCSObjectExistenceSensorAsync` | `from astronomer.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/google/cloud/example_dags/example_gcs.py) |
| `HttpSensorAsync` | `from astronomer.providers.http.sensors.http import HttpSensorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/http/example_dags/example_http.py) |
| `SnowflakeOperatorAsync` | `from astronomer.providers.snowflake.operators.snowflake import SnowflakeOperatorAsync` | [Example DAG](https://github.com/astronomer/astronomer-providers/blob/1.0.0/astronomer/providers/snowflake/example_dags/example_snowflake.py) |
