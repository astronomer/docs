---
title: "Deferrable operators"
sidebar_label: "Deferrable operators"
description: "Implement deferrable operators to save cost and resources with Airflow."
id: deferrable-operators
---

With Airflow 2.2 and later, you can use deferrable operators to run tasks in your Airflow environment. These operators leverage the Python [asyncio](https://docs.python.org/3/library/asyncio.html) library to efficiently run tasks waiting for an external resource to finish. This frees up your workers and allows you to utilize resources more effectively. In this guide, you'll review deferrable operator concepts and learn which operators are deferrable.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow sensors. See [Sensors 101](what-is-a-sensor.md).

## Terms and concepts

Review the following terms and concepts to gain a better understanding of deferrable operator functionality:

- [asyncio](https://docs.python.org/3/library/asyncio.html): A Python library used as the foundation for multiple asynchronous frameworks. This library is core to deferrable operator functionality, and is used when writing triggers.
- Triggers: Small, asynchronous sections of Python code. Due to their asynchronous nature, they coexist efficiently in a single process known as the triggerer.
- Triggerer: An Airflow service similar to a scheduler or a worker that runs an [asyncio event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop) in your Airflow environment. Running a triggerer is essential for using deferrable operators.
- Deferred: An Airflow task state indicating that a task has paused its execution, released the worker slot, and submitted a trigger to be picked up by the triggerer process.

The terms deferrable, async, and asynchronous are used interchangeably and have the same meaning.

With traditional operators, a task submits a job to an external system such as a Spark cluster and then polls the job status until it is completed. Although the task isn't doing significant work, it still occupies a worker slot during the polling process. As worker slots are occupied, tasks are queued and start times are delayed. The following image illustrates this process:

![Classic Worker](/img/guides/classic_worker_process.png)

With deferrable operators, worker slots are released when a task is polling for job status. When the task is deferred, the polling process is offloaded as a trigger to the triggerer, and the worker slot becomes available. The triggerer can run many asynchronous polling tasks concurrently, and this prevents polling tasks from occupying your worker resources. When the terminal status for the job is received, the task resumes, taking a worker slot while it finishes. The following image illustrates this process:

![Deferrable Worker](/img/guides/deferrable_operator_process.png)

## Use deferrable operators

Deferrable operators should be used whenever you have tasks that occupy a worker slot while polling for a condition in an external system. For example, using deferrable operators for sensor tasks can provide efficiency gains and reduce operational costs. Smart Sensors were deprecated in Airflow 2.2.4, and were removed in Airflow 2.4.0. Use deferrable operators instead of Smart Sensors because they provide greater functionality and they are supported by Airflow.

To use a deferrable version of an existing operator in your DAG, you only need to replace the import statement for the existing operator. For example, Airflow's `TimeSensorAsync` is a replacement of the non-deferrable `TimeSensor` ([source](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/time_sensor/index.html?highlight=timesensor#module-contents)). To use `TimeSensorAsync`, remove your existing `import` and replace it with the following:

```python
# Remove this import:
# from airflow.operators.sensors import TimeSensor
# Replace with:
from airflow.sensors.time_sensor import TimeSensorAsync as TimeSensor
```

There are numerous benefits to using deferrable operators including:

- Reduced resource consumption: Depending on the available resources and the workload of your triggers, you can run hundreds to thousands of deferred tasks in a single triggerer process. This can lead to a reduction in the number of workers needed to run tasks during periods of high concurrency. With less workers needed, you are able to scale down the underlying infrastructure of your Airflow environment.
- Resiliency against restarts: Triggers are stateless by design. This means your deferred tasks are not set to a failure state if a triggerer needs to be restarted due to a deployment or infrastructure issue. When a triggerer is back up and running in your environment, your deferred tasks will resume.
- Gateway to event-based DAGs: The presence of `asyncio` in core Airflow is a potential foundation for event-triggered DAGs.

Some additional notes about using deferrable operators:

- If you want to replace non-deferrable operators in an existing project with deferrable operators, Astronomer recommends importing the deferrable operator class as its non-deferrable class name. If you don't include this part of the import statement, you need to replace all instances of non-deferrable operators in your DAGs. In the above example, that would require replacing all instances of `TimeSensor` with `TimeSensorAsync`.
- Currently, not all operators have a deferrable version. There are a few open source deferrable operators, plus additional operators designed and maintained by Astronomer.
- If you're interested in the deferrable version of an operator that is not generally available, you can write your own and contribute it back to the open source project. 
- There are some use cases where it can be more appropriate to use a traditional sensor instead of a deferrable operator. For example, if your task needs to wait only a few seconds for a condition to be met, Astronomer recommends using a Sensor in [`reschedule` mode](https://github.com/apache/airflow/blob/1.10.2/airflow/sensors/base_sensor_operator.py#L46-L56) to avoid unnecessary resource overhead.

## Available deferrable operators

The following deferrable operators are installed by default in Airflow:

- [TimeSensorAsync](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/time_sensor/index.html?highlight=timesensor#module-contents)
- [DateTimeSensorAsync](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/date_time/index.html#airflow.sensors.date_time.DateTimeSensorAsync)

You can use additional deferrable operators built and maintained by Astronomer by installing the open source [Astronomer Providers](https://github.com/astronomer/astronomer-providers) Python package. The operators and sensors in this package are deferrable versions of commonly used operators. For example, the package includes:

- `SnowflakeOperatorAsync`
- `DatabricksSubmitRunOperatorAsync`
- `HttpSensorAsync`
 
For a full list of deferrable operators and sensors available in the `astronomer-providers` package, see [Changelog](https://astronomer-providers.readthedocs.io/en/stable/providers/operators_and_sensors_list.html). You can also create your own deferrable operator for your use case.

## Example workflow

In this sample DAG, a sensor is scheduled to run every minute and each task can take up to 20 minutes. When the default settings with 1 worker are used, there are 16 tasks running after 20 minutes, and each task occupies a worker slot:

![Classic Tree View](/img/guides/classic_tree_view.png)

Because worker slots are held during task execution time, you need a minimum of 20 worker slots to ensure that future runs are not delayed. To increase concurrency, you need to add additional resources such as a worker pod to your Airflow infrastructure. 

```python
from datetime import datetime
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensor
 
with DAG(
   "sync_dag",
   start_date=datetime(2021, 12, 22, 20, 0),
   end_date=datetime(2021, 12, 22, 20, 19),
   schedule="* * * * *",
   catchup=True,
   max_active_runs=32,
   max_active_tasks=32
) as dag:
 
   sync_sensor = DateTimeSensor(
       task_id="sync_task",
       target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
   )
```

By leveraging a deferrable operator for this sensor, you can achieve full concurrency while allowing your worker to complete additional work across your Airflow environment. With the following updated sample DAG, all 20 tasks enter a deferred state. This indicates that the triggers are registered to run in the triggerer process.

![Deferrable Tree View](/img/guides/deferrable_tree_view.png)

```python
from datetime import datetime
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensorAsync
 
with DAG(
   "async_dag",
   start_date=datetime(2021, 12, 22, 20, 0),
   end_date=datetime(2021, 12, 22, 20, 19),
   schedule="* * * * *",
   catchup=True,
   max_active_runs=32,
   max_active_tasks=32
) as dag:
 
   async_sensor = DateTimeSensorAsync(
       task_id="async_task",
       target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
   )
```

## Run deferrable tasks

To start a triggerer process, run `airflow triggerer` in your Airflow environment. Your output should be similar to the following image.

![Triggerer Logs](/img/guides/triggerer_logs.png)

If you are running Airflow on [Astro](https://docs.astronomer.io/cloud/deferrable-operators#prerequisites), the triggerer runs automatically if you are on Astro Runtime 4.0 and later. If you are using Astronomer Software 0.26 and later, you can add a triggerer to an Airflow 2.2 and later deployment in the **Deployment Settings** tab. See [Configure a Deployment on Astronomer Software - Triggerer](https://docs.astronomer.io/enterprise/configure-deployment#triggerer) to configure the triggerer.

As tasks are raised into a deferred state, triggers are registered in the triggerer. You can set the number of concurrent triggers that can run in a single triggerer process with the [`default_capacity`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#triggerer) configuration setting in Airflow. This can also be set with the `AIRFLOW__TRIGGERER__DEFAULT_CAPACITY` environment variable. The default value is `1,000`.

### High availability

Triggers are designed to be highly available. You can implement this by starting multiple triggerer processes. Similar to the [HA scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html#running-more-than-one-scheduler) introduced in Airflow 2.0, Airflow ensures that they co-exist with correct locking and high availability. See [High Availability](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#high-availability) for more information on this topic.

### Create a deferrable operator

If you have an operator that would benefit from being asynchronous but does not yet exist in OSS Airflow or Astronomer Providers, you can create your own. See [Writing Deferrable Operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#writing-deferrable-operators).
