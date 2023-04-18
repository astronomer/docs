---
title: "Airflow sensors"
sidebar_label: "Sensors"
id: what-is-a-sensor
---

<head>
  <meta name="description" content="Get an overview of Airflow sensors and see the new sensor-related features included in Airflow 2. Learn best practices for implementing sensors in production." />
  <meta name="og:description" content="Get an overview of Airflow sensors and see the new sensor-related features included in Airflow 2. Learn best practices for implementing sensors in production." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import sensor_decorator_example from '!!raw-loader!../code-samples/dags/what-is-a-sensor/sensor_decorator_example.py';
import sql_sensor_example_taskflow from '!!raw-loader!../code-samples/dags/what-is-a-sensor/sql_sensor_example_taskflow.py';
import sql_sensor_example_traditional from '!!raw-loader!../code-samples/dags/what-is-a-sensor/sql_sensor_example_traditional.py';

[Apache Airflow sensors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html) are a special kind of operator that are designed to wait for something to happen. When sensors run, they check to see if a certain condition is met before they are marked successful and let their downstream tasks execute. When used properly, they can be a great tool for making your DAGs more event driven.

In this guide, you'll learn how sensors are used in Airflow, best practices for implementing sensors in production, and how to use deferrable versions of sensors.

:::info

Sensors are one of several options to schedule your DAGs in an event-based manner. Learn more about sensors and how they compare to other Airflow features in [Video: Implementing Event-Based DAGs with Airflow](https://airflowsummit.org/sessions/2022/implementing-event-based-dags-with-airflow/). 

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Sensor basics

Sensors are a type of operator that checks if a condition is met at a specific interval. If the condition is met, the task is marked successful and the DAG can move to downstream tasks. If the condition isn't met, the sensor waits for another interval before checking again. 

All sensors inherit from the [`BaseSensorOperator`](https://github.com/apache/airflow/blob/main/airflow/sensors/base.py) and have the following parameters:

- `mode`: How the sensor operates. There are two types of modes:
    - `poke`: This is the default mode. When using `poke`, the sensor occupies a worker slot for the entire execution time and sleeps between pokes. This mode is best if you expect a short runtime for the sensor.
    - `reschedule`: When using this mode, if the criteria is not met then the sensor releases its worker slot and reschedules the next check for a later time. This mode is best if you expect a long runtime for the sensor, because it is less resource intensive and frees up workers for other tasks.
- `poke_interval`: When using `poke` mode, this is the time in seconds that the sensor waits before checking the condition again. The default is 60 seconds.
- `exponential_backoff`: When set to `True`, this setting creates exponentially longer wait times between pokes in `poke` mode.
- `timeout`: The maximum amount of time in seconds that the sensor checks the condition. If the condition is not met within the specified period, the task fails.
- `soft_fail`: If set to `True`, the task is marked as skipped if the condition is not met by the `timeout`.

Different types of sensors have different implementation details.

### Commonly used sensors

Many Airflow provider packages contain sensors that wait for various criteria in different source systems. The following are some of the most commonly used sensors:

- [`@task.sensor` decorator](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html#using-the-taskflow-api-with-sensor-operators): Allows you to turn any Python function that returns a [PokeReturnValue](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/base/index.html#airflow.sensors.base.PokeReturnValue) into an instance of the [BaseSensorOperator](https://registry.astronomer.io/providers/apache-airflow/modules/basesensoroperator) class. This way of creating a sensor is useful when checking for complex logic or if you are connecting to a tool via an API that has no specific sensor available.
- [`S3KeySensor`](https://registry.astronomer.io/providers/amazon/modules/s3keysensor): Waits for a key (file) to appear in an Amazon S3 bucket. This sensor is useful if you want your DAG to process files from Amazon S3 as they arrive.
- [`DateTimeSensor`](https://registry.astronomer.io/providers/apache-airflow/modules/datetimesensor): Waits for a specified date and time. This sensor is useful if you want different tasks within the same DAG to run at different times.
- [`ExternalTaskSensor`](https://registry.astronomer.io/providers/apache-airflow/modules/externaltasksensor): Waits for an Airflow task to be completed. This sensor is useful if you want to implement [cross-DAG dependencies](cross-dag-dependencies.md) in the same Airflow environment.
- [`HttpSensor`](https://registry.astronomer.io/providers/http/modules/httpsensor): Waits for an API to be available. This sensor is useful if you want to ensure your API requests are successful.
- [`SqlSensor`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlsensor): Waits for data to be present in a SQL table. This sensor is useful if you want your DAG to process data as it arrives in your database.

To review the available Airflow sensors, go to the [Astronomer Registry](https://registry.astronomer.io/modules?types=sensors).

### Example implementation

The following example DAG shows how you might use the `SqlSensor` sensor:

<Tabs
    defaultValue="taskflow"
    groupId= "example-implementation"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{sql_sensor_example_taskflow}</CodeBlock>

</TabItem>
<TabItem value="traditional">

<CodeBlock language="python">{sql_sensor_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

This DAG waits for data to be available in a Postgres database before running validation and storing tasks. The `SqlSensor` runs a SQL query and is marked successful when that query returns data. Specifically, when the result is not in the set (0, '0', '', None). The `SqlSensor` task in the example DAG (`waiting_for_partner`) runs the `CHECK_PARTNER.sql` script every 20 seconds (the `poke_interval`) until the data is returned. The `mode` is set to `reschedule`, meaning between each 20 second interval the task will not take a worker slot. The `timeout` is set to 5 minutes, and the task fails if the data doesn't arrive within that time. When the `SqlSensor` criteria is met, the DAG moves to the downstream tasks. You can find the full code for this example in the [webinar-sensors repo](https://github.com/marclamberti/webinar-sensors).

## Sensor decorator

Starting in Airflow 2.5, you can use the `@task.sensor` decorator from the TaskFlow API to use any Python function that returns a `PokeReturnValue` as an instance of the BaseSensorOperator. The following DAG shows how to use the sensor decorator:

<CodeBlock language="python">{sensor_decorator_example}</CodeBlock>

Here, `@task.sensor` decorates the `check_shibe_availability()` function, which checks if a given API returns a 200 status code. If the API returns a 200 status code, the sensor task is marked as successful. If any other status code is returned, the sensor pokes again after the `poke_interval` has passed.

The optional `xcom_value` parameter in `PokeReturnValue` defines what data will be pushed to [XCom](airflow-passing-data-between-tasks.md) once the `is_done=true`. You can use this data in any downstream tasks.

## Sensor best practices

When using sensors, keep the following in mind to avoid potential performance issues:

- Always define a meaningful `timeout` parameter for your sensor. The default for this parameter is seven days, which is a long time for your sensor to be running. When you implement a sensor, consider your use case and how long you expect the sensor to wait and then define the sensor's timeout accurately.
- Whenever possible and especially for long-running sensors, use the `reschedule` mode so your sensor is not constantly occupying a worker slot. This helps avoid deadlocks in Airflow where sensors take all of the available worker slots.
- If your `poke_interval` is very short (less than about 5 minutes), use the `poke` mode. Using `reschedule` mode in this case can overload your scheduler.
- Define a meaningful `poke_interval` based on your use case. There is no need for a task to check a condition every 60 seconds (the default) if you know the total amount of wait time will be 30 minutes.

## Deferrable operators

[Deferrable operators](deferrable-operators.md) (sometimes referred to as asynchronous operators) were released with Airflow 2.2 and are designed to eliminate the problem of any operator or sensor taking up a full worker slot for the entire time they are running. Deferrable versions of many sensors exist in open source Airflow and in the [Astronomer Providers package](https://github.com/astronomer/astronomer-providers). Astronomer recommends using these in most cases to reduce resource costs.

For DAG authors, using deferrable sensors is no different from using regular sensors. All you need is to do is run a `triggerer` process in Airflow and replace the names of all sensors in your DAG code with their deferrable counterparts.  For more details, see [Deferrable operators](deferrable-operators.md). 
