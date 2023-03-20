---
sidebar_label: 'Airflow alerts'
title: 'Configure Airflow alerts on Astronomer Software'
id: airflow-alerts
description: Configure email alerts on Astronomer Software to monitor the health of your Airflow Deployment and the status of your tasks.
---

Whether you're just starting to use Apache Airflow or your team is running it at scale, incorporating an alerting framework is critical to the health of your data. On Astronomer Software, users have access to three types of alerting solutions:

- Airflow task and DAG-level alerts, which notify you via email when an Airflow task or DAG fails, succeeds, or retries.
- Deployment-level alerts, which notify you when the health of an Airflow Deployment is low or if any of Airflow's underlying components are underperforming, including the Airflow scheduler.
- Platform-level alerts, which notify you when a component of your Astronomer platform is unhealthy, such as Elasticsearch, Astronomer's Houston API, or your Docker Registry.

This guide focuses on configuring task and DAG-level alerts. For information on configuring platform and Deployment-level alerts, read [Alerting on Astronomer Software](platform-alerts.md).

## Subscribe to task-level alerts

As an Airflow user, you can configure event-based email alerts directly in your DAG code by leveraging Airflow's [email util](https://github.com/apache/airflow/blob/master/airflow/utils/email.py). Depending on your use case, you may choose to be notified if a particular task or DAG fails, succeeds, retries, etc. On Astronomer, setting up task-level alerts requires configuring an SMTP service to handle the delivery of these emails.

If your team isn't already using an SMTP service, we recommend the following:

- [SendGrid](https://sendgrid.com/)
- [Amazon SES](https://aws.amazon.com/ses/)

Step-by-step instructions on how to integrate these two services with Astronomer are provided below, but you can use any SMTP service for this purpose.

> **Note:** By default, email alerts for process failures are sent whenever individual tasks fail. To receive only 1 email per DAG failure, refer to the "Limit alerts to the DAG level" topic below. For more information and best practices on Airflow alerts, read [Error Notifications in Airflow](https://docs.astronomer.io/learn/error-notifications-in-airflow).

### Integrate SendGrid with Astronomer

[SendGrid](https://sendgrid.com/) is an email delivery service that's easy to set up for Airflow task-level alerts. A free SendGrid account grants users 40,000 free emails within the first 30 days of an account opening and 100 emails per day after that. This should be more than enough emails for most alerting use cases.

To get started with SendGrid:

1. [Create a SendGrid account](https://signup.sendgrid.com). Be prepared to disclose some standard information about yourself and your organization.

2. [Verify a Single Sender Identity](https://sendgrid.com/docs/ui/sending-email/sender-verification/). Because you're sending emails only for internal administrative purposes, a single sender identity is sufficient for integrating with Astronomer. The email address you verify here is used as the sender for your Airflow alert emails.

3. Create a Sendgrid API key. In SendGrid, go to **Email API** > **Integration Guide**. Follow the steps to generate a new API key using SendGrid's Web API and cURL.

    For more information, see [Sendgrid documentation](https://docs.sendgrid.com/ui/account-and-settings/api-keys#creating-an-api-key).

4. Skip the step for exporting your API key to your development environment. Instead, execute the generated curl code directly in your command line, making sure to replace `$SENDGRID_API_KEY` in the `--header` field with your copied key.

5. Verify your integration in SendGrid to confirm that the key was activated. If you get an error indicating that SendGrid can't find the test email, try rerunning the cURL code in your terminal before retrying the verification.

6. In the Deployment view of the Astronomer Software UI, create an environment variable with the following values:

    - **Key**: `AIRFLOW__EMAIL__EMAIL_BACKEND`
    - **Value**: `airflow.providers.sendgrid.utils.emailer.send_email`

    For more information on this environment variable, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html#send-email-using-sendgrid).

7. In the Airflow UI, [create an Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

    - **Connection ID**: `smtp_default`
    - **Connection Type:**: `Email`
    - **Host**: `smtp.sendgrid.net`
    - **Login**: `apikey`
    - **Password**: `<your-sendgrid-api-key>`
    - **Port**: `587`

8. Click **Save** to finalize your configuration.

9. To begin receiving Airflow alerts via email for task failures within a given DAG, configure the following values in the DAG's `default_args`:

    ```python
    'email_on_failure': True,
    'email': ['<recipient-address>'],
    ```

### Integrate Amazon SES with Astronomer

This setup requires an AWS account and use of the [AWS Management Console](https://aws.amazon.com/console/).

1. In the AWS Management Console, go to **AWS Console** > **Simple Email Service** > **Email Addresses** to add and verify the email addresses you want to receive alerts.

2. Open the inbox of each email address you specified and verify them through the emails sent by Amazon.

3. In the AWS Console, go to **Simple Email Service** > **SMTP Settings** and use the **Create My SMTP Credentials** button to generate a username and password. This will look similar to an access and secret access key. Write down this username and password for step 5, as well as the **Server Name** and **Port**.

   > **Note:** You won't be able to access these values again, so consider storing them in a password manager.

4. Choose an Amazon EC2 region to use, then write down the code of this server for the next step. Refer to [Amazon's list of available regions and servers](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions) to determine which server best fits your needs.

5. In the Deployment view of the Astronomer Software UI, create an environment variable with the following values:

    - **Key**: `AIRFLOW__EMAIL__EMAIL_BACKEND`
    - **Value**: `airflow.providers.amazon.aws.utils.emailer.send_email`

    For more information on this environment variable, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html#send-email-using-aws-ses).

6. In the Airflow UI, [create an Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

    - **Connection ID**: `smtp_default`
    - **Connection Type:**: `Email`
    - **Host**: `<your-smtp-host>`
    - **Login**: `<your-aws-username>`
    - **Password**: `<your-aws-password>`
    - **Port**: `587`

7. Click **Save** to finalize your configuration.

8. To begin receiving Airflow alerts via email for task failures within a given DAG, configure the following values in the DAG's `default_args`:

    ```python
    'email_on_failure': True,
    'email': ['<recipient-address>'],
    ```

## Limit alerts to the DAG level

By default, email alerts configured via the `email_on_failure` param ([source](https://github.com/apache/airflow/blob/master/airflow/models/baseoperator.py)) are handled at the task level. If some number of your tasks fail, you'll receive an individual email for each of those failures.

If you want to limit failure alerts to the DAG-run level, you can instead set up your alerts using the `on_failure_callback` param ([source](https://github.com/apache/airflow/blob/v1-10-stable/airflow/models/dag.py#L167)). When you pass `on_failure_callback` directly in your DAG file, it defines a Python function that sends you one email per DAG failure, rather than multiple emails for each task that fails:

```
 :param on_failure_callback: A function to be called when a DagRun of this dag fails.
```

The code in your DAG might look something like this ([source](https://github.com/apache/airflow/blob/v1-10-stable/airflow/utils/email.py#L41)):

```python
     from airflow.models.email import send_email
     def new_email_alert(self, **kwargs):
     title = "TEST MESSAGE: THIS IS A MODIFIED TEST"
     body = ("This is the text "
     "That appears in the email body..<br>")
     send_email('my_email@email.com', title, body)
```
