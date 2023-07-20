---
title: "Microsoft Teams notifications"
description: "Configure notifications in Microsoft teams for DAG runs and tasks using Airflow callbacks."
id: example-ms-teams-callback
sidebar_label: "Teams notifications"
sidebar_custom_props: { icon: 'img/examples/ms_teams_logo.png' }
---

This example shows how to set up Airflow notifications in a [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams/group-chat-software) channel by using [Airflow callbacks](error-notifications-in-airflow.md#airflow-callbacks). Teams notifications about DAG runs and tasks let you to quickly inform many ream members about the status of your data pipelines.

## Before you start

Before trying this example, make sure you have:

- [Teams](https://www.microsoft.com/en-us/microsoft-teams/log-in) with a Business account supporting team channels.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).
- An Astro project running locally on your computer. See [Getting started with the Astro CLI](https://docs.astronomer.io/astro/cli/get-started-cli).

## Send task failure notifications to MS Teams

Follow these steps to receive notifications in MS Teams for failed tasks in an example DAG. Refer to the [Airflow callbacks section](error-notifications-in-airflow.md#airflow-callbacks) of our notifications guide to learn how to set up notifications for other types of events.

1. Open the folder containing your Astro Project. Copy the contents of the `include` folder in the [project GitHub repository](https://github.com/astronomer/cs-tutorial-msteams-callbacks/tree/main/include) to your Astro project `include` folder.

    ```text
    ├── .astro
    ├── dags
    └── include
        ├── hooks
        │   └── ms_teams_webhook_hook.py
        ├── operators
        │   └── ms_teams_webhook_operator.py
        ├── ms_teams_callback_functions.py
        └── ms_teams_callback_functions_with_partial.py
    ```

2. Create a [Microsoft Teams Incoming Webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=dotnet#create-incoming-webhooks-1) for the channel where you want to receive notifications. Copy and save the webhook URL.

3. In the Airflow UI, create an Airflow connection by clicking on **Admin** and then **Connections**. Create a new connection with the following parameters. Note that you won't be able to test this connection from the Airflow UI. 

    - **Connection Id**: `ms_teams_callbacks`
    - **Connection Type**: `HTTP`
    - **Host**: `<your-organization>.office.com/webhook/<your-webhook-id>`
    - **Schema**: `https`

    ![Connection](/img/examples/example-ms-teams-callback-connection.png)

  :::info

  Some corporate environments make use of outbound proxies. If you're behind an outbound proxy for internet access, put the proxy details in the **Extra** field when creating the HTTP Connection in the Airflow UI (For example, `{"proxy":"http://my-proxy:3128"}`). 

  :::

  :::info

  If the `HTTP` connection type is not available, double check that the [HTTP provider](https://registry.astronomer.io/providers/apache-airflow-providers-http/versions/latest) is installed in your Airflow environment. 

  :::

4. Import the failure callback function at the top of your DAG file.

    ```python
    from include.ms_teams_callback_functions import failure_callback
    ```

5. Set the `on_failure_callback` keyword of your DAG's `default_args` parameter to the imported `failure_callback` function.

    ```python
    @dag(
        start_date=datetime(2023, 7, 1),
        schedule="@daily",
        default_args={
            "on_failure_callback": failure_callback,
        }
    )
    ```

6. Run your DAG. Any failed task will trigger the `failure_callback` function which sends a notification message to your Teams channel.

The `include` folder of the [project repository](https://github.com/astronomer/cs-tutorial-msteams-callbacks) also contains callback functions for other triggers in addition to the failure callback shown here. You can modify any of the functions to customize the notification message. To learn more about all available callback parameters, see [Airflow callbacks](error-notifications-in-airflow.md#airflow-callbacks).

![Notification](/img/examples/example-ms-teams-callback-task-fail-teams-msg.png)

## See also

- [MS Teams developer documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/mstdd-landing)
- [Manage Airflow DAG notifications](error-notifications-in-airflow.md)
