---
title: "Use a listener to send a Slack notification when a Dataset is updated"
sidebar_label: "Listeners"
description: "Learn how to use Airflow Listeners."
id: airflow-listeners
---

import CodeBlock from '@theme/CodeBlock';
import producer_dag from '!!raw-loader!../code-samples/dags/airflow-listeners/producer_dag.py';

[Airflow listeners](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html#listeners) allow you to execute custom code when certain events occur anywhere in your Airflow instance, for example whenever any DAG run fails or an update to a Dataset is detected. 

Listeners are implemented as an [Airflow plugin](using-airflow-plugins.md) and can contain any code you like. In this tutorial you will learn how to use a listener to send a Slack notification whenever a Dataset is updated.

:::info

If you are looking to implement notifications for specific DAGs and tasks, consider using [Airflow callbacks](error-notifications-in-airflow.md#airflow-callbacks) instead.

:::

## Time to complete

This tutorial takes approximately 15 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow plugins. See [Airflow plugins](using-airflow-plugins.md).
- Airflow datasets. See [Datasets and data-aware scheduling in Airflow](airflow-datasets.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started) using the [Astro Runtime image](https://docs.astronomer.io/astro/runtime-release-notes) version 10.0.0 or higher (Airflow 2.8+).
- A Slack workspace with an [Incoming Webhook](https://api.slack.com/messaging/webhooks) configured.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-listener-tutorial && cd astro-listener-tutorial
    $ astro dev init
    ```

2. Add the following line to your `requirements.txt` file to install the Slack Airflow provider.

    ```text
    apache-airflow-providers-slack==8.4.0
    ```

3. To create an [Airflow connection](connections.md) to Slack, add the following environment variable to your `.env` file. Make sure to replace `<your-slack-webhook-token>` with your own Slack webhook token in the format of `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

    ```text
    AIRFLOW_CONN_SLACK_WEBHOOK_CONN='{
        "conn_type": "slackwebhook",
        "host": "https://hooks.slack.com/services/",
        "password": "<your-slack-webhook-token>"
    }'
    ```

## Step 2: Create your listener

Airflow listeners are defined using the `@hookimpl` decorator on functions defined with the same name and parameters as listed in [listeners spec](https://github.com/apache/airflow/tree/main/airflow/listeners/spec) source code. 

For example, the [@hookspec of the `on_task_instance_failed` function](https://github.com/apache/airflow/blob/main/airflow/listeners/spec/taskinstance.py) is:

```python
@hookspec
def on_task_instance_failed(
    previous_state: TaskInstanceState | None, task_instance: TaskInstance, session: Session | None
):
    """Execute when task state changes to FAIL. previous_state can be None."""
```

In order to create a listener that executes whenever any task instance fails in your whole Airflow environment, you need to define a function called `on_task_instance_failed` that takes three parameters: `previous_state`, `task_instance` and `session` and decorate it with `@hookimpl`.

```python
from airflow.listeners import hookimpl

@hookimpl
def on_task_instance_failed(
    previous_state: TaskInstanceState | None, task_instance: TaskInstance, session: Session | None
):
    # Your code here
```

In this tutorial you will create a listener that sends a Slack notification whenever a Dataset is updated.

1. Create a new file called `listeners_code.py` in your `plugins` folder.
2. Copy the following code into the file:

    ```python
    from airflow import Dataset
    from airflow.listeners import hookimpl
    from airflow.models.taskinstance import TaskInstance
    from airflow.utils.state import TaskInstanceState
    from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
    from sqlalchemy.orm.session import Session
    from datetime import datetime

    SLACK_CONN_ID = "slack_webhook_conn"


    @hookimpl
    def on_dataset_changed(dataset: Dataset):
        """Execute if a dataset is updated."""
        print("I am always listening for any Dataset changes and I heard that!")
        print("Posting to Slack...")
        hook = SlackWebhookHook(slack_webhook_conn_id=SLACK_CONN_ID)
        hook.send(text=f"A dataset was changed!")
        print("Done!")
        if dataset.uri == "file://include/bears":
            print("Oh! This is the bears dataset!")
            print("Bears are great :)")
            start_date = datetime.now().date()
            end_date = datetime(2024, 10, 4).date()
            days_until = (end_date - start_date).days
            print(f"Only approximately {days_until} days until fat bear week!")
    ```

    This listener is defined using the [`on_dataset_changed` hookspec](https://github.com/apache/airflow/blob/main/airflow/listeners/spec/dataset.py). It posts a message to Slack whenever a Dataset is updated and executes additional code printing messages to the logs if the dataset that is being updated has the URI `file://include/bears`.


## Step 3: Create the listener plugin

For Airflow to recognize your listener, you need to create a plugin that registers it.

1. Create a new file called `listener_plugin.py` in your `plugins` folder.
2. Copy the following code into the file:

    ```python
    from airflow.plugins_manager import AirflowPlugin
    from plugins import listener_code


    class MyListenerPlugin(AirflowPlugin):
        name = "my_listener_plugin"
        listeners = [listener_code]
    ```

:::info

Remember to restart your Airflow instance after making any changes to your plugins. For more information on Airflow plugins, see [Airflow plugins](using-airflow-plugins.md).

:::

## Step 4: Create your DAG

1. In your `dags` folder, create a file called `producer_dag.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{producer_dag}</CodeBlock>

    This simple DAG contains one task that queries the [placebear](https://placebear.com/) API and writes the image retrieved to a local `.png` file in the `include folder using the [Airflow Object Storage](airflow-object-storage-tutorial.md) feature.
    The task produces an update to the `file://include/bears` Dataset, which triggers the listener you created in [Step 2](#step-2-create-your-listener).

## Step 5: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow, then open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `producer_dag` DAG by clicking the play button.

3. After the DAG run completed, go to the task logs of the `get_bear` task to see print statements from your listener plugin.

    ```text
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - I am always listening for any Dataset changes and I heard that!
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - Posting to Slack...
    [2023-12-17, 14:46:51 UTC] {base.py:83} INFO - Using connection ID 'slack_webhook_conn' for task execution.
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - Done!
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - Oh! This is the bears dataset!
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - Bears are great :)
    [2023-12-17, 14:46:51 UTC] {logging_mixin.py:188} INFO - Only approximately 292 days until fat bear wee
    ```

4. In your Slack workspace, you can see a new message from your webhook.

    ![Screenshot of a Slack message sent by the webhook, saying "A dataset was changed!".](/img/tutorials/airflow-listeners_slack_message.png)

5. (Optional). View your complimentary bear picture at `include/bears/bear.png`.

## Conclusion

Congratulations! You now know how to create an Airflow listener to custom code whenever a specific event occurs in your whole Airflow environment.
