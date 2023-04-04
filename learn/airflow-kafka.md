---
title: "Use Apache Kafka with Apache Airflow"
sidebar_label: "Apache Kafka/Confluent"
description: "How to produce to and consume from Kafka topics using the Airflow Kafka provider"
id: airflow-kafka
sidebar_custom_props: { icon: 'img/integrations/kafka.png' }
---

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
    mkdir astro-kafka-tutorial && cd astro-kafka-tutorial
    astro dev init
    ```

2. Add the following packages to your `packages.txt` file:

    ```text
    build-essential
    librdkafka-dev
    ```

3. Add the following packages to your `requirements.txt` file:

    ```text
    confluent-kafka==1.8.2
    airflow-provider-kafka
    ```

:::info

If you are running Airflow as a standalone application and are using an M1 Mac, complete the additional setup in the [`airflow-provider-kafka` README](https://github.com/astronomer/airflow-provider-kafka#setup-on-m1-mac).

:::

4. Add the following environment variables in `.env`. Provide your own Kafka topic name, boostrap server, API Key and API Secret.

    ```text
    KAFKA_TOPIC_NAME=<your-kafka-topic-name>
    BOOSTRAP_SERVER=<your-bootstrap-server>
    SECURITY_PROTOCOL=SASL_SSL
    KAFKA_API_KEY=<your-api-key>
    KAFKA_API_SECRET=<your-api-secret>
    ```

:::info

If you are connecting to the local Kafka server created with the `server.properties` in the info box from the [Prerequisites](#prerequisites) section you will need to set `BOOTSTRAP_SERVER=host.docker.internal:19092`, `SECURITY_PROTOCOL=PLAINTEXT` and provide your topic name. You can set the API Key and API Secret to `None`.

:::

5. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 2: Create a DAG with a producer task

The [Airflow Kafka provider package](https://github.com/astronomer/airflow-provider-kafka) contains the ProduceToTopicOperator, which you can use to produce events directly to a Kafka topic.

1. Create a new file in your `dags` folder called `kafka_example_dag_1.py`.

2. Copy and paste the following code into the file:

    ```python
    # kafka_example_dag_1.py 

    import os
    import json
    import logging
    import functools
    from pendulum import datetime

    from airflow import DAG
    from airflow_provider_kafka.operators.produce_to_topic import ProduceToTopicOperator

    # get the topic name from .env
    my_topic = os.environ["KAFKA_TOPIC_NAME"]

    # get Kafka configuration information
    connection_config = {
        "bootstrap.servers": os.environ["BOOSTRAP_SERVER"],
        "security.protocol": os.environ["SECURITY_PROTOCOL"],
        "sasl.mechanism": "PLAIN",
        "sasl.username": os.environ["KAFKA_API_KEY"],
        "sasl.password": os.environ["KAFKA_API_SECRET"]
    }

    with DAG(
        dag_id="kafka_example_dag_1",
        start_date=datetime(2022, 11, 1),
        schedule=None,
        catchup=False,
    ):

        # define the producer function
        def producer_function():
            for i in range(5):
                yield (json.dumps(i), json.dumps(i+1))

        # define the producer task
        producer_task = ProduceToTopicOperator(
            task_id=f"produce_to_{my_topic}",
            topic=my_topic,
            producer_function=producer_function, 
            kafka_config=connection_config
        )
    ```

    The code above retrieves the environment variables you defined in [Step 1](#step-1-configure-your-astro-project) and packages them into a configuration dictionary that can be used by the ProduceToTopicOperator. Any Python function which returns a generator can be passed to the `producer_function` parameter of the ProduceToTopicOperator. Make sure your producer function returns a generator that contains key-value pairs where the value is in a format your Kafka topic accepts as input. In this example, the generator produces a JSON value. Additionally, if you have defined a schema for your Kafka topic, the generator needs to return compatible objects.

3. Run your DAG.

4. View the logs of your task instance. The 5 produced events will be listed.

    ![Producer logs](/img/guides/kafka-producer-logs.png)

5. View the produced events in your Kafka cluster. The example screenshot below shows them in the Confluent Cloud.

    ![Producer logs](/img/guides/confluent-produced-tasks.png)

## Step 3: Add a consumer task

The ConsumeFromTopicOperator enables Airflow to consume messages from topics.

1. Add the following import statement to `kafka_example_dag_1`.

    ```python
    from airflow_provider_kafka.operators.consume_from_topic import ConsumeFromTopicOperator
    ```

2. Add the following code after the `producer_task` in `kafka_example_dag_1`.

    ```python
    consumer_logger = logging.getLogger("airflow")

    def consumer_function(message, prefix=None):
        try:
            key = json.loads(message.key())
            value = json.loads(message.value())
            consumer_logger.info(f"{prefix} {message.topic()} @ {message.offset()}; {key} : {value}")
            return
        except:
            consumer_logger.info(f"Unable to consume message!")
            return

    consumer_task = ConsumeFromTopicOperator(
        task_id=f"consume_from_{my_topic}",
        topics=[my_topic],
        apply_function=functools.partial(consumer_function, prefix="consumed:::"),
        consumer_config={
            **connection_config
            "group.id": "consume",
            "enable.auto.commit": False,
            "auto.offset.reset": "beginning",
        },
        max_messages=30,
        max_batch_size=10,
    )

    producer_task >> consumer_task

    ```

   The `consumer_task` includes a function that reads from `my_topic` and prints the messages it consumes to the Airflow task log. The `consumer_task` uses the same `connection_config` as the `producer_task` with added configurations specific to Kafka Consumers. You can read more about consumer configuration in Kafka in the [Kafka documentation](https://kafka.apache.org/documentation/#consumerconfigs).

3. Run your DAG.

4. View the consumed messages in your Airflow task logs.

    ![Consumer log](/img/guides/kafka-consumer-logs.png)

:::tip

A common use case is to directly connect a blob storage (for example an Amazon S3 bucket) to your Kafka topic as a consumer. The ConsumeFromTopicOperator is helpful if you want to use Airflow to schedule the consuming task. Instead of writing the messages retrieved to the Airflow logs, you can for example write them to S3 using the [S3CreateObjectOperator](https://registry.astronomer.io/providers/amazon/modules/s3createobjectoperator).

:::

## Step 4: Listen for a message in the stream

A common use case is to run a downstream task when a specific message appears in your Kafka topic. The AwaitKafkaMessageOperator is a deferrable operator that will listen to your Kafka topic for a message that fulfills a specific criteria.

A deferrable operator is a sensor that will go into a deferred state in between checking for its condition in the target system. While in the deferred state the operator does not take up a worker slot, offering a significant efficiency improvement. See [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators).

1. In `kafka_example_dag_1`, add the following import statement:

    ```python
    from airflow_provider_kafka.operators.await_message import AwaitKafkaMessageOperator
    ```

2. Copy and paste the following code at the end of your DAG:

    ```python
    def await_function(message):
        if isinstance(json.loads(message.value()), int):
            if json.loads(message.value()) % 5 == 0:
                return f" Got the following message: {json.loads(message.value())}"

    await_message = AwaitKafkaMessageOperator(
        task_id=f"awaiting_message_in_{my_topic}",
        topics=[my_topic],
        # the apply function needs to be passed with its location for the triggerer
        apply_function="kafka_example_dag_1.await_function", 
        kafka_config={
            **connection_config
            "group.id": "awaiting_message",
            "enable.auto.commit": False,
            "auto.offset.reset": "beginning",
        },
        xcom_push_key="retrieved_message",
    )

    consumer_task >> await_message
    ```

    This code snippet includes an `await_function` which will parse each message in the Kafka topic and return the message if the value is an integer divisible by 5. The AwaitKafkaMessageOperator runs this function over messages polled from the Kafka topic. If no matching message is found, it continues to poll in a deferred state until it finds one.

3. Run the DAG. Notice how the task instance of the `await_message` task goes into a deferred state (purple square).

    ![Kafka deferred state](/img/guides/kafka-deferred-state.png)

4. (Optional) Add a downstream task to the `await_message` task, which only runs once `await_message` has completed successfully.

## How it works

The `airflow-kafka-provider` contains three hooks:

- `KafkaAdminClientHook`
- `KafkaConsumerHook`
- `KafkaProducerHook`

It uses four operators and one trigger:

- `ProduceToTopicOperator`
- `ConsumeFromTopicOperator`
- `AwaitKafkaMessageOperator`
- `EventTriggersFunctionOperator`
- `AwaitMessageTrigger`

The following section provides more detailed information on the parameters of each operator. For more information on the other modules in this provider see the [`airflow-provider-kafka`](https://github.com/astronomer/airflow-provider-kafka) source code.

### ProduceToTopicOperator

The ProduceToTopicOperator can be used to create a Kafka producer to produce messages to a Kafka topic. You can define the following parameters:

- `topic`: The Kafka topic you want to produce to.
- `producer_function`: A Python function that returns a generator that will create key/value pairs to be produced to Kafka as messages.
- `producer_function_args`: Positional arguments for the `producer_function`.
- `producer_function_kwargs`: Keyword arguments for the `producer_function`.
- `delivery_callback`: A custom function to be executed after each message that was produced to the Kafka topic (in case of success and failure). If no function is provided the ProduceToTopicOperator will log the produced record in case of success and an error message in case of failure.
- `synchronous`: Specifies if writing to Kafka should be fully synchronous. True by default.
- `kafka_config`: The configuration for the Kafka client, including the connection information. For a full list of parameters please refer to the [librdkafka GitHub repository](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md).
- `poll_timeout`: The delay between production to Kafka and calling [poll](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.Producer.poll) on the producer.

### ConsumeFromTopicOperator

The ConsumeFromTopicOperator can be used to create a Kafka consumer to read batches of messages and process them. You can define the following parameters:

- `topics`: A list of topics or regex patterns for the consumer to subscribe to i.e. read from.
- `apply_function`: A Python function that is applied to all messages that are read.
- `apply_function_args`: Positional arguments for the `apply_function`.
- `apply_function_kwargs`: Keyword arguments for the `apply_function`.
- `consumer_config`: The configuration for the Kafka client, including the connection information. For a full list of parameters please refer to the [librdkafka GitHub repository](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md).
- `commit_cadence`: In which situations the Kafka consumer created should commit offsets. The 3 options `end_of_operator` (default), `never` and `end_of_batch` are available.
- `max_messages`: Maximum number of messages the Kafka consumer created by this instance of the ConsumeFromTopicOperator can read from its topics.
- `max_batch_size`: Maximum number of messages the Kafka consumer can read when polling. The default is 1000.
- `poll_timeout`: How long the Kafka Consumer created should wait for potentially incoming messages after having read all currently available messages before ending its task. The default is 60 seconds.

### AwaitKafkaMessageOperator

The AwaitKafkaMessageOperator is a [deferrable operator](https://docs.astronomer.io/learn/deferrable-operators) that can be used to wait for a specific message to be published to one or more Kafka topics. You can define the following parameters:

- `topics`: A list of topics or regex patterns to read from.
- `apply_function`: A Python function that is applied to all messages that are read. If the function returns any data the task will be ended and marked as successful. The returned data will be pushed to XCom unless the BaseOperator argument `do_xcom_push` is set to `False`.
- `apply_function_args`: Positional arguments for the `apply_function`.
- `apply_function_kwargs`: Keyword arguments for the `apply_function`.
- `kafka_config`: The configuration for the Kafka client, including the connection information. For a full list of parameters please refer to the [librdkafka GitHub repository](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md).
- `poll_timeout`: The amount of time in seconds that the task should wait for a message in its active state.
- `poll_interval`: The amount of time in seconds that the task should wait in the deferred state.
- `xcom_push_key`: The key under which to save the returned data to XCom.

### EventTriggersFunctionOperator

The EventTriggersFunctionOperator is a [deferrable operator](https://docs.astronomer.io/learn/deferrable-operators) that waits for a specific message to be published to one or more Kafka topics, similar to the AwaitKafkaMessageOperator. Unlike the AwaitKafkaMessageOperator, the EventTriggersFunctionOperator will continue listening until the task is stopped by an external criterion such as a timeout of the DAG itself. If this external criterion isn't met, this task will stay in a deferred state indefinitely as long as the DAG is running. You can view an example DAG using this operator in the [`astronomer-providers` repository](https://github.com/astronomer/airflow-provider-kafka/blob/main/example_dags/listener_dag_function.py).

You can define the following parameters for this operator:

- `topics`: A list of topics or regex patterns to read from.
- `apply_function`: A Python function that is applied to all messages that are read. If the function returns any data, the `event_triggered_function` will run.
- `event_triggered_function`: A Python function that runs every time the operator consumes a message that causes the `apply_function` to return any data. The value returned by the `apply_function` is passed to the function provided to `event_triggered_function` as the first positional parameter.
- `apply_function_args`: Positional arguments for the `apply_function`.
- `apply_function_kwargs`: Keyword arguments for the `apply_function`.
- `kafka_config`: The configuration for the Kafka client, including the connection information. For a full list of parameters, see the [librdkafka GitHub repository](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md).
- `poll_timeout`: The amount of time in seconds that the task should wait for a message in its active state.
- `poll_interval`: The amount of time in seconds that the task should wait in the deferred state.

## Best practices

Apache Kafka is a tool optimized for streaming messages at high frequencies, for example in an IoT application. Airflow is designed to handle orchestration of data pipelines in batches.

Astronomer recommends to combine these two open source tools by handling low-latency processes with Kafka and data orchestration with Airflow.

Common patterns include:

- Configuring a Kafka cluster with a blob storage like S3 as a sink. Batch process data from S3 at regular intervals.
- Using the ProduceToTopicOperator in Airflow to produce messages to a Kafka cluster as one of several producers.
- Consuming data from a Kafka cluster via the ConsumeFromTopicOperator in batches using the apply function to extract and load information to a blob storage or data warehouse.
- Listening for specific messages in a data stream running through a Kafka cluster using the AwaitKafkaMessageOperator to trigger downstream tasks once the message appears.

## Conclusion

The Airflow Kafka provider offers 3 easy to use operators to interact with topics and messages in Kafka. You now know how to use these operators to connect Kafka and Airflow.
