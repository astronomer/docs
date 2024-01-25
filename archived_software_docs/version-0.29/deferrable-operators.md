---
sidebar_label: "Deferrable operators"
title: "Deferrable operators"
id: deferrable-operators
description: Run deferrable operators to improve performance and and reduce costs.
---

[Apache Airflow 2.2](https://airflow.apache.org/blog/airflow-2.2.0/) introduced [**deferrable operators**](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html), a powerful type of Airflow operator that's optimized for lower resource costs and improved performance. In Airflow, it's common to use [sensors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html) and some [operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html) to configure tasks that wait for some external condition to be met before executing or triggering another task. While tasks using standard operators and sensors take up a worker slot when checking if an external condition has been met, deferrable operators suspend themselves during that process. This releases the worker to take on other tasks.

Deferrable operators rely on a new Airflow component called the triggerer, which can be enabled on Astronomer Software. To ensure that you can test your DAGs locally, the triggerer is also built into the Astro CLI.

Deferrable operators provide the following benefits:

- Reduced resource consumption. Deferrable operators can lower the number of workers needed to run tasks during periods of high concurrency. Less workers can lower your infrastructure cost per Deployment.
- Resiliency against restarts. When you push code to a Astronomer Software Deployment, the triggerer process that deferrable operators rely on is gracefully restarted and does not fail.

Astronomer recommends using deferrable versions of operators or sensors that typically spend a long time waiting for a condition to be met. This includes `S3Sensor`, `HTTPSensor`, and `DatabricksSubmitRunOperator`.

### How it works

Airflow 2.2 introduces two new concepts to support deferrable operators: the Trigger and the triggerer.

A **trigger** is a small, asynchronous Python function that quickly and continuously evaluates a given condition. Because of its design, thousands of Triggers can be run at once in a single process. In order for an operator to be deferrable, it must have its own Trigger code that determines when and how operator tasks are deferred.

The **triggerer** is responsible for running Triggers and signaling tasks to resume when their conditions are met. Like the Scheduler, it is designed to be highly-available. If a machine running Triggers shuts down unexpectedly, Triggers can be recovered and moved to another machine also running a triggerer.

Tasks that are defined with a deferrable operator run according to the following process:

- The task is picked up by a worker, which executes an initial piece of code that initializes the task. During this time, the task is in a "running" state and takes up a worker slot.
- The task defines a Trigger and defers the function of checking on some condition to the triggerer. Because all of the deferring work happens in the triggerer, the task instance can now enter a "deferred" state. This frees the worker slot to take on other tasks.
- The triggerer runs the task's Trigger periodically to check whether the condition has been met.
- Once the Trigger condition succeeds, the task is again queued by the Scheduler. This time, when the task is picked up by a worker, it begins to complete its main function.

For more information on how deferrable operators work and how to use them, see the [Airflow Guide for Deferrable operators](deferrable-operators.md) or the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html).

## Astro Runtime prerequisites

To use deferrable operators both in a local Airflow environment and on Astronomer Software, you must have:

- An [Astronomer Software project](create-project.md) running [Astro Runtime version 4.2.0 or later](https://docs.astronomer.io/astro/runtime-release-notes#astro-runtime-420).
- The [Astro CLI version 1.0 or later](https://docs.astronomer.io/astro/cli-release-notes#v110) installed.
- Triggerers enabled. See [Enable triggerers](https://docs.astronomer.io/software/configure-deployment#enable-triggerers).

All versions of Astro Runtime version 4.2.0 and later support the triggerer and have the `astronomer-providers` package installed. See [Upgrade Airflow](manage-airflow-versions.md).

## Astronomer Certified prerequisites

- Astronomer Certified version 2.2 or later.
- The `astronomer-providers` package added to your Astro project `requirements.txt` file. [Add Python and OS-level packages](https://docs.astronomer.io/software/customize-image#install-python-packages-from-private-sources).

## Using deferrable operators

To use a deferrable version of an existing operator in your DAG, you need to replace the import statement for the existing operator.

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

## Astronomer deferrable operators

In addition to the deferrable operators that are published by the Apache Airflow open source project, Astronomer maintains [`astronomer-providers`](https://astronomer-providers.readthedocs.io/en/stable/), an open source collection of deferrable operators bundled as a provider package.

This package is installed on Astro Runtime by default and includes deferrable versions of commonly used operators, including the `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

For a complete list of available deferrable operators in `astronomer-providers` , see the [`astronomer-providers` CHANGELOG](https://astronomer-providers.readthedocs.io/en/stable/changelog.html). This page includes both import statements and example DAGs for each available operator.
