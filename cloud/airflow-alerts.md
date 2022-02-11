---
sidebar_label: 'Airflow Alerts'
title: 'Configure Airflow Alerts on Astronomer'
id: airflow-alerts
description: Set up email alerts for Airflow task successes and failures.
---

## Overview

You can utilize Airflow's alerting framework to monitor the health of individual tasks and DAGs across your Airflow Deployments. This guide provides information about configuring various Airflow alerts on Astronomer.

## Configure Slack Notifications, Custom Notifications, and SLAs

Most built-in Airflow alerts, including Slack alerts and SLAs, work out of the box on Astronomer Cloud. You can also write custom alerts that trigger a certain behavior whenever a given task or DAG succeeds or fails. For more information on configuring event-based notifications in Airflow generally, read Astronomer's guide on [Airflow Alerts](https://www.astronomer.io/guides/error-notifications-in-airflow).

Unlike Slack alerts, Airflow email alerts require additional configuration on Astronomer Cloud. The following section covers how to set up an SMTP service to enable Airflow email alerts.

## Configure Airflow Email Alerts

On Astronomer, setting up email alerts requires configuring an SMTP service for delivering each alert.

If your team isn't already using an SMTP service, we recommend one of the following:

- [SendGrid](https://sendgrid.com/)
- [Amazon SES](https://aws.amazon.com/ses/)

The following topics provide setup steps for integrating each of these external SMTP services on Astronomer Cloud, but note that any external SMTP service can be used.

### Integrate with SendGrid

[SendGrid](https://sendgrid.com/) is an email delivery service that's easy to set up for Airflow alerts. A free SendGrid account grants users 40,000 free emails within the first 30 days of an account opening and 100 emails per day after that. This should be more than enough emails for most alerting use cases.

To get started with SendGrid:

1. [Create a SendGrid account](https://signup.sendgrid.com). Be prepared to disclose some standard information about yourself and your organization.

2. [Verify a Single Sender Identity](https://sendgrid.com/docs/ui/sending-email/sender-verification/). Because you're sending emails only for internal administrative purposes, a single sender identity is sufficient for integrating with Astronomer. The email address you verify here is used as the sender for your Airflow alert emails.

3. Create a key using SendGrid's web API. In SendGrid, go to **Email API** > **Integration Guide**. Follow the steps to generate a new API key using SendGrid's Web API and cURL.

4. Skip the step for exporting your API key to your development environment. Instead, execute the generated curl code directly in your command line, making sure to replace `$SENDGRID_API_KEY` in the `--header` field with your copied key.

5. Verify your integration in SendGrid to confirm that the key was activated. If you get an error indicating that SendGrid can't find the test email, try rerunning the cURL code in your terminal before retrying the verification.

6. Open the Airflow UI for your Deployment and [create a connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

    - **Connection ID**: `smtp_default`
    - **Connection Type:**: `Email`
    - **Host**: `smtp.sendgrid.net`
    - **Login**: `apikey`
    - **Password**: `<your-api-key>`
    - **Port**: `587`

7. Click **Save** to finalize your configuration.

To begin receiving emails about Airflow alerts from a given DAG, configure the following values in the DAG's `default_args`:

```text
'email_on_failure': True,
'email': ['<recipient-address>'],
```

### Integrate with Amazon SES

This setup requires an AWS account and use of the [AWS Management Console](https://aws.amazon.com/console/).

1. In the AWS Management Console, go to **AWS Console** > **Simple Email Service** > **Email Addresses** to add and verify the email addresses you want to receive alerts.

2. Open the inbox of each email address you specified and verify them through the emails sent by Amazon.

3. In the AWS Console, go to **Simple Email Service** > **SMTP Settings** and use the **Create My SMTP Credentials** button to generate a username and password. This will look similar to an access and secret access key. Write down this username and password for step 5, as well as the **Server Name** and **Port**.

   > **Note:** You won't be able to access these values again, so consider storing them in a password manager.

4. Choose an Amazon EC2 region to use, then write down the code of this server for the next step. Refer to [Amazon's list of available regions and servers](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions) to determine which server best fits your needs.

5. Open the Airflow UI for your Deployment and [create a connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

   - **Connection ID**: `smtp_default`
   - **Connection Type:**: `Email`
   - **Host**: `<your-smtp-host>`
   - **Login**: `<your-aws-username>`
   - **Password**: `<your-aws-password>`
   - **Port**: `587`

6. Click **Save** to finalize your configuration.

To begin receiving emails about Airflow alerts from a given DAG, configure the following values in the DAG's `default_args`:

```text
'email_on_failure': True,
'email': ['<recipient-address>'],
```
