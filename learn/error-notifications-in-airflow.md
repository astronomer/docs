---
title: "Manage Airflow DAG notifications"
sidebar_label: "DAG notifications"
id: error-notifications-in-airflow
---

<head>
  <meta name="description" content="Master the basics of Apache Airflow notifications. Learn how to set up automatic email and Slack notifications to be alerted of events in your DAGs." />
  <meta name="og:description" content="Master the basics of Apache Airflow notifications. Learn how to set up automatic email and Slack notifications to be alerted of events in your DAGs." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import email_alert_example_dag from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/email_alert_example_dag.py';
import callbacks_example_dag from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/callbacks_example_dag.py';
import sla_dag_level_example_taskflow from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/sla_dag_level_example_taskflow.py';
import sla_dag_level_example_traditional from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/sla_dag_level_example_traditional.py';
import sla_task_level_example_taskflow from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/sla_task_level_example_taskflow.py';
import sla_task_level_example_traditional from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/sla_task_level_example_traditional.py';
import slack_notifier_example_dag from '!!raw-loader!../code-samples/dags/error-notifications-in-airflow/slack_notifier_example_dag.py';

When you're using a data orchestration tool, how do you know when something has gone wrong? Airflow users can check the Airflow UI to determine the status of their DAGs, but this is an inefficient way of managing errors systematically, especially if certain failures need to be addressed promptly or by multiple team members. Fortunately, Airflow has built-in notification mechanisms that can be leveraged to configure error notifications in a way that works for your organization. 

In this guide, you'll learn the basics of Airflow notifications and how to set up common notification mechanisms including email, pre-built and custom notifiers, and SLAs. You'll also learn how to leverage Airflow alerting when using Astro.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Task dependencies. See [Managing dependencies in Apache Airflow](managing-dependencies.md).

## Airflow notification types

Airflow has a few options for notifying you on the status of your DAGs and tasks:

- **Email notifications**: Most Airflow operators have parameters for setting email alerts in case of a task failure or retry. Use email alerts in production pipelines where task failures or retries need immediate attention by a data professional. 
- **Airflow callbacks**: Callback parameters (`*_callback`) exist both at the task and at the DAG level. You can pass any callable or [Airflow notifier](#notifiers) to these parameters, and Airflow will run them in the case of specific events, such as a task failure. Airflow callbacks offer a lot of flexibility to execute any code based on the state of a task or DAG. They are often used to define actions for specific instances of task failures or successes.
- **Airflow notifiers**: Notifiers are custom classes for Airflow callbacks that can be easily reused and standardized. Provider packages can ship pre-built notifiers like the [SlackNotifier](https://airflow.apache.org/docs/apache-airflow-providers-slack/7.3.1/_api/airflow/providers/slack/notifications/slack/index.html). Notifiers can be provided to callback parameters to define which task or DAG state should cause them to be executed. A common use case for notifiers is standardizing actions for task failures across several Airflow instances.
- **Airflow service-level agreements (SLAs)**: SLAs define the expected time it takes for a specific task to complete. If an SLA is missed, the callable or notifier provided to the `sla_miss_callback` parameter is executed. If you configure an SMTP connection, an email will be sent as well. Since an SLA miss does not stop a task from running, this type of notification is used when intervention is needed if a specific task is taking longer than expected.

Most notifications can be set at the level of both a DAG and a task. Setting a parameter within a DAG's `default_args` dictionary will apply it to all tasks in the DAG. You can see examples of this in the [set DAG and task-level callbacks](#set-dag-and-task-level-callbacks) section.

## Choose a notification type

It's best practice to use pre-built solutions whenever possible. This approach makes your DAGs more robust by reducing custom code and standardizing notifications across different Airflow environments.

If you want to deliver alerts to email, use [email notifications](#email-notifications) for task failures or retries and the [SmtpNotifier](https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/_api/airflow/providers/smtp/notifications/smtp/index.html) for other events such as successful task runs. To receive alerts for tasks taking longer than expected, use [SLAs](#airflow-service-level-agreements).

If a [notifier class]((#notifiers) exists for your use case, you should always use it instead of a custom callback. See the Airflow documentation for [an up-to-date list of available Notifiers](https://airflow.apache.org/docs/apache-airflow-providers/core-extensions/notifications.html). A notifier can be provided to any callback parameter (`*callback`). Only use custom [Airflow callbacks](#airflow-callbacks) when no notifier is available for your use case.

## Email notifications

If you have an SMTP connection configured in Airflow, you can use the `email`, `email_on_failure`, and `email_on_retry` task parameters to send notification emails from Airflow.

<Tabs
    defaultValue="taskflow"
    groupId="email-notifications"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
@task(
    email=["noreply@astronomer.io", "noreply2@astronomer.io"],
    email_on_failure=True,
    email_on_retry=True
)
def t1():
    return "hello"
```

</TabItem>
<TabItem value="traditional">

```python
def say_hello():
    return "hello"


t1 = PythonOperator(
    task_id="t1",
    python_callable=say_hello,
    email=["noreply@astronomer.io", "noreply2@astronomer.io"],
    email_on_failure=True,
    email_on_retry=True
)
```

</TabItem>
</Tabs>

You can also configure email notifications for all tasks in a DAG by defining the configurations in the `default_args` parameter.

```python
default_args = {
    "email": ["noreply@astronomer.io"],
    "email_on_failure": True,
    "email_on_retry": True,
}

@dag(
    start_date=datetime(2023, 4, 25),
    schedule="@daily",
    catchup=None,
    default_args=default_args
)
```

To allow Airflow to send emails, you have to provide values to the SMTP section of your `airflow.cfg` similar to this example:

```yaml
[smtp]
# If you want airflow to send emails on retries, failure, and you want to use
# the airflow.utils.email.send_email_smtp function, you have to configure an
# smtp server here
smtp_host = your-smtp-host.com
smtp_starttls = True
smtp_ssl = False
# Uncomment and set the user/pass settings if you want to use SMTP AUTH 
# smtp_user =                       
# smtp_password =  
smtp_port = 587
smtp_mail_from = noreply@astronomer.io
```

You can also set these values using environment variables. In this case, all parameters are preceded by `AIRFLOW__SMTP__`. For example, `smtp_host` can be specified by setting the `AIRFLOW__SMTP__SMTP_HOST` variable. For more on Airflow email configuration, see [Email Configuration](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html). 

If you are using Astro, [use environment variables](https://docs.astronomer.io/astro/environment-variables) to set up SMTP because the `airflow.cfg` cannot be directly edited.

### Custom email notifications

By default, email notifications are sent in a standard format that are defined in the `email_alert()` and `get_email_subject_content()` methods of the `TaskInstance` class:

```python
default_subject = 'Airflow alert: {{ti}}'
# For reporting purposes, the report is based on 1-indexed,
# not 0-indexed lists (i.e. Try 1 instead of
# Try 0 for the first attempt).
default_html_content = (
    'Try {{try_number}} out of {{max_tries + 1}}<br>'
    'Exception:<br>{{exception_html}}<br>'
    'Log: <a href="{{ti.log_url}}">Link</a><br>'
    'Host: {{ti.hostname}}<br>'
    'Mark success: <a href="{{ti.mark_success_url}}">Link</a><br>'
)
```

To see the full method, see the source code [here](https://github.com/apache/airflow/blob/main/airflow/models/taskinstance.py#L1802).

You can customize this content by setting the `subject_template` and/or `html_content_template` variables in your `airflow.cfg` with the path to your jinja template files for subject and content respectively.

If you want to send emails out on a more customizable basis, you can also use Airflow's callback functions to run custom functions that send email notifications. For example, if you want to send emails for successful task runs, you can provide an email function to the `on_success_callback` parameter:

```python
from airflow.utils.email import send_email

def success_email_function(context):
    dag_run = context.get("dag_run")

    msg = "DAG ran successfully"
    subject = f"DAG {dag_run} has completed"
    send_email(to=your_emails, subject=subject, html_content=msg)


@dag(
    start_date=datetime(2023, 4, 26),
    schedule="@daily",
    catchup=False,
    on_success_callback=success_email_function
)
```

## Airflow callbacks 

In Airflow you can define actions to be taken due to different DAG or task states using `*_callback` parameters:

- `on_success_callback`: Invoked when a task or DAG succeeds.
- `on_failure_callback`: Invoked when a task or DAG fails.
- `on_execute_callback`: Invoked right before a task begins executing. This callback only exists at the task level.
- `on_retry_callback`: Invoked when a task is retried. This callback only exists at the task level.
- `sla_miss_callback`: Invoked when a task or DAG misses its defined [Service Level Agreement (SLA)](#airflow-service-level-agreements). This callback is defined at the DAG level for DAGs with defined SLAs and will be applied to every task.

You can provide any Python callable to the `*_callback` parameters. As of Airflow 2.6, you can also use [notifiers](#notifiers) for your callbacks, and you can provide several callback items to the same callback parameter in a list.

### Notifiers

Airflow 2.6 added [notifiers](https://airflow.apache.org/docs/apache-airflow/stable/howto/notifications.html), which are pre-built or custom classes and can be used to standardize and modularize the functions you use to send notifications. Notifiers get passed to the relevant `*_callback` parameter of your DAG depending on what event you want to trigger the notification.

:::info

You can find a full list of all pre-built notifiers created for Airflow providers [here](https://airflow.apache.org/docs/apache-airflow-providers/core-extensions/notifications.html).

:::

Notifiers are defined in provider packages or imported from the include folder and can be used across any of your DAGs. This feature has the advantage that community members can define and share functionality previously used in callback functions as Airflow modules, creating pre-built callbacks to send notifications to other data tools.

An Airflow notifier can be created by inheriting from the `BaseNotifier` class and defining the action which should be taken in case the notifier is used in the `.notify()` method.

```python
class MyNotifier(BaseNotifier):
    """
    Basic notifier, prints the task_id, state and a message.
    """

    template_fields = ("message",)

    def __init__(self, message):
        self.message = message

    def notify(self, context):
        t_id = context["ti"].task_id
        t_state = context["ti"].state
        print(
            f"Hi from MyNotifier! {t_id} finished as: {t_state} and says {self.message}"
        )
```

To use the custom notifier in a DAG, provide its instantiation to any callback parameter. For example:

<Tabs
    defaultValue="taskflow"
    groupId="notifiers"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
@task(
    on_failure_callback=MyNotifier(message="Hello failed!"),
)
def t1():
    return "hello"
```

</TabItem>
<TabItem value="traditional">

```python
def say_hello():
    return "hello"


t1 = PythonOperator(
    task_id="t1",
    python_callable=say_hello,
    on_failure_callback=MyNotifier(message="Hello failed!"),
)
```

</TabItem>
</Tabs>

### Example pre-built notifier: Slack

An example of a community provided pre-built notifier is the [SlackNotifier](https://airflow.apache.org/docs/apache-airflow-providers-slack/latest/_api/airflow/providers/slack/notifications/slack_notifier/index.html). 

It can be imported from the Slack provider package and used with any `*_callback` function:

<CodeBlock language="python">{slack_notifier_example_dag}</CodeBlock>

The DAG above has one task sending a notification to Slack. It uses a Slack [Airflow connection](connections.md) with the connection ID `slack_conn`.

![Slack notification](/img/guides/slack_notification.png)

### Set DAG and task-level custom callbacks

To define a custom notification at the DAG level, you can set the `*_callback` parameters in your DAG instantiation. DAG-level notifications will trigger callback functions based on the state of the entire DAG run.

```python
def my_success_callback_function(context):
    pass


def my_failure_callback_function(context):
    pass


def my_sla_callback_function(context):
    pass


@dag(
    start_date=datetime(2023,4,25),
    schedule="@daily",
    catchup=False,
    on_success_callback=my_success_callback_function,
    on_failure_callback=my_failure_callback_function,
    sla_miss_callback=my_sla_callback_function
)
```

To apply a task-level callback to each task in your DAG, you can pass the callback function to the `default_args` parameter. Items listed in the dictionary provided to the `default_args` parameter will be set for each task in the DAG.

```python
def my_execute_callback_function(context):
    pass


def my_retry_callback_function(context):
    pass


def my_success_callback_function(context):
    pass


def my_failure_callback_function(context):
    pass


@dag(
    start_date=datetime(2023,4,25),
    schedule="@daily",
    catchup=False,
    default_args={
        "on_execute_callback": my_execute_callback_function,
        "on_retry_callback": my_retry_callback_function,
        "on_success_callback": my_success_callback_function,
        "on_failure_callback": my_failure_callback_function
    }
)
```

For use cases where an individual task should use a specific callback, the task-level callback parameters can be defined in the task instantiation. Callbacks defined at the individual task level will override callbacks passed in via `default_args`.

<Tabs
    defaultValue="taskflow"
    groupId="notification-levels"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
def my_execute_callback_function(context):
    pass


def my_retry_callback_function(context):
    pass


def my_success_callback_function(context):
    pass


def my_failure_callback_function(context):
    pass


@task(
    on_execute_callback=my_execute_callback_function,
    on_retry_callback=my_retry_callback_function,
    on_success_callback=my_success_callback_function,
    on_failure_callback=my_failure_callback_function,
)
def t1():
    return "hello"
```

</TabItem>
<TabItem value="traditional">

```python
def my_execute_callback_function(context):
    pass


def my_retry_callback_function(context):
    pass


def my_success_callback_function(context):
    pass


def my_failure_callback_function(context):
    pass


def say_hello():
    return "hello"


t1 = PythonOperator(
    task_id="t1",
    python_callable=say_hello,
    on_execute_callback=my_execute_callback_function,
    on_retry_callback=my_retry_callback_function,
    on_success_callback=my_success_callback_function,
    on_failure_callback=my_failure_callback_function,
)
```

</TabItem>
</Tabs>

## Airflow service-level agreements

[Airflow service-level agreements (SLAs)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#slas) are a type of notification that you can use if your tasks take longer than expected to complete. If a task takes longer than the maximum amount of time to complete as defined in the SLA, the SLA will be missed and notifications are triggered. This can be useful when you have long-running tasks that might require user intervention after a certain period of time, or if you have tasks that need to complete within a certain period. 

Exceeding an SLA does not stop a task from running. If you want tasks to stop running after a certain time, use [timeouts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#timeouts).

You can set an SLA for all tasks in your DAG by defining `'sla'` as a default argument, as shown in the following example DAG:

<Tabs
    defaultValue="taskflow"
    groupId="airflow-service-level-agreements"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{sla_dag_level_example_taskflow}</CodeBlock>

</TabItem>
<TabItem value="traditional">

<CodeBlock language="python">{sla_dag_level_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

SLAs have some unique behaviors that you should consider before you implement them:

- SLAs are relative to the DAG execution date, not the task start time. For example, in the previous DAG the `sla_task` will miss the 30 second SLA because it takes at least 40 seconds to complete. The `t1` task will also miss the SLA, because it is executed more than 30 seconds after the DAG execution date. In that case, the `sla_task` will be considered blocking to the `t1` task.
- SLAs will only be evaluated on scheduled DAG Runs. They will not be evaluated on manually triggered DAG Runs.
- SLAs can be set at the task level if a different SLA is required for each task. In the previous example, all task SLAs are still relative to the DAG execution date. For example, in the DAG below, `t1` has an SLA of 500 seconds. If the upstream tasks (`t0` and `sla_task`) combined take 450 seconds to complete, and `t1` takes 60 seconds to complete, then `t1` will miss its SLA even though the task did not take more than 500 seconds to execute.

<Tabs
    defaultValue="taskflow"
    groupId="airflow-service-level-agreements"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{sla_task_level_example_taskflow}</CodeBlock>

</TabItem>
<TabItem value="traditional">

<CodeBlock language="python">{sla_task_level_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

Missed SLAs are shown in the Airflow UI. To view them, go to **Browse** > **SLA Misses**:

![SLA UI](/img/guides/sla_ui_view.png)

If you configured an SMTP server in your Airflow environment, you'll receive an email with notifications of any missed SLAs similar to the following image:

![SLA Email](/img/guides/sla_email.png)

There is no functionality to disable email alerting for SLAs. If you have an `'email'` array defined and an SMTP server configured in your Airflow environment, an email will be sent to those addresses for each DAG run with missed SLAs.

## Astronomer notifications

If you are running Airflow with Astronomer Software or Astro, there are a number of options available for managing your Airflow notifications. All of the previous methods for sending task notifications from Airflow can be implemented on Astronomer. See the [Astronomer Software](https://docs.astronomer.io/software/airflow-alerts) and [Astro](https://docs.astronomer.io/astro/airflow-alerts) documentation to learn how to leverage notifications on the platform, including how to set up SMTP to enable email notifications.

Astronomer also provides deployment and platform-level alerting to notify you if any aspect of your Airflow or Astronomer infrastructure is unhealthy. For more on that, including how to customize notifications for Software users, see [Alerting in Astronomer Software](https://docs.astronomer.io/software/platform-alerts).

## Legacy: Slack notifications pre-2.6

:::info

In Airflow 2.6+ you can use the [SlackNotifier](#pre-built-notifier-slack) to send notifications to Slack from within Airflow in a modularized and standardized way.

:::

If you are on an Airflow version older than 2.6 and want to implement Slack notifications, follow this example.
It uses the [Slack provider](https://registry.astronomer.io/providers/slack) `SlackWebhookOperator` with a Slack Webhook to send messages. This is the method Slack recommends to post messages from apps.

1. From your Slack workspace, create a Slack app and an incoming Webhook. See [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks). 
2. Copy the Slack Webhook URL. You'll use it in your Python function.
3. Create an Airflow connection to provide your Slack Webhook to Airflow. Choose an HTTP connection type. Enter [`https://hooks.slack.com/services/`](https://hooks.slack.com/services/) as the Host, and enter the remainder of your Webhook URL from the last step as the Password (formatted as `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`). 

    ![Slack Connection](/img/guides/slack_webhook_connection.png)

    In Airflow 2.0 or later, you'll need to install the `apache-airflow-providers-slack` provider package to use the `SlackWebhookOperator`.

4. Create a Python function to use as your `on_failure_callback` method. Within the function, define the information you want to send and invoke the `SlackWebhookOperator` to send the message similar to this example:

    ```python
    from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

    def slack_notification(context):
        slack_msg = """
                :red_circle: Task Failed. 
                *Task*: {task}  
                *Dag*: {dag} 
                *Execution Time*: {exec_date}  
                *Log Url*: {log_url} 
                """.format(
            task=context.get("task_instance").task_id,
            dag=context.get("task_instance").dag_id,
            ti=context.get("task_instance"),
            exec_date=context.get("execution_date"),
            log_url=context.get("task_instance").log_url,
        )
        failed_alert = SlackWebhookOperator(
            task_id="slack_notification", http_conn_id="slack_webhook", message=slack_msg
        )
        return failed_alert.execute(context=context)

    @dag(
        start_date=datetime(2023, 1, 1),
        schedule="@daily",
        catchup=False
    )
    def post_to_slack():
        @task(
            on_success_callback=slack_notification
        )
        def post_to_slack():
            return 10

    post_to_slack()

    ```

5. Define your `on_failure_callback` parameter in your DAG either as a `default_arg` for the whole DAG, or for specific tasks. Set it equal to the function you created in the previous step.
