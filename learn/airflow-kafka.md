---
title: "Use Apache Kafka with Apache Airflow"
sidebar_label: "Apache Kafka/Confluent"
description: "How to produce to and consume from Kafka topics using the Airflow Kafka provider"
id: airflow-kafka
sidebar_custom_props: { icon: 'img/integrations/kafka.png' }
---

import CodeBlock from '@theme/CodeBlock';
import produce_consume_treats from '!!raw-loader!../code-samples/dags/airflow-kafka/produce_consume_treats.py';
import listen_to_the_stream from '!!raw-loader!../code-samples/dags/airflow-kafka/listen_to_the_stream.py';
import walking_my_pet from '!!raw-loader!../code-samples/dags/airflow-kafka/walking_my_pet.py';

[Apache Kafka](https://kafka.apache.org/documentation/) is an open source tool for handling event streaming. Combining Kafka and Airflow allows you to build powerful pipelines that integrate streaming data with batch processing.
In this tutorial, you'll learn how to install and use the Airflow Kafka provider to interact directly with Kafka topics.

:::caution

While it is possible to manage a Kafka cluster with Airflow, be aware that Airflow itself should not be used for streaming or low-latency processes. See the [Best practices](#best-practices) section for more information.

:::

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Apache Kafka. See the official [Introduction to Kafka](https://kafka.apache.org/intro).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Quickstart

If you have a GitHub account, you can use the [quickstart repository](https://github.com/astronomer/airflow-kafka-quickstart) for this tutorial, which automatically starts up Airflow and a local Kafka cluster and configures all necessary connections. Clone the repository and skip to [Step 6](#step-6-run-the-dags).

## Prerequisites

- A Kafka cluster with a topic. This tutorial uses a cluster hosted by [Confluent Cloud](https://www.confluent.io/), which has a free trial option. See the [Confluent documentation](https://developer.confluent.io/quickstart/kafka-on-confluent-cloud/) for how to create a Kafka cluster and topic in Confluent Cloud.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

:::info

To connect a [local Kafka cluster](https://kafka.apache.org/documentation/#quickstart) to an Airflow instance running in Docker, set the following properties in your Kafka cluster's `server.properties` file before starting your Kafka cluster:

```text
listeners=PLAINTEXT://:9092,DOCKER_HACK://:19092
advertised.listeners=PLAINTEXT://localhost:9092,DOCKER_HACK://host.docker.internal:19092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,DOCKER_HACK:PLAINTEXT
```

You can learn more about connecting to local Kafka from within a Docker container in [Confluent's Documentation](https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/#scenario-5).

:::

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-kafka-tutorial && cd astro-kafka-tutorial
    $ astro dev init
    ```

2. Add the following packages to your `packages.txt` file:

    ```text
    build-essential
    librdkafka-dev
    ```

3. Add the following packages to your `requirements.txt` file:

    ```text
    confluent-kafka==2.1.1
    apache-airflow-providers-apache-kafka==1.0.0
    ```

4. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 2: Create two Kafka connections

The Apache Kafka Airflow provider uses a Kafka connection provided to the `kafka_conn_id` parameter of each operator to interact with a Kafka cluster. For this tutorial you will define two Kafka connections, because two different consumers will be created.

1. In your web browser, go to `localhost:8080` to access the Airflow UI.

2. Click Admin -> Connections -> **+** to create a new connection.

3. Name your connection `kafka_default` and select the `Generic` connection type. Provide the details for the connection to your Kafka cluster as a JSON in the `Extra` field. If you are connecting to a local Kafka cluster created with the `server.properties` in the info box from the [Prerequisites](#prerequisites) section, use the following configuration:

    ```json
    {
    "bootstrap.servers": "kafka:19092",
    "group.id": "group_1",
    "security.protocol": "PLAINTEXT",
    "auto.offset.reset": "beginning"
    }
    ```

4. Click Save.

5. Create a second new connection. 

6.  Name your second connection `kafka_listener` and select the `Generic` connection type. Provide the same details as in step 2.3, with the exception that you will need to use a different `group.id`. Having a second connection with a different `group.id` is necessary because the DAGs in this tutorial will have two consuming tasks which consume messages from the same Kafka topic. Learn more in [Kafka's Consumer Configs documentation](https://kafka.apache.org/documentation/#consumerconfigs).

7. Click Save.

## Step 3: Create a DAG with a producer and a consumer task

The [Airflow Kafka provider package](https://registry.astronomer.io/providers/apache-airflow-providers-apache-kafka/versions/latest) contains a ProduceToTopicOperator, which you can use to produce messages directly to a Kafka topic, and a ConsumeFromTopicOperator, which you can use to directly consume messages from a topic.

1. Create a new file in your `dags` folder called `produce_consume_treats.py`.

2. Copy and paste the following code into the file:

    <CodeBlock language="python">{produce_consume_treats}</CodeBlock>

    This DAG will produce messages to a Kafka topic (`KAFKA_TOPIC`) and consume them. 

    - The `produce_treats` task produces `num_treats` messages to a Kafka topic, each carrying information containing the pet name, a randomly picked pet mood after the treat has been given and whether or not a treat was the last one in a series. The `ProduceToTopicOperator` accomplishes this by using using a function passed to its `producer_function` parameter which returns a generator containing contains key-value pairs. 
    The number of treats pushed to [XCom](airflow-passing-data-between-tasks.md#what-is-xcom) from the upstream `get_number_of_treats` task is retrieved and supplied to the `producer_function` as a positional argument via the `producer_function_args` parameter. The name of your pet is retrieved in the same fashion from the upstream `get_your_pet_name` task and provided as a kwarg to `producer_function_kwargs`.
    - The `consume_treats` task consumes messages from the same Kafka topic and modifies them using the callable provided to the `apply_function` parameter to print a string to the logs. The pet owner name is retrieved from XCom and supplied as a kwarg via the `apply_function_kwargs` parameter.

3. Run your DAG.

4. View the produced events in your Kafka cluster. The example screenshot below shows 4 messages that have been produced to a topic called `test_topic_1` in Confluent Cloud.

    ![Producer logs](/img/guides/confluent-produced-tasks.png)

5. View the logs of your `consume_treats` task. The consumed events will be listed.

    ![Consumer logs](/img/guides/kafka-producer-logs.png)

:::info

If you have defined a schema for your Kafka topic, the generator needs to return compatible objects. In this example, the generator produces a JSON value.

:::

:::tip

A common use case is to directly connect a blob storage (for example an Amazon S3 bucket) to your Kafka topic as a consumer. The ConsumeFromTopicOperator is helpful if you want to use Airflow to schedule the consuming task. Instead of writing the messages retrieved to the Airflow logs, you can for example write them to S3 using the [S3CreateObjectOperator](https://registry.astronomer.io/providers/amazon/modules/s3createobjectoperator).

:::

## Step 4: Create a listener DAG

A common use case is to run a downstream task when a specific message appears in your Kafka topic. The AwaitMessageTriggerFunctionSensor is a [deferrable operator](https://docs.astronomer.io/learn/deferrable-operators) that will listen to your Kafka topic for a message that fulfills specific criteria.



1. Create a new file in your `dags` folder called `listen_to_the_stream.py`.

2. Copy and paste the following code into the file:

    <CodeBlock language="python">{listen_to_the_stream}</CodeBlock>

    This DAG has one task called `listen_for_mood` which uses the AwaitMessageTriggerFunctionSensor to listen to messages in all topics supplied to its `topics` parameters. For each message which is consumed, the following actions are performed:

    - The message is consumed and processed by the `listen_function` supplied to the `apply_function` parameter of the AwaitMessageTriggerFunctionSensor. Note that the function is supplied in as a dot notation string, this is necessary because the Airflow triggerer component will need to access this function.
    - If the message consumed causes the `listen_function` to return a value, a [TriggerEvent](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html) fires.
    In this example a message about the last treat in a series of treats (`"final_treat": True`) and containing a pet mood listed in `PET_MOODS_NEEDING_A_WALK` will cause a TriggerEvent to be fired.
    - After a TriggerEvent has been fired, the AwaitMessageTriggerFunctionSensor will execute the function provided to the `event_triggered_function` parameter. This function takes in the return value of the `listen_function` as its first parameter (`event`).
    In this example the `event_triggered_function` starts a downstream DAG called `walking_my_pet` using the `.execute()` method of the `TriggerDagRunOperator`. The `pet_name` is provided to the downstream DAG via the `conf` parameters and `wait_for_completion` is set to True, causing the execution of the `event_triggered_function` to wait until the `walking_my_pet` DAG has completed. (Learn more about the [TriggerDagRunOperator](cross-dag-dependencies#triggerdagrunoperator)).
    - After the `event_triggered_function` has completed, the AwaitMessageTriggerFunctionSensor goes back into a deferred state.

    The AwaitMessageTriggerFunctionSensor will always be running and listening. In case the task fails, for example due to a malformed message being consumed, the DAG will complete as failed and automatically start its next DAG run thanks to the [`@continuous` schedule](scheduling-in-airflow.md#continuous-timetable).


## Step 5: Create a downstream DAG

The `event_triggered_function` of the AwaitMessageTriggerFunctionSensor operator starts a downstream DAG, in this step you will add this DAG to your environment.

1. Create a new file in your `dags` folder called `walking_my_pet.py`.

2. Copy and paste the following code into the file:

    <CodeBlock language="python">{walking_my_pet}</CodeBlock>

    This DAG only has one task that picks a random amount of minutes your pet will go for a walk with you. Note that the `walking_your_pet` task retrieves the `pet_name` from the [Airflow context `params`](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/params.html). The name of your pet was injected into this DAG's context via the `conf` parameter of the `TriggerDagRunOperator` in the `event_triggered_function` of the `listen_for_mood` task in the `listen_to_the_stream` DAG. 

## Step 6: Run the DAGs

Now that all 3 DAGs are ready, lets see how they work together.

1. Make sure all DAGs are unpaused in the Airflow UI and that your Kafka cluster is running.

2. Notice how the `listen_to_the_stream` DAG will immediately start running once it is unpaused with the `listen_for_mood` task going into a deferred state (purple square).

    ![Kafka deferred state](/img/guides/kafka-deferred-task.png)

3. Manually run the `produce_consume_treats` DAG to give your pet some treats (and produce a few messages to the Kafka cluster).

4. Check the logs of the `listen_for_mood` task in the `listen_to_the_stream` DAG to see if a message fitting the criteria defined by the `listen_function` has been detected. It is possible that you will need to run the `produce_consume_treats` DAG a couple of times for such a message to appear.

    If the TriggerEvent of the `listen_for_mood` task fires, you will see the run of the `walking_my_pet` DAG being intiated from within the `listen_for_mood` task logs.

    ![Kafka logs TDRO](/img/guides/kafka_tdro.png)


5. Finally, check the logs of the `walking_my_pet` task to see how long your pet enjoyed their walk!

## Best practices

Apache Kafka is a tool optimized for streaming messages at high frequencies, for example in an IoT application. Airflow is designed to handle orchestration of data pipelines in batches.

Astronomer recommends to combine these two open source tools by handling low-latency processes with Kafka and data orchestration with Airflow.

Common patterns include:

- Configuring a Kafka cluster with a blob storage like S3 as a sink. Batch process data from S3 at regular intervals.
- Using the ProduceToTopicOperator in Airflow to produce messages to a Kafka cluster as one of several producers.
- Consuming data from a Kafka cluster via the ConsumeFromTopicOperator in batches using the apply function to extract and load information to a blob storage or data warehouse.
- Listening for specific messages in a data stream running through a Kafka cluster using the AwaitMessageTriggerFunctionSensor to trigger downstream tasks once the message appears.

## Conclusion

Congratulations! You now know how to use the Apache Kafka Airflow provider to directly interact with a Kafka topic from within Apache Airflow.
