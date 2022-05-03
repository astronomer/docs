---
sidebar_label: 'Airflow Alerts'
title: 'Configure Airflow Alerts on Astro'
id: airflow-alerts
description: Set up email alerts for Airflow task successes and failures.
---

## Overview

For all teams, incorporating an alerting framework is critical to the health of your data pipelines. In addition to the observability functionality provided on Astro, Airflow's alerting framework includes support for:

- Slack notifications
- SLAs
- Email alerts

Slack alerts and SLAs do not require additional configuration on Astro. For best practices, see the Astronomer guide on [Airflow Alerts](https://www.astronomer.io/guides/error-notifications-in-airflow).

This guide focuses on setting up email alerts on Astro with an SMTP service.

## Configure Airflow Email Alerts

On Astro, setting up email alerts requires configuring an SMTP service for delivering each alert.

If your team isn't already using an SMTP service, we recommend one of the following:

- [SendGrid](https://sendgrid.com/)
- [Amazon SES](https://aws.amazon.com/ses/)

The following topics provide setup steps for integrating each of these external SMTP services on Astro, but any external SMTP service can be used.

### Integrate with SendGrid

[SendGrid](https://sendgrid.com/) is an email delivery service that's easy to set up for Airflow alerts. A free SendGrid account grants users 40,000 free emails within the first 30 days of an account opening and 100 emails per day after that. This should be more than enough emails for most alerting use cases.

To get started with SendGrid:

1. [Create a SendGrid account](https://signup.sendgrid.com). Be prepared to disclose some standard information about yourself and your organization.

2. [Verify a Single Sender Identity](https://sendgrid.com/docs/ui/sending-email/sender-verification/). Because you're sending emails only for internal administrative purposes, a single sender identity is sufficient for integrating with Astro. The email address you verify here is used as the sender for your Airflow alert emails.

3. Create a Sendgrid API key. In SendGrid, go to **Email API** > **Integration Guide**. Follow the steps to generate a new API key using SendGrid's Web API and cURL.

    For more information, see [Sendgrid documentation](https://docs.sendgrid.com/ui/account-and-settings/api-keys#creating-an-api-key).

4. Skip the step for exporting your API key to your development environment. Instead, execute the generated curl code directly in your command line, making sure to replace `$SENDGRID_API_KEY` in the `--header` field with your copied key.

5. Verify your integration in SendGrid to confirm that the key was activated. If you get an error indicating that SendGrid can't find the test email, try rerunning the cURL code in your terminal before retrying the verification.

6. In the Deployment view of the Cloud UI, create an environment variable with the following values:

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

### Integrate with Amazon SES

This setup requires an AWS account and use of the [AWS Management Console](https://aws.amazon.com/console/).

1. In the AWS Management Console, go to **AWS Console** > **Simple Email Service** > **Email Addresses** to add and verify the email addresses you want to receive alerts.

2. Open the inbox of each email address you specified and verify them through the emails sent by Amazon.

3. In the AWS Console, go to **Simple Email Service** > **SMTP Settings** and use the **Create My SMTP Credentials** button to generate a username and password. This will look similar to an access and secret access key. Write down this username and password for step 5, as well as the **Server Name** and **Port**.

   > **Note:** You won't be able to access these values again, so consider storing them in a password manager.

4. Choose an Amazon EC2 region to use, then write down the code of this server for the next step. Refer to [Amazon's list of available regions and servers](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions) to determine which server best fits your needs.

5. In the Deployment view of the Cloud UI, create an environment variable with the following values:
    - **Key**: `AIRFLOW__EMAIL__EMAIL_BACKEND`
    - **Value**: `airflow.providers.amazon.aws.utils.emailer.send_email`
    
    For more information on this environment variable, see [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html#send-email-using-aws-ses).

6. In the Airflow UI, [create an Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

   - **Connection ID**: `smtp_default`
   - **Connection Type:** `Email`
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
