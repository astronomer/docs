---
sidebar_label: 'Astro alerts'
title: 'Set up Astro alerts'
id: alerts
toc_main_heading_level: 2
---
import HostedBadge from '@site/src/components/HostedBadge';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Astro alerts provide an additional level of observability to Airflow's notification systems. You can configure an alert to notify you in Slack, PagerDuty, or through email when a DAG completes, if you have a DAG run failure, or if a task duration exceeds a specified time.

Unlike Airflow callbacks and SLAs, Astro alerts require no changes to DAG code. Follow this guide to set up your Slack, PagerDuty, or email to receive alerts from Astro and then configure your Deployment to send alerts.

:::info

To configure Airflow notifications, see [Airflow email notifications](airflow-email-notifications.md) and [Manage Airflow DAG notifications](https://www.astronomer.io/docs/learn/error-notifications-in-airflow).

:::

## Alert types

Each Astro alert has a notification channel and a trigger type. The notification channel determines the format and destination of an alert, and the trigger type defines what causes the alert trigger.

### Trigger types

You can trigger an alert to a notification channel using one of the following trigger types:

- **DAG failure**: The alert triggers whenever the specified DAG fails.
- **DAG success**: The alert triggers whenever the specified DAG completes
- **Task duration**: The alert triggers when a specified task takes longer than expected to complete.
- **Absolute Time**: The alert triggers when a given DAG does not have a successful DAG run within a defined time window.

:::info

You can only set a task duration trigger for an individual task. Alerting on task group duration is not supported.

:::

#### Deployment health triggers

<HostedBadge/>

:::privatepreview
:::

In addition to creating trigger types that cause alerts for DAGs, you can also create alerts with triggers that send alerts for [Deployment health incidents](deployment-health-incidents.md#deployment-incidents). You can use these alerts for proactive notification when Deployment health issues arise. For example, you can create an alert for when the Airflow metadata database storage is unusually high. These alerts:

- Use Astro architecture to identify infrastructure-level incidents that are otherwise hard to monitor.
- Give you granular information about your Deployment's performance, with more detail than **Healthy** or **Unhealthy**.
- Incorporate Astro's suggestions about Deployment health into your existing alerting workflows, including email, Slack, and Pagerduty, to allow you to respond faster.

You can set the following alerts to send you a notification for specific health incidents:

- **Airflow Database Storage Unusually High**: The alert triggers when the metadata database has tables that are larger than 50GiB (Info) or 75GiB (Warning).
- **Deprecated Runtime Version**: The alert triggers when your Deployment is using a deprecated Astro Runtime version.
- **Job Scheduling Disabled**: The alert triggers when the Airflow scheduler is configured to prevent automatic scheduling of new tasks using DAG schedules.
- **Worker Queue at Capacity**:  The alert triggers when at least one worker queue in this Deployment is running the maximum number of tasks and workers.

### Notification channels

You can send Astro alerts to the following notification channels

- Slack
- PagerDuty
- Email
- (Private Preview) DAG trigger

:::warning Private Preview - DAG Trigger

This feature is in [Private Preview](feature-previews.md). Please reach out to your customer success manager to enable this feature.

The **DAG Trigger** notification channel works differently from other notification channel types. Instead of sending a pre-formatted alert message, Astro makes a generic request through the Airflow REST API to trigger a DAG on Astro. You can configure the triggered DAG to complete any action, such as sending a message to your own incident management system or writing data about an incident to a table.

:::

## Prerequisites

- An [Astro project](cli/develop-project.md).
- An [Astro Deployment](create-deployment.md). Your Deployment must run Astro Runtime 7.1.0 or later to configure Astro alerts, and it must also have [OpenLineage enabled](set-up-data-lineage.md#disable-openlineage).
- A Slack workspace, PagerDuty service, or email address.

:::info

Astro alerts requires OpenLineage. By default, every Astro Deployment has OpenLineage enabled. If you disabled OpenLineage in your Deployment, you need to enable it to use Astro alerts. See [Disable OpenLineage](set-up-data-lineage.md#disable-openlineage) to find how to disable and re-enable OpenLineage.

:::

<!-- Sensitive header used in product - do not change without a redirect-->

## Step 1: Configure your notification channel

<Tabs
    defaultValue="Slack"
    groupId= "step-1-configure-your-notification-channel"
    values={[
        {label: 'Slack', value: 'Slack'},
        {label: 'PagerDuty', value: 'PagerDuty'},
        {label: 'Email', value: 'Email'},
        {label: 'DAG Trigger', value: 'DAG'}
    ]}>
<TabItem value="Slack">

To set up alerts in Slack, you need to create a Slack app in your Slack workspace. After you've created your app, you can generate a webhook URL in Slack where Astro will send Astro alerts.

1. Go to [Slack API: Applications](https://api.slack.com/apps/new) to create a new app in your organization's Slack workspace.

2. Click **From scratch** when prompted to choose how you want to create your app.

3. Enter a name for your app, like `astro-alerts`, choose the Slack workspace where you want Astro to send your alerts, and then click **Create App**.

  :::info
  If you do not have permission to install apps into your Slack workspace, you can still create the app, but you will need to request that an administrator from your team completes the installation.
  :::

4. Select **Incoming webhooks**.

5. On the **Incoming webhooks** page, click the toggle to turn on **Activate Incoming Webhooks**. See [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks).

6. In the **Webhook URLs for your Workspace** section, click **Add new Webhook to Workspace**.

  :::info

  If you do not have permission to install apps in your Slack workspace, click **Request to Add New Webhook** to send a request to your organization administrator.

  :::

7. Choose the channel where you want to send your Astro alerts and click **Allow**.

8. After your webhook is created, copy the webhook URL from the new entry in the **Webhook URLs for your Workspace** table.

</TabItem>
<TabItem value="PagerDuty">

To set up an alert integration with PagerDuty, you need access to your organization's PagerDuty Service. PagerDuty uses the [Events API v2](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started) to create a new integration that connects your Service with Astro.

1. Open your PagerDuty service and click the **Integrations** tab.

  ![Select PagerDuty integrations](/img/docs/pagerduty_alerts_integrations.png)

2. Click **Add an integration**.

3. Select **Events API v2** as the **Integration Type**.

4. On your **Integrations** page, open your new integration and enter an **Integration Name**.

5. Copy the **Integration Key** for your new Astro alert integration.

</TabItem>
<TabItem value="Email">

No external configuration is required for the email integration. Astronomer recommends allowlisting `astronomer.io` with your email provider to ensure that no alerts go to your spam folder. Alerts are sent from `no-reply@astronomer.io`.

</TabItem>
<TabItem value="DAG">

:::privatepreview
:::

The **DAG Trigger** notification channel works differently from other notification channel types. Instead of sending a pre-formatted alert message, Astro makes a generic request through the `DagRuns` endpoint of the [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run) to trigger any DAG in your Workspace. You can configure the triggered DAG to complete any action, such as sending a message to your own incident management system or writing data about an incident to a table.

The following parameters are used to pass metadata about the alert in the API call:

- `conf`: This parameter holds the alert payload:
  - `alertId`: A unique alert ID.
  - `alertType`: The type of alert triggered.
  - `dagName`: The name of the DAG that triggered the alert.
  - `message`: The detailed message with the cause of the alert.
  - `note`: By default, this is `Triggering DAG on Airflow <url>`.

The following is an example alert payload that would be passed through the API:

```json
{
  "dagName": "fail_dag",
  "alertType": "PIPELINE_FAILURE",
  "alertId": "d75e7517-88cc-4bab-b40f-660dd79df216",
  "message": "[Astro Alerts] Pipeline failure detected on DAG fail_dag. \\nStart time: 2023-11-17 17:32:54 UTC. \\nFailed at: 2023-11-17 17:40:10 UTC. \\nAlert notification time: 2023-11-17 17:40:10 UTC. \\nClick link to investigate in Astro UI: https://cloud.astronomer.io/clkya6zgv000401k8zafabcde/dags/clncyz42l6957401bvfuxn8zyxw/fail_dag/c6fbe201-a3f1-39ad-9c5c-817cbf99d123?utm_source=alert\"\\n"
}
```

These parameters are accessible in the triggered DAG using [DAG params](https://www.astronomer.io/docs/learn/airflow-params).

1. Create a DAG that you want to run when the alert is triggered. For example, you can use the following DAG to run arbitrary Python code when the alert is triggered:

  ```python
  import datetime
  from typing import Any

  from airflow.models.dag import DAG
  from airflow.operators.python import PythonOperator

  with DAG(
      dag_id="register_incident",
      start_date=datetime.datetime(2023, 1, 1),
      schedule=None,
  ):

      def _register_incident(params: dict[str, Any]):
          failed_dag = params["dagName"]
          print(f"Register an incident in my system for DAG {failed_dag}.")

      PythonOperator(task_id="register_incident", python_callable=_register_incident)

  ```

2. Deploy the DAG to any Deployment in the Workspace where you want to create the alert. The DAG that triggers the alert and the DAG that the alert runs can be in different Deployments, but they must be deployed in the same Workspace.

3. Create a [Deployment API token](deployment-api-tokens.md) for the Deployment where you deployed the DAG that the alert will run. Copy the token to use in the next step.

</TabItem>
</Tabs>

## Step 2: Add a notification channel.

You can enable alerts from the Astro UI.

1. In the Astro UI, click **Alerts** in the main menu.

2. Click the **Notification channels** tab.

3. Click **Add Notification Channel**.

4. Enter a name for your notification channel.

5. Choose the Channel Type.

6. Add the notification channel information.

    <Tabs
        defaultValue="Slack"
        groupId= "step-1-configure-your-notification-channel"
        values={[
            {label: 'Slack', value: 'Slack'},
            {label: 'PagerDuty', value: 'PagerDuty'},
            {label: 'Email', value: 'Email'},
            {label: 'DAG Trigger', value: 'DAG'}
        ]}>
    <TabItem value="Slack">

    Paste the Webhook URL from your Slack workspace app. If you need to find a URL for an app you've already created, go to your [Slack Apps](https://api.slack.com/apps) page, select your app, and then choose the **Incoming Webhooks** page.

    ![Add your Slack Webhook URL](/img/docs/astro_alerts_slack_v2.png)

    </TabItem>
    <TabItem value="PagerDuty">

    Paste the Integration Key from your PagerDuty Integration and select the **Severity** of the alert.

    ![Paste the Integration Key](/img/docs/astro_alerts_pagerduty_v2.png)

    </TabItem>
    <TabItem value="Email">

    Enter the email addresses that should receive the alert.

    ![Add an email address](/img/docs/astro_alerts_email_v2.png)

    </TabItem>
    <TabItem value="DAG">

    Select the Deployment where your DAG is deployed, then select the DAG. Enter the Deployment API token that you created in Step 1.

    ![Add an email address](/img/docs/astro_alerts_dag.png)

    </TabItem>
    </Tabs>

7. Click **Create notification channel**.

## Step 3: Create your alert in the Astro UI

1. In the Astro UI, click on **Alerts** and then the **Alerts** Tab.

2. Click **Add Alert**.

3. Choose the **Alert Type**

    - **DAG failure**: Send an alert if a DAG fails.

    - **DAG success**: Send an alert when a DAG completes.

    - **Task duration**: Enter the **Duration** for how long a task should take to run before you send an alert to your notification channels.

    - **Absolute Time**: Select the **Days of Week** that the alert should observe, the **Verification Time** when it should look for a DAG success, and the **Lookback Period** for how long it should look back for a verification time.

    For example, if an alert has a **Verification Time** of 3:00 PM and a **Lookback Period** of 60 minutes, it will trigger whenever the given DAG does not produce a successful DAG run from 2:00 to 3:00 PM. Astro applies the times you specify based on the time zone of your current web browser session, then translates them to UTC in your Airflow environment.

4. Choose the alert **Severity**, either **Info**, **Warning**, **Critical**, or **Error**.

5. Define the conditions on which you want your alert to send a notification.

  - Select the **Attribute**, **Operator**, and **DAGs** to define when you want Astro to send an Alert and which DAGs that you want the alert to apply to.

## Step 3: (Optional) Change an alert name

After you select a DAG that you want to apply an alert to, Astro automatically generates a name for your alert. However, you can choose to change the name of your alert.

1. Expand the **Change alert names...** section.

2. Edit the **Alert Name**.

3. Click **Create Alert** to save your changes.

## (Optional) Test your DAG failure alert

Astro alerts work whether your DAG run is manual or scheduled, so you can test your configured Astro alerts by failing your DAG manually.

1. In the Astro UI, click **DAGs**.

2. Choose the DAG that has your alert configured.

3. Trigger a DAG run.

4. Select **Mark as** and choose **Failed** to trigger an alert for a DAG failure.

  ![Manually marking a successful DAG run as Failed.](/img/docs/astro_alerts_manual_fail.png)

5. Check your Slack, PagerDuty, or Email alerts for your DAG failure alert. The alert includes information about the DAG, Workspace, Deployment, and data lineage associated with the failure as well as direct links to the Astro UI.

    ![Example of a Slack test alert.](/img/docs/slack_alerts_example.png)

