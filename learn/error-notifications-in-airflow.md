---
title: "Manage Airflow DAG notifications"
sidebar_label: "DAG alerts"
description: "Methods for managing notifications in your Airflow DAGs."
id: error-notifications-in-airflow
---

When you're using a data orchestration tool, how do you know when something has gone wrong? Airflow users can check the Airflow UI to determine the status of their DAGs, but this is an inefficient way of managing errors systematically, especially if certain failures need to be addressed promptly or by multiple team members. Fortunately, Airflow has built-in notification mechanisms that can be leveraged to configure error notifications in a way that works for your organization. 

In this guide, you'll learn the basics of Airflow notifications and how to set up common notification mechanisms including email, Slack, and SLAs. You'll also learn how to make the most of Airflow alerting when using Astro.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Task dependencies. See [Managing dependencies in Apache Airflow](managing-dependencies.md).

## Airflow notification basics

Having your DAGs defined as Python code gives you full autonomy to define your tasks and notifications in whatever way makes sense for your organization.

This section provides an overview of the notification options that are available in Airflow. 

### Notification levels

Sometimes, it's helpful to standardize notifications across your entire DAG. Notifications set at the DAG level filter down to each task in the DAG. These notifications are usually defined in `default_args`.

In the following DAG example, `email_on_failure` is set to `True`, meaning any task in this DAG's context will send a failure email to all addresses in the `email` array.

```python
from datetime import datetime
from airflow import DAG

default_args = {
	'owner': 'airflow',
	'start_date': datetime(2018, 1, 30),
	'email': ['noreply@astronomer.io'],
	'email_on_failure': True
}

with DAG('sample_dag',
	default_args=default_args,
	schedule_interval='@daily',
	catchup=False) as dag:

...
```

Sometimes, it's helpful to limit notifications to specific tasks. The `BaseOperator` includes support for built-in notification arguments. So, you can configure each task individually. In the following example DAG, email notifications are turned off by default at the DAG level, but are enabled for the `will_email` task.

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {
	'owner': 'airflow',
	'start_date': datetime(2018, 1, 30),
	'email_on_failure': False,
	'email': ['noreply@astronomer.io'],
	'retries': 1
}

with DAG('sample_dag',
	default_args=default_args,
	schedule_interval='@daily',
	catchup=False) as dag:

	wont_email = DummyOperator(
		task_id='wont_email'
	)
	
	will_email = DummyOperator(
		task_id='will_email',
		email_on_failure=True
	)
```

### Notification triggers

The most common trigger for notifications in Airflow is a task failure. However, notifications can be set based on other events, including retries and successes.

Emails on retries can be useful for debugging indirect failures; if a task needed to retry but eventually succeeded, this might indicate that the problem was caused by extraneous factors like load on an external system. To turn on email notifications for retries, simply set the `email_on_retry` parameter to `True` as shown in the DAG below.

```python
from datetime import datetime, timedelta
from airflow import DAG

default_args = {
	'owner': 'airflow',
	'start_date': datetime(2018, 1, 30),
	'email': ['noreply@astronomer.io'],
	'email_on_failure': True,
	'email_on_retry': True,
	'retry_exponential_backoff': True,
	'retry_delay': timedelta(seconds=300),
	'retries': 3
}

with DAG('sample_dag',
	default_args=default_args,
	schedule_interval='@daily',
	catchup=False) as dag:

...
```

When working with retries, you should configure a `retry_delay`. This is the amount of time between a task failure and when the next try will begin. You can also turn on `retry_exponential_backoff`, which progressively increases the wait time between retries. This can be useful if you expect that extraneous factors might cause failures periodically.

### Custom notifications

The email notification parameters shown in the previous sections are examples of built-in Airflow alerting mechanisms. These have to be turned on and don't require any additional configuration.

You can define your own notifications to customize how Airflow alerts you about failures or successes. The most straightforward way of doing this is by defining `on_failure_callback` and `on_success_callback` Python functions. These functions can be set at the DAG or task level, and the functions are called when tasks fail or complete successfully. The following example DAG has a custom `on_failure_callback` function set at the DAG level and an `on_success_callback` function for the `success_task`.

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

def custom_failure_function(context):
	"Define custom failure notification behavior"
	dag_run = context.get('dag_run')
	task_instances = dag_run.get_task_instances()
	print("These task instances failed:", task_instances)

def custom_success_function(context):
	"Define custom success notification behavior"
	dag_run = context.get('dag_run')
    task_instances = dag_run.get_task_instances()
    print("These task instances succeeded:", task_instances)

default_args = {
	'owner': 'airflow',
	'start_date': datetime(2018, 1, 30),
	'on_failure_callback': custom_failure_function
	'retries': 1
}

with DAG('sample_dag',
		default_args=default_args,
		schedule_interval='@daily',
		catchup=False) as dag:

	failure_task = DummyOperator(
		task_id='failure_task'
	)
	
	success_task = DummyOperator(
		task_id='success_task',
		on_success_callback=custom_success_function
	)
```

Custom notification functions can also be used to send email notifications. For example, if you want to send emails for successful task runs, you can define an email function in your `on_success_callback`. For example:

```python
from airflow.utils.email import send_email

def success_email_function(context):
    dag_run = context.get('dag_run')

    msg = "DAG ran successfully"
    subject = f"DAG {dag_run} has completed"
    send_email(to=your_emails, subject=subject, html_content=msg)

```

This functionality may also be useful when your pipelines have conditional branching, and you want to be notified if a certain path is taken.

## Email notifications

Email notifications are a native Airflow feature. The `email_on_failure` and `email_on_retry` parameters can be set to `True` either at the DAG level or task level to send emails when tasks fail or retry. The `email` parameter can be used to specify which email(s) you want to receive the notification. If you want to receive email notifications for all DAG failures and retries, you define default arguments similar to this example:

```python
from datetime import datetime, timedelta
from airflow import DAG

default_args = {
	'owner': 'airflow',
	'start_date': datetime(2018, 1, 30),
	'email': ['noreply@astronomer.io'],
	'email_on_failure': True,
	'email_on_retry': True,
	'retry_delay' = timedelta(seconds=300)
	'retries': 1
}

with DAG('sample_dag',
	default_args=default_args,
	schedule_interval='@daily',
	catchup=False) as dag:

...
```

To allow Airflow to send emails, you complete the SMTP section of your `airflow.cfg` similar to this example:

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

If you are using Astro, you use environment variables to set up SMTP because the `airflow.cfg` cannot be directly edited.

### Customize email notifications

By default, email notifications are sent in a standard format that are defined in the `email_alert()` and `get_email_subject_content()` methods of the `TaskInstance` class. The default email content appears similar to this example:

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

## Slack notifications

In the following example, you'll use the [Slack provider](https://registry.astronomer.io/providers/slack) `SlackWebhookOperator` with a Slack Webhook to send messages. This is the method Slack recommends to post messages from apps.

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
                task=context.get('task_instance').task_id,
                dag=context.get('task_instance').dag_id,
                ti=context.get('task_instance'),
                exec_date=context.get('execution_date'),
                log_url=context.get('task_instance').log_url,
            )
        failed_alert = SlackWebhookOperator(
            task_id='slack_notification',
            http_conn_id='slack_webhook',
            message=slack_msg)
        return failed_alert.execute(context=context)
    ```

 5. Define your `on_failure_callback` parameter in your DAG either as a `default_arg` for the whole DAG, or for specific tasks. Set it equal to the function you created in the previous step.

## Airflow service-level agreements

[Airflow service-level agreements (SLAs)](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#slas) are a type of notification that you can use if your tasks take longer than expected to complete. If a task takes longer than the maximum amount of time to complete as defined in the SLA, the SLA will be missed and notifications are triggered. This can be useful when you have long-running tasks that might require user intervention after a certain period of time, or if you have tasks that need to complete within a certain period. 

Exceeding an SLA does not stop a task from running. If you want tasks to stop running after a certain time, use [timeouts](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#timeouts).

You can set an SLA for all tasks in your DAG by defining `'sla'` as a default argument, as shown in the following example DAG:

```python
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import time

def my_custom_function(ts,**kwargs):
    print("task is sleeping")
    time.sleep(40)

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': 'noreply@astronomer.io',
    'email_on_retry': False,
    'sla': timedelta(seconds=30)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('sla-dag',
         start_date=datetime(2021, 1, 1),
         max_active_runs=1,
         schedule_interval=timedelta(minutes=2),
         default_args=default_args,
         catchup=False 
         ) as dag:

    t0 = DummyOperator(
        task_id='start'
    )

    t1 = DummyOperator(
        task_id='end'
    )

    sla_task = PythonOperator(
        task_id='sla_task',
        python_callable=my_custom_function
    )

    t0 >> sla_task >> t1
```

SLAs have some unique behaviors that you should consider before you implement them:

- SLAs are relative to the DAG execution date, not the task start time. For example, in the previous DAG the `sla_task` will miss the 30 second SLA because it takes at least 40 seconds to complete. The `t1` task will also miss the SLA, because it is executed more than 30 seconds after the DAG execution date. In that case, the `sla_task` will be considered blocking to the `t1` task.
- SLAs will only be evaluated on scheduled DAG Runs. They will not be evaluated on manually triggered DAG Runs.
- SLAs can be set at the task level if a different SLA is required for each task. In the previous example, all task SLAs are still relative to the DAG execution date. For example, in the DAG below, `t1` has an SLA of 500 seconds. If the upstream tasks (`t0` and `sla_task`) combined take 450 seconds to complete, and `t1` takes 60 seconds to complete, then `t1` will miss its SLA even though the task did not take more than 500 seconds to execute.

```python
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import time

def my_custom_function(ts,**kwargs):
    print("task is sleeping")
    time.sleep(40)

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': 'noreply@astronomer.io',
    'email_on_retry': False
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('sla-dag',
         start_date=datetime(2021, 1, 1),
         max_active_runs=1,
         schedule_interval=timedelta(minutes=2),
         default_args=default_args,
         catchup=False 
         ) as dag:

    t0 = DummyOperator(
        task_id='start',
        sla=timedelta(seconds=50)
    )

    t1 = DummyOperator(
        task_id='end',
        sla=timedelta(seconds=500)
    )

    sla_task = PythonOperator(
        task_id='sla_task',
        python_callable=my_custom_function,
        sla=timedelta(seconds=5)
    )

    t0 >> sla_task >> t1
```

Missed SLAs are shown in the Airflow UI. To view them, go to **Browse** > **SLA Misses**:

![SLA UI](/img/guides/sla_ui_view.png)

If you configured an SMTP server in your Airflow environment, you'll receive an email with notifications of any missed SLAs similar to the following image:

![SLA Email](/img/guides/sla_email.png)

There is no functionality to disable email alerting for SLAs. If you have an `'email'` array defined and an SMTP server configured in your Airflow environment, an email will be sent to those addresses for each DAG run with missed SLAs.

## Astronomer notifications

If you are running Airflow with Astronomer Software or Astro, there are a number of options available for managing your Airflow notifications. All of the previous methods for sending task notifications from Airflow can be implemented on Astronomer. See the [Astronomer Software](https://docs.astronomer.io/software/airflow-alerts) and [Astro](https://docs.astronomer.io/astro/airflow-alerts) documentation to learn how to leverage notifications on the platform, including how to set up SMTP to enable email notifications.

Astronomer also provides deployment and platform-level alerting to notify you if any aspect of your Airflow or Astronomer infrastructure is unhealthy. For more on that, including how to customize notifications for Software users, see [Alerting in Astronomer Software](https://docs.astronomer.io/software/platform-alerts).
