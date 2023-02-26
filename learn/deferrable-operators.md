---
title: "Deferrable operators"
sidebar_label: "Deferrable operators"
description: "Implement deferrable operators to save cost and resources with Airflow."
id: deferrable-operators
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import sync_dag from '!!raw-loader!../code-samples/dags/deferrable-operators/sync_dag.py';
import async_dag from '!!raw-loader!../code-samples/dags/deferrable-operators/async_dag.py';

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

To use a deferrable version of a core Airflow operator in your DAG, you only need to replace the import statement for the existing operator. For example, Airflow's `TimeSensorAsync` is a replacement of the non-deferrable `TimeSensor` ([source](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/time_sensor/index.html?highlight=timesensor#module-contents)). To use `TimeSensorAsync`, remove your existing `import` and replace it with the following:

```python
# Remove this import:
# from airflow.operators.sensors import TimeSensor
# Replace with:
from airflow.sensors.time_sensor import TimeSensorAsync as TimeSensor
```

If you are using a deferrable operator that is part of the [Astronomer Providers](https://github.com/astronomer/astronomer-providers) package, you will also need to ensure that package is installed in your Airflow environment. For example, to use the Snowflake deferrable operator:

1. Add the following to your `requirements.txt` file:

   ```python
   astronomer-providers[snowflake]
   ```

2. Update the import statement in your DAG:

   ```python
   # Remove this import:
   # from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
   # Replace with:
   from astronomer.providers.snowflake.operators.snowflake import (
      SnowflakeOperatorAsync as SnowflakeOperator,
   )
   ```

Note that importing the asynchronous operator using the alias of the analogous traditional operator (e.g. `import SnowflakeOperatorAsync as SnowflakeOperator`) is simply to make updating existing DAGs easier. This is not required, and may not be preferrable when authoring a new DAG.

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

The example DAG below is scheduled to run once for every minute within a defined time-frame (between its `start_date` and its `end_date`). Every DAG run contains one task using sensor that will potentially take up to 20 minutes to complete.

When using the **Classical sensor** `DateTimeSensor` with default settings one worker slot is taken up by every sensor that runs. By leveraging a **Deferrable operator** for this sensor, the `DateTimeSensorAsync` you can achieve full concurrency while allowing your workers to complete additional work across your Airflow environment. 

<Tabs
    defaultValue="classical"
    groupId= "datetime-async"
    values={[
        {label: 'Classical sensor', value: 'classical'},
        {label: 'Deferrable operator', value: 'deferrable'},
    ]}>

<TabItem value="classical">

The screenshot below shows 16 running DAG instances, each taking up one worker slot.

![Classic Tree View](/img/guides/classic_sensor_slot_taking.png)

The DAG code uses a classic sensor and default configuration of concurrency:

<CodeBlock language="python">{sync_dag}</CodeBlock>

</TabItem>

The screenshot below shows 16 DAG instances running, each with one task in a deferred state (violet square) which does not take up a worker slot. Tasks in other DAGs can use the available worker slots making the version using a deferrable operator more cost and time-efficient.

<TabItem value="deferrable">

![Deferrable Tree View](/img/guides/deferrable_grid_view.png)

The only difference in the DAG code is using the deferrable operator `DateTimeSensorAsync` over `DateTimeSensor`:

<CodeBlock language="python">{async_dag}</CodeBlock>

</TabItem>
</Tabs>

By default only 16 active DAG runs will be scheduled and only 16 tasks can be active (not in a deferred state) in a DAG. To increase concurrency, increase the value of the DAG following parameters:

- `max_active_runs` to allow for more active DAG runs 
- `max_active_task` to allow for more active tasks per DAG run.

Learn more about concurrency and parallelism parameters in the [Scaling Airflow to optimize performance](airflow-scaling-workers.md) guide.

## Run deferrable tasks

To start a triggerer process, run `airflow triggerer` in your Airflow environment. Your output should be similar to the following image.

![Triggerer Logs](/img/guides/triggerer_logs.png)

If you are running Airflow on [Astro](https://docs.astronomer.io/cloud/deferrable-operators#prerequisites), the triggerer runs automatically if you are on Astro Runtime 4.0 and later. If you are using Astronomer Software 0.26 and later, you can add a triggerer to an Airflow 2.2 and later deployment in the **Deployment Settings** tab. See [Configure a Deployment on Astronomer Software - Triggerer](https://docs.astronomer.io/enterprise/configure-deployment#triggerer) to configure the triggerer.

As tasks are raised into a deferred state, triggers are registered in the triggerer. You can set the number of concurrent triggers that can run in a single triggerer process with the [`default_capacity`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#triggerer) configuration setting in Airflow. This can also be set with the `AIRFLOW__TRIGGERER__DEFAULT_CAPACITY` environment variable. The default value is `1,000`.

### High availability

Triggers are designed to be highly available. You can implement this by starting multiple triggerer processes. Similar to the [HA scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html#running-more-than-one-scheduler) introduced in Airflow 2.0, Airflow ensures that they co-exist with correct locking and high availability. See [High Availability](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#high-availability) for more information on this topic.

### Create a deferrable operator

If you have an operator that would benefit from being asynchronous but does not yet exist in OSS Airflow or Astronomer Providers, you can create your own. See [Writing Deferrable Operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#writing-deferrable-operators).
