---
sidebar_label: 'Airflow alerts'
title: 'Configure Airflow alerts on Astro'
id: airflow-alerts
description: Set up email alerts for Airflow task successes and failures.
---

For all teams, incorporating an alerting framework is critical to the health of your data pipelines. In addition to the observability functionality provided on Astro, Airflow's alerting framework includes support for:

- Slack notifications
- SLAs
- Email alerts

Slack alerts and SLAs do not require additional configuration on Astro. For best practices, see the Astronomer guide on [Airflow alerts](https://docs.astronomer.io/learn/error-notifications-in-airflow).

This guide focuses on setting up email alerts on Astro with an SMTP service.

## Configure Airflow email alerts

On Astro, setting up email alerts requires configuring an SMTP service for delivering each alert.

If your organization isn't using an SMTP service currently, Astronomer recommends one of the following:

- [SendGrid](https://sendgrid.com/)
- [Amazon SES](https://aws.amazon.com/ses/)

The following topics provide setup steps for integrating each of these external SMTP services on Astro, but any external SMTP service can be used.

### Integrate with SendGrid

[SendGrid](https://sendgrid.com/) is an email delivery service that's easy to set up for Airflow alerts. A free SendGrid account grants users 40,000 free emails within the first 30 days of an account opening and 100 emails per day after that. This should be more than enough emails for most alerting use cases.

1. [Create a SendGrid account](https://signup.sendgrid.com). Be prepared to disclose some standard information about yourself and your organization.

2. [Verify a Single Sender Identity](https://sendgrid.com/docs/ui/sending-email/sender-verification/). Because you're sending emails only for internal administrative purposes, a single sender identity is sufficient for integrating with Astro. The email address you verify here is used as the sender for your Airflow alert emails.

3. Create a Sendgrid API key. In SendGrid, go to **Email API** > **Integration Guide**. Follow the steps to generate a new API key using SendGrid's Web API and cURL.

    For more information, see [Sendgrid documentation](https://docs.sendgrid.com/ui/account-and-settings/api-keys#creating-an-api-key).

4. Skip the step for exporting your API key to your development environment. Instead, execute the generated curl code directly in your command line, making sure to replace `$SENDGRID_API_KEY` in the `--header` field with your copied key.

5. Verify your integration in SendGrid to confirm that the key was activated. If you get an error indicating that SendGrid can't find the test email, try rerunning the cURL code in your terminal before retrying the verification.

6. Add the following line to your Astro project `requirements.txt` file to install the [SendGrid Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-sendgrid/stable/index.html):

    ```text
    apache-airflow-providers-sendgrid
    ```

7. In the Deployment view of the Cloud UI, add the following environment variables:

    - `AIRFLOW__EMAIL__EMAIL_BACKEND` = `airflow.providers.sendgrid.utils.emailer.send_email`
    - `AIRFLOW__EMAIL__EMAIL_CONN_ID` = `smtp_default`
    - `SENDGRID_MAIL_FROM` = `<validated-sendgrid-sender-email-address>`

    For more information about these environment variables, see [Send email using SendGrid](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html#send-email-using-sendgrid).

8. In the Airflow UI, [create an Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) with the following values:

    - **Connection ID**: `smtp_default`
    - **Connection Type:**: `Email`
    - **Host**: `smtp.sendgrid.net`
    - **Login**: `apikey`
    - **Password**: `<your-sendgrid-api-key>`
    - **Port**: `587`

9. Click **Save** to finalize your configuration.

10. To receive email alerts for task failures within a given DAG, configure the following values in the DAG's `default_args`:

    ```python
    'email_on_failure': True,
    'email': ['<recipient-address>'],
    ```

### Integrate with Amazon SES

Use your existing Amazon SES instance to send Airflow alerts by email.

1. Sign in to the AWS Management Console and open the Amazon SES console at https://console.aws.amazon.com/ses/.

2. Click the menu icon and then click **Verified Identities**.

3. Optional. Complete one of the following tasks:

    - To confirm the email account is working and the Amazon SES service can send emails to it, click an email address in the **Identity** column and then click **Send test email**. When the owner of the email address receives the test email, they need to select the validation link in the email.
    - To add a new email address, click **Create Identity**, add the email address, and then click **Create Identity**.

    For email alerts, Astronomer recommends using one email address as the sender and a second email address as the recipient. All email addresses must be verified.

    For more information about configuring Amazon SES, read [Creating an email address identity](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html#:~:text=of%20those%20Regions.-,Creating%20an%20email%20address%20identity,-Complete%20the%20following) and  [Verifying an email address identity](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html#:~:text=address%20identity.-,Verifying%20an%20email%20address%20identity,-After%20you%E2%80%99ve%20created) in the Amazon documentation.

4. Click **Account dashboard**.

5. In the **Simple Mail Transfer Protocol (SMTP) settings** pane, copy the value displayed below **SMTP endpoint**.

6. Obtain your Amazon SES SMTP credentials:
    - Click **Create SMTP credentials** in the **Simple Mail Transfer Protocol (SMTP) settings** pane.
    - Enter a name for your SMTP user in the **IAM User Name** field or accept the default value.
    - Click **Create** and then **Show User SMTP Security Credentials**.
    - Click **Download Credentials** or copy them and store them in a safe place.
    - Click **Close Window**.

7. In the Cloud UI, select a Workspace and then select a Deployment.

8. In the environment variables area, click **Edit Variables** and add these variables:
    - `ENV AIRFLOW__SMTP__SMTP_HOST`: Enter the value you copied in step 5
    - `ENV AIRFLOW__SMTP__SMTP_STARTTLS`: Enter `True`.
    - `ENV AIRFLOW__SMTP__SMTP_SSL`: Enter `False`.
    - `ENV AIRFLOW__SMTP__SMTP_USER`: Enter the value you copied in step 6.
    - `ENV AIRFLOW__SMTP__SMTP_PASSWORD`: Enter the value you copied in step 6.
    - `ENV AIRFLOW__SMTP__SMTP_PORT`: Enter `587`.
    - `ENV AIRFLOW__SMTP__SMTP_MAIL_FROM`: Enter your from email.
    - `ENV AIRFLOW__EMAIL__EMAIL_BACKEND`: Enter `airflow.utils.email.send_email_smtp`.

    See [Set environment variables on Astro](https://docs.astronomer.io/astro/environment-variables).

9. To begin receiving Airflow alerts by email for task failures within a given DAG, configure the following values in the DAG's `default_args`:

    ```python
    'email_on_failure': True,
    'email': ['<recipient-address>'],
    ```
