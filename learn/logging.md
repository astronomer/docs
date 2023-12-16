---
title: "Airflow logging"
sidebar_label: "Airflow logging"
description: "An introduction to Airflow logging."
id: logging
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import custom_logs_taskflow from '!!raw-loader!../code-samples/dags/logging/custom_logs_taskflow.py';
import custom_logs_traditional from '!!raw-loader!../code-samples/dags/logging/custom_logs_traditional.py';

Airflow provides an extensive logging system for monitoring and debugging your data pipelines. Your webserver, scheduler, metadata database, and individual tasks all generate logs. You can export these logs to a local file, your console, or to a specific remote storage solution.

In this guide, you'll learn the basics of Airflow logging, including:

- Where to find logs for different Airflow components.
- How to add custom task logs from within a DAG.
- When and how to configure logging settings.
- Remote logging.

You'll also use example code to:

- Send logs to an S3 bucket using the [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- Add multiple handlers to the Airflow task logger.

In addition to standard logging, Airflow provides observability features that you can use to collect metrics, trigger callback functions with task events, monitor Airflow health status, and track errors and user activity. For more information about the monitoring options in Airflow, see [Logging & Monitoring](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/index.html). Astro builds on these features, providing more detailed metrics about how your tasks run and use resources in your cloud. To learn more, see [Deployment metrics](https://docs.astronomer.io/astro/deployment-metrics).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow core components. See [Airflow's components](airflow-components.md).

## Airflow logging

Logging in Airflow leverages the [Python stdlib `logging` module](https://docs.python.org/3/library/logging.html). The `logging` module includes the following classes:

- Loggers (`logging.Logger`): The interface that the application code directly interacts with. Airflow defines 4 loggers by default: `root`, `flask_appbuilder`, `airflow.processor` and `airflow.task`.
- Handlers (`logging.Handler`): Send log records to their destination. By default, Airflow uses `RedirectStdHandler`, `FileProcessorHandler` and `FileTaskHandler`.
- Filters (`logging.Filter`): Determine which log records are emitted. Airflow uses `SecretsMasker` as a filter to prevent sensitive information from being printed into logs.
- Formatters (`logging.Formatter`): Determine the layout of log records. Two formatters are predefined in Airflow:
    - `airflow_colored`: `"[%(blue)s%(asctime)s%(reset)s] {%(blue)s%(filename)s:%(reset)s%(lineno)d} %(log_color)s%(levelname)s%(reset)s - %(log_color)s%(message)s%(reset)s"`
    - `airflow`: `"[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"`

See [Logging facility for Python](https://docs.python.org/3/library/logging.html) for more information on the methods available for these classes, including the attributes of a LogRecord object and the 6 available levels of logging severity (`CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, and `NOTSET`).

The four default loggers in Airflow each have a handler with a predefined log destination and formatter:

- `root` (level: `INFO`): Uses `RedirectStdHandler` and `airflow_colored`. It outputs to `sys.stderr/stout` and acts as a catch-all for processes which have no specific logger defined.
- `flask_appbuilder` (level: `WARNING`): Uses `RedirectStdHandler` and `airflow_colored`. It outputs to `sys.stderr/stout`. It handles logs from the webserver.
- `airflow.processor` (level: `INFO`): Uses `FileProcessorHandler` and `airflow`. It writes logs from the scheduler to the local file system.
- `airflow.task` (level: `INFO`): Uses `FileTaskHandlers` and `airflow`. It writes task logs to the local file system.

By default, log file names have the following format:

- For standard tasks: `dag_id={dag_id}/run_id={run_id}/task_id={task_id}/attempt={try_number}.log`
- For [dynamically mapped tasks](dynamic-tasks.md): `dag_id={dag_id}/run_id={run_id}/task_id={task_id}/map_index={map_index}/attempt={try_number}.log`

These filename formats can be reconfigured using `log_filename_template` in `airflow.cfg`.

You can view the full default logging configuration under `DEFAULT_LOGGING_CONFIG` in the [Airflow source code](https://github.com/apache/airflow/blob/main/airflow/config_templates/airflow_local_settings.py).

The Airflow UI shows logs using a `read()` method on task handlers which is not part of stdlib. `read()` checks for available logs and displays them in a predefined order:

- Remote logs (if remote logging is enabled)
- Logs on the local filesystem
- Logs from [worker specific webserver subprocesses](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-log-server-port)

 When using the Kubernetes Executor and a worker pod still exists, `read()` shows the first 100 lines from the Kubernetes pod logs. If a worker pod spins down, the logs are no longer available. For more information, see [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/).  

## Log locations

By default, Airflow outputs logs to the `base_log_folder` configured in `airflow.cfg`, which is located in your `$AIRFLOW_HOME` directory.

### Local Airflow environment

If you run Airflow locally, logging information is accessible in the following locations:

- Scheduler: Logs are printed to the console and accessible in `$AIRFLOW_HOME/logs/scheduler`.
- Webserver and Triggerer: Logs are printed to the console. As of Airflow 2.6, individual triggers' log messages can be found in the logs of tasks that use deferrable operators.
- Task: Logs can be viewed in the Airflow UI or at `$AIRFLOW_HOME/logs/`. To view task logs directly in your terminal, run `astro dev run tasks test <dag_id> <task_id>` with the [Astro CLI](https://docs.astronomer.io/astro/cli/overview) or `airflow tasks test <dag_id> <task_id>` if you are running Airflow with other tools.
- Metadata database: Logs are handled differently depending on which database you use.

### Docker Airflow environment

If you run Airflow in Docker using the [Astro CLI](https://docs.astronomer.io/software/install-cli) or by [following the Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html), you can find the logs for each Airflow component in the following locations:

- Scheduler: Logs are in `/usr/local/airflow/logs/scheduler` within the scheduler Docker container by default. To enter a docker container in a bash session, run `docker exec -it <container_id> /bin/bash`.
- Webserver: Logs appear in the console by default. You can access the logs by running `docker logs <webserver_container_id>`.
- Metadata database: Logs appear in the console by default. You can access the logs by running `docker logs <postgres_container_id>`.
- Triggerer: Logs appear in the console by default. You can access the logs by running `docker logs <triggerer_container_id>`. As of Airflow 2.6, individual triggers' log messages can be found in the logs of tasks that use deferrable operators.
- Task: Logs appear in `/usr/local/airflow/logs/` within the scheduler Docker container. To access task logs in the Airflow UI click on the square of a task instance in the Grid views and then select the **Logs** tab.

![Logs in Grid View](/img/guides/logging-task_logs_grid_view.gif)

The Astro CLI includes a command to show webserver, scheduler, triggerer and Celery worker logs from the local Airflow environment. For more information, see [astro dev logs](https://docs.astronomer.io/astro/cli/astro-dev-logs).


:::note

As of Airflow 2.8, logs from other Airflow components, such as the scheduler or executor will be forwarded to the task logs if an error in the component causes the task to fail. For example if a task runs out of memory, causing a [zombie process](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/stable/core-concepts/tasks.html#zombie-undead-tasks), information about the zombie will be printed to the task logs. You can disable this behavior by setting [`AIRFLOW__LOGGING__ENABLE_TASK_CONTEXT_LOGGER=False`](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/stable/configurations-ref.html#enable-task-context-logger).

:::

## Add custom task logs from a DAG

All hooks and operators in Airflow generate logs when a task is run. You can't modify logs from within other operators or in the top-level code, but you can add custom logging statements from within your Python functions by accessing the `airflow.task` logger.

The advantage of using a logger over print statements is that you can log at different levels and control which logs are emitted to a specific location. For example, by default the `airflow.task` logger is set at the level of `INFO`, which means that logs at the level of `DEBUG` aren't logged. To see `DEBUG` logs when debugging your Python tasks, you  need to set `AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG` or change the value of `logging_level` in `airflow.cfg`. After debugging, you can change the `logging_level` back to `INFO` without modifying your DAG code.

The following example DAG shows how to instantiate an object using the existing `airflow.task` logger, add logging statements of different severity levels from within a Python function, and what the log output would be with default Airflow logging settings. There are many use cases for adding additional logging statements from within DAGs ranging from logging warnings when a specific set of conditions appear over additional debugging messages to catching exceptions but still keeping a record of them having occurred.


<Tabs
    defaultValue="taskflow"
    groupId="add-custom-task-logs-from-a-dag"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{custom_logs_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{custom_logs_traditional}</CodeBlock>

</TabItem>
</Tabs>

For the previous DAG, the logs for the `extract` task show the following lines under the default Airflow logging configuration (set at the level of `INFO`):

```bash
[2022-06-06, 07:25:09 UTC] {logging_mixin.py:115} INFO - This log is created with a print statement
[2022-06-06, 07:25:09 UTC] {more_logs_dag.py:15} INFO - This log is informational
[2022-06-06, 07:25:09 UTC] {more_logs_dag.py:16} WARNING - This log is a warning
[2022-06-06, 07:25:09 UTC] {more_logs_dag.py:17} ERROR - This log shows an error!
[2022-06-06, 07:25:09 UTC] {more_logs_dag.py:18} CRITICAL - This log shows a critical error!
```

## When to configure logging

Logging in Airflow is ready to use without any additional configuration. However, there are many use cases where customization of logging is beneficial. For example:

- Changing the format of existing logs to contain additional information. For example, the full pathname of the source file from which the logging call was made.
- Adding additional handlers. For example, to log all critical errors in a separate file.
- Storing logs remotely.
- Adding your own custom handlers. For example, to log remotely to a destination not yet supported by existing providers.

## How to configure logging

Logging in Airflow can be configured in `airflow.cfg` and by providing a custom `log_config.py` file. It is best practice to not declare configs or variables within the `.py` handler files except for testing or debugging purposes.

In the Airflow CLI, run the following commands to return the current task handler and logging configuration. If you're running Airflow in Docker, make sure to enter your Docker container before running the commands:

```console
airflow info          # shows the current handler
airflow config list   # shows current parameters under [logging]
```

A full list parameters relating to logging that can be configured in `airflow.cfg` can be found in the [base_log_folder](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#logging). They can also be configured by setting their corresponding environment variables.

For example, to change your logging level from the default `INFO` to `LogRecords` with a level of `ERROR` or above, you set `logging_level = ERROR` in `airflow.cfg` or define an environment variable `AIRFLOW__LOGGING__LOGGING_LEVEL=ERROR`.

Advanced configuration might necessitate the logging config class to be overwritten. To enable custom logging, you need to create the configuration file `~/airflow/config/log_config.py` and specify your modifications to `DEFAULT_LOGGING_CONFIG`. You might need to do this to add a custom handler.

## Remote logging

When scaling your Airflow environment you might produce more logs than your Airflow environment can store. In this case, you need reliable, resilient, and auto-scaling storage. The easiest solution is to use remote logging to a remote service which is already supported by the following community-managed providers:

- Alibaba: `OSSTaskHandler` (`oss://`)
- Amazon: `S3TaskHandler` (`s3://`), `CloudwatchTaskHandler` (`cloudwatch://`)
- [Elasticsearch](https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/logging/index.html): `ElasticsearchTaskHandler` (further configured with `elasticsearch` in `airflow.cfg`)
- [Google](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/logging/index.html): `GCSTaskHandler` (`gs://`), `StackdriverTaskHandler` (`stackdriver://`)
- [Microsoft Azure](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/logging/index.html): `WasbTaskHandler` (`wasb`)

By configuring `REMOTE_BASE_LOG_FOLDER` with the prefix of a supported provider, you can override the default task handler (`FileTaskHandler`) to send logs to a remote destination task handler. For example, `GCSTaskHandler`.

If you want different behavior or to add several handlers to one logger, you need to make changes to `DEFAULT_LOGGING_CONFIG`.

Logs are sent to remote storage only once a task has been completed or failed. This means that logs of currently running tasks are accessible only from your local Airflow environment.

## Remote logging example: Send task logs to Amazon S3

1. Add the `apache-airflow-providers-amazon` provider package to `requirements.txt`.

2. Start your Airflow environment and go to **Admin** > **Connections** in the Airflow UI.

3. Create a connection of type **Amazon S3** and set `login` to your AWS access key ID and `password` to your AWS secret access key. See [AWS Account and Access Keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html) for information about retrieving your AWS access key ID and AWS secret access key.  

4. Add the following commands to the Dockerfile. Include the double underscores around `LOGGING`:

    ```docker
    # allow remote logging and provide a connection ID (see step 2)
    ENV AIRFLOW__LOGGING__REMOTE_LOGGING=True
    ENV AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID=${AMAZONS3_CON_ID}

    # specify the location of your remote logs using your bucket name
    ENV AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER=s3://${S3BUCKET_NAME}/logs

    # optional: serverside encryption for S3 logs
    ENV AIRFLOW__LOGGING__ENCRYPT_S3_LOGS=True
    ```

    These environment variables configure remote logging to one S3 bucket (`S3BUCKET_NAME`). Behind the scenes, Airflow uses these configurations to create an `S3TaskHandler` which overrides the default `FileTaskHandler`.  

5. Restart your Airflow environment and run any task to verify that the task logs are copied to your S3 bucket.

    ![Logs in S3 bucket](/img/guides/logs_s3_bucket.png)

## Advanced configuration example: Add multiple handlers to the same logger

For full control over the logging configuration, you create and modify a `log_config.py` file. This is relevant for use cases such as adding several handlers to the same logger with different formatters, filters, or destinations, or to add your own custom handler. You may want to do this in order to save logs of different severity levels in different locations, apply additional filters to logs stored in a specific location, or to further configure a custom logging solution with a destination for which no provider is available.

The following example adds a second remote logging Amazon S3 bucket to receive logs with a different file structure.

Complete Steps 1 and 2 in [Remote Logging Example: Sending Task Logs to Amazon S3](#remote-logging-example-sending-task-logs-to-amazon-s3) to configure your Airflow environment for Amazon S3 remote logging and then add the following commands to your Dockerfile:

```docker
#### Remote logging to S3

# Define the base log folder
ENV BASE_LOG_FOLDER=/usr/local/airflow/logs

# create a directory for your custom log_config.py file and copy it
ENV PYTHONPATH=/usr/local/airflow
RUN mkdir $PYTHONPATH/config
COPY include/log_config.py $PYTHONPATH/config/
RUN touch $PYTHONPATH/config/__init__.py

# allow remote logging and provide a connection ID (the one you specified in step 2)
ENV AIRFLOW__LOGGING__REMOTE_LOGGING=True
ENV AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID=hook_tutorial_s3_conn

# specify the location of your remote logs, make sure to provide your bucket names above
ENV AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER=s3://${S3BUCKET_NAME}/logs
ENV AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER_2=s3://${S3BUCKET_NAME_2}/logs

# set the new logging configuration as logging config class
ENV AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS=config.log_config.LOGGING_CONFIG

# optional: serverside encryption for S3 logs
ENV AIRFLOW__LOGGING__ENCRYPT_S3_LOGS=True
```

By setting these environment variables you can configure remote logging to two Amazon S3 buckets (`S3BUCKET_NAME` and `S3BUCKET_NAME_2`).
Additionally, to the first remote log folder (`AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER`) a second remote log folder `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER_2` is set as an environment variable to be retrieved from within `log_config.py`. The `AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS` is replaced with your custom `LOGGING_CONFIG` class that you will define.

Create a `log_config.py` file. While you can put this file anywhere in your Airflow project as long as it is not within a folder listed in `.dockerignore`, it is best practice to put it outside of your `dags/` folder, such as `/include`, to prevent the scheduler wasting resources by continuously parsing the file. Update the COPY statement in the previous example depending on where you decide to store this file.

Within `log_config.py`, create and modify a deepcopy of `DEFAULT_LOGGING_CONFIG` as follows:

```python
from copy import deepcopy
import os

# import the default logging configuration
from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG

LOGGING_CONFIG = deepcopy(DEFAULT_LOGGING_CONFIG)

# add an additional handler
LOGGING_CONFIG["handlers"]["secondary_s3_task_handler"] = {
    # you can import your own custom handler here
    "class": "airflow.providers.amazon.aws.log.s3_task_handler.S3TaskHandler",
    # you can add a custom formatter here
    "formatter": "airflow",
    # the following env variables were set in the dockerfile
    "base_log_folder": os.environ["BASE_LOG_FOLDER"],
    "s3_log_folder": os.environ["AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER_2"],
    "filename_template":
    # providing a custom structure for log directory and filename
    "{{ ti.dag_id }}/{{ ti.task_id }}_{{ ts }}_{{ try_number }}.log",
    # if needed, custom filters can be added here
    "filters": ["mask_secrets"],
}

# this line adds the "secondary_s3_task_handler" as a handler to airflow.task
LOGGING_CONFIG["loggers"]["airflow.task"]["handlers"] = [
    "task",
    "secondary_s3_task_handler",
]

```

This modified version of `DEFAULT_LOGGING_CONFIG` creates a second S3TaskHandler using the Amazon S3 location provided as `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER_2`. It is configured with a custom `filename_template`, further customization is of course possible with regards to formatting, log level, and additional filters.

Restart your Airflow environment and run any task to verify that the task logs are copied to both of your S3 buckets.

![Logs in the secondary S3 bucket](/img/guides/logs_second_s3_bucket.png)
