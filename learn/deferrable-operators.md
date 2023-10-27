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

With Airflow 2.2 and later, you can use deferrable operators to run tasks in your Airflow environment. These operators leverage the Python [asyncio](https://docs.python.org/3/library/asyncio.html) library to efficiently run tasks waiting for an external resource to finish. This frees up your workers and allows you to utilize resources more effectively. In this guide, you'll review deferrable operator concepts and learn how to use deferrable operators in your DAGs.

:::tip Other ways to learn:

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: Deferrable Operators](https://academy.astronomer.io/astro-runtime-deferrable-operators) module.
- Webinar: [Astronomer Providers](https://www.astronomer.io/events/webinars/astronomer-providers/).

:::

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

With deferrable operators, worker slots are released when a task is polling for the job status. When the task is deferred, the polling process is offloaded as a trigger to the triggerer, and the worker slot becomes available. The triggerer can run many asynchronous polling tasks concurrently, and this prevents polling tasks from occupying your worker resources. When the terminal status for the job is received, the task resumes, taking a worker slot while it finishes. The following image illustrates this process:

![Deferrable Worker](/img/guides/deferrable_operator_process.png)

There are numerous benefits to using deferrable operators including:

- Reduced resource consumption: Depending on the available resources and the workload of your triggers, you can run hundreds to thousands of deferred tasks in a single triggerer process. This can lead to a reduction in the number of workers needed to run tasks during periods of high concurrency. With less workers needed, you are able to scale down the underlying infrastructure of your Airflow environment.
- Resiliency against restarts: Triggers are stateless by design. This means your deferred tasks are not set to a failure state if a triggerer needs to be restarted due to a deployment or infrastructure issue. When a triggerer is back up and running in your environment, your deferred tasks will resume.

:::tip

When you can't use a deferrable operator for a longer running sensor task, such as when you can't run a triggerer, Astronomer recommends using a sensor in [`reschedule` mode](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html) to reduce unnecessary resource overhead. See the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#difference-between-mode-reschedule-and-deferrable-true-in-sensors) for details about the differences between deferrable operators and schedulers in `reschedule` mode.

:::

## Use deferrable operators

Deferrable operators should be used whenever you have tasks that occupy a worker slot while polling for a condition in an external system. For example, using deferrable operators for sensor tasks can provide efficiency gains and reduce operational costs. Use deferrable operators instead of Smart Sensors, which were removed in Airflow 2.4.0.

### Start a triggerer

To use deferrable operators, you must have a triggerer running in your Airflow environment. If you are running Airflow on [Astro](https://docs.astronomer.io/astro) or using the [Astro CLI](https://docs.astronomer.io/astro/cli/overview), the triggerer runs automatically if you are on Astro Runtime 4.0 and later. If you are using Astronomer Software 0.26 and later, you can add a triggerer to an Airflow 2.2 and later deployment in the **Deployment Settings** tab. See [Configure a Deployment on Astronomer Software - Triggerer](https://docs.astronomer.io/enterprise/configure-deployment#triggerer) to configure the triggerer.

If you are not using Astro, run `airflow triggerer` to start a triggerer process in your Airflow environment. Your output should look similar to the following image:

![Triggerer Logs](/img/guides/triggerer_logs.png)

As tasks are raised into a deferred state, triggers are registered in the triggerer. You can set the number of concurrent triggers that can run in a single triggerer process with the [`default_capacity`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#triggerer) configuration setting in Airflow. This config can also be set with the `AIRFLOW__TRIGGERER__DEFAULT_CAPACITY` environment variable. The default value is `1000`.

### Use deferrable versions of operators

Many Airflow operators, such as the [TriggerDagRunOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/TriggerDagRunOperator) and the [WasbBlobSensor](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest/modules/WasbBlobSensor), can be set to run in deferrable mode using the `deferrable` parameter. You can check if the operator you want to use has a `deferrable` parameter in the [Astronomer Registry](https://registry.astronomer.io/).

To always use the deferrable version of an operator if it's available in Airflow 2.7+, set the Airflow config `operators.default_deferrable` to `True`. You can do so by defining the following environment variable in your Airflow environment:

```text
AIRFLOW__OPERATORS__DEFAULT_DEFERRABLE=True
```

After you set the variable, all operators with a `deferrable` parameter will run as their deferrable version by default. You can override the config setting at the operator level using the `deferrable` parameter directly:

```python
trigger_dag_run = TriggerDagRunOperator(
   task_id="task_in_downstream_dag",
   trigger_dag_id="downstream_dag",
   wait_for_completion=True,
   poke_interval=20,
   deferrable=False,  # turns off deferrable mode just for this operator instance
)
```

If the operator you want to use does not have a `deferrable` parameter, you can look for a separate deferrable version of the operator in the [Astronomer Registry](https://registry.astronomer.io/). These operators usually have the same name as the original operator, but with the word `Async` appended to the end. For example, the [TimeSensorAsync](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/TimeSensorAsync) is the deferrable version of the [TimeSensor](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/TimeSensor).

To use a deferrable version of a core Airflow operator in your DAG, you only need to replace the import statement for the existing operator. For example, to use TimeSensorAsync instead of the TimeSensor, remove your existing `import` statement and replace it with an import of `TimeSensorAsync` that is aliased as `TimeSensor`:

```python
# Remove this import:
# from airflow.operators.sensors import TimeSensor
# Replace with:
from airflow.sensors.time_sensor import TimeSensorAsync as TimeSensor
```

If you are using a deferrable operator that is part of a provider package, you will also need to ensure that package is installed in your Airflow environment. For example, to use the deferrable Snowflake operator [SnowflakeOperatorAsync](https://registry.astronomer.io/providers/astronomer-providers/versions/latest/modules/SnowflakeOperatorAsync) from the [Astronomer Providers](https://github.com/astronomer/astronomer-providers) package:

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

Note that importing the asynchronous operator using the alias of the analogous traditional operator (e.g. `import SnowflakeOperatorAsync as SnowflakeOperator`) is simply to make updating existing DAGs easier. This is not required, and may not be preferable when authoring a new DAG.

## Available deferrable operators

The easiest way to check if an operator has a `deferrable` parameter or an `-Async` version is to search the [Astronomer Registry](https://registry.astronomer.io/). 

Some deferrable operators are installed by default in Airflow, including the [TimeSensorAsync](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/TimeSensorAsync)
and [TriggerDagRunOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/TriggerDagRunOperator). 

Other deferrable operators are available in provider packages, including many built and maintained by Astronomer as part of the open source [Astronomer Providers](https://github.com/astronomer/astronomer-providers) Python package. For a full list of deferrable operators and sensors available in the `astronomer-providers` package, see the [Astronomer providers documentation](https://astronomer-providers.readthedocs.io/en/stable/providers/operators_and_sensors_list.html). 

## Example workflow

The following example DAG is scheduled to run every minute between its `start_date` and its `end_date`. Every DAG run contains one sensor task that will potentially take up to 20 minutes to complete.

<CodeBlock language="python">{sync_dag}</CodeBlock>

Using `DateTimeSensor`, one worker slot is taken up by every sensor that runs. By using the deferrable version of this sensor, `DateTimeSensorAsync`, you can achieve full concurrency while freeing up your workers to complete additional tasks across your Airflow environment. 

In the following screenshot, running the DAG produces 16 running task instances, each containing one active `DateTimeSensor` taking up one worker slot.

![Standard sensor Grid View](/img/guides/standard_sensor_slot_taking.png)

Because Airflow imposes default limits on the number of active runs of the same DAG or number of active tasks in a DAG across all runs, you'll have to scale up Airflow to concurrently run any other DAGs and tasks as described in the [Scaling Airflow to optimize performance](airflow-scaling-workers.md) guide.

Switching out the `DateTimeSensor` for `DateTimeSensorAsync` will create 16 running DAG instances, but the tasks for these DAGs are in a deferred state which does not take up a worker slot. The only difference in the DAG code is using the deferrable operator `DateTimeSensorAsync` over `DateTimeSensor`:

<CodeBlock language="python">{async_dag}</CodeBlock>

In the following screenshot, all tasks are shown in a deferred (violet) state. Tasks in other DAGs can use the available worker slots, making the deferrable operator more cost and time-efficient.

![Deferrable sensor Grid View](/img/guides/deferrable_grid_view.png)

## High availability

Triggers are designed to be highly available. You can implement this by starting multiple triggerer processes. Similar to the [HA scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html#running-more-than-one-scheduler) introduced in Airflow 2.0, Airflow ensures that they co-exist with correct locking and high availability. See [High Availability](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#high-availability) for more information on this topic.

## Create a deferrable operator

If you have an operator that would benefit from being asynchronous but does not yet exist in OSS Airflow or Astronomer Providers, you can create your own. See [Writing Deferrable Operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#writing-deferrable-operators).
